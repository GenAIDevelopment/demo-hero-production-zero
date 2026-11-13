"""Shared Gemini helpers for the workshop notebooks.

- get_api_key(): finds the key (Colab Secrets, env var, .env, hidden prompt) and never prints it.
- call_gemini(fn): retries politely on "slow down" (429) and busy (5xx) errors, and turns every other
  error into a plain-English fix instead of a stack trace. Works for google-genai and LangChain errors.
- make_chat(...): the LangChain chat model (ChatGoogleGenerativeAI) with the workshop's settings.
- setup_tracing(): LangSmith tracing, on only when LANGSMITH_API_KEY is set.

00_setup_check.ipynb keeps its own copy of this logic on purpose: it is sent on its own before the
workshop and must work without the repo.
"""
import getpass
import os
import time

WAITS = [10, 20, 40]  # seconds to wait before each retry


class Friendly(Exception):
    """An error already explained in plain English. .reason is short, .fix is what to do."""

    def __init__(self, reason, fix):
        super().__init__(fix)
        self.reason, self.fix = reason, fix


def get_api_key():
    """Return (key, where_it_came_from), or (None, None) after printing the fix."""
    try:
        from google.colab import userdata  # only exists inside Colab
    except ImportError:
        userdata = None
    if userdata is not None:
        try:
            key = (userdata.get("GOOGLE_API_KEY") or "").strip()
            if key:
                return key, "Colab Secrets"
            print("⚠️  The Colab secret GOOGLE_API_KEY exists but is empty. Paste your key into its Value.")
        except Exception as e:
            kind = type(e).__name__
            if kind == "NotebookAccessError":
                print("⚠️  Found the secret GOOGLE_API_KEY, but this notebook isn't allowed to read it.\n"
                      "    Fix: click the 🔑 key icon in the left sidebar, find GOOGLE_API_KEY and switch\n"
                      "    ON 'Notebook access'. Then: Runtime → Run all.")
            elif kind == "SecretNotFoundError":
                print("⚠️  No Colab secret called GOOGLE_API_KEY.\n"
                      "    Fix: 🔑 key icon in the left sidebar → '+ Add new secret' → Name: GOOGLE_API_KEY\n"
                      "    → paste your key as the Value → switch on 'Notebook access'.")
            elif kind == "TimeoutException":
                print("⚠️  Colab took too long to hand over the secret. Run this cell again.")
            else:
                print(f"⚠️  Couldn't read Colab Secrets ({kind}).")
    for name in ("GOOGLE_API_KEY", "GEMINI_API_KEY"):  # GOOGLE_ wins, same as Google's SDK
        if os.environ.get(name, "").strip():
            return os.environ[name].strip(), f"environment variable {name}"
    try:
        from dotenv import dotenv_values, find_dotenv
        path = find_dotenv(usecwd=True)
        key = (dotenv_values(path).get("GOOGLE_API_KEY") or "").strip() if path else ""
        if key:
            return key, ".env file"
    except ImportError:
        pass
    try:
        key = getpass.getpass("Paste your Gemini API key (hidden), then press Enter: ").strip()
        if key:
            return key, "typed in"
    except Exception:
        pass  # no keyboard (automated run)
    print("❌ No API key found. Run 00_setup_check.ipynb first: it walks you through it.")
    return None, None


# LangChain wraps Gemini's errors (e.g. GoogleRateLimitError) and keeps the original as __cause__.
_CODE_BY_CLASS = {"GoogleAuthenticationError": 401, "GooglePermissionDeniedError": 403,
                  "GoogleModelNotFoundError": 404, "GoogleRateLimitError": 429, "GoogleInvalidRequestError": 400}


def error_code(e):
    """The HTTP status code behind an error, whether it came from google-genai or LangChain."""
    for err in (e, getattr(e, "__cause__", None)):
        code = getattr(err, "code", None)
        if isinstance(code, int):
            return code
    return _CODE_BY_CLASS.get(type(e).__name__)


def _is_network_error(e):
    names = {type(x).__name__ for x in (e, getattr(e, "__cause__", None)) if x is not None}
    return bool(names & {"ConnectError", "ConnectTimeout", "ReadTimeout", "NetworkError", "RemoteProtocolError",
                         "ConnectionError", "TimeoutError", "gaierror"})


def explain(e, model=None):
    """Turn a Gemini error into Friendly(reason, fix)."""
    code = error_code(e)
    low = str(getattr(e, "message", "") or e).lower()
    if "api key not valid" in low or "api_key_invalid" in low or code == 401:
        return Friendly("wrong key", "Google says this key isn't valid. Copy it again from "
                        "https://aistudio.google.com/apikey (the whole key, no spaces).")
    if "leaked" in low:
        return Friendly("blocked key", "Google blocked this key because it was shared publicly. "
                        "Make a new one at https://aistudio.google.com/apikey.")
    if "location" in low and "not supported" in low:
        return Friendly("region", "The Gemini API isn't available in your region.")
    if code == 404:
        return Friendly("model not available", f"Your key can't use the model '{model}'.")
    if code == 429 and "limit: 0" in low:
        return Friendly("not on free tier", f"The model '{model}' isn't part of your free tier.")
    if code == 429 and "perday" in low.replace(" ", "").replace("_", ""):
        return Friendly("daily limit", "You've used today's free quota for this model. It resets daily.")
    if code == 403:
        return Friendly("project not allowed", "Google won't let this key's project use the Gemini API. "
                        "Create a fresh key in a NEW project at https://aistudio.google.com/apikey.")
    if code == 429:
        return Friendly("too busy", "Free tier says slow down, and it didn't calm down. Wait a minute, run again.")
    if isinstance(code, int) and code >= 500:
        return Friendly("google busy", "Google's servers are busy right now. Wait a minute and run again.")
    if code is None and _is_network_error(e):
        return Friendly("no connection", "Couldn't reach Google. Check your internet connection.")
    return Friendly("unexpected", f"Unexpected error ({type(e).__name__}, code {code}): {low[:200]}")


def call_gemini(fn, model=None, quiet=False):
    """Run fn(). Retry on 429/5xx with friendly waits; raise Friendly for everything else."""
    for attempt in range(len(WAITS) + 1):
        try:
            return fn()
        except Exception as e:
            code = error_code(e)
            text = str(e).lower()
            retryable = ((code == 429 and "limit: 0" not in text and "perday" not in text.replace("_", ""))
                         or (isinstance(code, int) and code >= 500))
            if retryable and attempt < len(WAITS):
                if not quiet:
                    why = "Free tier says slow down" if code == 429 else "Google is busy"
                    print(f"⏳ {why}. Waiting {WAITS[attempt]}s…")
                time.sleep(WAITS[attempt])
                continue
            raise explain(e, model) from None


def make_chat(model, api_key, temperature=0, seed=None):
    """A LangChain Gemini chat model with the workshop's settings.

    max_retries=1 switches LangChain's own silent retries off (0 would mean "use Google's default"),
    so call_gemini() is the only retry layer and students see the friendly "slow down" message.
    temperature=None leaves the model's default (1.0 for Gemini 3 models).
    """
    from langchain_google_genai import ChatGoogleGenerativeAI
    kwargs = dict(model=model, google_api_key=api_key, max_retries=1)
    if temperature is not None:
        kwargs["temperature"] = temperature
    if seed is not None:
        kwargs["seed"] = seed
    return ChatGoogleGenerativeAI(**kwargs)


def setup_tracing(project="demo-hero-production-zero"):
    """Turn on LangSmith tracing if a LANGSMITH_API_KEY is available; otherwise leave it off.

    LangChain and LangGraph trace automatically once LANGSMITH_TRACING=true and LANGSMITH_API_KEY are
    set, with no code change. Without a key, nothing is sent and the notebook runs the same.
    """
    key = os.environ.get("LANGSMITH_API_KEY", "").strip()
    if not key:
        try:
            from google.colab import userdata
            key = (userdata.get("LANGSMITH_API_KEY") or "").strip()
        except Exception:
            pass
    if not key:
        try:
            from dotenv import dotenv_values, find_dotenv
            path = find_dotenv(usecwd=True)
            key = (dotenv_values(path).get("LANGSMITH_API_KEY") or "").strip() if path else ""
        except ImportError:
            pass
    if not key:
        os.environ["LANGSMITH_TRACING"] = "false"
        return False
    os.environ["LANGSMITH_API_KEY"] = key
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ.setdefault("LANGSMITH_PROJECT", project)
    return True

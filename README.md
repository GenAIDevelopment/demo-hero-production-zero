# Demo Hero, Production Zero

**Why your AI breaks in the real world, and how to fix it.** The code and data for a 3-hour hands-on
workshop by Learning Thoughts.

You are the engineers on call at **QuickBasket**, a fictional quick-commerce company. Its new AI
assistant, AskQB, goes live tomorrow morning. Two beliefs get tested with real measurements:

1. **"A good prompt is enough."** A support bot that answers from the company's policy.
2. **"An agent is just a chatbot with tools."** A support agent that can issue refunds.

> Everything here is synthetic. QuickBasket, its customers, orders, policies and help centre are made
> up for training. No real company or person appears in this repository.

## Before the workshop: get a free Gemini API key (2 minutes)

1. Go to <https://aistudio.google.com/apikey> and sign in with your own Google account.
2. Click **Create API key**. If it asks for a project, let it create a new one.
3. Copy the key. Keep it secret: never paste it into a notebook cell, a chat or a screenshot.
4. Open the setup-check notebook below in Colab.
5. In Colab, click the 🔑 key icon in the left sidebar → **Add new secret** → Name `GOOGLE_API_KEY` →
   paste the key as the Value → switch on **Notebook access**.
6. **Runtime → Run all.** You are ready when you see "✅ YOU'RE READY".

The free tier is enough for everything here. It sometimes says "slow down"; the notebooks wait and retry.

## The notebooks, in order

| # | Notebook | Open | What it is |
|---|---|---|---|
| 0 | `00_setup_check.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenAIDevelopment/demo-hero-production-zero/blob/main/00_setup_check.ipynb) | Checks your key and the models it can reach. Do this before the workshop. |
| 1 | `quickbasket/myth1_prompt_is_enough.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenAIDevelopment/demo-hero-production-zero/blob/main/quickbasket/myth1_prompt_is_enough.ipynb) | Myth 1: a prompt-only bot, the whole help centre in the prompt, then retrieval with citations. |
| 1s | `quickbasket/myth1_prompt_is_enough_solution.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenAIDevelopment/demo-hero-production-zero/blob/main/quickbasket/myth1_prompt_is_enough_solution.ipynb) | The same notebook, already run. Read along here if you fall behind. |
| 2 | `quickbasket/myth2_agent_with_tools.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenAIDevelopment/demo-hero-production-zero/blob/main/quickbasket/myth2_agent_with_tools.ipynb) | Myth 2: a LangGraph agent with a "master key", then narrow tools on an MCP server. |
| 2s | `quickbasket/myth2_agent_with_tools_solution.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/GenAIDevelopment/demo-hero-production-zero/blob/main/quickbasket/myth2_agent_with_tools_solution.ipynb) | The same notebook, already run. |

Cells are labelled 🟢 **RUN** (just run it), 🛠 **HACK** (change one value and see what breaks) and
👀 **WATCH** (the presenter runs it live; you can too).

A full **Run all** makes live model calls and takes a few minutes. One cell in notebook 1 sends the whole
help centre (about 120,000 tokens) in a single request; run that one once at most on a free key.

## What's in the repository

| Path | What it is |
|---|---|
| `quickbasket/quickbasket_policy.pdf` | The 2-page customer policy (version 4.2, the source of truth) |
| `quickbasket/kb/` | The help centre: 14 documents, including older policy versions that were replaced |
| `quickbasket/quickbasket.db`, `scenarios.json` | 212 synthetic orders, 60 customers |
| `quickbasket/incident_cards.md` | Nine incident tickets, each with an interview question |
| `quickbasket/myth1_questions.json`, `myth2_requests.json` | The test sets, written before anything was run |
| `quickbasket/myth1_results.json`, `myth2_results.json` | Measured results the notebooks display |
| `quickbasket/kb_chunker.py` | Cuts the help centre into labelled chunks |
| `quickbasket/qb_mcp_server.py` | The MCP server: four narrow tools that enforce the policy |
| `quickbasket/refund_audit.py` | Plain-code checker that decides whether an agent run was safe |
| `quickbasket/build_*.py`, `kb_src/` | Scripts that rebuild the policy, the orders and the help centre |
| `common/` | Shared helpers: API key lookup, retries, prices |
| `workshop/production_readiness_scorecard.md` | Score yourself before and after |
| `workshop/career_kit/` | Postmortem template, LinkedIn post template, interview answers |

## Running on your own laptop

```
git clone https://github.com/GenAIDevelopment/demo-hero-production-zero.git
cd demo-hero-production-zero
python -m venv .venv            # Python 3.11 or newer
.venv/Scripts/activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Put `GOOGLE_API_KEY=your-key` in a file called `.env` in this folder (it is ignored by git), then open the
notebooks in VS Code or Jupyter.

## Want to go further?

This workshop is a slice of the **Generative AI Developer Program** at Learning Thoughts: RAG,
agents, MCP, fine-tuning and local models, each ending in a capstone project. Browse to
[info@learningthoughts.io](https://qualitythought.in/gen-ai/) to ask about the next batch.

## Licence

Code and data: Apache License 2.0 (see `LICENSE`). The bundled DejaVu fonts have their own licence in
`quickbasket/fonts/LICENSE-DejaVu.txt`.

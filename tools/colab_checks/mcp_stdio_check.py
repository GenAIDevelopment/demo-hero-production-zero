"""Checks the MCP server the way the Myth 2 notebook uses it, without any model or API key:
start it over stdio, load its tools through the LangChain MCP adapter, press a button, stop it.
Repeats several times and then checks that no server process is left running.

    python tools/colab_checks/mcp_stdio_check.py            (from the repo root; Windows, Linux or Colab)

Inside a notebook (where an event loop is already running), use:  await check()
"""
import asyncio
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QB = os.path.join(ROOT, "quickbasket")
WORK = os.path.join(QB, "stdiocheck_work.db")


def server_processes():
    """Command lines of running qb_mcp_server.py processes."""
    try:
        if os.name == "nt":
            out = subprocess.run(["powershell", "-NoProfile", "-Command",
                                  "Get-CimInstance Win32_Process -Filter \"name like 'python%'\" | "
                                  "Select-Object -ExpandProperty CommandLine"], capture_output=True, text=True).stdout
        else:
            out = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True).stdout
        return [l for l in out.splitlines() if "qb_mcp_server.py" in l]
    except FileNotFoundError:
        return None


async def check(rounds=3):
    from langchain_mcp_adapters.tools import load_mcp_tools
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    shutil.copyfile(os.path.join(QB, "quickbasket.db"), WORK)
    env = dict(os.environ, QB_WORK_DB=WORK, QB_SESSION_CUSTOMER="C-1001", QB_APPROVAL_LIMIT="500", PYTHONIOENCODING="utf-8")
    params = StdioServerParameters(command=sys.executable, args=[os.path.join(QB, "qb_mcp_server.py")], env=env)
    ok = True
    for i in range(1, rounds + 1):
        t0 = time.time()
        with open(os.devnull, "w") as quiet:
            async with stdio_client(params, errlog=quiet) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = {t.name: t for t in await load_mcp_tools(session)}
                    mine = await tools["get_order"].ainvoke({"customer_id": "C-1001", "order_id": "QB-10309"})
                    other = await tools["get_order"].ainvoke({"customer_id": "C-1001", "order_id": "QB-10311"})
        text = lambda r: r if isinstance(r, str) else "".join(p.get("text", "") for p in r)
        good = json.loads(text(mine))["status"] == "ok" and json.loads(text(other))["status"] == "not_found"
        ok &= good and len(tools) == 4
        print(f"round {i}: {len(tools)} tools, own order {'ok' if good else 'WRONG'}, "
              f"start-to-stop {time.time() - t0:.1f}s")
    await asyncio.sleep(1)
    left = server_processes()
    if left is None:
        print("could not list processes on this system (check by hand)")
    else:
        ok &= not left
        print(f"server processes still running: {len(left)}")
    os.remove(WORK)
    print("PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    sys.exit(0 if asyncio.run(check()) else 1)

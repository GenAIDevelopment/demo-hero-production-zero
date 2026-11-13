"""Writes a 2-cell notebook that runs the MCP check with top-level await, as Colab would. argv[1] = output path."""
import sys
import nbformat as nbf
nb = nbf.v4.new_notebook()
nb.cells = [nbf.v4.new_code_cell("import asyncio, os, sys\nsys.path.insert(0, os.path.join(os.getcwd(), 'tools', 'colab_checks'))\n"
                                 "print('event loop already running:', asyncio.get_event_loop().is_running())\nfrom mcp_stdio_check import check"),
            nbf.v4.new_code_cell("ok = await check()\nprint('top-level await in a notebook kernel:', 'PASS' if ok else 'FAIL')")]
nb.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}}
nbf.write(nb, sys.argv[1])

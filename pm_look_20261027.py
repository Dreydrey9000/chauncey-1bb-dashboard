#!/opt/homebrew/bin python3
# PM 2026-10-27 lookalike pull: rowan + bedros, 240s socket timeout, one pass.
import json, sys, time, re, urllib.request, socket

ENV_PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/tokscript_pull.py"
# reuse the proven caller logic but with a longer timeout
src = open(ENV_PATH).read().replace("timeout=90", "timeout=240")
ns = {"__name__": "tokscript_pm"}
exec(compile(src, "tokscript_pull.py", "exec"), ns)

# Morning inspire brief pull — 2026-10-23 am
# Rotation: rowancheung (Drey contrast), bedroskeuilian + davidmeltzer (Kevin lane; gerardadams dead)
import json, sys, subprocess

SCRIPT = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/tokscript_pull.py'
OUT = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/inspire_am_2026-10-23.txt'

res = subprocess.run(['/opt/homebrew/bin/python3', SCRIPT, 'rowancheung', 'bedroskeuilian', 'davidmeltzer'],
                      capture_output=True, text=True, timeout=420)
open(OUT, 'w').write(res.stdout + '\n---STDERR---\n' + res.stderr)
print(res.stdout)
if res.returncode != 0:
    print('EXIT', res.returncode)

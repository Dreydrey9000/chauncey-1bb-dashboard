# Append the liamottley pull (run separately this run) to the AM raw capture for durable provenance
import subprocess, datetime

SCRIPT = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/tokscript_pull.py'
OUT = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/inspire_am_2026-10-23.txt'

res = subprocess.run(['/opt/homebrew/bin/python3', SCRIPT, 'liamottley'], capture_output=True, text=True, timeout=240)
with open(OUT, 'a') as f:
    f.write('\n=== liamottley re-pull ' + datetime.datetime.now().isoformat(timespec='seconds') + ' (append; first pull went to terminal only) ===\n')
    f.write(res.stdout)
print(res.stdout)
if res.returncode != 0:
    print('EXIT', res.returncode, res.stderr[:300])

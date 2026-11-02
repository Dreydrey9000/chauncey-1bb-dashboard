# Verify inspire.js deploy: date marker + reel URLs + quote parity (2026-11-02 PM edition)
import hashlib, re, urllib.request

MARKER = '2026-11-02 (PM)'
REELS = ['DfPl_vDEgHD', 'DfPYWCsR5ig']

local = open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/site/inspire.js').read()
req = urllib.request.Request('https://1bb-dashboard.pages.dev/inspire.js',
                             headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'})
remote = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')

ok = True
if MARKER not in remote:
    ok = False; print('FAIL: date marker missing remotely')
for r in REELS:
    if r not in remote:
        ok = False; print(f'FAIL: reel {r} missing remotely')
h_l, h_r = hashlib.sha256(local.encode()).hexdigest(), hashlib.sha256(remote.encode()).hexdigest()
print('local  sha256', h_l)
print('remote sha256', h_r)
if h_l != h_r:
    ok = False; print('FAIL: byte mismatch local vs remote')
q_l = len(re.findall(r"(?<!\\)'", local)); q_r = len(re.findall(r"(?<!\\)'", remote))
print(f'quotes local={q_l} remote={q_r}')
if q_l != q_r:
    ok = False; print('FAIL: quote parity')
print('VERIFY:', 'PASS' if ok else 'FAIL')

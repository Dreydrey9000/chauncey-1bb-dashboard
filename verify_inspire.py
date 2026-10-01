import hashlib, re, time, urllib.request

# Generic inspire.js deploy verifier — compares live file against the LOCAL file
# (source of truth for the current run). No per-run hardcoded markers: whatever
# reel URLs and date marker the local brief carries must appear in the deployed file.
# Retries once on mismatch: Cloudflare Pages can serve the previous version for a
# few seconds after "Deployment complete" (observed 2026-09-30).

URL = 'https://1bb-dashboard.pages.dev/inspire.js'
LOCAL = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/site/inspire.js'
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

local = open(LOCAL, encoding='utf-8').read()
local_stripped = local.strip()

def fetch():
    req = urllib.request.Request(URL, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', 'replace')

body = fetch()
if hashlib.sha256(body.strip().encode('utf-8')).hexdigest() != hashlib.sha256(local_stripped.encode('utf-8')).hexdigest():
    time.sleep(15)  # possible CDN lag on fresh deploy
    body = fetch()

remote_hash = hashlib.sha256(body.strip().encode('utf-8')).hexdigest()
local_hash = hashlib.sha256(local_stripped.encode('utf-8')).hexdigest()

marker = re.search(r"date:\s*'([^']+)'", local)
marker = marker.group(1) if marker else ''
reel_urls = sorted(set(re.findall(r'https://www\.instagram\.com/reel/[A-Za-z0-9_-]+/', local)))

checks = {
    f'date marker ({marker})': marker != '' and marker in body,
    'all local reel URLs deployed': bool(reel_urls) and all(u in body for u in reel_urls),
    'structural quotes even': len(re.findall(r"(?<!\\)'", body.split('window.INSPIRE')[1])) % 2 == 0,
    'deployed == local (sha256, stripped)': remote_hash == local_hash,
}
print('HTTP OK, chars:', len(body), '| local chars:', len(local))
for name, ok in checks.items():
    print(('PASS' if ok else 'FAIL'), '-', name)
print('ALL PASS' if all(checks.values()) else 'SOMETHING FAILED')

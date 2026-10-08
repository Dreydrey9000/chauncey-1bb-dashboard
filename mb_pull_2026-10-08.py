#!/usr/bin/env python3
"""Morning-brief pull for 2026-10-08: health, 14d daily metrics (received),
follower stats, and recent posts for Drey IG + Kevin IG via Zernio REST.
Writes JSON snapshots to dashboard/raw/mb_2026-10-08_*.json and prints a digest."""
import json, urllib.request, urllib.error, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
OUT = os.path.join(BASE, 'raw')
os.makedirs(OUT, exist_ok=True)

ACCOUNTS = {
    'drey': '6a1c7e1e2b2567671a7f25ee',
    'kevin': '6a1c97b22b2567671a7ff845',
}

def get(url, timeout=90):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def fetch(url):
    try:
        return get(url)
    except urllib.error.HTTPError as e:
        body = e.read()[:300].decode('utf-8', 'replace')
        return {'_http_error': e.code, '_body': body}
    except Exception as e:
        return {'_error': f'{type(e).__name__}: {e}'}

today = datetime.date.today()
frm14 = (today - datetime.timedelta(days=14)).isoformat()

# 1) health
ids = ','.join(ACCOUNTS.values())
health = fetch(f'https://getlate.dev/api/v1/accounts/health?accountIds={ids}')
print('HEALTH:', json.dumps(health)[:800])

# 2) daily metrics 14d attribution=received
for name, acc in ACCOUNTS.items():
    d = fetch(f'https://getlate.dev/api/v1/analytics/daily-metrics?platform=instagram'
              f'&accountId={acc}&fromDate={frm14}&toDate={today.isoformat()}&attribution=received')
    path = os.path.join(OUT, f'mb_2026-10-08_daily_{name}.json')
    with open(path, 'w') as f:
        json.dump(d, f)
    print(f'DAILY_{name}: saved {path} bytes={os.path.getsize(path)} preview={json.dumps(d)[:300]}')

# 3) follower stats
fs = fetch(f'https://getlate.dev/api/v1/accounts/follower-stats?accountIds={ids}&fromDate={frm14}')
path = os.path.join(OUT, 'mb_2026-10-08_followers.json')
with open(path, 'w') as f:
    json.dump(fs, f)
print(f'FOLLOWERS: saved {path} preview={json.dumps(fs)[:300]}')

# 4) recent posts (page 1 only, for top-post identification)
for name, acc in ACCOUNTS.items():
    p = fetch(f'https://getlate.dev/api/v1/analytics?platform=instagram&accountId={acc}'
              f'&fromDate={frm14}&toDate={today.isoformat()}&limit=50&page=1')
    path = os.path.join(OUT, f'mb_2026-10-08_posts_{name}.json')
    with open(path, 'w') as f:
        json.dump(p, f)
    print(f'POSTS_{name}: saved {path} bytes={os.path.getsize(path)}')

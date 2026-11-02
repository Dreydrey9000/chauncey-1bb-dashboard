#!/usr/bin/env python3
"""Morning brief pull 2026-11-02: health, daily metrics, follower stats (REST fallback)."""
import json, urllib.request, urllib.error, datetime, os

KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
BASE = 'https://getlate.dev/api/v1'
DREY = '6a1c7e1e2b2567671a7f25ee'
KEVIN = '6a1c97b22b2567671a7ff845'
TODAY = datetime.date.today().isoformat()
FROM = (datetime.date.today() - datetime.timedelta(days=14)).isoformat()
OUT = {}

def get(path, **params):
    q = '&'.join(f'{k}={v}' for k, v in params.items())
    url = f'{BASE}/{path}?{q}'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:500]
    except Exception as e:
        return -1, f'{type(e).__name__}: {e}'

# 1. Health
s, b = get('accounts/health')
OUT['health_raw'] = {'status': s, 'body': b[:4000]}
print(f'[health {s}]', b[:600].replace('\n', ' '), sep=' ')

# 2. Daily metrics per account
for name, acc in (('drey', DREY), ('kevin', KEVIN)):
    s, b = get('analytics/daily-metrics', platform='instagram', accountId=acc,
               fromDate=FROM, toDate=TODAY, attribution='received')
    OUT[f'{name}_daily_raw'] = {'status': s, 'body': b}
    print(f'[{name} daily {s}] len={len(b)}')

# 3. Follower stats per account
for name, acc in (('drey', DREY), ('kevin', KEVIN)):
    s, b = get('accounts/follower-stats', accountId=acc, fromDate=FROM)
    OUT[f'{name}_followers_raw'] = {'status': s, 'body': b}
    print(f'[{name} followers {s}] len={len(b)}')

path = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/morning_2026-11-02.json'
os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w') as f:
    json.dump(OUT, f)
print('saved', path)

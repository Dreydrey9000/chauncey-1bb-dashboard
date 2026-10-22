#!/usr/bin/env python3
"""Morning brief pull 2026-10-22: Zernio REST fallback for Drey IG + Kevin IG.
Outputs JSON files under dashboard/raw/mb_2026-10-22/ for the brief builder.
"""
import json, urllib.request, urllib.error, datetime, os, ast, sys

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw', 'mb_2026-10-22')
os.makedirs(RAW, exist_ok=True)
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']

today = datetime.date.today()
D = today - datetime.timedelta(days=1)   # "yesterday"
from14 = (today - datetime.timedelta(days=14)).isoformat()
to_today = today.isoformat()

ACCOUNTS = [
    ('drey_ig', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin_ig', '6a1c97b22b2567671a7ff845'),
]

def get(url, timeout=90):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def unwrap(res):
    if isinstance(res, dict) and 'result' in res and isinstance(res['result'], str):
        try:
            return ast.literal_eval(res['result'])
        except Exception:
            return json.loads(res['result'])
    return res

def save(name, obj):
    p = os.path.join(RAW, name)
    with open(p, 'w') as f:
        json.dump(obj, f, indent=1, default=str)
    print(f'saved {name} ({os.path.getsize(p)} bytes)')

failures = []

# 1. health
try:
    res = unwrap(get("https://getlate.dev/api/v1/accounts/health"))
    save('health.json', res)
    s = json.dumps(res, default=str)
    for acc, aid in ACCOUNTS:
        hit = ('OK' if aid in s else 'NOT-IN-PAYLOAD')
        print(f'health {acc}: {hit}')
except Exception as e:
    failures.append('health')
    print(f'health FAILED: {type(e).__name__}: {e}')

# 2. daily metrics 14d
for key, aid in ACCOUNTS:
    url = (f"https://getlate.dev/api/v1/analytics/daily-metrics?platform=instagram"
           f"&accountId={aid}&fromDate={from14}&toDate={to_today}&attribution=received")
    try:
        res = unwrap(get(url))
        save(f'daily_{key}.json', res)
    except urllib.error.HTTPError as e:
        body = b''
        try:
            body = e.read()
        except Exception:
            pass
        failures.append(f'daily_{key}')
        print(f'daily_{key} FAILED: HTTP {e.code} {body[:300].decode(errors="replace")}')
    except Exception as e:
        failures.append(f'daily_{key}')
        print(f'daily_{key} FAILED: {type(e).__name__}: {e}')

# 3. follower stats 14d
ids = ','.join(a for _, a in ACCOUNTS)
for variant, url in [
    ('fs_a', f"https://getlate.dev/api/v1/accounts/follower-stats?accountIds={ids}&fromDate={from14}&toDate={to_today}"),
    ('fs_b', f"https://getlate.dev/api/v1/accounts/follower-stats?accountIds={ids}&fromDate={from14}"),
]:
    try:
        res = unwrap(get(url))
        save(f'followers_{variant}.json', res)
        break
    except Exception as e:
        print(f'{variant} failed: {type(e).__name__}: {e}')
else:
    failures.append('followers')

print('FAILURES:', json.dumps(failures))

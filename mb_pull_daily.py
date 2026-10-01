#!/usr/bin/env python3
"""Morning brief pull: daily metrics (14d, attribution=received) + follower stats via Zernio REST.
Writes /tmp/mb_daily_<NAME>.json and /tmp/mb_followers.json for the chart/brief steps."""
import json, urllib.request, urllib.error, datetime as dt, sys

KEY = json.load(open(__import__('os').path.expanduser('~/.zernio/config.json')))['apiKey']
today = dt.date.today()
from14 = (today - dt.timedelta(days=14)).isoformat()

ACCOUNTS = [('DREY', '6a1c7e1e2b2567671a7f25ee'), ('KEVIN', '6a1c97b22b2567671a7ff845')]

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())

ok = True
for name, acc in ACCOUNTS:
    url = (f"https://getlate.dev/api/v1/analytics/daily-metrics?platform=instagram&accountId={acc}"
           f"&fromDate={from14}&toDate={today.isoformat()}&attribution=received")
    try:
        res = get(url)
        with open(f'/tmp/mb_daily_{name}.json', 'w') as f:
            json.dump(res, f)
        print(f'{name} daily-metrics OK ({len(json.dumps(res))} bytes)')
    except urllib.error.HTTPError as e:
        ok = False
        print(f'{name} daily-metrics HTTP {e.code}: {e.read()[:300]}')
    except Exception as e:
        ok = False
        print(f'{name} daily-metrics FAILED {type(e).__name__}: {e}')

ids = ','.join(a for _, a in ACCOUNTS)
try:
    res = get(f"https://getlate.dev/api/v1/accounts/follower-stats?accountIds={ids}&fromDate={from14}&toDate={today.isoformat()}")
    with open('/tmp/mb_followers.json', 'w') as f:
        json.dump(res, f)
    print('followers OK (' + str(len(json.dumps(res))) + ' bytes)')
except Exception as e:
    ok = False
    print(f'followers FAILED {type(e).__name__}: {e}')

sys.exit(0 if ok else 1)

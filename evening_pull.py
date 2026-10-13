#!/usr/bin/env python3
"""Evening Check pull: Zernio REST daily-metrics for Drey+Kevin IG (4-day window).
Writes raw payload to dashboard/raw/evening_<name>_<date>.json for reuse."""
import json, urllib.request, urllib.error, datetime, os, ast, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE_DIR, 'raw')
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']

today = datetime.date.today()
from_date = (today - datetime.timedelta(days=4)).isoformat()
to_date = today.isoformat()

ACCOUNTS = [
    ('drey', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin', '6a1c97b22b2567671a7ff845'),
]

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())

def unwrap(res):
    if isinstance(res, dict) and 'result' in res and isinstance(res['result'], str):
        try:
            return ast.literal_eval(res['result'])
        except Exception:
            return json.loads(res['result'])
    return res

failures = []
for name, acc in ACCOUNTS:
    candidates = [
        f"https://getlate.dev/api/v1/analytics/daily-metrics?platform=instagram&accountId={acc}&fromDate={from_date}&toDate={to_date}&attribution=received",
        f"https://getlate.dev/api/v1/analytics/daily_metrics?platform=instagram&accountId={acc}&fromDate={from_date}&toDate={to_date}&attribution=received",
        f"https://getlate.dev/api/v1/analytics/daily-metrics?platform=instagram&account_id={acc}&from_date={from_date}&to_date={to_date}&attribution=received",
        f"https://getlate.dev/api/v1/analytics/metrics/daily?platform=instagram&accountId={acc}&fromDate={from_date}&toDate={to_date}&attribution=received",
    ]
    ok = False
    for url in candidates:
        try:
            data = unwrap(get(url))
            out = os.path.join(RAW, f'evening_{name}_{to_date}.json')
            with open(out, 'w') as f:
                json.dump({'fetched_at': datetime.datetime.now().isoformat(), 'url': url, 'payload': data}, f, default=str)
            print(f'=== {name}: OK via {url.split("v1/")[1].split("?")[0]}')
            print(json.dumps(data, default=str)[:3000])
            ok = True
            break
        except urllib.error.HTTPError as e:
            print(f'{name}: {url.split("v1/")[1].split("?")[0]} -> HTTP {e.code}: {e.read()[:200]}')
        except Exception as e:
            print(f'{name}: {url.split("v1/")[1].split("?")[0]} -> {type(e).__name__}: {str(e)[:200]}')
    if not ok:
        failures.append(name)
        sys.exit(1)
print('ALL OK')

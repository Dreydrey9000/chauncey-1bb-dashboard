#!/usr/bin/env python3
"""Evening check pull: Zernio daily metrics for Drey IG + Kevin IG (REST fallback).
Tries several plausible endpoint paths, saves the first that works to daily_<key>.json.
"""
import json, urllib.request, urllib.error, datetime, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']

today = datetime.date.today()
from_date = (today - datetime.timedelta(days=4)).isoformat()
to_date = today.isoformat()

ACCOUNTS = [
    ('drey_ig', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin_ig', '6a1c97b22b2567671a7ff845'),
]

PATHS = [
    "analytics/daily-metrics",
    "analytics/daily",
    "daily-metrics",
    "metrics/daily",
    "analytics/metrics/daily",
    "analytics",
]

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def unwrap(res):
    if isinstance(res, dict) and 'result' in res and isinstance(res['result'], str):
        import ast
        try:
            return ast.literal_eval(res['result'])
        except Exception:
            return json.loads(res['result'])
    return res

for key, acc_id in ACCOUNTS:
    found = False
    for path in PATHS:
        url = (f"https://getlate.dev/api/v1/{path}?platform=instagram&accountId={acc_id}"
               f"&fromDate={from_date}&toDate={to_date}&attribution=received")
        try:
            res = unwrap(get(url))
        except urllib.error.HTTPError as e:
            body = b''
            try:
                body = e.read()
            except Exception:
                pass
            print(f"{key} {path}: HTTP {e.code} {body[:200].decode(errors='replace')}")
            continue
        except Exception as e:
            print(f"{key} {path}: {type(e).__name__}: {e}")
            continue
        out = os.path.join(BASE, f"daily_{key}.json")
        with open(out, 'w') as f:
            json.dump(res, f, indent=1, default=str)
        print(f"{key}: {path} OK -> {out}")
        print(json.dumps(res, default=str)[:2500])
        found = True
        break
    if not found:
        print(f"{key}: ALL PATHS FAILED")
print("DONE")

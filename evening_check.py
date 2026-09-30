#!/usr/bin/env python3
"""Evening check: pull 5-day daily metrics for Drey/Kevin IG via Zernio REST.
Probe for a daily-metrics endpoint; fall back to per-post attribution math.
Prints everything; writes raw JSON to raw/evening_<handle>.json for the record.
"""
import json, urllib.request, urllib.error, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw')
os.makedirs(RAW, exist_ok=True)
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']

ACCOUNTS = [
    ('drey', 'instagram', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin', 'instagram', '6a1c97b22b2567671a7ff845'),
]

today = datetime.date.today()
from_date = (today - datetime.timedelta(days=4)).isoformat()
to_date = today.isoformat()
print(f'window: {from_date} .. {to_date} (attribution=received)')

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, None
    except Exception as e:
        return 0, {'error': f'{type(e).__name__}: {e}'}

def unwrap(res):
    if isinstance(res, dict) and 'result' in res and isinstance(res['result'], str):
        import ast
        try:
            return ast.literal_eval(res['result'])
        except Exception:
            return json.loads(res['result'])
    return res

# --- probe daily-metrics endpoint shapes ---
probes = [
    ('daily-metrics', '/analytics/daily-metrics'),
    ('daily_metrics', '/analytics/daily_metrics'),
]
drey_acc = ACCOUNTS[0][2]
probe_found = None
for name, path in probes:
    url = (f'https://getlate.dev/api/v1{path}?platform=instagram&accountId={drey_acc}'
           f'&fromDate={from_date}&toDate={to_date}&attribution=received')
    status, body = get(url)
    print(f'PROBE {name}: HTTP {status}')
    if status == 200 and body:
        s = json.dumps(body)[:800]
        print(f'  body: {s}')
        probe_found = path
    elif body is not None:
        print(f'  err: {json.dumps(body)[:300]}')
if probe_found:
    with open(os.path.join(RAW, 'evening_probe.json'), 'w') as f:
        json.dump({'path': probe_found}, f)

# --- main pull: daily metrics if available, else post-level fallback ---
for handle, platform, acc in ACCOUNTS:
    print(f'\n===== {handle.upper()} ({acc}) =====')
    if probe_found:
        url = (f'https://getlate.dev/api/v1{probe_found}?platform={platform}&accountId={acc}'
               f'&fromDate={from_date}&toDate={to_date}&attribution=received')
        status, data = get(url)
        data = unwrap(data) if data else None
        if status == 200 and data:
            with open(os.path.join(RAW, f'evening_{handle}.json'), 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(json.dumps(data, indent=2, default=str)[:3000])
            continue
        print(f'daily-metrics failed for {handle}: HTTP {status}')

    # fallback: post-level analytics, attribution by post receive date
    url = (f'https://getlate.dev/api/v1/analytics?platform={platform}&accountId={acc}'
           f'&fromDate={from_date}&toDate={to_date}&limit=50&page=1')
    status, data = get(url)
    data = unwrap(data) if data else None
    if status != 200 or not data:
        print(f'POST PULL FAILED: HTTP {status} {json.dumps(data)[:300] if data else ""}')
        continue
    with open(os.path.join(RAW, f'evening_{handle}.json'), 'w') as f:
        json.dump(data, f, indent=2, default=str)
    posts = data.get('posts') or []
    print(f'overview: {json.dumps(data.get("overview", {}))[:400]}')
    print(f'posts in window: {len(posts)}')
    for p in posts:
        keep = {k: p.get(k) for k in ('id', 'postedAt', 'timestamp', 'date', 'createdAt',
                                       'caption', 'type', 'mediaType',
                                       'reach', 'impressions', 'views',
                                       'likes', 'comments', 'shares', 'saves')}
        cap = (keep.get('caption') or '')[:60].replace('\n', ' ')
        keep['caption'] = cap
        print(json.dumps(keep, default=str))

print('\nDONE')

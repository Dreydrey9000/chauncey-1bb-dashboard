#!/usr/bin/env python3
"""Probe Zernio REST for the daily-metrics endpoint (MCP unavailable)."""
import json, urllib.request, urllib.error

KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
ACC = '6a1c7e1e2b2567671a7f25ee'

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:
        return -1, f'{type(e).__name__}: {e}'

candidates = [
    'analytics/daily-metrics',
    'analytics/daily',
    'daily-metrics',
    'analytics/metrics/daily',
    'analytics/daily-metrics/instagram',
]
for path in candidates:
    u = (f'https://getlate.dev/api/v1/{path}?platform=instagram&accountId={ACC}'
         '&fromDate=2026-10-23&toDate=2026-10-27&attribution=received')
    s, b = get(u)
    print(f'[{s}] {path}')
    print('   ', b.replace('\n', ' ')[:400])
    print()

# also try the account_id query param name variant on daily-metrics
u = (f'https://getlate.dev/api/v1/analytics/daily-metrics?platform=instagram&profileId={ACC}'
     '&fromDate=2026-10-23&toDate=2026-10-27&attribution=received')
s, b = get(u)
print(f'[{s}] analytics/daily-metrics (profileId param)')
print('   ', b.replace('\n', ' ')[:400])

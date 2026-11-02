#!/usr/bin/env python3
"""Re-pull health fully + analyze pull 2026-11-02."""
import json, urllib.request, os

KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
RAW = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/morning_2026-11-02.json'))

req = urllib.request.Request('https://getlate.dev/api/v1/accounts/health',
                             headers={'Authorization': f'Bearer {KEY}'})
with urllib.request.urlopen(req, timeout=90) as r:
    h = json.loads(r.read().decode())

for a in h.get('accounts', []):
    if a.get('accountId') in ('6a1c7e1e2b2567671a7f25ee', '6a1c97b22b2567671a7ff845'):
        print('HEALTH', a.get('username'), a.get('status'),
              '| sync', a.get('analyticsSync', {}).get('status'), a.get('analyticsSync', {}).get('lastSyncedAt'),
              '| token', a.get('tokenValid'), '| issues', a.get('issues'))

d = json.loads(RAW['drey_daily_raw']['body'])
print('\nDAILY keys:', list(d.keys()))
metrics = d.get('metrics', d.get('data', d))
if isinstance(metrics, list):
    print('n days:', len(metrics), '| day keys:', sorted(metrics[-1].keys()))
    for row in metrics:
        print(row)
else:
    print(json.dumps(d, indent=1)[:3000])

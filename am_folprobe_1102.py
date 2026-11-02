#!/usr/bin/env python3
"""Probe follower-stats response + find the right filter for our two accounts."""
import json, urllib.request, urllib.error

KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
RAW = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/morning_2026-11-02.json'))
DREY = '6a1c7e1e2b2567671a7f25ee'
KEVIN = '6a1c97b22b2567671a7ff845'

fs = json.loads(RAW['drey_followers_raw']['body'])
print('dateRange:', fs.get('dateRange'), '| granularity:', fs.get('granularity'))
print('n accounts:', len(fs.get('accounts', [])))
print('stats type:', type(fs.get('stats')))
st = fs.get('stats')
if isinstance(st, list):
    print('stats[0]:', json.dumps(st[0])[:600])
elif isinstance(st, dict):
    print('stats keys:', list(st.keys()))
    k0 = list(st.keys())[0]
    print('stats[first]:', json.dumps(st[k0])[:600])

def get(path, **params):
    q = '&'.join(f'{k}={v}' for k, v in params.items())
    req = urllib.request.Request(f'https://getlate.dev/api/v1/{path}?{q}',
                                 headers={'Authorization': f'Bearer {KEY}'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return -1, f'{type(e).__name__}: {e}'

# try profileId variant
for acc in (DREY, KEVIN):
    s, b = get('accounts/follower-stats', profileId=acc, fromDate='2026-10-19')
    d = json.loads(b) if s == 200 else {}
    accts = d.get('accounts', [])
    stats = d.get('stats')
    stats_s = json.dumps(stats) if stats is not None else 'null'
    print(f'\n[{acc} profileId {s}] n_accounts={len(accts)} stats_len={len(stats_s)}')
    if s == 200 and len(stats_s) < 5000:
        print(stats_s[:1500])

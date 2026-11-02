#!/usr/bin/env python3
"""Pull this week's posts for both accounts (Instagram, 7d) + best performer analytics."""
import json, urllib.request, urllib.error, os

KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
BASE = 'https://getlate.dev/api/v1'
DREY = '6a1c7e1e2b2567671a7f25ee'
KEVIN = '6a1c97b22b2567671a7ff845'
OUT = {}

def get(path, **params):
    q = '&'.join(f'{k}={v}' for k, v in params.items())
    req = urllib.request.Request(f'{BASE}/{path}?{q}',
                                 headers={'Authorization': f'Bearer {KEY}'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return -1, f'{type(e).__name__}: {e}'

for name, acc in (('drey', DREY), ('kevin', KEVIN)):
    s, b = get('posts', platform='instagram', accountId=acc,
               fromDate='2026-10-27', toDate='2026-11-02', limit=50)
    OUT[f'{name}_posts_raw'] = {'status': s, 'body': b}
    print(f'[{name} posts {s}] len={len(b)}')
    if s == 200:
        d = json.loads(b)
        posts = d.get('posts', d.get('data', []))
        print(f'  n={len(posts)}')
        for p in posts[:20]:
            an = p.get('analytics') or {}
            print(f"  {p.get('publishedAt', '?')[:10]} | views={an.get('views')} likes={an.get('likes')} "
                  f"comments={an.get('comments')} | {(p.get('content') or '')[:60]!r}")

path = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_posts_1102.json'
with open(path, 'w') as f:
    json.dump(OUT, f)
print('saved', path)

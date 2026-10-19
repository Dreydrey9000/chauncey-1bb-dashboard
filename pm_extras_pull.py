#!/usr/bin/env python3
"""Evening extras: TikTok fresh posts (3-day window) + IG daily-metrics impressions for today,
to catch same-day activity that per-post analytics lag on."""
import json, os, urllib.request, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
API = 'https://getlate.dev/api/v1'

TT = [('drey_tt', '6a1c7f242b2567671a7f30a4'), ('kevin_tt', '6a1c97a12b2567671a7ff6ff')]
IG = [('drey_ig', '6a1c7e1e2b2567671a7f25ee'), ('kevin_ig', '6a1c97b22b2567671a7ff845')]

fd = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
td = datetime.date.today().isoformat()

def get(path):
    req = urllib.request.Request(f'{API}/{path}', headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

for name, aid in TT:
    try:
        d = get(f'analytics?platform=tiktok&accountId={aid}&fromDate={fd}&toDate={td}&limit=50&page=1')
        posts = d.get('posts', [])
        print(f'=== {name}: {len(posts)} tiktok posts since {fd}')
        for p in posts:
            an = p.get('analytics') or {}
            print(' ', json.dumps({'url': p.get('platformPostUrl'), 'at': p.get('publishedAt'),
                                   'views': an.get('views'), 'likes': an.get('likes')}, default=str)[:300])
            print('   cap:', str(p.get('content') or '')[:100].replace('\n', ' '))
    except Exception as e:
        print(f'{name}: FAILED {e!r}')

for name, aid in IG:
    for qs in (f'fromDate={fd}&toDate={td}', f'from={fd}&to={td}'):
        try:
            d = get(f'analytics/daily-metrics?platform=instagram&accountId={aid}&{qs}')
            s = json.dumps(d, default=str)
            print(f'=== {name} daily-metrics ({qs}): {s[:600]}')
            break
        except Exception as e:
            print(f'{name} daily-metrics ({qs}): FAILED {e!r}')

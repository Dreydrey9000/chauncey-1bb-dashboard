#!/usr/bin/env python3
"""Evening delta 2026-11-25 PM: fresh Zernio pull (3-day window) + medians from posts_all.csv."""
import json, os, csv, urllib.request, datetime, statistics

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw')
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
API = 'https://getlate.dev/api/v1'

ACCOUNTS = [
    ('drey_ig',  'instagram', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin_ig', 'instagram', '6a1c97b22b2567671a7ff845'),
]
fd = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
td = datetime.date.today().isoformat()

def get(path):
    req = urllib.request.Request(f'{API}/{path}', headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

fresh = {}
for key, platform, aid in ACCOUNTS:
    try:
        d = get(f'analytics?platform={platform}&accountId={aid}&fromDate={fd}&toDate={td}&limit=50&page=1')
        posts = d.get('posts', [])
        out = []
        for p in posts:
            an = p.get('analytics') or {}
            out.append({
                'id': p.get('_id') or p.get('latePostId'),
                'url': p.get('platformPostUrl'),
                'caption': str(p.get('content') or '')[:120],
                'posted_at': p.get('publishedAt'),
                'views': an.get('views'),
                'likes': an.get('likes'),
                'comments': an.get('comments'),
            })
        fresh[key] = out
        print(f'=== {key}: {len(out)} posts since {fd}')
        for o in out:
            print(json.dumps(o, default=str)[:400])
    except Exception as e:
        fresh[key] = {'error': repr(e)[:300]}
        print(f'{key}: FAILED {e!r}')

with open(os.path.join(RAW, f'pm_delta_{td}.json'), 'w') as f:
    json.dump({'fetched_at': datetime.datetime.now().isoformat(), 'fresh': fresh}, f, default=str)
print('saved raw/pm_delta_' + td + '.json')

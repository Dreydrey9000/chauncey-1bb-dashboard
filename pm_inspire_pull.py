#!/usr/bin/env python3
"""Evening inspire delta: pull fresh founder posts (last 3 days) via Zernio REST
and compare per-post views against the medians in posts_all.csv (which reflects
the 6:30a refresh). Writes raw/pm_delta_<date>.json for reuse."""
import json, os, csv, urllib.request, urllib.error, datetime, statistics

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

# medians from posts_all.csv for beat/miss calls
def medians(prefix):
    rows = []
    with open(os.path.join(BASE, 'posts_all.csv')) as f:
        for r in csv.DictReader(f):
            if r['account'] == prefix:
                try:
                    rows.append((r['date'], int(float(r['views'] or 0)), r['post_type'] if 'post_type' in r else ''))
                except Exception:
                    pass
    all_v = [v for _, v, _ in rows]
    print(f'{prefix}: n={len(rows)} overall median views={statistics.median(all_v) if all_v else "n/a"}')

for k in ('drey_ig', 'kevin_ig'):
    medians(k)

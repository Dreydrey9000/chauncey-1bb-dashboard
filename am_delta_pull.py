# AM brief 2026-10-21: pull fresh Zernio data (3-day window) for beat/miss calls
import json, os, urllib.request
from datetime import datetime, timezone

DASH = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']

ACCTS = {
    'drey_ig': ('instagram', '6a1c7e1e2b2567671a7f25ee'),
    'kevin_ig': ('instagram', '6a1c97b22b2567671a7ff845'),
}

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())

def unwrap(res):
    if isinstance(res, dict) and 'result' in res and isinstance(res['result'], str):
        import ast
        try:
            return ast.literal_eval(res['result'])
        except Exception:
            return json.loads(res['result'])
    return res

out = {}
for label, (platform, acc_id) in ACCTS.items():
    posts = []
    page = 1
    while True:
        url = (f'https://getlate.dev/api/v1/analytics?platform={platform}'
               f'&accountId={acc_id}&fromDate=2026-10-18&toDate=2026-10-21'
               f'&limit=50&page={page}')
        data = unwrap(get(url))
        rows = data.get('posts') or []
        if not rows:
            break
        posts.extend(rows)
        if len(rows) < 50:
            break
        page += 1
    out[label] = posts
    print(f'{label}: {len(posts)} posts')

json.dump(out, open(DASH + '/raw/am_delta_2026-10-21.json', 'w'), indent=1)

cutoff = datetime(2026, 10, 19, tzinfo=timezone.utc)
for label, posts in out.items():
    print('=' * 12, label)
    for p in posts:
        ts = p.get('publishedAt') or p.get('published_at') or ''
        try:
            dt = datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
        except Exception:
            dt = None
        if not dt or dt < cutoff:
            continue
        a = p.get('analytics') or {}
        print(json.dumps({
            'ts': str(ts),
            'url': p.get('platformPostUrl'),
            'views': a.get('views'),
            'likes': a.get('likes'),
            'comments': a.get('comments'),
            'is_reel': '/reel/' in (p.get('platformPostUrl') or ''),
            'caption': (p.get('content') or '')[:90],
        }))

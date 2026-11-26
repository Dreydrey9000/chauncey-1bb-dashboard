# AM fresh pull (2026-11-26): founder posts, last 3 days, FULL captions (for slogan check + fresh numbers)
import json, os, urllib.request, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
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

out = {}
for key, platform, aid in ACCOUNTS:
    d = get(f'analytics?platform={platform}&accountId={aid}&fromDate={fd}&toDate={td}&limit=50&page=1')
    posts = d.get('posts', [])
    rows = []
    for p in posts:
        an = p.get('analytics') or {}
        rows.append({
            'url': p.get('platformPostUrl'),
            'caption': str(p.get('content') or ''),
            'posted_at': p.get('publishedAt'),
            'views': an.get('views'), 'likes': an.get('likes'), 'comments': an.get('comments'),
        })
    out[key] = rows
    print(f'=== {key} ({len(rows)} posts since {fd}) ===')
    for r in rows:
        cap = r['caption'].replace('\n', ' ¶ ')
        print(f"{r['posted_at']} | views={r['views']} likes={r['likes']} com={r['comments']} | {r['url']}")
        print(f'    CAPTION-FULL: {cap}')

with open(os.path.join(BASE, 'raw', f'am_delta_{td}.json'), 'w') as f:
    json.dump({'fetched_at': datetime.datetime.now().isoformat(), 'fresh': out}, f, default=str)
print('saved raw/am_delta_' + td + '.json')

#!/usr/bin/env python3
"""Fetch full per-post analytics for all posts of this week, rank best per account."""
import json, urllib.request, urllib.error

KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
BASE = 'https://getlate.dev/api/v1'
P = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_posts_1102.json'))

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

result = {}
for name in ('drey', 'kevin'):
    d = json.loads(P[f'{name}_posts_raw']['body'])
    posts = d.get('posts', d.get('data', []))
    ranked = []
    for p in posts:
        pl = (p.get('platforms') or [{}])[0]
        pid = pl.get('platformPostId') or p.get('_id')
        s, b = get('analytics', platform='instagram', postId=pid)
        an = json.loads(b) if s == 200 else {'error': b[:120]}
        views = an.get('views') or an.get('impressions')
        ranked.append({
            'platformPostId': pid, 'publishedAt': pl.get('publishedAt'),
            'caption': p.get('content'), 'url': pl.get('platformPostUrl'),
            'analytics': an,
        })
        print(f"{name} {str(pl.get('publishedAt'))[:10]} views={views} likes={an.get('likes')} "
              f"comments={an.get('comments')} saves={an.get('saves')} | {(p.get('content') or '')[:48]!r}")
    ok = [r for r in ranked if (r['analytics'].get('views') or r['analytics'].get('impressions'))]
    if ok:
        best = max(ok, key=lambda r: r['analytics'].get('views') or r['analytics'].get('impressions'))
        print(f"  >> {name} BEST: {json.dumps({k: best['analytics'].get(k) for k in ('views','likes','comments','saves','shares','reach')})} | {best['caption'][:70]!r}")
    result[name] = ranked

with open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_postan_1102.json', 'w') as f:
    json.dump(result, f, indent=1)
print('saved')

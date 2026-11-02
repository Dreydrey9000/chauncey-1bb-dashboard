#!/usr/bin/env python3
"""Fetch per-post analytics for this week's posts + identify best performer."""
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

for name in ('drey', 'kevin'):
    d = json.loads(P[f'{name}_posts_raw']['body'])
    posts = d.get('posts', d.get('data', []))
    print(f'\n== {name}: {len(posts)} posts ==')
    ranked = []
    for p in posts:
        pl = (p.get('platforms') or [{}])[0]
        pub = pl.get('publishedAt') or ''
        cap = (p.get('content') or '').replace('\n', ' ')[:55]
        pid = pl.get('platformPostId') or p.get('_id')
        s, b = get('analytics', platform='instagram', postId=pid)
        an = {}
        if s == 200:
            try:
                an = json.loads(b)
            except Exception:
                an = {'raw': b[:200]}
        views = (an.get('views') if isinstance(an, dict) else None)
        print(f"  {pub[:10] or '?'} pid={str(pid)[:24]} views={views} | {cap!r}")
        ranked.append({'pid': pid, 'publishedAt': pub, 'caption': p.get('content'),
                       'url': pl.get('platformPostUrl'), 'status': s, 'analytics': an})
    ranked_ok = [r for r in ranked if isinstance(r['analytics'], dict) and r['analytics'].get('views')]
    if ranked_ok:
        best = max(ranked_ok, key=lambda r: r['analytics'].get('views') or 0)
        print(f"  BEST: {best['analytics'].get('views')} views | {best['caption'][:70]!r} | {best['url']}")
    with open(f'/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_postan_{name}_1102.json', 'w') as f:
        json.dump(ranked, f, indent=1)

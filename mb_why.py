#!/usr/bin/env python3
"""Morning brief WHY: top posts last 7 days from raw Zernio pulls + daily post-day identification."""
import json, glob, ast, datetime as dt

today = dt.date.today()
cutoff = (today - dt.timedelta(days=7)).isoformat()

def load_raw(key):
    posts = []
    for f in sorted(glob.glob(f'/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/{key}_p*.txt')):
        payload = json.load(open(f))
        res = payload.get('result') if isinstance(payload, dict) else payload
        if isinstance(res, str):
            try:
                res = ast.literal_eval(res)
            except Exception:
                res = json.loads(res)
        posts.extend(res.get('posts') or [])
    return posts

def num(p, k):
    v = p.get(k)
    return v if isinstance(v, (int, float)) else 0

for key, label in (('drey_ig', 'DREY'), ('kevin_ig', 'KEVIN')):
    posts = load_raw(key)
    dated = []
    for p in posts:
        d = (p.get('publishedAt') or p.get('createdAt') or p.get('date') or '')[:10]
        dated.append((d, p))
    ds = sorted({d for d, _ in dated if d})
    print(f'== {label} == total {len(posts)}, date range {ds[0] if ds else None} -> {ds[-1] if ds else None}')
    if posts:
        a = posts[0].get('analytics') or {}
        print('analytics keys:', sorted(a.keys()) if isinstance(a, dict) else type(a))
        c0 = posts[0].get('content')
        print('content type:', type(c0).__name__, '| str sample:', (c0[:80] if isinstance(c0, str) else ''))
    recent = [(d, p) for d, p in dated if d and d >= cutoff]
    print(f'posts since {cutoff}: {len(recent)}')

    def an(p, k):
        a = p.get('analytics') or {}
        v = a.get(k) if isinstance(a, dict) else None
        return v if isinstance(v, (int, float)) else 0

    ranked = sorted(recent, key=lambda dp: an(dp[1], 'views') or an(dp[1], 'likes'), reverse=True)
    for d, p in ranked[:6]:
        a = p.get('analytics') or {}
        c = p.get('content') or {}
        cap = ((c.get('caption') if isinstance(c, dict) else c) or '')[:80].replace('\n', ' ')
        stats = {k: a.get(k) for k in ('views', 'likes', 'comments', 'shares', 'saves') if isinstance(a, dict) and k in a}
        print(d, p.get('mediaType'), stats, '|', cap)
    print()

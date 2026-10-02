#!/usr/bin/env python3
"""Kevin prev7 top posts (explain WoW drop) + yesterday's post detail."""
import json, glob, ast, datetime as dt

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

def an(p, k):
    a = p.get('analytics') or {}
    v = a.get(k) if isinstance(a, dict) else None
    return v if isinstance(v, (int, float)) else 0

posts = load_raw('kevin_ig')
prev = [(p.get('publishedAt', '')[:10], p) for p in posts if '2026-09-18' <= p.get('publishedAt', '')[:10] <= '2026-09-24']
yday = [(p.get('publishedAt', '')[:10], p) for p in posts if p.get('publishedAt', '')[:10] == '2026-10-01']
print(f'prev7 posts: {len(prev)}, yesterday posts: {len(yday)}')
ranked = sorted(prev, key=lambda dp: an(dp[1], 'views'), reverse=True)
print('-- prev7 top 5 by views --')
for d, p in ranked[:5]:
    c = p.get('content')
    cap = (c if isinstance(c, str) else (c or {}).get('caption', ''))[:90].replace('\n', ' ')
    print(d, p.get('mediaType'), {k: an(p, k) for k in ('views', 'likes', 'comments', 'shares', 'saves')}, '|', cap)
print('-- yesterday (10-01) --')
for d, p in yday:
    c = p.get('content')
    cap = (c if isinstance(c, str) else (c or {}).get('caption', ''))[:150].replace('\n', ' ')
    print(d, p.get('mediaType'), {k: an(p, k) for k in ('views', 'likes', 'comments', 'shares', 'saves', 'reach')}, '|', cap)
# daily reach series for chart check
for name in ('DREY', 'KEVIN'):
    rows = json.load(open(f'/tmp/mb_daily_{name}.json'))['dailyData']
    print(name, 'series:', [(r['date'][5:], r.get('metrics', {}).get('reach')) for r in rows])

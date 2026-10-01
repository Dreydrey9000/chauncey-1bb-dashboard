#!/usr/bin/env python3
"""Rank last-7d IG posts per account (publishedAt + analytics sub-dict)."""
import json, ast, glob, datetime as dt

def load_raw(key):
    posts = []
    for f in sorted(glob.glob(f'/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/{key}_p*.txt')):
        payload = json.load(open(f))
        res = payload.get('result') if isinstance(payload, dict) else payload
        if isinstance(res, str):
            try: res = ast.literal_eval(res)
            except Exception: res = json.loads(res)
        posts.extend(res.get('posts') or [])
    return posts

def parse_analytics(p):
    a = p.get('analytics')
    if isinstance(a, str):
        try: a = ast.literal_eval(a)
        except Exception: a = {}
    return a or {}

today = dt.date.today()
cutoff = (today - dt.timedelta(days=7)).isoformat()

for key, label in (('drey_ig', 'DREY'), ('kevin_ig', 'KEVIN')):
    ps = load_raw(key)
    rows = []
    for p in ps:
        d = str(p.get('publishedAt') or '')[:10]
        a = parse_analytics(p)
        views = a.get('views') or a.get('impressions') or 0
        rows.append({'date': d, 'views': views, 'reach': a.get('reach'), 'likes': a.get('likes'),
                     'comments': a.get('comments'), 'shares': a.get('shares'), 'saves': a.get('saves'),
                     'type': p.get('mediaType'), 'product': p.get('mediaProductType'),
                     'url': p.get('platformPostUrl'), 'caption': str(p.get('content') or '')})
    rows.sort(key=lambda r: r['date'], reverse=True)
    recent = [r for r in rows if r['date'] >= cutoff]
    print(f'-- {label}: {len(recent)} posts since {cutoff} (newest: {rows[0]["date"] if rows else "none"}) --')
    ranked = sorted(recent, key=lambda r: (r['views'] or 0), reverse=True)
    for r in ranked[:6]:
        inter = (r['likes'] or 0) + (r['comments'] or 0) + (r['shares'] or 0) + (r['saves'] or 0)
        print(r['date'], f"views={r['views']} reach={r['reach']} likes={r['likes']} comments={r['comments']} shares={r['shares']} saves={r['saves']} inter={inter} {r['product']}/{r['type']}")
        print('   ', r['url'], '|', r['caption'][:90].replace('\n', ' '))

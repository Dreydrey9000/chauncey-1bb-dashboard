#!/usr/bin/env python3
"""Per-post analytics summary from posts_<key>_ig.json (analytics sub-dict)."""
import json, os, datetime

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw', 'mb_2026-10-22')
today = datetime.date.today()

for key in ['drey', 'kevin']:
    posts = json.load(open(os.path.join(RAW, f'posts_{key}_ig.json')))
    print(f'\n================ {key.upper()} posts (last 14d) ================')
    rows = []
    for p in posts:
        a = p.get('analytics') or {}
        pub = p.get('publishedAt', '?')
        cap = (p.get('content') or '').strip().split('\n')[0][:70]
        rows.append({
            'date': pub[:10],
            'type': p.get('mediaType', '?'),
            'views': a.get('views', a.get('playCount')),
            'reach': a.get('reach'),
            'likes': a.get('likes'),
            'comments': a.get('comments'),
            'saves': a.get('saves'),
            'shares': a.get('shares'),
            'caption': cap,
            'url': p.get('platformPostUrl', ''),
            'external': p.get('isExternal'),
        })
    rows.sort(key=lambda r: r['date'], reverse=True)
    for r in rows:
        print(f"{r['date']} {r['type']:<9} views={r['views']} reach={r['reach']} likes={r['likes']} "
              f"c={r['comments']} s={r['saves']} sh={r['shares']} ext={r['external']} | {r['caption']}")
    # top this week by views then likes
    wk = [r for r in rows if r['date'] >= (today - datetime.timedelta(days=7)).isoformat()]
    if wk:
        top = max(wk, key=lambda r: (r.get('views') or 0, r.get('likes') or 0))
        print(f"--> TOP THIS WEEK: {top['date']} views={top['views']} likes={top['likes']} | {top['caption']}")
    with open(os.path.join(RAW, f'postrows_{key}.json'), 'w') as f:
        json.dump(rows, f, indent=1, default=str)
print('\nsaved postrows_<key>.json')

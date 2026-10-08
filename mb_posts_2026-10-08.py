#!/usr/bin/env python3
"""Post-level analytics for the 2026-10-08 brief: this week's top posts + follower deltas."""
import json, os

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw')

fs = json.load(open(os.path.join(RAW, 'mb_2026-10-08_followers.json')))
for acc in fs.get('accounts', []):
    print('==', acc.get('username'), '==')
    print('  currentFollowers:', acc.get('currentFollowers'), '| growth(14d):', acc.get('growth'), f"({acc.get('growthPercentage')}%)")
    st = acc.get('accountStats') or {}
    print('  mediaCount:', st.get('mediaCount'), '| follows:', st.get('followsCount'))

INTER = ['likes', 'comments', 'shares', 'saves']

for name in ['kevin', 'drey']:
    p = json.load(open(os.path.join(RAW, f'mb_2026-10-08_posts_{name}.json')))
    posts = p.get('posts') or []
    def score(po):
        a = po.get('analytics') or {}
        return sum(a.get(k) or 0 for k in INTER)
    wk = [po for po in posts if str(po.get('publishedAt') or '')[:10] >= '2026-10-01']
    print(f'== {name} this-week posts: {len(wk)} of {len(posts)} ==')
    for po in sorted(wk, key=score, reverse=True)[:3]:
        a = po.get('analytics') or {}
        print(' ', str(po.get('publishedAt'))[:10], po.get('mediaType'), '| likes', a.get('likes'), 'comments', a.get('comments'),
              'shares', a.get('shares'), 'saves', a.get('saves'), '| reach', a.get('reach'), 'views', a.get('views'),
              '|', str(po.get('content') or '').replace('\n', ' ')[:80])

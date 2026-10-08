#!/usr/bin/env python3
"""Inspect follower payload and post field names for the 2026-10-08 brief."""
import json, os

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw')

fs = json.load(open(os.path.join(RAW, 'mb_2026-10-08_followers.json')))
for acc in fs.get('accounts', []):
    print('==', acc.get('username'), '==')
    print('  currentFollowers:', acc.get('currentFollowers'))
    print('  lastUpdated:', acc.get('lastUpdated'))
    print('  growth:', acc.get('growth'), 'growthPercentage:', acc.get('growthPercentage'))
    dp = acc.get('dataPoints')
    print('  dataPoints type:', type(dp).__name__, 'len:', len(dp) if hasattr(dp, '__len__') else None)
    if isinstance(dp, list) and dp:
        print('  first:', json.dumps(dp[0])[:200])
        print('  last:', json.dumps(dp[-1])[:200])
    elif isinstance(dp, dict):
        items = sorted(dp.items())[:3]
        print('  sample:', items)
    st = acc.get('accountStats')
    if st:
        print('  accountStats:', json.dumps(st)[:300])

for name in ['kevin', 'drey']:
    p = json.load(open(os.path.join(RAW, f'mb_2026-10-08_posts_{name}.json')))
    posts = p.get('posts') or []
    print(f'== posts_{name}: {len(posts)} ==')
    if posts:
        print('  keys:', sorted(posts[0].keys()))
        print('  sample0:', json.dumps(posts[0])[:600])

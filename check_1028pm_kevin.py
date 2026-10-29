#!/usr/bin/env python3
"""One-off: print all Kevin IG posts in raw/pm_delta_2026-10-28.json (yesterday 6:01p ET pull)."""
import json, os
BASE = os.path.dirname(os.path.abspath(__file__))
j = json.load(open(os.path.join(BASE, 'raw', 'pm_delta_2026-10-28.json')))
posts = j['fresh'].get('kevin_ig', [])
print('kevin_ig posts in 10-28 6:01p ET pull:', len(posts))
for p in posts:
    print(p.get('posted_at'), '| views', p.get('views'), '| likes', p.get('likes'),
          '| com', p.get('comments'), '|', p.get('url'))
    print('   ', str(p.get('caption'))[:100].replace('\n', ' '))

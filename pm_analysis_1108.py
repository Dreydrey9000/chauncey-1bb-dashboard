#!/usr/bin/env python3
"""PM 2026-11-08: posts_all.csv recent rows + medians by founder and media type."""
import csv, os, statistics, collections

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
print('cols:', list(rows[0].keys()))

for acct in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acct]
    print(f'\n=== {acct} n={len(sub)}')
    recent = [r for r in sub if r['date'] >= '2026-11-04']
    for r in sorted(recent, key=lambda x: x['date']):
        print(' | '.join(str(r.get(k, '')) for k in
              ('date', 'post_type', 'media_type', 'views', 'likes', 'comments', 'caption'))[:220])
    # medians by type
    by = collections.defaultdict(list)
    for r in sub:
        try:
            v = int(float(r['views'] or 0))
        except Exception:
            continue
        t = r.get('post_type') or r.get('media_type') or '?'
        by[t].append(v)
    for t, vs in sorted(by.items()):
        print(f'  median[{t}] n={len(vs)} = {statistics.median(vs)}')
    allv = [int(float(r['views'] or 0)) for r in sub if (r['views'] or '').strip().replace('.', '', 1).isdigit()]
    print(f'  median[ALL] n={len(allv)} = {statistics.median(allv)}')

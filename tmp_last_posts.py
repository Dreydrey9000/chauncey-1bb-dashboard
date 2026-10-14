# Last post dates per account (cron-safe temp script)
import csv
from collections import defaultdict

rows = list(csv.DictReader(open('posts_all.csv')))
last = {}
for r in rows:
    acc = r['account']
    if acc not in last or r['date'] > last[acc][0]:
        last[acc] = (r['date'], r['views'], r['theme'], r['is_reel'], r['url'][:60])
for acc, v in sorted(last.items()):
    print(acc, '->', v)

# Drey theme medians (ig only) to re-verify the standing anchor
import statistics
th = defaultdict(list)
for r in rows:
    if r['account'] == 'drey_ig':
        try:
            th[r['theme']].append(float(r['views']))
        except (TypeError, ValueError):
            pass
print('\ndrey_ig theme medians:')
for t, v in sorted(th.items(), key=lambda x: -statistics.median(x[1])):
    print(f'  {t:12s} n={len(v):2d} median={statistics.median(v):7.0f}')

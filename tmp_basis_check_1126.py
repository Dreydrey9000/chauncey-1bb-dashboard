# Basis check: Drey reel medians — all-time (n=53) vs last-30-reels (AM convention 159.5 n=30).
import csv, statistics
BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = list(csv.DictReader(open(BASE + '/posts_all.csv')))
fr = [r for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and '/reel/' in str(r.get('url', '')) and '/stories/' not in str(r.get('url', ''))]
fr.sort(key=lambda r: r['ts'], reverse=True)
vals = [int(float(r['views'] or 0)) for r in fr]
print(f'all-time: n={len(vals)} median={repr(statistics.median(vals))}')
print(f'last 30: n=30 median={repr(statistics.median(vals[:30]))}')
print(f'last 30 values: {vals[:30]}')
print(f'152 vs last-30 median: {round(152/statistics.median(vals[:30])*100, 1)}%')
print(f'152 vs all-time median: {round(152/statistics.median(vals)*100, 1)}%')

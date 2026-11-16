import csv, statistics
from collections import defaultdict

rows = list(csv.DictReader(open('posts_all.csv')))
for r in rows:
    r['views_n'] = int(r['views']) if r['views'] not in (None, '') else None
    r['reel'] = r['is_reel'] == 'True'

def med(v):
    v = sorted(x for x in v if x is not None)
    return statistics.median(v) if v else None

# Drey IG reels by theme
print("=== DREY IG reels by theme (n, median views) ===")
g = defaultdict(list)
for r in rows:
    if r['account'] == 'drey_ig' and r['reel'] and r['views_n'] is not None:
        g[r['theme']].append(r['views_n'])
for t, v in sorted(g.items(), key=lambda kv: -med(kv[1])):
    print(f"{t:12s} n={len(v):3d} median={med(v):8.0f}")

print()
print("=== KEVIN IG by theme x format (n, median views) ===")
g2 = defaultdict(list)
for r in rows:
    if r['account'] == 'kevin_ig' and r['views_n'] is not None:
        g2[(r['theme'], r['reel'])].append(r['views_n'])
for (t, reel), v in sorted(g2.items(), key=lambda kv: -med(kv[1])):
    print(f"{t:12s} {'reel' if reel else 'static':6s} n={len(v):3d} median={med(v):8.0f}")

print()
print("=== 5 most recent per founder (date, theme, reel, views) ===")
for acct in ('drey_ig', 'kevin_ig'):
    print(f"--- {acct}")
    sub = sorted([r for r in rows if r['account'] == acct], key=lambda r: r['date'], reverse=True)[:5]
    for r in sub:
        print(f"{r['date']} {r['theme']:10s} {'reel' if r['reel'] else 'static':6s} views={r['views_n']}")

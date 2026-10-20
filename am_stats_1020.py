#!/opt/homebrew/bin python3
"""AM brief medians for 2026-10-20 — recomputed from posts_all.csv (official API export)."""
import csv, statistics, os
BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
def med(name, pred):
    v = [int(r['views']) for r in rows if r['account'] and pred(r) and r['views'] not in ('', '0')]
    v2 = [int(r['views']) for r in rows if r['account'] and pred(r) and r['views'] != '']
    print(f'{name}: n={len(v2)} median={statistics.median(v2) if v2 else None} (excl-0 n={len(v)} median={statistics.median(v) if v else None})')
med('drey_ig ALL', lambda r: r['account'] == 'drey_ig')
med('drey_ig reels', lambda r: r['account'] == 'drey_ig' and r['is_reel'] == 'True')
med('drey_ig ai_systems', lambda r: r['account'] == 'drey_ig' and r['theme'] == 'ai_systems')
med('drey_ig confession', lambda r: r['account'] == 'drey_ig' and r['theme'] == 'confession')
med('kevin_ig ALL', lambda r: r['account'] == 'kevin_ig')
med('kevin_ig statics', lambda r: r['account'] == 'kevin_ig' and r['is_reel'] == 'False')
med('kevin_ig reels', lambda r: r['account'] == 'kevin_ig' and r['is_reel'] == 'True')
med('kevin_ig identity', lambda r: r['account'] == 'kevin_ig' and r['theme'] == 'identity')
med('kevin_ig room', lambda r: r['account'] == 'kevin_ig' and r['theme'] == 'room')
# last drey reels by date for streak context
dreys = sorted([r for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'True'], key=lambda r: r['date'])
print('\nDrey last 6 reels:')
for r in dreys[-6:]:
    print(f"  {r['date']} views={r['views']} theme={r['theme']} {r['url']}")

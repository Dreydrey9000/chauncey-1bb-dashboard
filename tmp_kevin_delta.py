# Kevin theme medians + Oct 12/13 detail + mtime check (cron-safe temp script)
import csv, os, statistics, datetime
from collections import defaultdict

st = os.stat('posts_all.csv')
print('posts_all.csv mtime:', datetime.datetime.fromtimestamp(st.st_mtime).isoformat())

rows = list(csv.DictReader(open('posts_all.csv')))

th = defaultdict(list)
for r in rows:
    if r['account'] == 'kevin_ig':
        try:
            th[r['theme']].append(float(r['views']))
        except (TypeError, ValueError):
            pass
print('\nkevin_ig theme medians (views):')
for t, v in sorted(th.items(), key=lambda x: -statistics.median(x[1])):
    print(f'  {t:12s} n={len(v):2d} median={statistics.median(v):7.0f}')

print('\nOct 12-13 kevin posts, vs ig_reel median 912 / ig_static median 1720:')
for r in rows:
    if r['account'] == 'kevin_ig' and r['date'] in ('2026-10-12', '2026-10-13'):
        v = r['views']
        kind = 'reel' if r['is_reel'] == 'True' else 'static'
        med = 912 if kind == 'reel' else 1720
        try:
            ratio = float(v) / med
            verdict = 'BEAT' if ratio >= 1.15 else ('AT' if ratio >= 0.85 else 'MISSED')
        except ValueError:
            verdict = '?'
        print(f"  {r['date']} {kind:6s} theme={r['theme']:12s} views={v:>5s}  ({ratio:.2f}x {kind} median -> {verdict})")

# Oct 13 theme pull for kevin: room reel 952 vs room median
room = [float(r['views']) for r in rows if r['account'] == 'kevin_ig' and r['theme'] == 'room' and r['views']]
print(f"\nkevin room median n={len(room)}: {statistics.median(room):.0f}")

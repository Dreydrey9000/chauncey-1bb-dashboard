#!/usr/bin/env python3
"""PM brief analysis: today's CSV rows, per-theme medians (last 60d), static vs reel, hour-of-day."""
import csv, statistics, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        r['views_n'] = int(float(r['views'])) if r['views'] not in ('', None, 'unavailable') else None
        rows.append(r)

TODAY = '2026-11-17'
print('=== rows dated', TODAY, '===')
for r in rows:
    if r['date'] == TODAY:
        print(f"  {r['account']} {r['ts']} reel={r['is_reel']} theme={r['theme']} views={r['views_n']} | {r['content'][:60]!r}")

cutoff = (datetime.date.today() - datetime.timedelta(days=60)).isoformat()

def med(vals):
    vals = [v for v in vals if v is not None]
    return (statistics.median(vals), len(vals)) if vals else (None, 0)

for acct in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acct and r['date'] >= cutoff and r['views_n'] is not None]
    print(f'=== {acct} last-60d (from {cutoff}) ===')
    print('  overall:', med([r['views_n'] for r in sub]))
    themes = {}
    for r in sub:
        themes.setdefault(r['theme'], []).append(r['views_n'])
    for t, vs in sorted(themes.items(), key=lambda kv: -(statistics.median(kv[1]) if kv[1] else 0)):
        m, n = med(vs)
        print(f'  theme {t}: median={m} n={n}')
    st = [r['views_n'] for r in sub if r['is_reel'] == 'False']
    rl = [r['views_n'] for r in sub if r['is_reel'] == 'True']
    print('  statics:', med(st), ' reels:', med(rl))

# hour-of-day for drey reels (all time, views>0)
print('=== drey_ig reels by local hour (ET) ===')
byh = {}
for r in rows:
    if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and r['views_n']:
        try:
            dt = datetime.datetime.fromisoformat(r['ts']).astimezone(datetime.timezone(datetime.timedelta(hours=-5)))
            byh.setdefault(dt.hour, []).append(r['views_n'])
        except Exception:
            pass
for h in sorted(byh):
    m, n = med(byh[h])
    print(f'  {h:02d}:00 ET median={m} n={n}')

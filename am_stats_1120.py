#!/usr/bin/env python3
"""AM brief stats from posts_all.csv — medians and streaks cited in the 2026-11-20 AM edition."""
import csv, statistics as st
from datetime import datetime, timezone

rows = []
with open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv', newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append(r)

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

def med(vals, label):
    vals = [v for v in vals if v is not None]
    if not vals:
        print(f'{label}: n=0')
        return None
    m = st.median(vals)
    print(f'{label}: median={m:.0f} n={len(vals)} vals={sorted(int(v) for v in vals)}')
    return m

# cutoff: last 7 days of data (2026-11-13..2026-11-19)
def in_window(r, start='2026-11-13'):
    return r['date'] >= start

print('=== DREY IG reels (is_reel=True) ===')
drey_reels = [r for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and num(r['views']) is not None]
med([num(r['views']) for r in drey_reels], 'all-time')
d7 = [r for r in drey_reels if in_window(r)]
med([num(r['views']) for r in d7], '7-day (>=11-13)')
for r in sorted(d7, key=lambda r: r['date']):
    print(f"  {r['date']} views={num(r['views']):.0f} theme={r['theme']} {r['url'].rsplit('/', 2)[-2]}")

print('=== DREY IG by theme (all-time, reels+static) ===')
for theme in ('room', 'confession', 'ai_systems'):
    med([num(r['views']) for r in rows if r['account'] == 'drey_ig' and r['theme'] == theme and num(r['views']) is not None], f'drey theme={theme}')

print('=== KEVIN IG statics (is_reel=False, non-story urls = /p/) ===')
kev_stat = [r for r in rows if r['account'] == 'kevin_ig' and r['is_reel'] == 'False' and '/p/' in r['url'] and num(r['views']) is not None]
med([num(r['views']) for r in kev_stat], 'all-time statics')
k7 = [r for r in kev_stat if in_window(r)]
med([num(r['views']) for r in k7], '7-day statics (>=11-13)')
for r in sorted(k7, key=lambda r: r['date']):
    print(f"  {r['date']} views={num(r['views']):.0f} theme={r['theme']} {r['url'].rsplit('/', 2)[-2]}")

print('=== KEVIN identity statics vs others ===')
ident_stat = [num(r['views']) for r in kev_stat if r['theme'] == 'identity']
print('identity statics:', sorted(int(v) for v in ident_stat))
med(ident_stat, 'identity statics')

print('=== KEVIN reels all-time + 7d ===')
kev_reels = [num(r['views']) for r in rows if r['account'] == 'kevin_ig' and r['is_reel'] == 'True' and num(r['views']) is not None]
med(kev_reels, 'kevin reels all-time')

print('=== Fresh-post early reads (Nov 18-19) ===')
for r in rows:
    if r['date'] >= '2026-11-18' and '/stories/' not in r['url'] and num(r['views']) is not None:
        print(f"  {r['account']} {r['ts'][:16]} reel={r['is_reel']} views={num(r['views']):.0f} comments={r['comments']} theme={r['theme']} {r['url'].rsplit('/', 2)[-2]}")

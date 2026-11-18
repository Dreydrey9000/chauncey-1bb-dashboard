#!/usr/bin/env python3
"""Theme-level check for tonight's delta: drey ai_systems reel run + kevin identity."""
import csv, statistics as st
from collections import defaultdict

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))

drey_reels = [r for r in rows if r['account'] == 'drey_ig' and r['is_reel'] == 'True']
by_theme = defaultdict(list)
for r in drey_reels:
    try:
        by_theme[r['theme']].append(int(float(r['views'] or 0)))
    except ValueError:
        pass
print('drey_ig reels by theme:')
for t, vs in sorted(by_theme.items(), key=lambda kv: -st.median(kv[1])):
    print(f"  {t:14s} n={len(vs):2d} median={st.median(vs):7.0f}")

print('\ndrey ai_systems reels, most recent 12:')
ais = sorted([r for r in drey_reels if r['theme'] == 'ai_systems'], key=lambda r: r['ts'])
for r in ais[-12:]:
    print(f"  {r['date']} views={r['views']:>5s} {r['url']}")

kv_ig_reels = [r for r in rows if r['account'] == 'kevin_ig' and r['is_reel'] == 'True']
kv_by = defaultdict(list)
for r in kv_ig_reels:
    try:
        kv_by[r['theme']].append(int(float(r['views'] or 0)))
    except ValueError:
        pass
print('\nkevin_ig reels by theme:')
for t, vs in sorted(kv_by.items(), key=lambda kv: -st.median(kv[1])):
    print(f"  {t:14s} n={len(vs):2d} median={st.median(vs):7.0f}")

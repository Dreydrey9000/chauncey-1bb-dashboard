#!/usr/bin/env python3
"""PM 11-18: pull liamottley + davidmeltzer, and kevin_ig static theme medians."""
import subprocess, csv, statistics as st
from collections import defaultdict

r = subprocess.run(['/opt/homebrew/bin/python3', 'tokscript_pull.py', 'liamottley', 'davidmeltzer'],
                   capture_output=True, text=True, cwd='/Users/andrethomas/.hermes/workspaces/chauncey/dashboard')
print(r.stdout[-4000:])
print(r.stderr[-500:])

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
kv_statics = defaultdict(list)
for row in rows:
    if row['account'] == 'kevin_ig' and row['is_reel'] == 'False' and '/stories/' not in row['url']:
        try:
            kv_statics[row['theme']].append(int(float(row['views'] or 0)))
        except ValueError:
            pass
print('\nkevin_ig STATICS by theme:')
for t, vs in sorted(kv_statics.items(), key=lambda kv: -st.median(kv[1])):
    print(f"  {t:14s} n={len(vs):2d} median={st.median(vs):7.0f}")

# drey recent reels with hour (ET) for slot check
print('\ndrey_ig reels Nov 14-18 (UTC ts -> ET hour):')
for row in rows:
    if row['account'] == 'drey_ig' and row['is_reel'] == 'True' and row['date'] >= '2026-11-14':
        print(f"  {row['ts']}  views={row['views']:>5s}  theme={row['theme']}")

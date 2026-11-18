#!/usr/bin/env python3
"""Evening delta math: per-account per-format medians vs today's posts."""
import csv, statistics as st
from collections import defaultdict

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
groups = defaultdict(list)
for r in rows:
    try:
        v = int(float(r['views'] or 0))
    except ValueError:
        continue
    fmt = 'reel' if r['is_reel'] == 'True' else ('story' if '/stories/' in r['url'] else 'static')
    groups[(r['account'], fmt)].append(v)

for k in sorted(groups):
    vs = sorted(groups[k])
    print(f"{k[0]:9s} {k[1]:6s} n={len(vs):3d} median={st.median(vs):8.0f}  p25={vs[len(vs)//4]:6d}  p75={vs[3*len(vs)//4]:6d}")

print()
print("TODAY (2026-11-18 ET) founder posts:")
for r in rows:
    if r['date'] == '2026-11-18':
        v = r['views']
        print(f"  {r['account']:9s} {r['url'][:60]:60s} views={v} likes={r['likes']} comments={r['comments']} theme={r['theme']}")

#!/usr/bin/env python3
"""Evening medians, correct columns: is_reel + theme."""
import csv, statistics, datetime, collections, os
BASE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        rows.append(r)

def istrue(x):
    return str(x).strip().lower() in ('true', '1', 'yes')

for acct in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acct]
    reels = [int(float(r['views'] or 0)) for r in sub if istrue(r.get('is_reel')) and r.get('views')]
    statics = [int(float(r['views'] or 0)) for r in sub if not istrue(r.get('is_reel')) and r.get('views')]
    bytheme = collections.defaultdict(list)
    for r in sub:
        if r.get('views'):
            bytheme[(r.get('theme') or '?').strip()].append(int(float(r['views'])))
    print(f'== {acct} n={len(sub)}')
    if reels:
        print(f'   reels n={len(reels)} median={statistics.median(reels):.0f}')
    if statics:
        print(f'   statics n={len(statics)} median={statistics.median(statics):.0f}')
    for th, vs in sorted(bytheme.items(), key=lambda kv: -statistics.median(kv[1])):
        if len(vs) >= 2:
            print(f'   theme {th:20s} n={len(vs):3d} median={statistics.median(vs):8.0f}')
    # last 5 posts with dates
    print('   last 5:')
    for r in sub[-5:]:
        print(f'     {r.get("date")} reel={istrue(r.get("is_reel"))} theme={r.get("theme")} views={r.get("views")} url={r.get("url")}')

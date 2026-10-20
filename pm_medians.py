#!/usr/bin/env python3
"""Median views by account x is_reel x theme from posts_all.csv (evening brief citations)."""
import csv, statistics, os
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        rows.append(r)

def views(r):
    try:
        return int(float(r['views'] or 0))
    except Exception:
        return None

groups = defaultdict(list)
for r in rows:
    v = views(r)
    if v is None:
        continue
    key = (r['account'], r.get('is_reel') or '', (r.get('theme') or '').strip().lower())
    groups[key].append(v)

fmt = defaultdict(list)
for r in rows:
    v = views(r)
    if v is None:
        continue
    fmt[(r['account'], r.get('is_reel') or '')].append(v)
print('--- combined per format ---')
for (acct, isreel), vals in sorted(fmt.items()):
    label = 'REELS' if isreel in ('True', 'true', '1') else 'STATICS'
    print(f'{acct:9s} {label:8s} n={len(vals):3d} median={statistics.median(vals):8.0f}')

for (acct, isreel, theme), vals in sorted(groups.items()):
    if len(vals) >= 2:
        print(f'{acct:9s} reel={isreel:5s} theme={theme or "-":22s} n={len(vals):3d} median={statistics.median(vals):8.0f}')
    else:
        print(f'{acct:9s} reel={isreel:5s} theme={theme or "-":22s} n=1  only={vals}')

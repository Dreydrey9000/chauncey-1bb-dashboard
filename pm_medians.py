#!/usr/bin/env python3
"""Evening beat/miss: per-type medians from posts_all.csv + today's fresh posts."""
import csv, statistics, json, os
from datetime import date

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))

def med(acct, reel=None, exclude_days=0):
    vs = []
    cutoff = date.today().isoformat()
    for r in rows:
        if r['account'] != acct:
            continue
        if r['date'] >= cutoff:
            continue  # today not in median base
        if reel is not None and (r['is_reel'] == 'True') != reel:
            continue
        try:
            v = int(float(r['views'] or 0))
        except Exception:
            continue
        if v > 0 or reel is not None:
            vs.append(v)
    return len(vs), statistics.median(vs) if vs else None

print('Drey reels (excl today):', med('drey_ig', reel=True))
print('Drey non-reel (excl today):', med('drey_ig', reel=False))
print('Kevin reels (excl today):', med('kevin_ig', reel=True))
print('Kevin non-reel (excl today):', med('kevin_ig', reel=False))

# theme medians for drey reels
from collections import defaultdict
tm = defaultdict(list)
for r in rows:
    if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and r['date'] < date.today().isoformat():
        try:
            v = int(float(r['views'] or 0))
            tm[r['theme']].append(v)
        except Exception:
            pass
for t, vs in sorted(tm.items(), key=lambda kv: -statistics.median(kv[1]) if kv[1] else 0):
    if len(vs) >= 2:
        print(f'drey reel theme {t}: n={len(vs)} median={statistics.median(vs)}')

# Kevin theme medians, reels vs static split
ktm = defaultdict(list)
for r in rows:
    if r['account'] == 'kevin_ig' and r['date'] < date.today().isoformat():
        try:
            v = int(float(r['views'] or 0))
            ktm[(r['theme'], r['is_reel'] == 'True')].append(v)
        except Exception:
            pass
for (t, isr), vs in sorted(ktm.items(), key=lambda kv: -statistics.median(kv[1]) if kv[1] else 0):
    if len(vs) >= 3:
        print(f'kevin {t} {"reel" if isr else "static"}: n={len(vs)} median={statistics.median(vs)}')

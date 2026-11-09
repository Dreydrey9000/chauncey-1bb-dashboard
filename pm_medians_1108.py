#!/usr/bin/env python3
"""PM 2026-11-08: medians by is_reel and theme for beat/miss calls."""
import csv, os, statistics, collections

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))

def med(vals):
    return statistics.median(vals) if vals else None

for acct in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acct]
    print(f'=== {acct}')
    byreel = collections.defaultdict(list)
    bytheme = collections.defaultdict(list)
    for r in sub:
        try:
            v = int(float(r['views'] or 0))
        except Exception:
            continue
        byreel[r.get('is_reel', '')].append(v)
        t = (r.get('theme') or '').strip()
        if t:
            bytheme[t].append(v)
    for k, vs in sorted(byreel.items()):
        print(f'  is_reel={k!r}: n={len(vs)} median={med(vs)}')
    for t, vs in sorted(bytheme.items(), key=lambda x: -med(x[1])):
        print(f'  theme={t}: n={len(vs)} median={med(vs)}')

# last 8 posts per founder with type + theme for context
for acct in ('drey_ig', 'kevin_ig'):
    sub = sorted([r for r in rows if r['account'] == acct], key=lambda r: r['ts'])
    print(f'--- last 8 {acct}')
    for r in sub[-8:]:
        print(f"  {r['date']} reel={r.get('is_reel','')} theme={r.get('theme','')} views={r['views']} likes={r['likes']} comments={r['comments']} | {r['content'][:60]!r}")

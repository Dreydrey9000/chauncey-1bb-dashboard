#!/usr/bin/env python3
"""Recompute 14-day medians used for evening beat/miss calls (reels + statics per founder)."""
import csv, datetime, statistics, os
BASE = os.path.dirname(os.path.abspath(__file__))
CUT = datetime.date(2026, 10, 24)
rows = {'drey_ig': {'reel': [], 'static': []}, 'kevin_ig': {'reel': [], 'static': []}}
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        acc = r['account']
        if acc not in rows:
            continue
        try:
            d = datetime.date.fromisoformat(r['date'][:10])
            v = int(float(r['views'] or 0))
        except Exception:
            continue
        if d < CUT:
            continue
        is_reel = str(r.get('is_reel', '')).strip().lower() == 'true' or '/reel/' in (r.get('url') or '')
        rows[acc]['reel' if is_reel else 'static'].append((d.isoformat(), v, (r.get('content') or '')[:40]))
for acc, kinds in rows.items():
    for kind, vals in kinds.items():
        if vals:
            vs = [v for _, v, _ in vals]
            print(f'{acc} {kind}: n={len(vs)} median={statistics.median(vs)} min={min(vs)} max={max(vs)}')
            for d, v, c in sorted(vals, reverse=True)[:3]:
                print(f'   {d} {v} | {c}')

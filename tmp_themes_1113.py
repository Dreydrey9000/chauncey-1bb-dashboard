#!/usr/bin/env python3
"""Theme stats for evening brief 2026-11-13."""
import csv, statistics
rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
for acct in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acct]
    themes = {}
    for r in sub:
        t = (r['theme'] or 'none').strip() or 'none'
        themes.setdefault(t, []).append(int(r['views'] or 0))
    print(f'== {acct} (n={len(sub)})')
    for t, v in sorted(themes.items(), key=lambda kv: -statistics.mean(kv[1]))[:8]:
        print(f'   {t:22s} n={len(v):3d} avg={statistics.mean(v):7.0f} median={statistics.median(v):7.0f}')
    # static vs reels for kevin
    reels = [int(r['views'] or 0) for r in sub if r['is_reel'] == 'True']
    stat  = [int(r['views'] or 0) for r in sub if r['is_reel'] == 'False']
    if reels and stat:
        print(f'   reels n={len(reels)} avg={statistics.mean(reels):.0f} | static n={len(stat)} avg={statistics.mean(stat):.0f}')

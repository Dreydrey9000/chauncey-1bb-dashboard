#!/usr/bin/env python3
"""Evening theme-median check for 2026-10-16 PM brief (posts_all.csv)."""
import csv, statistics as st, os
BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))

def meds(acct, label):
    rs = [r for r in rows if r['account'] == acct and r['views']]
    allv = [int(r['views']) for r in rs]
    reels = [int(r['views']) for r in rs if r['is_reel'] == 'True']
    stats_ = [int(r['views']) for r in rs if r['is_reel'] != 'True']
    print(f'{label}: n={len(allv)} all_median={st.median(allv):.0f} | reels n={len(reels)} median={st.median(reels) if reels else 0:.0f} | statics n={len(stats_)} median={st.median(stats_) if stats_ else 0:.0f}')
    themes = {}
    for r in rs:
        themes.setdefault(r['theme'], []).append(int(r['views']))
    for t, v in sorted(themes.items(), key=lambda kv: -st.median(kv[1])):
        if len(v) >= 2:
            print(f'   {t}: n={len(v)} median={st.median(v):.0f}')

meds('drey_ig', 'DREY_IG')
meds('kevin_ig', 'KEVIN_IG')

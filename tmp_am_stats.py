#!/usr/bin/env python3
"""Morning brief stats: 30d medians per founder account from posts_all.csv."""
import csv, statistics as st
from collections import defaultdict

ROWS = list(csv.DictReader(open('posts_all.csv')))
CUT = '2026-09-25'  # 30d window ending 2026-10-24

def n(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None

for acct in ('drey_ig', 'kevin_ig'):
    rows = [r for r in ROWS if r['account'] == acct and r['date'] >= CUT]
    reels = [r for r in rows if r['is_reel'] == 'True']
    statics = [r for r in rows if r['is_reel'] != 'True']
    for name, grp in (('REELS', reels), ('STATICS', statics)):
        vs = sorted(v for v in (n(r['views']) for r in grp) if v is not None)
        if vs:
            print(f"{acct} {name}: n={len(vs)} median={st.median(vs):.0f} min={vs[0]} max={vs[-1]} all={vs}")
    bytheme = defaultdict(list)
    for r in rows:
        v = n(r['views'])
        if v is not None:
            bytheme[r['theme']].append(v)
    for t, vs in sorted(bytheme.items(), key=lambda kv: -st.median(kv[1])):
        print(f"   theme {t}: n={len(vs)} median={st.median(vs):.0f}")
    print(f"   latest 5 {acct}:")
    for r in sorted(rows, key=lambda r: r['ts'], reverse=True)[:5]:
        print(f"     {r['date']} {'reel' if r['is_reel']=='True' else 'stat'} {r['theme']:11s} views={r['views']:>5} likes={r['likes']:>3} comments={r['comments']:>2} watch_ms={r['watch_ms']} dur={r['dur_s']} | {r['url']}")
    print()

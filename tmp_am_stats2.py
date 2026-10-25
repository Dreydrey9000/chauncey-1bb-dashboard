#!/usr/bin/env python3
"""All-time medians + confession-reel engagement detail (drey_ig)."""
import csv, statistics as st

ROWS = list(csv.DictReader(open('posts_all.csv')))

def n(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None

for acct in ('drey_ig', 'kevin_ig'):
    rows = [r for r in ROWS if r['account'] == acct]
    for name, flag in (('reels', 'True'), ('statics', '!= True')):
        grp = [r for r in rows if (r['is_reel'] == flag if flag != '!= True' else r['is_reel'] != 'True')]
        vs = [v for v in (n(r['views']) for r in grp) if v is not None]
        print(f"{acct} all-time {name}: n={len(vs)} median={st.median(vs):.0f}")

print()
print("drey_ig reels 2026-10-15..24 detail:")
for r in ROWS:
    if r['account'] == 'drey_ig' and r['is_reel'] == 'True' and r['date'] >= '2026-10-15':
        print(f"  {r['date']} {r['theme']:11s} v={r['views']:>5} likes={r['likes']:>3} com={r['comments']:>2} shares={r['shares']} saves={r['saves']} er={r['er']} watch_ms={r['watch_ms']:>6} dur={r['dur_s']} | {r['url'].split('/')[-2]}")

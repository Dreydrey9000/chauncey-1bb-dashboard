#!/usr/bin/env python3
"""AM inspire analysis: founder medians + last-10-days posts from posts_all.csv."""
import csv, statistics

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv'
rows = list(csv.DictReader(open(BASE)))

def toint(x):
    try:
        return int(float(x))
    except Exception:
        return None

for acct in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acct]
    print(f'===== {acct} (n={len(sub)}) =====')
    def med(filt, label):
        vals = [toint(r['views']) for r in sub if filt(r) and toint(r['views']) is not None]
        print(f'  {label}: n={len(vals)} median={statistics.median(vals):,.0f}' if vals else f'  {label}: no data')
    med(lambda r: True, 'overall')
    med(lambda r: r['is_reel'].lower() == 'true', 'reels')
    med(lambda r: r['is_reel'].lower() != 'true', 'statics')
    for theme in sorted(set(r['theme'] for r in sub)):
        med(lambda r, t=theme: r['theme'] == t, f'theme {theme}')
    print('  --- posts since 10/09 ---')
    recent = sorted([r for r in sub if r['date'] >= '2026-10-09'], key=lambda r: (r['date'], r['ts']))
    for r in recent:
        v = toint(r['views'])
        fmt = 'REEL' if r['is_reel'].lower() == 'true' else 'STAT'
        cap = str(r['content'])[:70].replace('\n', ' ')
        print(f"  {r['date']} {fmt} {r['theme']:11s} views={v} likes={r['likes']} com={r['comments']} | {cap}")
        print(f"      {r['url']}")

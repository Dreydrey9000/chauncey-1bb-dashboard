#!/usr/bin/env python3
"""Compute evening-check derived numbers from raw/evening_*.json (no hand math)."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

DATA = {
    'drey': json.load(open(os.path.join(BASE, 'raw', 'evening_drey.json')))['dailyData'],
    'kevin': json.load(open(os.path.join(BASE, 'raw', 'evening_kevin.json')))['dailyData'],
}

def row(d):
    m = d['metrics']
    inter = m['likes'] + m['comments'] + m['shares'] + m['saves']
    er = (inter / m['reach'] * 100) if m['reach'] else None
    return dict(date=d['date'], posts=d['postCount'], reach=m['reach'],
                likes=m['likes'], comments=m['comments'], shares=m['shares'],
                saves=m['saves'], interactions=inter,
                er=round(er, 1) if er is not None else 'n/a')

for handle, days in DATA.items():
    print(f'===== {handle.upper()} =====')
    rows = [row(d) for d in days]
    for r in rows:
        print(r)
    tot = {k: sum(r[k] for r in rows) for k in ('posts', 'reach', 'likes', 'comments', 'shares', 'saves', 'interactions')}
    tot['er_5d'] = round(tot['interactions'] / tot['reach'] * 100, 1) if tot['reach'] else 'n/a'
    print('5-day totals:', tot)
    t, y = rows[-1], rows[-2]
    for k in ('reach', 'likes', 'interactions'):
        if y[k]:
            pct = (t[k] - y[k]) / y[k] * 100
            print(f"today_vs_yday {k}: {t[k]} vs {y[k]} = {pct:+.0f}%")
    # spike check vs 5-day mean (excluding today-partial)
    prior = [r for r in rows[:-1]]
    mean_reach = sum(r['reach'] for r in prior) / len(prior)
    for r in rows:
        if mean_reach and r['reach'] / mean_reach >= 1.5:
            print(f"SPIKE {r['date']}: reach {r['reach']} vs prior-day mean {mean_reach:.0f} (+{(r['reach']/mean_reach-1)*100:.0f}%)")
    print()

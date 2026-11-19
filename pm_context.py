#!/usr/bin/env python3
"""Last-7-day context: best posts per founder for evening beat/miss framing."""
import csv, os
from datetime import date, timedelta

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
cutoff = (date.today() - timedelta(days=7)).isoformat()

for acct in ('drey_ig', 'kevin_ig'):
    best = []
    reel_recent = []
    for r in rows:
        if r['account'] != acct or r['date'] < cutoff:
            continue
        try:
            v = int(float(r['views'] or 0))
        except Exception:
            continue
        label = ('REEL' if r['is_reel'] == 'True' else 'static') if '/stories/' not in r['url'] else 'story'
        if label != 'story':
            best.append((v, r['date'], label, r['url'].split('/')[-2], r['theme']))
        if label == 'REEL':
            reel_recent.append((v, r['date'], r['url'].split('/')[-2]))
    best.sort(reverse=True)
    print(f'== {acct} last 7 days, non-story, top 6:')
    for v, d, l, u, t in best[:6]:
        print(f'  {v:>6} {d} {l:6} {u} {t}')
    print(f'  recent reel finals: {reel_recent}')

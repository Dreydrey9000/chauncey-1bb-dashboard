#!/usr/bin/env python3
"""Evening math for 2026-10-09: table, deltas, ER, flags from evening_raw.json."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(BASE, '..', 'evening_raw.json')))
TODAY = '2026-10-09'
YDAY = '2026-10-08'

for name in ('drey', 'kevin'):
    days = raw['data'][name]['dailyData']
    print(f'===== {name} =====')
    tot = dict(posts=0, reach=0, likes=0, comments=0, shares=0, saves=0, inter=0)
    rows = {}
    for d in days:
        m = d['metrics']
        inter = m['likes'] + m['comments'] + m['shares'] + m['saves']
        er = (inter / m['reach'] * 100) if m['reach'] else 0.0
        rows[d['date']] = (d['postCount'], m['reach'], m['likes'], m['comments'],
                           m['shares'], m['saves'], inter, er)
        tot['posts'] += d['postCount']; tot['reach'] += m['reach']
        tot['likes'] += m['likes']; tot['comments'] += m['comments']
        tot['shares'] += m['shares']; tot['saves'] += m['saves']; tot['inter'] += inter
        print(f"{d['date']}  posts={d['postCount']} reach={m['reach']} likes={m['likes']} "
              f"comments={m['comments']} shares={m['shares']} saves={m['saves']} "
              f"inter={inter} ER={er:.1f}%")
    tot_er = tot['inter'] / tot['reach'] * 100 if tot['reach'] else 0.0
    print(f"WINDOW TOTAL: posts={tot['posts']} reach={tot['reach']} likes={tot['likes']} "
          f"comments={tot['comments']} shares={tot['shares']} saves={tot['saves']} "
          f"inter={tot['inter']} ER={tot_er:.1f}%")
    t, y = rows[TODAY], rows[YDAY]
    print('DELTA today vs yesterday:')
    for i, lbl in enumerate(['posts', 'reach', 'likes', 'comments', 'shares', 'saves', 'inter'], 0):
        pct = ((t[i] - y[i]) / y[i] * 100) if y[i] else None
        flag = ' FLAG>50%' if pct is not None and abs(pct) > 50 else ''
        ps = f'{pct:+.0f}%' if pct is not None else 'n/a (y=0)'
        print(f'  {lbl}: {t[i]} vs {y[i]} ({ps}){flag}')
    print(f'  ER: {t[7]:.1f}% vs {y[7]:.1f}%')
    print()

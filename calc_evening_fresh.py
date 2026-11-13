#!/usr/bin/env python3
"""Evening calc from fresh per-account raw files (evening_<name>_<date>.json)."""
import json, datetime, glob, os

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw')
today = datetime.date.today().isoformat()

def pct(a, b):
    if not b:
        return 'n/a'
    return f'{(a - b) / b * 100:+.0f}%'

def flag(p):
    if p == 'n/a':
        return ''
    v = float(p.replace('%', '').replace('+', ''))
    return ' **SPIKE**' if v > 50 else (' **DROP**' if v < -50 else '')

for name in ('drey', 'kevin'):
    path = os.path.join(RAW, f'evening_{name}_{today}.json')
    data = json.load(open(path))['payload']
    rows = {d['date']: d for d in data['dailyData']}
    dates = sorted(rows)
    t, y = rows[dates[-1]], rows[dates[-2]]
    pattern = [rows[x] for x in dates[:-1]]  # 4 days before today
    def m(d): return d['metrics']
    def inter(x): return sum(x.get(f, 0) or 0 for f in ('likes', 'comments', 'shares', 'saves'))
    print(f'=== {name}_ig ({dates[0]}..{dates[-1]}) ===')
    for d in dates:
        mm = m(rows[d])
        er = inter(mm) / mm['reach'] * 100 if mm['reach'] else 0
        print(f"  {d} posts={rows[d]['postCount']} reach={mm['reach']} likes={mm['likes']} comments={mm['comments']} shares={mm['shares']} saves={mm['saves']} inter={inter(mm)} ER={er:.1f}%")
    tm, ym = m(t), m(y)
    for f in ('reach', 'likes', 'comments', 'shares', 'saves'):
        tv, yv = tm.get(f, 0) or 0, ym.get(f, 0) or 0
        vals = [p['metrics'].get(f, 0) or 0 for p in pattern]
        avg = sum(vals) / len(vals)
        p1, p2 = pct(tv, yv), pct(tv, avg)
        print(f'  {f:9s} today={tv:<5} yest={yv:<5} d_yest={p1}{flag(p1):<10} 4d_avg={avg:.0f} d_avg={p2}{flag(p2)}')
    er_t = inter(tm) / tm['reach'] * 100 if tm['reach'] else 0
    er_y = inter(ym) / ym['reach'] * 100 if ym['reach'] else 0
    print(f'  ER today={er_t:.1f}% yest={er_y:.1f}%  posts today={t["postCount"]} yest={y["postCount"]}')
    print()

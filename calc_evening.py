#!/usr/bin/env python3
"""Compute today-vs-yesterday + 4-day-pattern deltas from the evening pull."""
import json

data = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/evening_daily_2026-10-27.json'))

def pct(a, b):
    if b in (0, None):
        return 'n/a (base 0)'
    return f'{(a - b) / b * 100:+.0f}%'

for key in ('drey_ig', 'kevin_ig'):
    rows = {d['date']: d for d in data[key]['dailyData']}
    dates = sorted(rows)
    today, yest = rows[dates[-1]], rows[dates[-2]]
    prior = rows[dates[0]], rows[dates[1]], rows[dates[2]]  # 3 full prior days + yesterday = 4-day pattern
    print(f'=== {key} ===')
    def m(d): return d['metrics']
    tm, ym = m(today), m(yest)
    # 4-day pattern = the four days before today
    pattern = [rows[x] for x in dates[:-1]]
    for field in ('reach', 'likes', 'comments', 'shares', 'saves', 'views'):
        t, y = tm.get(field, 0) or 0, ym.get(field, 0) or 0
        vals = [(p['metrics'].get(field, 0) or 0) for p in pattern]
        avg = sum(vals) / len(vals)
        print(f'{field:9s} today={t:<6} yest={y:<6} delta={pct(t, y):<14} 4day(avg of {vals})={avg:.0f} vs_avg={pct(t, avg)}')
    t_reach = tm.get('reach', 0) or 0
    y_reach = ym.get('reach', 0) or 0
    def inter(x): return sum(x.get(f, 0) or 0 for f in ('likes', 'comments', 'shares', 'saves'))
    er_t = inter(tm) / t_reach * 100 if t_reach else None
    er_y = inter(ym) / y_reach * 100 if y_reach else None
    print(f'ER        today={er_t:.1f}% yest={er_y:.1f}%')
    print(f'posts     today={today["postCount"]} yest={yest["postCount"]}')
    print()

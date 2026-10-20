#!/usr/bin/env python3
"""Evening Check 2026-10-20: compare today vs yesterday + 4-day pattern from raw pulls."""
import json

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw'
for name in ['drey', 'kevin']:
    d = json.load(open(f'{BASE}/evening_{name}_2026-10-20.json'))
    rows = d['payload']['dailyData']
    print(f'=== {name.upper()} ===')
    for r in rows:
        m = r['platformMetrics']['instagram']
        inter = m['likes'] + m['comments'] + m['shares'] + m['saves']
        er = inter / m['reach'] * 100 if m['reach'] else 0.0
        print(f"{r['date']}: posts={m['postCount']} reach={m['reach']} likes={m['likes']} "
              f"comments={m['comments']} shares={m['shares']} saves={m['saves']} "
              f"inter={inter} ER={er:.1f}%")
    y = rows[-2]['platformMetrics']['instagram']
    t = rows[-1]['platformMetrics']['instagram']
    prior = [x['platformMetrics']['instagram'] for x in rows[:4]]
    avg_reach = sum(x['reach'] for x in prior) / 4
    dr = (t['reach'] - y['reach']) / y['reach'] * 100 if y['reach'] else None
    vs_avg = (t['reach'] - avg_reach) / avg_reach * 100
    print(f"reach yesterday->today: {y['reach']} -> {t['reach']} ({dr:+.1f}%) | "
          f"4-day avg {avg_reach:.0f} | today vs avg {vs_avg:+.1f}%")
    print()

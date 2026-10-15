#!/usr/bin/env python3
"""Evening Check analysis: today vs yesterday + 4-day pattern from Zernio daily-metrics."""
import json, os

RAW = os.path.expanduser('~/.hermes/workspaces/chauncey/dashboard/raw')

for name in ('drey', 'kevin'):
    payload = json.load(open(os.path.join(RAW, f'evening_{name}_2026-10-15.json')))['payload']
    print(f'===== {name.upper()} =====')
    for r in payload['dailyData']:
        m = r['platformMetrics']['instagram']
        inter = m['likes'] + m['comments'] + m['shares'] + m['saves']
        er = inter / m['reach'] * 100 if m['reach'] else 0.0
        print(f"{r['date']} posts={r['postCount']} reach={m['reach']} likes={m['likes']} "
              f"com={m['comments']} sh={m['shares']} sv={m['saves']} ER={er:.1f}%")
    y, t = payload['dailyData'][-2], payload['dailyData'][-1]
    my, mt = y['platformMetrics']['instagram'], t['platformMetrics']['instagram']
    for f in ('reach', 'likes', 'comments', 'shares', 'saves'):
        old, new = my[f], mt[f]
        pct = (new - old) / old * 100 if old else None
        flag = '  <-- FLAG >50%' if pct is not None and abs(pct) > 50 else ''
        print(f"  {f}: {old} -> {new} ({'n/a' if pct is None else f'{pct:+.0f}%'}){flag}")

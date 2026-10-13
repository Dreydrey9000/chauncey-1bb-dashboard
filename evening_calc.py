#!/usr/bin/env python3
"""Compute per-day ER/totals from the evening pulls; print derived figures only."""
import json, datetime

today = datetime.date.today().isoformat()
for name in ('drey', 'kevin'):
    d = json.load(open(f'/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/evening_{name}_{today}.json'))
    rows = d['payload']['dailyData']
    print(f'=== {name} ===')
    tot_i = tot_r = 0
    for r in rows:
        m = r['metrics']
        inter = m['likes'] + m['comments'] + m['shares'] + m['saves']
        er = (inter / m['reach'] * 100) if m['reach'] else 0
        tot_i += inter; tot_r += m['reach']
        print(f"{r['date']} posts={m.get('postCount', r.get('postCount'))} reach={m['reach']} likes={m['likes']} "
              f"comments={m['comments']} shares={m['shares']} saves={m['saves']} interactions={inter} ER={er:.1f}%")
    print(f'TOTALS reach={tot_r} interactions={tot_i} ER={(tot_i/tot_r*100 if tot_r else 0):.1f}%')
    t = rows[-1]['metrics']; y = rows[-2]['metrics']
    for k in ('reach', 'likes', 'comments', 'shares', 'saves'):
        if y[k]:
            pct = (t[k] - y[k]) / y[k] * 100
            print(f'delta {k}: {t[k]} vs {y[k]} = {pct:+.0f}%')
        else:
            print(f'delta {k}: {t[k]} vs {y[k]}')

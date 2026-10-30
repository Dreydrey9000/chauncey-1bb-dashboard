#!/usr/bin/env python3
"""Print founder posts from the last 3 CSV days with beat/miss vs per-account median."""
import csv, statistics, os

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
dates = sorted(set(r['date'] for r in rows))[-3:]
print('window:', dates)

def med(acct):
    vals = sorted(float(r['views'] or 0) for r in rows if r['account'] == acct and float(r['views'] or 0) > 0)
    return statistics.median(vals) if vals else 0

for acct in ('drey_ig', 'drey_tt', 'kevin_ig', 'kevin_tt'):
    m = med(acct)
    sel = [r for r in rows if r['account'] == acct and r['date'] in dates]
    for r in sorted(sel, key=lambda x: x['ts']):
        v = float(r['views'] or 0)
        verdict = 'n/a (no views yet)' if v == 0 else ('BEAT' if v > m else 'MISS')
        print(f"{r['date']} {acct:9s} views={v:>7.0f} vs med {m:>6.0f} -> {verdict} | {r['url']}")
        print(f"   theme={r['theme']} likes={r['likes']} com={r['comments']} | {r['content'][:100]!r}")

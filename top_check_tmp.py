#!/usr/bin/env python3
"""Check Kevin IG all-time top posts by views."""
import csv
rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
def toint(x):
    try:
        return int(float(x))
    except Exception:
        return None
for acct in ('kevin_ig', 'drey_ig'):
    sub = [(toint(r['views']), r['date'], r['url']) for r in rows if r['account'] == acct and toint(r['views']) is not None]
    sub.sort(reverse=True)
    print(f'== {acct} top 5 ==')
    for v, d, u in sub[:5]:
        print(f'  {v:>7,}  {d}  {u}')

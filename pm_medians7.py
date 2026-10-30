#!/usr/bin/env python3
"""7-day medians by founder/account/type for tonight's citations (local CSV)."""
import csv, statistics, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
cutoff = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()

def med(acct, is_reel, since=None):
    vals = sorted(float(r['views'] or 0) for r in rows
                  if r['account'] == acct and (r['is_reel'].lower() == str(is_reel).lower())
                  and float(r['views'] or 0) > 0 and (since is None or r['date'] >= since))
    return (statistics.median(vals), len(vals)) if vals else (None, 0)

for acct in ('drey_ig', 'kevin_ig'):
    for reel in ('True', 'False'):
        m7, n7 = med(acct, reel, cutoff)
        mall, nall = med(acct, reel)
        kind = 'REEL' if reel == 'True' else 'STATIC'
        s7 = f'{m7:.0f} (n={n7})' if n7 else 'none'
        sa = f'{mall:.0f} (n={nall})' if nall else 'none'
        print(f'{acct:9s} {kind:6s} 7d median={s7:12s} all-time={sa}')

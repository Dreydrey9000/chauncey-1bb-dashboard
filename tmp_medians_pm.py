#!/usr/bin/env python3
"""Evening medians check: any posts dated today + per-type medians from posts_all.csv."""
import csv, statistics, datetime, collections, os
BASE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    rdr = csv.DictReader(f)
    print('fields:', rdr.fieldnames)
    for r in rdr:
        rows.append(r)
today = '2026-10-18'
print('--- rows dated', today, '---')
n = 0
for r in rows:
    if (r.get('date') or '').startswith(today):
        print({k: r.get(k) for k in ('account', 'date', 'views', 'post_type', 'caption', 'url') if k in r})
        n += 1
print('today rows:', n)
print('--- per-account, per-type medians (all time) + last-30d ---')
cutoff = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
for acct in ('drey_ig', 'kevin_ig'):
    by = collections.defaultdict(list)
    by30 = collections.defaultdict(list)
    for r in rows:
        if r.get('account') != acct:
            continue
        try:
            v = int(float(r['views'] or 0))
        except Exception:
            continue
        pt = r.get('post_type') or '?'
        by[pt].append(v)
        if (r.get('date') or '') >= cutoff:
            by30[pt].append(v)
    print(f'== {acct} (n={sum(len(v) for v in by.values())})')
    for pt in sorted(by):
        m = statistics.median(by[pt]); m30 = statistics.median(by30[pt]) if by30.get(pt) else None
        print(f'  {pt:14s} n={len(by[pt]):3d} median={m:8.0f}  last30(n={len(by30.get(pt, []))})={m30}')
    allv = [v for vs in by.values() for v in vs]
    allv30 = [v for vs in by30.values() for v in vs]
    print(f'  overall median={statistics.median(allv):.0f}  last30 median={statistics.median(allv30):.0f}')

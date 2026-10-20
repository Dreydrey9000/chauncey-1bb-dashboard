#!/usr/bin/env python3
"""Evening CSV check: posts dated today in posts_all.csv vs per-account medians."""
import csv, statistics, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
today = datetime.date.today().isoformat()
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        rows.append(r)

print('columns:', list(rows[0].keys()))
print('total rows:', len(rows))

def parse_date(s):
    s = (s or '')[:10]
    try:
        return datetime.date.fromisoformat(s).isoformat()
    except Exception:
        return None

# per-account median views (overall + reels only) over the last 90 days
from collections import defaultdict
by_acct = defaultdict(list)
for r in rows:
    d = parse_date(r.get('date'))
    if not d:
        continue
    try:
        v = int(float(r['views'] or 0))
    except Exception:
        continue
    by_acct[r['account']].append((d, v, r.get('post_type') or '', (r.get('caption') or '')[:70], r.get('url') or ''))

for acct in sorted(by_acct):
    items = by_acct[acct]
    all_v = [v for _, v, _, _, _ in items]
    print(f'--- {acct}: n={len(items)} median_views={statistics.median(all_v):.0f}' if all_v else f'--- {acct}: no data')
    # today's posts
    todays = [it for it in items if it[0] == today]
    if todays:
        for d, v, pt, cap, url in todays:
            print(f'  TODAY {d} | type={pt} views={v} | {cap!r} | {url}')
    else:
        print('  TODAY: no posts dated today in CSV')
    # also last 2 days for context
    for look in {it[0] for it in items if it[0] >= (datetime.date.today() - datetime.timedelta(days=2)).isoformat() and it[0] != today}:
        for d, v, pt, cap, url in [it for it in items if it[0] == look]:
            print(f'  {d} | type={pt} views={v} | {cap!r}')

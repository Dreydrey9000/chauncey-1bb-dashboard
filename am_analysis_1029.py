#!/usr/bin/env python3
"""Morning brief analysis: 7-day medians per founder/type from posts_all.csv,
overlaid with fresh REST numbers from raw/pm_delta_*.json (newer wins)."""
import csv, json, os, statistics, datetime, collections

BASE = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date(2026, 10, 29)
CUTOFF = TODAY - datetime.timedelta(days=7)

rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        try:
            d = datetime.date.fromisoformat(r['date'])
        except Exception:
            continue
        rows.append(r)

# fresh overlay: newest pm_delta file
fresh = {}
rawdir = os.path.join(BASE, 'raw')
deltas = sorted(x for x in os.listdir(rawdir) if x.startswith('pm_delta_'))
if deltas:
    j = json.load(open(os.path.join(rawdir, deltas[-1])))
    print('fresh overlay file:', deltas[-1], 'fetched_at:', j.get('fetched_at'))
    for acct, posts in (j.get('fresh') or {}).items():
        if isinstance(posts, list):
            for p in posts:
                if p.get('url') and p.get('views') is not None:
                    ts = str(p.get('posted_at') or '')
                    fresh[(acct, p['url'])] = (ts[:10], int(p['views']), p.get('likes'), p.get('comments'))

def view_for(r):
    key = (r['account'], r.get('url', ''))
    if key in fresh:
        return fresh[key][1], True
    try:
        return int(float(r['views'] or 0)), False
    except Exception:
        return None, False

buckets = collections.defaultdict(list)
detail = collections.defaultdict(list)
for r in rows:
    try:
        d = datetime.date.fromisoformat(r['date'])
    except Exception:
        continue
    if d < CUTOFF or d > TODAY:
        continue
    acct = r['account']
    if acct not in ('drey_ig', 'kevin_ig'):
        continue
    v, is_fresh = view_for(r)
    if v is None:
        continue
    is_reel = '/reel/' in (r.get('url') or '')
    kind = 'reel' if is_reel else 'static'
    buckets[(acct, kind)].append(v)
    detail[(acct, kind)].append((r['date'], v, is_fresh, (r.get('caption') or '')[:40].replace('\n', ' ')))

# fresh posts not in CSV (e.g. 10-28 evening / 10-29)
seen_urls = {(r['account'], r.get('url', '')) for r in rows}
for (acct, url), (day, v, likes, com) in fresh.items():
    if (acct, url) not in seen_urls:
        try:
            d = datetime.date.fromisoformat(day)
        except Exception:
            continue
        if d >= CUTOFF:
            is_reel = '/reel/' in url
            kind = 'reel' if is_reel else 'static'
            buckets[(acct, kind)].append(v)
            detail[(acct, kind)].append((day, v, 'NEW-REST', ''))

for k in sorted(buckets):
    label = f'{k[0]} {k[1]}'
    vals = buckets[k]
    print(f'{label}: n={len(vals)} median={statistics.median(vals):.0f} min={min(vals)} max={max(vals)}')
    for d, v, tag, cap in sorted(detail[k]):
        print(f'   {d} {"FRESH" if tag is True else tag if isinstance(tag, str) else "csv"} {v:>6}  {cap}')

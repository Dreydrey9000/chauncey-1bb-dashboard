#!/usr/bin/env python3
"""Evening medians for beat/miss calls: per-founder, per-type, all-time + 30d."""
import csv, os, statistics, datetime, collections

BASE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        rows.append(r)

CUTOFF = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
TODAY = datetime.date.today().isoformat()
print('today =', TODAY, '| 30d cutoff =', CUTOFF)

def views(r):
    try:
        return int(float(r['views'] or 0))
    except Exception:
        return None

for acct in ('drey_ig', 'kevin_ig'):
    sel = [r for r in rows if r['account'] == acct]
    print(f'--- {acct} (csv rows: {len(sel)}, latest csv date: {max(r["date"] for r in sel)})')
    today_rows = [r for r in sel if r['date'] == TODAY]
    print(f'  rows dated TODAY in csv: {len(today_rows)}')
    for label, filt in (('all-time', lambda r: True), ('30d', lambda r: r['date'] >= CUTOFF)):
        for rtype in ('reel', 'static'):
            is_reel = (rtype == 'reel')
            vs = [views(r) for r in sel if filt(r) and (r['is_reel'].strip().lower() == 'true') == is_reel and views(r) is not None]
            if vs:
                print(f'  {label} {rtype}: n={len(vs)} median={statistics.median(vs):.0f}')

# Kevin theme lanes (all-time + 30d), reels+statics mixed, top 6 by n
for acct in ('kevin_ig', 'drey_ig'):
    sel = [r for r in rows if r['account'] == acct]
    lanes = collections.defaultdict(list)
    lanes30 = collections.defaultdict(list)
    for r in sel:
        v = views(r)
        if v is None:
            continue
        lanes[r['theme']].append(v)
        if r['date'] >= CUTOFF:
            lanes30[r['theme']].append(v)
    print(f'--- {acct} lanes 30d (n>=2):')
    for theme, vs in sorted(lanes30.items(), key=lambda kv: -statistics.median(kv[1]) if len(kv[1]) > 1 else 0):
        if len(vs) >= 2:
            print(f'  {theme}: n={len(vs)} median={statistics.median(vs):.0f} max={max(vs)}')

# Drey confession-opener vs other reels, 30d: manual split by caption prefix "You're too busy"/"When I'm"/first-person confession vs tool explainers
sel = [r for r in rows if r['account'] == 'drey_ig' and r['is_reel'].strip().lower() == 'true' and r['date'] >= CUTOFF]
conf_keys = ("when i'm", "i used to", "you're too busy", "i was", "my ")
for r in sorted(sel, key=lambda r: r['date'], reverse=True):
    v = views(r)
    c = (r['content'] or '').lower()
    tag = 'CONF' if c.startswith(conf_keys) else '    '
    print(f"  {r['date']} {tag} {v:>6}  {(r['content'] or '')[:60]!r}")

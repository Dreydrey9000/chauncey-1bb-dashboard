#!/usr/bin/env python3
"""Evening brief helper: medians by account/type/theme from posts_all.csv + today's rows."""
import csv, statistics, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        try:
            r['views_i'] = int(float(r['views'] or 0))
        except Exception:
            continue
        rows.append(r)

today = datetime.date.today().isoformat()
print('TODAY:', today)

def med(vals):
    return statistics.median(vals) if vals else 0

def fmt(m):
    return f'{m:.0f}' if m is not None else 'n/a'

for acct in ('drey_ig', 'kevin_ig'):
    a = [r for r in rows if r['account'] == acct]
    cutoff = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
    a30 = [r for r in a if r['date'] >= cutoff]
    print(f'\n=== {acct} (n={len(a)}, last={max(r["date"] for r in a)})')
    print(f'  overall median {fmt(med([r["views_i"] for r in a]))} | 30d n={len(a30)} median {fmt(med([r["views_i"] for r in a30]))}')
    for label, src in (('all-time', a), ('30d', a30)):
        reels = [r['views_i'] for r in src if r['is_reel'] == 'True']
        stats_ = [r['views_i'] for r in src if r['is_reel'] == 'False']
        print(f'  {label}: reels n={len(reels)} med {fmt(med(reels))} | statics n={len(stats_)} med {fmt(med(stats_))}')
    themes = {}
    for r in a30:
        themes.setdefault(r['theme'], []).append(r['views_i'])
    for t, v in sorted(themes.items(), key=lambda kv: -med(kv[1]) if kv[1] else 0):
        print(f'  30d theme {t}: n={len(v)} med {fmt(med(v))} max {max(v)}')

print('\n=== posts dated >= 2026-10-21 in CSV ===')
for r in rows:
    if r['date'] >= '2026-10-21':
        print(f"{r['date']} {r['account']:9s} reel={r['is_reel']:5s} theme={r['theme']:11s} views={r['views_i']:5d} {r['url']}")
        print(f"    {str(r['content'])[:100].replace(chr(10),' ')}")

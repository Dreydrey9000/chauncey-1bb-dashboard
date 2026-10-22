#!/usr/bin/env python3
"""Evening lane medians from posts_all.csv (reels vs statics per founder, key themes)."""
import csv, statistics, os

BASE = os.path.dirname(os.path.abspath(__file__))

def load():
    rows = []
    with open(os.path.join(BASE, 'posts_all.csv')) as f:
        for r in csv.DictReader(f):
            try:
                v = int(float(r['views'] or 0))
            except Exception:
                continue
            rows.append({
                'account': r['account'], 'date': r['date'], 'views': v,
                'is_reel': r.get('is_reel', ''), 'theme': r.get('theme', ''),
                'er': r.get('er', ''), 'url': r['url'],
            })
    return rows

rows = load()
maxd = max(r['date'] for r in rows)
print('CSV max date:', maxd, '| total rows:', len(rows))

def med(filt, label):
    v = [r['views'] for r in rows if filt(r)]
    print(f'{label}: n={len(v)} median={statistics.median(v) if v else "n/a"}')

for acct in ('drey_ig', 'kevin_ig'):
    is_r = lambda r: r['account'] == acct and (r['is_reel'].strip().lower() in ('true', '1'))
    is_s = lambda r: r['account'] == acct and (r['is_reel'].strip().lower() not in ('true', '1'))
    med(lambda r: r['account'] == acct, f'{acct} ALL')
    med(is_r, f'{acct} REELS')
    med(is_s, f'{acct} STATICS')
    themes = {}
    for r in rows:
        if r['account'] == acct and r['theme']:
            themes.setdefault(r['theme'], []).append(r['views'])
    for t, v in sorted(themes.items(), key=lambda kv: -statistics.median(kv[1])):
        if len(v) >= 2:
            print(f'  {acct} theme {t}: n={len(v)} median={statistics.median(v)}')

# today's posts in CSV?
for r in rows:
    if r['date'] >= '2026-10-22':
        print('CSV has 10-22:', r['account'], r['views'], r['url'])

#!/usr/bin/env python3
"""Median views by account/theme/format from posts_all.csv, for inspire briefs.
Run: /opt/homebrew/bin/python3 inspire_medians.py"""
import csv, statistics, datetime, os
BASE = os.path.dirname(os.path.abspath(__file__))

rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        try:
            r['views_n'] = int(float(r['views'] or 0))
        except Exception:
            r['views_n'] = None
        r['date_d'] = None
        try:
            r['date_d'] = datetime.date.fromisoformat((r['date'] or '')[:10])
        except Exception:
            pass
        rows.append(r)

dates = [r['date_d'] for r in rows if r['date_d']]
ref = max(dates) if dates else datetime.date.today()
print(f'csv latest post date: {ref} | rows: {len(rows)}')

TRUE = ('True', 'true', '1', 'TRUE', 'Yes')
FALSE = ('False', 'false', '0', '', 'No')

def show(label, subset):
    v = [r['views_n'] for r in subset if r['views_n'] is not None]
    if v:
        print(f'{label:40s} n={len(v):3d} median={int(statistics.median(v)):6d} max={max(v)}')

accts = sorted({r['account'] for r in rows})
for acct in accts:
    for days in (7, 14):
        sub = [r for r in rows if r['account'] == acct and r['date_d'] and (ref - r['date_d']).days <= days]
        show(f'{acct} {days}d ALL', sub)
        show(f'{acct} {days}d reels', [r for r in sub if str(r.get('is_reel')) in TRUE])
        show(f'{acct} {days}d statics', [r for r in sub if str(r.get('is_reel')) in FALSE])
        for t in sorted({r.get('theme', '') for r in sub}):
            if t:
                show(f'{acct} {days}d theme={t}', [r for r in sub if r.get('theme') == t])
    print()

print('--- last 10 posts per founder IG account ---')
for acct in ('drey_ig', 'kevin_ig'):
    sub = sorted([r for r in rows if r['account'] == acct and r['date_d']], key=lambda r: r['date_d'], reverse=True)[:10]
    for r in sub:
        print(f"{acct} {r['date']} reel={r.get('is_reel')} views={r['views_n']} theme={r.get('theme','')} :: {str(r.get('content',''))[:70]}")
    print()

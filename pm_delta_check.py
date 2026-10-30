#!/usr/bin/env python3
"""Evening delta helper: check today's founder posts vs per-account medians from
posts_all.csv (LOCAL ONLY — no network). Prints rows for the beat/miss call."""
import csv, statistics, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE, 'posts_all.csv')
today = datetime.date.today().isoformat()

rows = list(csv.DictReader(open(path)))
print('CSV rows:', len(rows), '| local today:', today)

dates = sorted(set(r['date'] for r in rows))
print('CSV date range:', dates[0], '->', dates[-1])

def med(vals):
    vals = sorted(v for v in vals if v > 0)
    return statistics.median(vals) if vals else None

for label, pref in (('DREY', 'drey_'), ('KEVIN', 'kevin_')):
    print()
    print('=' * 12, label, '=' * 12)
    for acct in sorted(set(r['account'] for r in rows if r['account'].startswith(pref))):
        arows = [r for r in rows if r['account'] == acct]
        m = med([float(r['views'] or 0) for r in arows])
        print(f'{acct}: n={len(arows)} median views={m:.0f}' if m else f'{acct}: no view data')
    tod = [r for r in rows if r['account'].startswith(pref) and r['date'] == today]
    print(f'TODAY posts ({today}): {len(tod)}')
    for r in sorted(tod, key=lambda x: x['ts']):
        v = r['views'] or '0'
        print(f"  {r['account']} {r['ts'][:16]} reel={r['is_reel']} theme={r['theme']} views={v} likes={r['likes']} com={r['comments']} er={r['er']}")
        print(f"    url={r['url']}")
        print(f"    txt={r['content'][:110]!r}")
    if not tod:
        last = max((r for r in rows if r['account'].startswith(pref)), key=lambda x: x['ts'])
        d, a = last['date'], last['account']
        print(f'  (none today - latest {label} post: {d} {a})')

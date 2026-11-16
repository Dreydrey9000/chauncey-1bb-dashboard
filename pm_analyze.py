#!/usr/bin/env python3
"""Evening delta analysis: today's founder posts vs medians (posts_all.csv + pm_delta)."""
import csv, json, datetime, statistics, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        rows.append(r)

def to_int(x):
    try:
        return int(float(x)) if str(x).strip() not in ('', 'None') else None
    except Exception:
        return None

def med(rs, key='views'):
    vals = [to_int(r.get(key)) for r in rs]
    vals = [v for v in vals if v is not None]
    return (statistics.median(vals), len(vals)) if vals else (None, 0)

today = '2026-11-16'
print('=== date coverage ===')
dates = sorted({r['date'] for r in rows if r.get('date')})
print('min/max:', dates[0] if dates else '-', dates[-1] if dates else '-')
print('last 6 dates:', dates[-6:])

for acct in ('drey_ig', 'kevin_ig'):
    rs = [r for r in rows if r['account'] == acct]
    m_all, n_all = med(rs)
    print(f"\n=== {acct}: n={len(rs)} all-time median views={m_all}")
    # last 7 days rows
    recent = [r for r in rs if r['date'] >= '2026-11-10']
    for r in sorted(recent, key=lambda x: x['date']):
        print(f"  CSV {r['date']} reel={r.get('is_reel')} theme={r.get('theme','')!r:20.20} views={r.get('views')} | {r['content'][:60]!r}")
    # medians by theme (all time)
    themes = {}
    for r in rs:
        t = (r.get('theme') or '').strip()
        if t:
            themes.setdefault(t, []).append(r)
    print('  --- theme medians (n>=4):')
    for t, trs in sorted(themes.items(), key=lambda kv: -med(kv[1])[0] if med(kv[1])[0] else 0):
        m, n = med(trs)
        if m is not None and n >= 4:
            print(f'    {t:28.28} median={m:>7} n={n}')
    # format split
    reels = [r for r in rs if str(r.get('is_reel')).lower() in ('1', 'true', 'yes')]
    stats = [r for r in rs if r not in reels]
    mr, nr = med(reels); ms, ns = med(stats)
    print(f'  reels median={mr} (n={nr}) | statics median={ms} (n={ns})')

print('\n=== pm_delta (fresh Zernio, last 3 days) ===')
pm = json.load(open(os.path.join(BASE, 'raw', f'pm_delta_{today}.json')))
for k, posts in pm['fresh'].items():
    print(k, len(posts) if isinstance(posts, list) else posts)
    if isinstance(posts, list):
        for p in posts:
            print(f"  {str(p['posted_at'])[:16]} views={p['views']} likes={p['likes']} com={p['comments']} {p['url']}")
            print(f"    {p['caption'][:80]!r}")

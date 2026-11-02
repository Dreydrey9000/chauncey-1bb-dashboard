#!/usr/bin/env python3
"""PM 2026-11-02: merge posts_all.csv with fresh Zernio pull, compute 7d medians
by format (reel vs static) for drey_ig/kevin_ig, and call beat/miss for today."""
import csv, json, os, statistics, datetime, collections

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw')

# 1. load CSV rows for the two IG accounts
rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        if r['account'] in ('drey_ig', 'kevin_ig'):
            rows.append(r)

# 2. overlay fresh pull (newer stats + any posts missing from CSV)
fresh = json.load(open(os.path.join(RAW, 'pm_delta_2026-11-02.json')))['fresh']
by_url = {}
for r in rows:
    by_url[r['url'].strip().rstrip('/')] = r
for acct, posts in fresh.items():
    if isinstance(posts, dict) and 'error' in posts:
        continue
    for p in posts:
        u = (p.get('url') or '').strip().rstrip('/')
        if not u:
            continue
        if u in by_url:
            r = by_url[u]
            for fld, k in (('views', 'views'), ('likes', 'likes'), ('comments', 'comments')):
                if p.get(k) is not None:
                    r[fld] = p[k]
            r['caption'] = p.get('caption') or r.get('content', '')
        else:
            # new post not yet in CSV
            ts = p.get('posted_at') or ''
            day = ts[:10]
            by_url[u] = {
                'account': acct, 'ts': ts, 'date': day,
                'content': p.get('caption') or '', 'url': u,
                'views': p.get('views') or 0, 'likes': p.get('likes') or 0,
                'comments': p.get('comments') or 0, 'reach': '', 'shares': '',
                'saves': '', 'er': '', 'is_reel': 'True' if '/reel/' in u else 'False',
                'theme': '',
            }

allrows = list(by_url.values())
WIN_START = '2026-10-26'  # 7d window incl today

def is_reel(r):
    return '/reel/' in r['url']

out = {}
for acct in ('drey_ig', 'kevin_ig'):
    sub = [r for r in allrows if r['account'] == acct and r['date'] >= WIN_START]
    reels = [int(float(r['views'])) for r in sub if is_reel(r)]
    stats_ = [int(float(r['views'])) for r in sub if not is_reel(r)]
    out[acct] = {
        'reel_median': statistics.median(reels) if reels else None,
        'reel_n': len(reels),
        'static_median': statistics.median(stats_) if stats_ else None,
        'static_n': len(stats_),
    }
    print(f'== {acct} 7d ({WIN_START}..2026-11-02): reel median {out[acct]["reel_median"]} (n={out[acct]["reel_n"]}), static median {out[acct]["static_median"]} (n={out[acct]["static_n"]})')

print()
print('== TODAY 2026-11-02 posts (merged):')
today = [r for r in allrows if r['date'] == '2026-11-02']
for r in sorted(today, key=lambda x: x['ts']):
    fmt = 'REEL' if is_reel(r) else 'STATIC'
    m = out.get(r['account'], {})
    med = m.get('reel_median' if is_reel(r) else 'static_median')
    v = int(float(r['views']))
    call = 'BEAT' if med and v > med else ('MISS' if med else 'n/a')
    print(f"  {r['account']} {fmt} {v} vs median {med} -> {call} | likes={r['likes']} comments={r['comments']} | {r['url']}")
    print(f"    {str(r['content'])[:100]}")

# yesterday update check (11-01 identity reel matured)
print()
print('== 11-01 Kevin identity reel updated views:')
for r in allrows:
    if r['date'] == '2026-11-01' and r['account'] == 'kevin_ig':
        print(f"  {int(float(r['views']))} views | {r['url']} | {str(r['content'])[:60]}")

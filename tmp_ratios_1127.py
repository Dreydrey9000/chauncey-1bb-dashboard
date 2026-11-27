#!/usr/bin/env python3
"""Final ratio checks for PM brief 2026-11-27."""
import csv, statistics, json

BASE = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard"
with open(f"{BASE}/posts_all.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
fresh = json.load(open(f"{BASE}/raw/pm_delta_2026-11-27.json"))['fresh']

def is_feed(r):
    return ('/stories/' not in (r.get('url') or '')) and bool((r.get('content') or '').strip())

def v(r):
    try:
        return float(r['views'])
    except (ValueError, TypeError):
        return None

# Kevin reel max (with fresh overlay)
fr = {p['url']: p for p in fresh['kevin_ig']}
reels = []
for r in rows:
    if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'True':
        vv = v(r) or 0
        if r['url'] in fr and fr[r['url']]['views'] is not None:
            vv = max(vv, float(fr[r['url']]['views']))
        if vv > 0:
            reels.append((vv, r['date'], r['url']))
top = sorted(reels, reverse=True)[:3]
print('KEVIN top 3 REELS:', top)
print('KEVIN reel count n=%d, reel median=%r' % (len(reels), statistics.median([x[0] for x in reels])))

# Drey max + ratios
dmax = max(v(r) or 0 for r in rows if r['account'] == 'drey_ig' and is_feed(r))
print('DREY all-time max views: %r' % dmax)
print('Rowan today (13295) / Drey max = %.2fx' % (13295 / dmax))
print('Rowan today comments 7h: 17 | Drey last 20 feed posts comments: 0')

# Auto-slot series fresh
for p in fresh['drey_ig']:
    if p['url'].endswith(('DgLxSX2B13h/', 'DgNmOF_hrLs/', 'DgOWCZZIXQG/', 'DgQK_4Nox2Q/')):
        print('DREY auto-series:', p['posted_at'], p['url'][-20:-1], 'views', p['views'])

# Kevin static today vs medians
print('KEVIN static today 509 vs statics median 2024 -> %.0f%%' % (509 / 2024 * 100))
# Drey midnight 202 vs 270.5
print('DREY midnight 202 vs 270.5 -> %.0f%%' % (202 / 270.5 * 100))
# statics/reels ratio drey
print('DREY statics 420 vs reels 183 -> %.1fx' % (420 / 183))
# Kevin windows ratio
print('KEVIN reels 3-7p 1380 vs other 852 -> %.1fx' % (1380 / 852))
print('KEVIN statics 4-9p 2984.5 vs other 1795 -> %.1fx' % (2984.5 / 1795))
# Kevin identity static Tue final
idp = fr.get('https://www.instagram.com/p/DgLOx8wEeIk/')
print('KEVIN Tue identity static fresh:', idp['views'] if idp else 'n/a')

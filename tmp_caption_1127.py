#!/usr/bin/env python3
"""Fetch FULL captions for 2026-11-27 posts (slogan check) + recompute Kevin
reel/static timing-window medians from posts_all.csv (this run's numbers only)."""
import json, os, csv, statistics, urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
API = 'https://getlate.dev/api/v1'
TODAY = '2026-11-27'

ACCOUNTS = [
    ('drey_ig',  'instagram', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin_ig', 'instagram', '6a1c97b22b2567671a7ff845'),
]

def get(path):
    req = urllib.request.Request(f'{API}/{path}', headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

for key, platform, aid in ACCOUNTS:
    d = get(f'analytics?platform={platform}&accountId={aid}&fromDate={TODAY}&toDate={TODAY}&limit=50&page=1')
    print(f'=== {key}: {len(d.get("posts", []))} posts on {TODAY}')
    for p in d.get('posts', []):
        an = p.get('analytics') or {}
        print('URL:', p.get('platformPostUrl'))
        print('posted:', p.get('publishedAt'), '| views', an.get('views'), '| likes', an.get('likes'), '| comments', an.get('comments'))
        print('CAPTION FULL:')
        print(p.get('content') or '(empty)')
        print('-' * 60)

# Kevin timing windows from CSV (feed only, views>0)
with open(os.path.join(BASE, 'posts_all.csv'), newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

def is_feed(r):
    return ('/stories/' not in (r.get('url') or '')) and bool((r.get('content') or '').strip())

def v(r):
    try:
        return float(r['views'])
    except (ValueError, TypeError):
        return None

def hour_et(r):
    ts = r['ts']  # e.g. 2026-11-24T15:50:43+00:00
    try:
        hh = int(ts[11:13])
        return (hh - 5) % 24  # UTC-5 (EST)
    except Exception:
        return None

kev_reels_3_7 = [v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'True' and (h := hour_et(r)) is not None and 15 <= h < 19]
kev_reels_other = [v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'True' and ((h := hour_et(r)) is None or not (15 <= h < 19))]
kev_stat_4_9 = [v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'False' and (h := hour_et(r)) is not None and 16 <= h < 21]
kev_stat_other = [v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'False' and ((h := hour_et(r)) is None or not (16 <= h < 21))]

def m(x):
    x = [a for a in x if a and a > 0]
    return (statistics.median(x), len(x)) if x else (None, 0)

print('kevin reels 3-7p ET: median=%r n=%d' % m(kev_reels_3_7))
print('kevin reels other:   median=%r n=%d' % m(kev_reels_other))
print('kevin statics 4-9p ET: median=%r n=%d' % m(kev_stat_4_9))
print('kevin statics other:   median=%r n=%d' % m(kev_stat_other))

# Drey slogan count check on last 19 feed posts
drey_recent = [r for r in rows if r['account'] == 'drey_ig' and is_feed(r)][-19:]
with_slogan = sum(1 for r in drey_recent if 'Follow for' in (r.get('content') or ''))
print(f'drey last 19 feed posts: {with_slogan} carry slogan, {19 - with_slogan} without')
comments_recent = sum(float(r['comments'] or 0) for r in drey_recent)
print(f'drey comments across last 19 feed posts: {comments_recent}')

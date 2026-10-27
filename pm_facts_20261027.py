#!/opt/homebrew/bin/python3
"""PM 2026-10-27 fact checks: Kevin static likes median, Drey comment drought, top-week ranks."""
import csv, os, statistics

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))

def to_int(v):
    try:
        return int(float(v))
    except Exception:
        return None

k = [r for r in rows if r['account'] == 'kevin_ig']
kstatics = [r for r in k if r['is_reel'] == 'False']
lks = [to_int(r['likes']) for r in kstatics]
lks = [v for v in lks if v is not None]
print('kevin statics likes: median', statistics.median(lks), 'n', len(lks))

d = [r for r in rows if r['account'] == 'drey_ig']
d = sorted(d, key=lambda r: r['date'], reverse=True)
last10 = d[:10]
zero_c = sum(1 for r in last10 if to_int(r['comments']) == 0)
print(f'drey last 10 posts: {zero_c} with 0 comments')

# Drey: rank of today's two reels (fresh REST: 1541, 1776) among last-7-day posts
week = [r for r in d if r['date'] >= '2026-10-21']
wv = sorted([(to_int(r['views']) or 0, r['date'], (r['content'] or '')[:40]) for r in week], reverse=True)
print('drey posts since 10-21 by views:')
for v, dt, c in wv:
    print(f'  {v:>6} {dt} {c}')

# Kevin reels last 2 days vs statics
kr = [r for r in k if r['is_reel'] == 'True' and r['date'] >= '2026-10-26']
print('kevin reels since 10-26:', [(r['date'], to_int(r['views'])) for r in kr])
ks = [r for r in kstatics if r['date'] >= '2026-10-26']
print('kevin statics since 10-26:', [(r['date'], to_int(r['views']), to_int(r['comments'])) for r in ks])

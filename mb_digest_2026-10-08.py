#!/usr/bin/env python3
"""Digest the 2026-10-08 morning-brief pulls: yesterday raw, WoW deltas,
14d follower deltas, and this week's top posts."""
import json, os, datetime
from collections import defaultdict

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw')

def load(fn):
    with open(os.path.join(RAW, fn)) as f:
        return json.load(f)

M = ['impressions', 'reach', 'likes', 'comments', 'shares', 'saves', 'clicks']

for name in ['drey', 'kevin']:
    d = load(f'mb_2026-10-08_daily_{name}.json')
    days = {}
    for row in d.get('dailyData', []):
        pm = (row.get('platformMetrics') or {}).get('instagram') or {}
        days[row['date']] = {
            'posts': row.get('postCount', 0) or pm.get('postCount', 0),
            **{m: pm.get(m, 0) or 0 for m in M},
        }
    dates = sorted(days)
    y = '2026-10-07'
    print(f'== {name.upper()} daily rows: {dates[0]}..{dates[-1]} ==')
    if y in days:
        row = days[y]
        inter = row['likes'] + row['comments'] + row['shares'] + row['saves']
        er = (inter / row['reach'] * 100) if row['reach'] else None
        print(f'  yesterday {y}: posts={row["posts"]} reach={row["reach"]} impr={row["impressions"]} '
              f'likes={row["likes"]} comments={row["comments"]} shares={row["shares"]} saves={row["saves"]} '
              f'clicks={row["clicks"]} ER={er:.1f}%' if er is not None else f'  yesterday {y}: {row} (no reach)')
    else:
        print(f'  yesterday {y}: NOT IN DATA')
    # WoW: Oct 1-7 vs Sep 24-30
    def rng(a, b):
        rows = [days[dt] for dt in dates if a <= dt <= b]
        agg = {k: sum(r[k] for r in rows) for k in ['posts'] + M}
        return agg
    cur, prev = rng('2026-10-01', '2026-10-07'), rng('2026-09-24', '2026-09-30')
    for label, dct in [('last7', cur), ('prior7', prev)]:
        print(f'  {label}: posts={dct["posts"]} reach={dct["reach"]} impr={dct["impressions"]} '
              f'likes={dct["likes"]} comments={dct["comments"]} shares={dct["shares"]} saves={dct["saves"]} clicks={dct["clicks"]}')
    inter_cur = cur['likes'] + cur['comments'] + cur['shares'] + cur['saves']
    inter_prev = prev['likes'] + prev['comments'] + prev['shares'] + prev['saves']
    def pct(c, p):
        return f'{(c - p) / p * 100:+.0f}%' if p else 'n/a'
    print(f'  WoW reach {pct(cur["reach"], prev["reach"])} | interactions {inter_cur} vs {inter_prev} {pct(inter_cur, inter_prev)}')
    print(f'  daily reach by date: ' + ', '.join(f'{dt[5:]}:{days[dt]["reach"]}(p{days[dt]["posts"]})' for dt in dates))

# followers
fs = load('mb_2026-10-08_followers.json')
for acc in fs.get('accounts', []):
    user = acc.get('username')
    hist = acc.get('followerHistory') or acc.get('history') or []
    if not hist:
        print(f'FOLLOWERS {user}: no history keys; top-level keys={list(acc.keys())}')
        continue
    pts = sorted(hist, key=lambda h: h.get('date', ''))
    if len(pts) >= 2:
        a, b = pts[0], pts[-1]
        print(f'FOLLOWERS {user}: {a["date"]}={a.get("followers")} -> {b["date"]}={b.get("followers")} delta={b.get("followers", 0) - a.get("followers", 0)} over {len(pts)} pts')

# top posts this week
for name in ['drey', 'kevin']:
    p = load(f'mb_2026-10-08_posts_{name}.json')
    posts = p.get('posts') or []
    print(f'== {name.upper()} posts in window: {len(posts)} ==')
    def score(po):
        st = po.get('stats') or po.get('metrics') or {}
        return (st.get('likes') or 0) + (st.get('comments') or 0) + (st.get('shares') or 0) + (st.get('saves') or 0)
    for po in sorted(posts, key=score, reverse=True)[:3]:
        st = po.get('stats') or po.get('metrics') or {}
        print(f'  {po.get("postedAt") or po.get("date") or po.get("createdAt")} | {po.get("type")} | '
              f'likes={st.get("likes")} comments={st.get("comments")} shares={st.get("shares")} saves={st.get("saves")} '
              f'reach={st.get("reach")} views={st.get("views")} | {str(po.get("caption"))[:70]}')

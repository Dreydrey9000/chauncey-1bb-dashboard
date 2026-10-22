#!/usr/bin/env python3
"""Morning brief analysis 2026-10-22: compute yesterday/WoW/followers + pull post lists."""
import json, urllib.request, datetime, os, ast, sys

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw', 'mb_2026-10-22')
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']

today = datetime.date.today()
ACCOUNTS = [('drey', '6a1c7e1e2b2567671a7f25ee'), ('kevin', '6a1c97b22b2567671a7ff845')]

def get(url, timeout=90):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def unwrap(res):
    if isinstance(res, dict) and 'result' in res and isinstance(res['result'], str):
        try:
            return ast.literal_eval(res['result'])
        except Exception:
            return json.loads(res['result'])
    return res

M = ['likes', 'comments', 'shares', 'saves']

out = {}
for key, aid in ACCOUNTS:
    d = json.load(open(os.path.join(RAW, f'daily_{key}_ig.json')))
    days = d['dailyData']
    by = {x['date']: x['metrics'] for x in days}
    dates = sorted(by.keys())
    print(f'\n================ {key.upper()} @ IG ================')
    print('dates covered:', dates[0], '->', dates[-1], f'({len(dates)} days)')

    # any nonzero clicks anywhere? (detect whether metric is populated)
    nonzero_clicks = [dt for dt, m in by.items() if m.get('clicks')]
    print('days with nonzero clicks:', nonzero_clicks if nonzero_clicks else 'NONE -> clicks not populated by API')

    y = (today - datetime.timedelta(days=1)).isoformat()
    if y in by:
        m = by[y]
        inter = sum(m.get(k, 0) for k in M)
        er = (inter / m['reach'] * 100) if m.get('reach') else None
        pc = next(x['postCount'] for x in days if x['date'] == y)
        print(f'YESTERDAY {y}: posts={pc} reach={m["reach"]} impr={m["impressions"]} '
              f'likes={m["likes"]} comments={m["comments"]} shares={m["shares"]} saves={m["saves"]} '
              f'interactions={inter} ER={"%.1f%%" % er if er is not None else "n/a (no reach)"}')
    else:
        print(f'YESTERDAY {y}: NOT IN DATA')

    def window(a, b):
        ds = [dt for dt in dates if a <= dt <= b]
        tot = {k: sum(by[dt].get(k, 0) for dt in ds) for k in ['reach', 'impressions'] + M}
        tot['interactions'] = sum(tot[k] for k in M)
        tot['posts'] = sum(1 for dt in ds if by[dt].get('postCount')) # days w/ posts handled below
        return ds, tot

    last7_a = (today - datetime.timedelta(days=8)).isoformat()   # 8 days back -> covers 7 complete days ending yesterday
    # use exact windows: last7 = Oct 15-21, prior7 = Oct 8-14
    d_end = (today - datetime.timedelta(days=1))
    d7 = (d_end - datetime.timedelta(days=6))
    p_end = d7 - datetime.timedelta(days=1)
    p7 = p_end - datetime.timedelta(days=6)
    ds1, t1 = window(d7.isoformat(), d_end.isoformat())
    ds0, t0 = window(p7.isoformat(), p_end.isoformat())
    print(f'WoW window: {d7}..{d_end} ({len(ds1)}d) vs {p7}..{p_end} ({len(ds0)}d)')
    for k in ['reach', 'interactions', 'impressions']:
        delta = ((t1[k] - t0[k]) / t0[k] * 100) if t0[k] else None
        print(f'  {k}: {t1[k]} vs {t0[k]} -> {"%+.0f%%" % delta if delta is not None else "n/a (prior=0)"}')
    posts_l7 = sum(by[dt].get('postCount', 0) or 0 for dt in ds1)
    posts_p7 = sum(by[dt].get('postCount', 0) or 0 for dt in ds0)
    print(f'  posts(days with posts): last7={posts_l7} prior7={posts_p7}')

    # top day by reach in last 7
    top = max(ds1, key=lambda dt: by[dt]['reach'])
    print(f'  TOP DAY last7: {top} reach={by[top]["reach"]} impr={by[top]["impressions"]} '
          f'inter={sum(by[top].get(k,0) for k in M)}')

    # daily series for chart
    series = [{'date': dt, 'reach': by[dt]['reach'], 'impressions': by[dt]['impressions'],
               'posts': next(x['postCount'] for x in days if x['date'] == dt)} for dt in dates]
    out[key] = {'series': series, 'wow': {'last7': t1, 'prior7': t0, 'posts_l7': posts_l7, 'posts_p7': posts_p7}}

# follower stats
f = json.load(open(os.path.join(RAW, 'followers_fs_a.json')))
print('\n================ FOLLOWERS ================')
out['followers'] = {}
for acc in f['accounts']:
    aid = acc['_id']
    key = 'drey' if aid == '6a1c7e1e2b2567671a7f25ee' else 'kevin'
    st = f.get('stats', {})
    pts = st.get(aid) or st.get(acc.get('profileId')) or []
    if not pts and isinstance(st, dict):
        # maybe keyed differently
        for v in st.values():
            if isinstance(v, list) and len(v) >= 10:
                pts = v
                break
    if pts:
        srt = sorted(pts, key=lambda p: p.get('date', ''))
        first, last = srt[0], srt[-1]
        delta = last.get('followers', last.get('count', 0)) - first.get('followers', first.get('count', 0))
        print(f'{key} @{acc["username"]}: {first.get("date")}={first.get("followers", first.get("count"))} '
              f'-> {last.get("date")}={last.get("followers", last.get("count"))}  14d delta={delta:+d} '
              f'(current={acc.get("currentFollowers")}, api growth={acc.get("growth")})')
        out['followers'][key] = {'first': first, 'last': last, 'delta': delta,
                                 'current': acc.get('currentFollowers')}
    else:
        print(f'{key} @{acc["username"]}: series NOT FOUND in stats keys={list(st)[:5] if isinstance(st, dict) else type(st)}')
        print('stats sample:', json.dumps(st, default=str)[:400])

# posts lists (14d) for WHY
from14 = (today - datetime.timedelta(days=14)).isoformat()
for key, aid in ACCOUNTS:
    try:
        posts, page = [], 1
        while True:
            url = (f"https://getlate.dev/api/v1/analytics?platform=instagram&accountId={aid}"
                   f"&fromDate={from14}&toDate={today.isoformat()}&limit=50&page={page}")
            data = unwrap(get(url))
            chunk = data.get('posts') or []
            posts.extend(chunk)
            total = (data.get('overview') or {}).get('totalPosts', len(posts))
            if len(posts) >= total or len(chunk) < 50 or page > 5:
                break
            page += 1
        p = os.path.join(RAW, f'posts_{key}_ig.json')
        with open(p, 'w') as fh:
            json.dump(posts, fh, indent=1, default=str)
        print(f'\n{key}: {len(posts)} posts saved')
        # print compact per-post summary
        for pp in posts:
            cap = (pp.get('caption') or '')[:60].replace('\n', ' ')
            print(f'  {pp.get("postedAt", pp.get("date", "?"))[:10]} type={pp.get("type", pp.get("mediaType","?"))} '
                  f'views={pp.get("views", pp.get("playCount","?"))} likes={pp.get("likes","?")} '
                  f'comments={pp.get("comments","?")} saves={pp.get("saves","?")} | {cap}')
    except Exception as e:
        print(f'{key} posts FAILED: {type(e).__name__}: {e}')

with open(os.path.join(RAW, 'analysis.json'), 'w') as fh:
    json.dump(out, fh, indent=1, default=str)
print('\nanalysis.json saved')

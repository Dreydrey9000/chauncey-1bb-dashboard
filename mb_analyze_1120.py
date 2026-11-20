#!/usr/bin/env python3
"""Morning brief analysis 2026-11-20 — correct Zernio raw schema.
Fields: _id, content, mediaProductType, publishedAt (UTC ISO), analytics{...}, platformPostUrl.
Followers: followers.json -> stats[accountId] = [{date, followers}].
Dates converted to America/New_York (audience tz).
"""
import json, ast, os, glob, datetime, collections, zoneinfo

RAW = os.path.expanduser('~/.hermes/workspaces/chauncey/dashboard/raw')
OUT = os.path.expanduser('~/.hermes/workspaces/chauncey/briefs/work/mb_2026-11-20.json')
ET = zoneinfo.ZoneInfo('America/New_York')

TODAY = datetime.date(2026, 11, 20)
YDAY = TODAY - datetime.timedelta(days=1)           # Nov 19
W1 = (TODAY - datetime.timedelta(days=7), YDAY)      # Nov 13-19
W2 = (TODAY - datetime.timedelta(days=14), TODAY - datetime.timedelta(days=8))  # Nov 6-12
D14 = (TODAY - datetime.timedelta(days=14), YDAY)

def et_date(iso):
    try:
        dt = datetime.datetime.fromisoformat(iso.replace('Z', '+00:00'))
        return dt.astimezone(ET).date()
    except Exception:
        return None

def load_posts(key):
    posts = []
    for f in sorted(glob.glob(os.path.join(RAW, f'{key}_p*.txt'))):
        pg = ast.literal_eval(json.load(open(f))['result'])
        posts.extend(pg.get('posts') or [])
    seen, out = set(), []
    for p in posts:
        i = p.get('_id')
        if i in seen: continue
        seen.add(i); out.append(p)
    return out

def a(p, k):
    return (p.get('analytics') or {}).get(k) or 0

result = {'date': TODAY.isoformat(), 'yesterday': YDAY.isoformat(),
          'w1': [W1[0].isoformat(), W1[1].isoformat()],
          'w2': [W2[0].isoformat(), W2[1].isoformat()], 'accounts': {}}

for key, handle, accid in [('drey_ig', 'itisdrey', '6a1c7e1e2b2567671a7f25ee'),
                            ('kevin_ig', 'kclavier', '6a1c97b22b2567671a7ff845')]:
    upd = load_posts(key)
    days = {}
    all14 = []
    for p in upd:
        d = et_date(p.get('publishedAt') or '')
        if d is None: continue
        if not (D14[0] <= d <= YDAY): continue
        all14.append((d, p))
        r = days.setdefault(d, {'posts': 0, 'reach': 0, 'impressions': 0, 'likes': 0,
            'comments': 0, 'shares': 0, 'saves': 0, 'profileViews': 0, 'websiteClicks': 0,
            'follows': 0, 'reels': 0, 'stories': 0, 'feed': 0, 'posts_today': []})
        r['posts'] += 1
        t = p.get('mediaProductType') or '?'
        if t == 'REELS': r['reels'] += 1
        elif t == 'STORY': r['stories'] += 1
        elif t == 'FEED': r['feed'] += 1
        r['reach'] += a(p, 'reach'); r['impressions'] += a(p, 'impressions')
        r['likes'] += a(p, 'likes'); r['comments'] += a(p, 'comments')
        r['shares'] += a(p, 'shares'); r['saves'] += a(p, 'saves')
        r['profileViews'] += a(p, 'profileViews'); r['websiteClicks'] += a(p, 'websiteClicks')
        r['follows'] += a(p, 'follows') or 0
        r['posts_today'].append({'type': t, 'caption': (p.get('content') or '')[:80],
            'reach': a(p, 'reach'), 'impressions': a(p, 'impressions'), 'likes': a(p, 'likes'),
            'comments': a(p, 'comments'), 'shares': a(p, 'shares'), 'saves': a(p, 'saves'),
            'profileViews': a(p, 'profileViews'), 'websiteClicks': a(p, 'websiteClicks'),
            'skipRate': (p.get('analytics') or {}).get('reelsSkipRate'),
            'avgWatchMs': (p.get('analytics') or {}).get('igReelsAvgWatchTime'),
            'url': p.get('platformPostUrl')})

    def week(x, y):
        r = {'posts': 0, 'reach': 0, 'impressions': 0, 'likes': 0, 'comments': 0,
             'shares': 0, 'saves': 0, 'reels': 0, 'stories': 0, 'feed': 0}
        for d, rec in days.items():
            if x <= d <= y:
                for k in r: r[k] += rec[k]
        r['interactions'] = r['likes'] + r['comments'] + r['shares'] + r['saves']
        return r

    y = dict(days.get(YDAY, {'posts': 0, 'reach': 0, 'impressions': 0, 'likes': 0, 'comments': 0,
        'shares': 0, 'saves': 0, 'profileViews': 0, 'websiteClicks': 0, 'follows': 0,
        'reels': 0, 'stories': 0, 'feed': 0}))
    y['posts_today'] = days.get(YDAY, {}).get('posts_today', [])
    y['interactions'] = y['likes'] + y['comments'] + y['shares'] + y['saves']
    y['er'] = round(y['interactions'] / y['reach'] * 100, 1) if y.get('reach') else None

    w1, w2 = week(*W1), week(*W2)

    wkposts = [(d, p) for d, p in all14 if W1[0] <= d <= W1[1]]
    def imp(p): return a(p, 'impressions')
    top3 = sorted(wkposts, key=lambda x: -imp(x[1]))[:3]
    top_info = [{'date': d.isoformat(), 'caption': (p.get('content') or '')[:130],
                 'type': p.get('mediaProductType'), 'impressions': imp(p), 'reach': a(p, 'reach'),
                 'likes': a(p, 'likes'), 'shares': a(p, 'shares'), 'saves': a(p, 'saves'),
                 'comments': a(p, 'comments'),
                 'skipRate': (p.get('analytics') or {}).get('reelsSkipRate'),
                 'avgWatchMs': (p.get('analytics') or {}).get('igReelsAvgWatchTime'),
                 'url': p.get('platformPostUrl')} for d, p in top3]

    # followers
    fl = json.load(open(os.path.join(RAW, 'followers.json')))
    series = (fl.get('stats') or {}).get(accid) or []
    win = [s for s in series if D14[0].isoformat() <= s['date'] <= D14[1].isoformat()]
    fol = None
    if win:
        fol = {'first': win[0], 'last': win[-1],
               'delta': win[-1]['followers'] - win[0]['followers'],
               'min': min(s['followers'] for s in win),
               'max': max(s['followers'] for s in win),
               'latest_overall': series[-1] if series else None, 'n_days': len(win)}

    result['accounts'][key] = {'handle': handle, 'daily': {d.isoformat(): v for d, v in sorted(days.items())},
                               'yesterday': y, 'w1': w1, 'w2': w2, 'top_posts': top_info,
                               'posts_14d': len(all14), 'followers': fol}
    print(f"{key}: {len(upd)} dedup | 14d {len(all14)} | yday posts={y['posts']} reach={y['reach']} int={y['interactions']}"
          f" | w1 reach={w1['reach']} int={w1['interactions']} vs w2 reach={w2['reach']} int={w2['interactions']}"
          f" | fol={fol['delta'] if fol else 'N/A'} last={fol['last']['followers'] if fol else 'N/A'}")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(result, open(OUT, 'w'), indent=1)
print('saved', OUT)

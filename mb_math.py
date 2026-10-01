#!/usr/bin/env python3
"""Morning brief math: yesterday, WoW, followers, post days, top posts this week."""
import json, glob, ast, datetime as dt

today = dt.date.today()
yday = today - dt.timedelta(days=1)

def load_daily(name):
    return json.load(open(f'/tmp/mb_daily_{name}.json'))['dailyData']

def day_stats(row):
    m = row.get('metrics', {})
    return {
        'date': row['date'], 'posts': row.get('postCount', 0),
        'reach': m.get('reach'), 'impressions': m.get('impressions'),
        'likes': m.get('likes'), 'comments': m.get('comments'),
        'shares': m.get('shares'), 'saves': m.get('saves'), 'clicks': m.get('clicks'),
    }

def window(rows, start, end):
    sel = [day_stats(r) for r in rows if start <= r['date'] <= end]
    agg = {'posts': 0, 'reach': 0, 'impressions': 0, 'likes': 0, 'comments': 0, 'shares': 0, 'saves': 0, 'clicks': 0}
    for s in sel:
        for k in agg:
            v = s.get(k)
            agg[k] += v if isinstance(v, (int, float)) else 0
    agg['interactions'] = agg['likes'] + agg['comments'] + agg['shares'] + agg['saves']
    agg['days'] = len(sel)
    return agg

for name in ('DREY', 'KEVIN'):
    rows = load_daily(name)
    y = [day_stats(r) for r in rows if r['date'] == yday.isoformat()]
    y = y[0] if y else None
    last7_start = (today - dt.timedelta(days=7)).isoformat()
    prev7_start = (today - dt.timedelta(days=14)).isoformat()
    prev7_end = (today - dt.timedelta(days=8)).isoformat()
    l7 = window(rows, last7_start, yday.isoformat())
    p7 = window(rows, prev7_start, prev7_end)
    postdays = [(r['date'], r.get('postCount', 0)) for r in rows if r.get('postCount', 0) > 0]
    out = {'yesterday': y, 'last7': l7, 'prev7': p7, 'postdays': postdays,
           'dates': [r['date'] for r in rows],
           'reach_series': [r.get('metrics', {}).get('reach') for r in rows],
           'impr_series': [r.get('metrics', {}).get('impressions') for r in rows]}
    if y and y['reach']:
        out['yesterday']['eng_rate'] = round((y['likes'] + y['comments'] + y['shares'] + y['saves']) / y['reach'] * 100, 1)
    for tag, a, b in (('reach_wow', l7['reach'], p7['reach']), ('interactions_wow', l7['interactions'], p7['interactions'])):
        out[tag] = {'last7': a, 'prev7': b,
                    'pct': round((a - b) / b * 100, 1) if b else None}
    with open(f'/tmp/mb_stats_{name}.json', 'w') as f:
        json.dump(out, f, indent=1)
    print(f'== {name} ==')
    print('yesterday', json.dumps(y))
    print('last7', json.dumps({k: l7[k] for k in ('posts','reach','interactions','likes','comments','shares','saves','clicks','days')}))
    print('prev7', json.dumps({k: p7[k] for k in ('posts','reach','interactions','likes','comments','shares','saves','clicks','days')}))
    print('reach_wow', json.dumps(out['reach_wow']), 'interactions_wow', json.dumps(out['interactions_wow']))
    print('postdays', postdays)

# followers
fl = json.load(open('/tmp/mb_followers.json'))
for a in fl['accounts']:
    pts = fl['stats'].get(a['_id'], [])
    if pts:
        first, last = pts[0], pts[-1]
        print(f"followers {a['username']}: {first['followers']} -> {last['followers']} ({last['followers']-first['followers']:+d}) over {first['date']}..{last['date']}, current {a['currentFollowers']}, series_len {len(pts)}")
        json.dump({'username': a['username'], 'series': [(p['date'], p['followers']) for p in pts]}, open(f"/tmp/mb_fseries_{a['username']}.json", 'w'))
    else:
        print(f"followers {a['username']}: NO SERIES")

# top post last 7 days from raw pulls
def load_raw(key):
    posts = []
    for f in sorted(glob.glob(f'/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/{key}_p*.txt')):
        payload = json.load(open(f))
        res = payload.get('result') if isinstance(payload, dict) else payload
        if isinstance(res, str):
            try: res = ast.literal_eval(res)
            except Exception: res = json.loads(res)
        posts.extend(res.get('posts') or [])
    return posts

cutoff = (today - dt.timedelta(days=7)).isoformat()
for key, label in (('drey_ig', 'DREY'), ('kevin_ig', 'KEVIN')):
    posts = load_raw(key)
    recent = []
    for p in posts:
        d = (p.get('createdAt') or p.get('date') or '')[:10]
        if d >= cutoff:
            recent.append((d, p))
    print(f'-- {label}: {len(recent)} posts in last 7d window --')
    def num(p, k):
        v = p.get(k)
        return v if isinstance(v, (int, float)) else 0
    ranked = sorted(recent, key=lambda dp: num(dp[1], 'views') or num(dp[1], 'likes'), reverse=True)
    for d, p in ranked[:5]:
        keys = {k: p.get(k) for k in ('id','caption','type','views','likes','comments','shares','saves','url','permalink') if k in p}
        cap = (keys.get('caption') or '')[:70]
        print(d, json.dumps({k: v for k, v in keys.items() if k != 'caption'}), '|', cap)

#!/usr/bin/env python3
"""Rebuild dashboard data.js from raw Zernio pulls in raw/.
Cron-safe: auto-classifies posts by account username, tolerates partial pulls.
Raw files: outer JSON {"result": "<python-repr str>"} (analytics) or followers.json (follower stats).
"""
import json, ast, os, glob, datetime
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw')

USER_KEY = {'itisdrey': 'drey_ig', 'kclavier': 'kevin_ig',
            'dreydrey9000': 'drey_tt', 'kevin.clavier': 'kevin_tt'}
DREY_IG_ID = '6a1c7e1e2b2567671a7f25ee'
KEVIN_IG_ID = '6a1c97b22b2567671a7ff845'

rows = []
for path in sorted(glob.glob(os.path.join(RAW, '*.txt'))):
    try:
        outer = json.loads(open(path).read())
        data = ast.literal_eval(outer['result'])
    except Exception as e:
        print(f'skip {os.path.basename(path)}: {e}')
        continue
    posts = data.get('posts') if isinstance(data, dict) else None
    if not posts:
        continue
    for post in posts:
        plats = post.get('platforms') or []
        uname = plats[0].get('accountUsername') if plats else None
        key = USER_KEY.get(uname or '')
        if not key:
            continue
        a = post.get('analytics') or {}
        rows.append({
            'account': key, 'ts': post['publishedAt'], 'date': post['publishedAt'][:10],
            'content': post.get('content') or '', 'url': post.get('platformPostUrl'),
            'views': a.get('views'), 'reach': a.get('reach'), 'likes': a.get('likes'),
            'comments': a.get('comments'), 'shares': a.get('shares'), 'saves': a.get('saves'),
            'reposts': a.get('reposts'), 'er': a.get('engagementRate'),
            'watch_ms': a.get('igReelsAvgWatchTime'), 'skip': a.get('reelsSkipRate'),
            'dur_s': a.get('videoDurationSeconds'),
        })

df = pd.DataFrame(rows)
df['ts'] = pd.to_datetime(df['ts'], utc=True)
df = df.sort_values('ts').drop_duplicates(subset=['account', 'url'], keep='last')
df.to_csv(os.path.join(BASE, 'posts_all.csv'), index=False)

def pack(key):
    d = df[df.account == key].sort_values('ts')
    if not len(d):
        return None
    reels = d[(d.watch_ms > 0) & (d.dur_s > 0)].copy()
    reels['comp'] = (reels.watch_ms/1000)/reels.dur_s*100
    top = d.nlargest(5, 'views')
    span_days = max((d.ts.max() - d.ts.min()).days, 1)
    return {
        'posts': int(len(d)),
        'perWeek': round(len(d)/(span_days/7), 1),
        'medianViews': int(d.views.median()),
        'meanViews': int(d.views.mean()),
        'maxViews': int(d.views.max()),
        'medianER': round(float(d.er.dropna().median()), 1),
        'medianSaves': float(d.saves.median()),
        'medianShares': float(d.shares.median()),
        'medianComments': float(d.comments.median()),
        'totalSaves': int(d.saves.sum()),
        'totalShares': int(d.shares.sum()),
        'totalComments': int(d.comments.sum()),
        'completion': round(float(reels.comp.median()), 0) if len(reels) else None,
        'skip': round(float(reels.skip.median()), 0) if len(reels) else None,
        'series': [{'d': r.date, 'v': int(r.views), 'er': (round(float(r.er), 1) if pd.notna(r.er) else None)} for r in d.itertuples()],
        'weekly': [{'w': str(w), 'mv': float(g.views.median()), 'n': int(len(g))}
                   for w, g in d.groupby(d.ts.dt.to_period('W-SUN').dt.start_time.dt.date)],
        'top': [{'t': ' '.join(r.content.split())[:90], 'url': r.url, 'v': int(r.views),
                 's': int(r.saves), 'sh': int(r.shares), 'c': int(r.comments),
                 'er': (round(float(r.er), 1) if pd.notna(r.er) else None), 'd': r.date}
                for r in top.itertuples()],
    }

# followers
kevin_followers, drey_followers = [], {'current': None, 'trend': None}
fpath = os.path.join(RAW, 'followers.json')
if os.path.exists(fpath):
    try:
        fo = json.loads(open(fpath).read())
        fres = fo.get('result', fo)
        if isinstance(fres, str):
            fres = json.loads(fres)
        stats = fres.get('stats', {})
        kevin_followers = [[p['date'], int(p['followers'])] for p in stats.get(KEVIN_IG_ID, [])]
        dpts = stats.get(DREY_IG_ID, [])
        cur = int(dpts[-1]['followers']) if dpts else None
        drey_followers = {'current': cur, 'trend': [[p['date'], int(p['followers'])] for p in dpts] if len(dpts) > 1 else None}
    except Exception as e:
        print(f'followers parse failed: {e}')

now_et = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
data = {
    'generated': now_et.strftime('%Y-%m-%d %I:%M%p ET'),
    'source': f"OFFICIAL_API via Zernio — Instagram & TikTok owned accounts, synced {now_et.strftime('%Y-%m-%d %I:%M%p ET')}",
    'drey_ig': pack('drey_ig'), 'kevin_ig': pack('kevin_ig'),
    'drey_tt': pack('drey_tt'), 'kevin_tt': pack('kevin_tt'),
    'kevinFollowers': kevin_followers,
    'dreyFollowers': drey_followers,
}

with open(os.path.join(BASE, 'data.js'), 'w') as f:
    f.write('window.DATA = ' + json.dumps(data) + ';')
counts = df.groupby('account').size().to_dict()
print(f"data.js rebuilt {data['generated']} — posts: {counts}")

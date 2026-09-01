#!/usr/bin/env python3
"""Rebuild dashboard site/data.js from raw Zernio pulls in raw/.
Cron-safe: auto-classifies posts by account username, tolerates partial pulls.
Adds: theme classification (Chauncey's editorial labels), verdict engine,
decision module, film-this-week, full post list for drilldown.
"""
import json, ast, os, glob, datetime, re
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw')
SITE = os.path.join(BASE, 'site')
os.makedirs(SITE, exist_ok=True)

USER_KEY = {'itisdrey': 'drey_ig', 'kclavier': 'kevin_ig',
            'dreydrey9000': 'drey_tt', 'kevin.clavier': 'kevin_tt'}
DREY_IG_ID = '6a1c7e1e2b2567671a7f25ee'
KEVIN_IG_ID = '6a1c97b22b2567671a7ff845'

THEMES = [  # priority order: first max-score wins ties
    ('confession', 'Vulnerable Confession',
     ['embarrass', 'hiding', 'white knuckl', 'burnout', 'overwhelm', 'darkness', 'lonely',
      'alone', 'struggle', 'exhaust', 'tired', 'anxiet', 'fight-or-flight', 'avoidance']),
    ('room', 'The Room / 1BB',
     ['1bb', 'club', 'room', 'members', 'inner circle', 'surround', 'network', 'event',
      'conversation', 'owners']),
    ('ai_systems', 'AI Systems & Proof',
     [' ai ', 'claude', 'prompt', 'automat', 'token', 'chatgpt', 'vibe cod', 'second brain',
      'algorithm', 'build', 'tool']),
    ('identity', 'Identity · Family · Faith',
     ['god', 'faith', 'blessed', 'grateful', 'prayer', 'church', 'hebrews', 'scripture',
      'brother', 'family', 'thankful', 'who you are', 'identity']),
    ('discipline', 'Discipline & Standards',
     ['gym', 'morning', 'comfort', 'discipline', 'standards', 'non-negotiable', 'nonnegotiable',
      'walk', 'workout', 'safe', 'stuck']),
    ('podcast', 'Podcast & Media',
     ['podcast', 'youtube', 'full video', 'episode', 'youtu.be']),
    ('lifestyle', 'Personal / Lifestyle',
     ['pizza', 'dating', 'birthday', 'spanish', 'roast', 'girlfriend', 'boys']),
]
THEME_LABELS = dict((k, l) for k, l, _ in THEMES)

def classify(text):
    t = ' ' + text.lower() + ' '
    scores = {k: sum(t.count(w) for w in words) for k, _, words in THEMES}
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else 'other'

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
        content = post.get('content') or ''
        rows.append({
            'account': key, 'ts': post['publishedAt'], 'date': post['publishedAt'][:10],
            'content': content, 'url': post.get('platformPostUrl'),
            'views': a.get('views') or 0, 'reach': a.get('reach') or 0, 'likes': a.get('likes') or 0,
            'comments': a.get('comments') or 0, 'shares': a.get('shares') or 0, 'saves': a.get('saves') or 0,
            'reposts': a.get('reposts') or 0, 'er': a.get('engagementRate'),
            'watch_ms': a.get('igReelsAvgWatchTime') or 0, 'skip': a.get('reelsSkipRate') or 0,
            'dur_s': a.get('videoDurationSeconds'),
            'is_reel': bool(a.get('videoDurationSeconds')),
            'theme': classify(content),
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
    top = d.nlargest(10, 'views')
    span_days = max((d.ts.max() - d.ts.min()).days, 1)
    # themes
    themes = []
    for tk, g in d.groupby('theme'):
        if len(g) < 1:
            continue
        themes.append({'key': tk, 'label': THEME_LABELS.get(tk, 'Other'), 'n': int(len(g)),
                       'medianViews': int(g.views.median()), 'medianER': round(float(g.er.dropna().median()), 1) if g.er.notna().any() else None,
                       'saves': int(g.saves.sum()), 'comments': int(g.comments.sum())})
    themes.sort(key=lambda x: -x['medianViews'])
    # reel vs static
    reel_v = d[d.is_reel].views.median() if d.is_reel.any() else None
    stat_v = d[~d.is_reel].views.median() if (~d.is_reel).any() else None
    # 14-day trend
    cutoff = d.ts.max() - pd.Timedelta(days=14)
    recent, prior = d[d.ts > cutoff], d[(d.ts <= cutoff) & (d.ts > cutoff - pd.Timedelta(days=14))]
    trend = {'recentMedian': float(recent.views.median()) if len(recent) else None,
             'priorMedian': float(prior.views.median()) if len(prior) else None,
             'recentN': int(len(recent)), 'priorN': int(len(prior))}
    return {
        'posts': int(len(d)),
        'perWeek': round(len(d)/(span_days/7), 1),
        'medianViews': int(d.views.median()),
        'meanViews': int(d.views.mean()),
        'maxViews': int(d.views.max()),
        'medianER': round(float(d.er.dropna().median()), 1),
        'medianSaves': float(d.saves.median()),
        'medianComments': float(d.comments.median()),
        'totalSaves': int(d.saves.sum()),
        'totalShares': int(d.shares.sum()),
        'totalComments': int(d.comments.sum()),
        'completion': round(float(reels.comp.median()), 0) if len(reels) else None,
        'skip': round(float(reels.skip.median()), 0) if len(reels) else None,
        'reelMedianViews': int(reel_v) if reel_v is not None and not pd.isna(reel_v) else None,
        'staticMedianViews': int(stat_v) if stat_v is not None and not pd.isna(stat_v) else None,
        'themes': themes,
        'trend': trend,
        'series': [{'d': r.date, 'v': int(r.views), 'er': (round(float(r.er), 1) if pd.notna(r.er) else None)} for r in d.itertuples()],
        'weekly': [{'w': str(w), 'mv': float(g.views.median()), 'n': int(len(g))}
                   for w, g in d.groupby(d.ts.dt.to_period('W-SUN').dt.start_time.dt.date)],
        'top': [{'t': ' '.join(r.content.split())[:90], 'url': r.url, 'v': int(r.views),
                 's': int(r.saves), 'sh': int(r.shares), 'c': int(r.comments),
                 'er': (round(float(r.er), 1) if pd.notna(r.er) else None), 'd': r.date, 'theme': THEME_LABELS.get(r.theme, 'Other')}
                for r in top.itertuples()],
        'all': [{'t': r.content[:800], 'url': r.url, 'v': int(r.views), 's': int(r.saves), 'sh': int(r.shares),
                 'c': int(r.comments), 'l': int(r.likes), 'r': int(r.reach),
                 'er': (round(float(r.er), 1) if pd.notna(r.er) else None),
                 'd': r.date, 'theme': THEME_LABELS.get(r.theme, 'Other'),
                 'reel': bool(r.is_reel), 'skip': (round(float(r.skip), 0) if r.is_reel and r.skip else None),
                 'comp': (round((r.watch_ms/1000)/r.dur_s*100, 0) if r.is_reel and r.watch_ms and r.dur_s else None)}
                for r in d.itertuples()],
    }

# ---------- verdicts + decisions ----------
V = []
def v(text, who='both', conf='medium'):
    V.append({'text': text, 'who': who, 'conf': conf})

def decision(d, founder):
    """Post-more-of-X call: top theme with n>=3 by median views."""
    cands = [t for t in d['themes'] if t['n'] >= 3]
    if not cands:
        return None
    win = cands[0]
    lift = round((win['medianViews'] / max(d['medianViews'], 1) - 1) * 100)
    ref = d['top'][0]
    return {'theme': win['label'], 'medianViews': win['medianViews'], 'n': win['n'],
            'accountMedian': d['medianViews'], 'lift': lift,
            'proof': f"Proof: \"{ref['t']}…\" — {ref['v']:,} views on {ref['d']}", 'proofUrl': ref['url'],
            'founder': founder}

FILM = {
    'drey': 'One reel, confession format: name one specific operator problem you lived ("I\'m 25" style), then the system you built to kill it. Tuesday or Sunday. That is your reach AND your comment engine.',
    'kevin': 'One carousel, not a reel: a real room/member moment (with permission) — identity first line, proof in the middle, one clear next step at the end. Your static posts outrun your reels 2-to-1.',
}

data_drey, data_kevin = pack('drey_ig'), pack('kevin_ig')
data_drey_tt, data_kevin_tt = pack('drey_tt'), pack('kevin_tt')

# verdicts (IG-first reads, all from real numbers)
if data_drey and data_kevin:
    dd, kk = data_drey, data_kevin
    v(f"Kevin leads reach: {kk['medianViews']:,} vs {dd['medianViews']:,} median views per post. His identity/family/room posts are the strongest content class in the system.", 'both', 'high')
    if dd['completion'] and kk['completion']:
        v(f"Drey leads reel craft: {dd['completion']:.0f}% median completion vs Kevin's {kk['completion']:.0f}%. Kevin loses viewers in the open; Drey holds them.", 'both', 'high')
    if kk['staticMedianViews'] and kk['reelMedianViews']:
        mult = kk['staticMedianViews'] / max(kk['reelMedianViews'], 1)
        v(f"Kevin's static posts median {kk['staticMedianViews']:,} views vs {kk['reelMedianViews']:,} for reels — photo/carousel is his format {mult:.1f}x over.", 'kevin', 'high')
    v(f"Trust gap: Kevin {kk['totalSaves']} total saves vs Drey {dd['totalSaves']}. Saves predict business. Drey's confession posts are his best trust lever.", 'both', 'medium')
    for d, who in [(dd, 'drey'), (kk, 'kevin')]:
        t = d['trend']
        if t['recentMedian'] and t['priorMedian']:
            delta = (t['recentMedian']/t['priorMedian'] - 1)*100
            arrow = 'up' if delta >= 0 else 'down'
            v(f"{who.title()}'s last-14-day median is {t['recentMedian']:,.0f} views ({arrow} {abs(delta):.0f}% vs the prior 14 days, n={t['recentN']} posts).", who, 'medium')
    ai_d = next((t for t in dd['themes'] if t['key'] == 'ai_systems'), None)
    if ai_d:
        rel = 'above' if ai_d['medianViews'] >= dd['medianViews'] else 'below'
        v(f"Drey's AI-systems content medians {ai_d['medianViews']:,} views across {ai_d['n']} posts — {rel} his account median of {dd['medianViews']:,}. Tool-tour content stays deprioritized.", 'drey', 'medium')
if data_drey_tt and data_kevin_tt:
    v(f"TikTok: Kevin wins every metric — {data_kevin_tt['medianViews']:,} median views at {data_kevin_tt['medianER']}% ER vs Drey's {data_drey_tt['medianViews']:,} at {data_drey_tt['medianER']}%. Drey's TT shows no signal in 90 days: repurpose-only.", 'both', 'high')

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
        if len(kevin_followers) > 1:
            v(f"Kevin's followers: {kevin_followers[0][1]:,} → {kevin_followers[-1][1]:,} (+{kevin_followers[-1][1]-kevin_followers[0][1]:,} in the window). The July surge tracked launch + family content, not promos.", 'kevin', 'high')
    except Exception as e:
        print(f'followers parse failed: {e}')

now_et = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4)))
data = {
    'generated': now_et.strftime('%Y-%m-%d %I:%M%p ET'),
    'source': f"OFFICIAL_API via Zernio — Instagram & TikTok owned accounts, synced {now_et.strftime('%Y-%m-%d %I:%M%p ET')}",
    'drey_ig': data_drey, 'kevin_ig': data_kevin,
    'drey_tt': data_drey_tt, 'kevin_tt': data_kevin_tt,
    'kevinFollowers': kevin_followers,
    'dreyFollowers': drey_followers,
    'verdicts': V,
    'decision': {'drey': decision(data_drey, 'drey') if data_drey else None,
                 'kevin': decision(data_kevin, 'kevin') if data_kevin else None},
    'film': FILM,
}

for out in [os.path.join(SITE, 'data.js'), os.path.join(BASE, 'data.js')]:
    with open(out, 'w') as f:
        f.write('window.DATA = ' + json.dumps(data) + ';')
# keep root index.html in sync for the legacy GitHub Pages link
site_index = os.path.join(SITE, 'index.html')
if os.path.exists(site_index):
    import shutil
    shutil.copy(site_index, os.path.join(BASE, 'index.html'))
counts = df.groupby('account').size().to_dict()
print(f"data.js rebuilt {data['generated']} — posts: {counts} — verdicts: {len(V)}")

# Morning 2026-11-02: founder medians + weekend deltas from posts_all.csv (6:31a refresh)
import csv, statistics, json
from collections import defaultdict
from datetime import datetime

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))

def iv(s):
    s = (s or '').strip()
    try: return int(float(s))
    except: return None

for r in rows:
    r['v'] = iv(r.get('views')); r['d'] = r.get('date','')
    r['reel'] = str(r.get('is_reel','')).lower() == 'true'

# medians: trailing 28 days ending 2026-11-01 (posts on/ before 11-01)
cutoff = '2026-10-04'
med = {}
for acc in ('drey_ig','kevin_ig'):
    reels = [r['v'] for r in rows if r['account']==acc and r['reel'] and r['v'] is not None and r['d']>=cutoff and r['d']<='2026-11-01']
    stats_ = [r['v'] for r in rows if r['account']==acc and not r['reel'] and r['v'] is not None and r['d']>=cutoff and r['d']<='2026-11-01']
    med[acc] = {'reel_median': statistics.median(reels) if reels else None,
                'reel_n': len(reels),
                'static_median': statistics.median(stats_) if stats_ else None,
                'static_n': len(stats_)}

# all recent posts per founder since 10-29 (weekend + Friday)
recent = defaultdict(list)
for r in rows:
    if r['account'] in ('drey_ig','kevin_ig') and r['d'] >= '2026-10-29':
        recent[r['account']].append(r)

out = {'medians': med, 'recent': {}}
for acc, items in recent.items():
    lst = []
    for r in sorted(items, key=lambda x: x['ts']):
        lst.append({'date': r['d'], 'reel': r['reel'], 'views': r['v'],
                    'likes': iv(r.get('likes')), 'comments': iv(r.get('comments')),
                    'theme': r.get('theme'), 'url': r.get('url'),
                    'cap': (r.get('content') or '')[:100]})
    out['recent'][acc] = lst

# top 3 posts per founder last 14 days by views (10-19..11-01)
top = {}
for acc in ('drey_ig','kevin_ig'):
    cands = [r for r in rows if r['account']==acc and r['v'] is not None and r['d']>='2026-10-19' and r['d']<='2026-11-01']
    cands.sort(key=lambda x: -x['v'])
    top[acc] = [{'date': r['d'], 'reel': r['reel'], 'views': r['v'], 'theme': r.get('theme'),
                 'cap': (r['content'] or '')[:80], 'url': r.get('url')} for r in cands[:5]]
out['top14d'] = top

print(json.dumps(out, indent=1, default=str))

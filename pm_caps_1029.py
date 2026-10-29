#!/usr/bin/env python3
"""PM 10-29: full captions for today's posts + 7-day reel/static medians from CSV+fresh."""
import json, csv, os, statistics, datetime, urllib.request
BASE = os.path.dirname(os.path.abspath(__file__))
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
API = 'https://getlate.dev/api/v1'
ACCOUNTS = [('drey_ig','instagram','6a1c7e1e2b2567671a7f25ee'),
            ('kevin_ig','instagram','6a1c97b22b2567671a7ff845')]
def get(path):
    req = urllib.request.Request(f'{API}/{path}', headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())
print('===== FULL CAPTIONS, posts published 2026-10-29 =====')
for name, platform, aid in ACCOUNTS:
    d = get(f'analytics?platform={platform}&accountId={aid}&fromDate=2026-10-26&toDate=2026-10-29&limit=50&page=1')
    for p in d.get('posts', []):
        ts = str(p.get('publishedAt') or '')
        if not ts.startswith('2026-10-29'):
            continue
        an = p.get('analytics') or {}
        print(f"\n--- {name} {ts} {p.get('platformPostUrl')}")
        print(f"views={an.get('views')} likes={an.get('likes')} comments={an.get('comments')}")
        print(str(p.get('content') or '')[:600])
print('\n===== MEDIANS (posts_all.csv, 2026-10-22..2026-10-28, by founder x format) =====')
def is_reel(url): return '/reel/' in (url or '')
rows = {}
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        if r['account'] in ('drey_ig','kevin_ig') and '2026-10-22' <= r['date'] <= '2026-10-28':
            try: v = int(float(r['views'] or 0))
            except: continue
            rows.setdefault((r['account'], is_reel(r['url'])), []).append(v)
for (acct, reel), vs in sorted(rows.items()):
    fmt = 'REEL' if reel else 'STATIC'
    print(f'{acct} {fmt}: n={len(vs)} median={statistics.median(vs):.0f} list={sorted(vs)}')

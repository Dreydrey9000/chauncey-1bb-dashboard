#!/usr/bin/env python3
"""PM inspire delta analysis: beat/miss vs posts_all.csv medians + Zernio daily-metrics for fresh posts."""
import csv, json, statistics, urllib.request, urllib.error, os
BASE = os.path.dirname(os.path.abspath(__file__))

rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
print('CSV columns:', list(rows[0].keys()))
today = '2026-10-17'
todays = [r for r in rows if str(r.get('date', '')).startswith(today)]
print('Posts dated %s in CSV: %d' % (today, len(todays)))
for r in todays:
    print(' ', r['account'], r.get('post_type'), r.get('views'), str(r.get('caption', ''))[:60])

def med(acct, kw=None, ptype=None):
    v = []
    for r in rows:
        if r['account'] != acct or not r.get('views'):
            continue
        if ptype is not None and r.get('post_type') != ptype:
            continue
        if kw is not None and kw not in (str(r.get('theme', '')) + str(r.get('caption', ''))).lower():
            continue
        try:
            v.append(int(float(r['views'])))
        except ValueError:
            pass
    return (statistics.median(v), len(v)) if v else (None, 0)

for acct in ('drey_ig', 'kevin_ig'):
    print('\n%s medians:' % acct)
    print('  all:', med(acct))
    print('  confession:', med(acct, 'confession'))
    print('  room:', med(acct, 'room'))
    if acct == 'drey_ig':
        print('  ai:', med(acct, 'ai'))
    print('  statics:', med(acct, ptype='static'))
    print('  reels:', med(acct, ptype='reel'))
    print('  identity:', med(acct, 'identity'))

kv = []
for r in rows:
    if r['account'] == 'kevin_ig' and r.get('views'):
        try:
            kv.append((int(float(r['views'])), r.get('date'), str(r.get('caption', ''))[:40]))
        except ValueError:
            pass
print('\nKevin top 8:')
for v, d, c in sorted(kv, reverse=True)[:8]:
    print('  %7d %s %s' % (v, d, c))

KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
API = 'https://getlate.dev/api/v1'

def get(path):
    req = urllib.request.Request('%s/%s' % (API, path), headers={'Authorization': 'Bearer ' + KEY})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

ACCOUNTS = [('drey_ig', 'instagram', '6a1c7e1e2b2567671a7f25ee'),
            ('kevin_ig', 'instagram', '6a1c97b22b2567671a7ff845')]
for name, platform, aid in ACCOUNTS:
    got = False
    for qs in ('fromDate=2026-10-15&toDate=2026-10-17', 'from=2026-10-15&to=2026-10-17'):
        try:
            d = get('analytics/daily-metrics?platform=%s&accountId=%s&%s' % (platform, aid, qs))
            print('\n=== %s daily-metrics (%s):' % (name, qs))
            print(json.dumps(d, default=str)[:1000])
            got = True
            break
        except Exception as e:
            print('%s variant %s failed: %r' % (name, qs[:10], repr(e)[:120]))
    if not got:
        print('%s: all daily-metrics variants failed' % name)

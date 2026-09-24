#!/usr/bin/env python3
"""Daily Zernio pull for CRON_REFRESH.md — direct Late API (MCP unavailable).
Writes raw/<key>_p<n>.txt as {"result": <python repr>} to match gen_data.py parser.
On account failure: keeps previous raw files, records the failure.
"""
import json, os, glob, urllib.request, urllib.error, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw')
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
API = 'https://getlate.dev/api/v1'

ACCOUNTS = [
    ('drey_ig',  'instagram', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin_ig', 'instagram', '6a1c97b22b2567671a7ff845'),
    ('drey_tt',  'tiktok',    '6a1c7f242b2567671a7f30a4'),
    ('kevin_tt', 'tiktok',    '6a1c97a12b2567671a7ff6ff'),
    ('club_ig',  'instagram', '6a97cdbf77555aae01be704a'),
]
FOLLOWER_IDS = '6a1c7e1e2b2567671a7f25ee,6a1c97b22b2567671a7ff845,6a97cdbf77555aae01be704a'

to_date = datetime.date.today()
from_date = to_date - datetime.timedelta(days=90)
fd, td = from_date.isoformat(), to_date.isoformat()
print(f'window {fd} → {td}')

def get(path):
    req = urllib.request.Request(f'{API}/{path}',
                                 headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

failures, counts = [], {}
for key, platform, aid in ACCOUNTS:
    try:
        page = 1
        pages_data = []
        total = None
        while True:
            d = get(f'analytics?platform={platform}&accountId={aid}'
                    f'&fromDate={fd}&toDate={td}&limit=50&page={page}')
            if 'posts' not in d:
                raise RuntimeError(f'unexpected payload keys: {list(d.keys())}')
            pages_data.append(d)
            total = d.get('overview', {}).get('totalPosts', 0)
            got = sum(len(p.get('posts', [])) for p in pages_data)
            max_pages = d.get('pagination', {}).get('pages', 1)
            if got >= total or page >= max_pages:
                break
            page += 1
        # success — now replace raw files
        for old in glob.glob(os.path.join(RAW, f'{key}_p*.txt')):
            os.remove(old)
        for i, d in enumerate(pages_data, 1):
            with open(os.path.join(RAW, f'{key}_p{i}.txt'), 'w') as f:
                f.write(json.dumps({'result': repr(d)}))
        counts[key] = total
        print(f'{key}: {total} posts, {len(pages_data)} page(s) written')
    except Exception as e:
        failures.append(f'{key}: {e}')
        print(f'{key}: FAILED ({e}) — kept previous raw files')

# follower stats
try:
    fs = get(f'accounts/follower-stats?accountIds={FOLLOWER_IDS}&fromDate={fd}&toDate={td}')
    with open(os.path.join(RAW, 'followers.json'), 'w') as f:
        json.dump(fs, f)
    accts = {a['username']: a.get('currentFollowers') for a in fs.get('accounts', [])}
    print(f'followers.json saved: {accts}')
except Exception as e:
    failures.append(f'followers: {e}')
    print(f'followers FAILED ({e}) — kept previous file')

print('FAILURES:', failures if failures else 'none')

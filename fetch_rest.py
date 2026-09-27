#!/usr/bin/env python3
"""Daily dashboard refresh via Zernio REST fallback (MCP OAuth revoked 2026-09-24).
Writes raw/<key>_p<n>.txt in the exact format gen_data.py expects:
{"result": "<repr of python dict with overview+posts>"}
"""
import json, urllib.request, urllib.error, datetime, os, glob, sys

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw')
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']

today = datetime.date.today()
from_date = (today - datetime.timedelta(days=90)).isoformat()
to_date = today.isoformat()

ACCOUNTS = [
    ('drey_ig', 'instagram', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin_ig', 'instagram', '6a1c97b22b2567671a7ff845'),
    ('drey_tt', 'tiktok', '6a1c7f242b2567671a7f30a4'),
    ('kevin_tt', 'tiktok', '6a1c97a12b2567671a7ff6ff'),
    ('club_ig', 'instagram', '6a97cdbf77555aae01be704a'),
]

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())

def unwrap(res):
    # REST may return the payload directly or wrapped like {"result": "..."}
    if isinstance(res, dict) and 'result' in res and isinstance(res['result'], str):
        import ast
        try:
            return ast.literal_eval(res['result'])
        except Exception:
            return json.loads(res['result'])
    return res

failed = []
pulled = {}

for key, platform, acc_id in ACCOUNTS:
    try:
        pages = []
        page = 1
        overview = None
        while True:
            url = (f"https://getlate.dev/api/v1/analytics?platform={platform}"
                   f"&accountId={acc_id}&fromDate={from_date}&toDate={to_date}"
                   f"&limit=50&page={page}")
            data = unwrap(get(url))
            if overview is None:
                overview = data.get('overview', {})
            posts = data.get('posts') or []
            if not posts:
                break
            pages.append({'overview': overview, 'posts': posts})
            total = overview.get('totalPosts', 0)
            got = sum(len(p['posts']) for p in pages)
            if got >= total or len(posts) < 50:
                break
            page += 1
            if page > 20:
                break
        # success: wipe stale files, write new
        for old in glob.glob(os.path.join(RAW, f'{key}_p*.txt')):
            os.remove(old)
        for i, p in enumerate(pages, 1):
            with open(os.path.join(RAW, f'{key}_p{i}.txt'), 'w') as f:
                f.write(json.dumps({'result': repr(p)}))
        pulled[key] = sum(len(p['posts']) for p in pages)
        print(f'{key}: {pulled[key]} posts in {len(pages)} page(s)')
    except Exception as e:
        failed.append(key)
        print(f'{key}: FAILED ({type(e).__name__}: {e}) — keeping previous raw files')

# followers
try:
    ids = '6a1c7e1e2b2567671a7f25ee,6a1c97b22b2567671a7ff845,6a97cdbf77555aae01be704a'
    url = (f"https://getlate.dev/api/v1/accounts/follower-stats?accountIds={ids}"
           f"&fromDate={from_date}&toDate={to_date}")
    res = get(url)
    with open(os.path.join(RAW, 'followers.json'), 'w') as f:
        json.dump(res, f)
    print('followers.json saved')
except Exception as e:
    failed.append('followers')
    print(f'followers: FAILED ({type(e).__name__}: {e})')

print('SUMMARY pulled=' + json.dumps(pulled) + ' failed=' + json.dumps(failed))

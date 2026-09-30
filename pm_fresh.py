#!/usr/bin/env python3
"""PM freshness check v3: correct parser — stats under post['analytics'], plus platform permalink."""
import json, urllib.request, os

KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']

ACCOUNTS = [
    ('kevin_ig', '6a1c97b22b2567671a7ff845'),
    ('kevin_tt', '6a1c97a12b2567671a7ff6ff'),
]

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + KEY})
    return json.loads(urllib.request.urlopen(req, timeout=90).read())

for key, acc_id in ACCOUNTS:
    platform = 'instagram' if key.endswith('_ig') else 'tiktok'
    url = (f"https://getlate.dev/api/v1/analytics?platform={platform}"
           f"&accountId={acc_id}&fromDate=2026-09-29&toDate=2026-09-30&limit=50&page=1")
    res = get(url)
    if isinstance(res, dict) and 'result' in res and isinstance(res['result'], str):
        import ast
        try:
            res = ast.literal_eval(res['result'])
        except Exception:
            res = json.loads(res['result'])
    sync = (res.get('overview') or {}).get('lastSync')
    print(f"===== {key} (lastSync {sync}) =====")
    for p in res.get('posts') or []:
        a = p.get('analytics') or {}
        cap = str(p.get('content') or '')[:60].replace('\n', ' ')
        plat = (p.get('platforms') or [{}])[0]
        print(f"{p.get('publishedAt')} | views={a.get('views')} likes={a.get('likes')} "
              f"comments={a.get('comments')} shares={a.get('shares')} saves={a.get('saves')} "
              f"skip={a.get('reelsSkipRate')}% dur={a.get('videoDurationSeconds')}s "
              f"updated={a.get('lastUpdated')} | {cap}")
    print()

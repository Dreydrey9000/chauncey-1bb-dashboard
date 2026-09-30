#!/usr/bin/env python3
"""Debug v2: dump full post JSON for today's kevin_ig posts to locate stats fields."""
import json, urllib.request, os

KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
url = ("https://getlate.dev/api/v1/analytics?platform=instagram"
       "&accountId=6a1c97b22b2567671a7ff845&fromDate=2026-09-30&toDate=2026-09-30"
       "&limit=5&page=1")
req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + KEY})
res = json.loads(urllib.request.urlopen(req, timeout=90).read())
if isinstance(res, dict) and 'result' in res and isinstance(res['result'], str):
    import ast
    try:
        res = ast.literal_eval(res['result'])
    except Exception:
        res = json.loads(res['result'])
posts = res.get('posts') or []
print('n posts:', len(posts))
for p in posts:
    print(json.dumps(p, default=str, indent=1)[:1600])
    print('=====')

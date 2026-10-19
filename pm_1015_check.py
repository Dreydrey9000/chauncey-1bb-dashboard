#!/usr/bin/env python3
"""Check the 10/15 drey_ig reel (0 views this morning) — single-day pull."""
import json, os, urllib.request

KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
url = ('https://getlate.dev/api/v1/analytics?platform=instagram'
       '&accountId=6a1c7e1e2b2567671a7f25ee&fromDate=2026-10-15&toDate=2026-10-15&limit=50&page=1')
req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + KEY})
with urllib.request.urlopen(req, timeout=60) as r:
    d = json.loads(r.read().decode())
for p in d.get('posts', []):
    an = p.get('analytics') or {}
    print(json.dumps({'url': p.get('platformPostUrl'), 'at': p.get('publishedAt'),
                      'views': an.get('views'), 'likes': an.get('likes'),
                      'comments': an.get('comments')}, default=str))
    print('cap:', str(p.get('content') or '')[:100].replace('\n', ' '))

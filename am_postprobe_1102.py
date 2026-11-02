#!/usr/bin/env python3
"""Probe post objects for ids/timestamps + fetch best-post analytics per account."""
import json, urllib.request, urllib.error

KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
BASE = 'https://getlate.dev/api/v1'
P = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_posts_1102.json'))

d = json.loads(P['drey_posts_raw']['body'])
posts = d.get('posts', d.get('data', []))
print('post keys:', sorted(posts[0].keys()))
print('platforms[0] keys:', sorted((posts[0].get('platforms') or [{}])[0].keys()))
p0 = posts[0]
pl = (p0.get('platforms') or [{}])[0]
print(json.dumps({k: p0.get(k) for k in ('id', '_id', 'postId', 'publishedAt', 'contentType', 'type')}, indent=0))
print('platforms[0]:', json.dumps({k: pl.get(k) for k in sorted(pl.keys()) if k != 'id'}, indent=0)[:800])

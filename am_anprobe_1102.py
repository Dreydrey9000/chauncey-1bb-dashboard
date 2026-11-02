#!/usr/bin/env python3
"""Probe the analytics endpoint shape for one post."""
import json, urllib.request, urllib.error

KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
BASE = 'https://getlate.dev/api/v1'

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]
    except Exception as e:
        return -1, f'{type(e).__name__}: {e}'

pid = '18160751107504102'  # Drey 'Asked Ryan why he bites his straws'
for path in (
    f'analytics/posts/{pid}',
    f'posts/{pid}/analytics',
    f'analytics?platform=instagram&postId={pid}',
    f'analytics/post/{pid}',
    f'analytics?postId={pid}',
    f'posts/{pid}',
):
    s, b = get(f'{BASE}/{path}')
    print(f'[{s}] {path}')
    print('  ', b[:400].replace('\n', ' '))
    print()

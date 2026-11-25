#!/usr/bin/env python3
"""Evening inspire brief 2026-11-25 PM: lookalike reels pull (TokScript) + founder delta vs medians."""
import json, os, subprocess, sys

# --- Part 1: pull lookalike reels via saved tokscript_pull.py machinery ---
sys.path.insert(0, '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard')

# Load the key from profile .env
KEY = None
envp = os.path.expanduser('~/.hermes/profiles/chauncey/.env')
for line in open(envp):
    line = line.strip()
    if line.startswith('MCP_TOKSCRIPT_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
if not KEY:
    print('NO KEY FOUND'); sys.exit(1)

import urllib.request

def call_tool(username, count=12):
    url = 'https://api.tokscript.com/mcp'
    headers = {
        'Authorization': 'Bearer ' + KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream',
    }
    def post(payload):
        req = urllib.request.Request(url, json.dumps(payload).encode(), headers)
        resp = urllib.request.urlopen(req, timeout=120)
        return resp.read().decode('utf-8', 'replace')
    # initialize
    init = post({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
                 'params': {'protocolVersion': '2024-11-05', 'capabilities': {},
                            'clientInfo': {'name': 'chauncey-brief', 'version': '1.0'}}})
    try:
        post({'jsonrpc': '2.0', 'method': 'notifications/initialized', 'params': {}})
    except Exception:
        pass
    raw = post({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
                'params': {'name': 'get_instagram_user_reels',
                           'arguments': {'username': username, 'count': count}}})
    # parse SSE data: lines
    text_blob = ''
    for line in raw.splitlines():
        if line.startswith('data:'):
            chunk = line[5:].strip()
            if chunk:
                text_blob += chunk + '\n'
    try:
        obj = json.loads(text_blob)
    except Exception:
        # maybe single event
        try:
            obj = json.loads(raw)
        except Exception:
            return {'error': 'unparsed', 'raw': raw[:800]}
    if 'error' in obj and obj.get('error'):
        return {'error': obj['error']}
    res = obj.get('result', obj)
    # payload text -> parse inner JSON
    items = []
    try:
        content = res.get('content', [])
        payload = ''
        for c in content:
            if isinstance(c, dict) and c.get('type') == 'text':
                payload += c.get('text', '')
        data = json.loads(payload)
        if isinstance(data, dict):
            items = data.get('posts', []) or data.get('reels', [])
            if not items and any(isinstance(v, list) for v in data.values()):
                for v in data.values():
                    if isinstance(v, list) and v and isinstance(v[0], dict):
                        items = v; break
    except Exception as e:
        return {'error': 'inner-parse: ' + repr(e)[:120], 'raw': str(res)[:500]}
    out = []
    for it in items:
        if not isinstance(it, dict):
            continue
        stats = it.get('stats') if isinstance(it.get('stats'), dict) else {}
        flat = {**it, **stats}
        def g(*names, default=None):
            for n in names:
                if flat.get(n) not in (None, ''):
                    return flat.get(n)
            return default
        out.append({
            'url': g('url', 'link', 'permalink', 'web_link'),
            'views': g('views', 'viewCount', 'playCount', 'play_count'),
            'likes': g('likes', 'likeCount', 'like_count'),
            'comments': g('comments', 'commentCount', 'comment_count'),
            'date': g('date', 'taken_at', 'createdAt', 'created_at', 'timestamp'),
            'caption': str(g('caption', 'title', 'text', default=''))[:140],
        })
    return {'username': username, 'reels': out}

LOOKALIKES = ['liamottley', 'rowancheung', 'bedroskeuilian', 'davidmeltzer', 'gerardadams']
results = {}
for u in LOOKALIKES:
    print('=' * 20, u, '=' * 20, flush=True)
    r = call_tool(u, 12)
    results[u] = r
    if 'error' in r:
        print('  ERROR:', r['error'])
    else:
        for reel in r['reels']:
            print('  ', reel['date'], '| views=', reel['views'], 'likes=', reel['likes'],
                  'comments=', reel['comments'], '|', reel['url'])
            print('       cap:', reel['caption'].replace('\n', ' ')[:120])

with open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/pm_look_20261125.json', 'w') as f:
    json.dump(results, f, indent=1, default=str)
print('\nSaved pm_look_20261125.json')

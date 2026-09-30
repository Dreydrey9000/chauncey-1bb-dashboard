# TokScript MCP direct caller — get_instagram_user_reels for lookalike scan (rebuilt from pipeline-pitfalls.md note)
import json, os, urllib.request

ENV = '/Users/andrethomas/.hermes/profiles/chauncey/.env'
key = None
for line in open(ENV):
    line = line.strip()
    if line.startswith('MCP_TOKSCRIPT_API_KEY='):
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
if not key:
    raise SystemExit('no MCP_TOKSCRIPT_API_KEY in profile .env')

URL = 'https://api.tokscript.com/mcp'
MID = 1

def rpc(method, params=None, notif=False, accept='application/json, text/event-stream'):
    global MID
    body = {'jsonrpc': '2.0', 'method': method}
    if params is not None:
        body['params'] = params
    if not notif:
        body['id'] = MID
        MID += 1
    hdr = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'Accept': accept}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=hdr)
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            raw = resp.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        if e.code == 406 and accept != 'text/event-stream':
            return rpc(method, params, notif, accept='text/event-stream')
        if e.code == 406 and accept == 'text/event-stream':
            return rpc(method, params, notif, accept='application/json')
        raise
    try:
        j = json.loads(raw)
        if 'result' in j or 'error' in j:
            if 'error' in j:
                raise RuntimeError('rpc error: ' + json.dumps(j['error'])[:300])
            return j['result']
    except json.JSONDecodeError:
        pass
    if notif and not raw.strip():
        return None
    payload = None
    for line in raw.splitlines():
        if line.startswith('data:'):
            chunk = line[5:].strip()
            if not chunk:
                continue
            try:
                j = json.loads(chunk)
            except json.JSONDecodeError:
                continue
            if 'result' in j or 'error' in j:
                payload = j
    if payload is None:
        raise RuntimeError('no JSON payload in SSE; first 200 chars: ' + raw[:200])
    if 'error' in payload:
        raise RuntimeError('rpc error: ' + json.dumps(payload['error'])[:300])
    return payload['result']

rpc('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {}, 'clientInfo': {'name': 'chauncey-brief', 'version': '1.0'}})
rpc('notifications/initialized', notif=True)

import sys
USERS = sys.argv[1:] or ['liamottley', 'gerardadams', 'bedroskeuilian']
for user in USERS:
    print('=' * 20, user, '=' * 20)
    try:
        res = rpc('tools/call', {'name': 'get_instagram_user_reels', 'arguments': {'username': user, 'count': 12}})
        items = None
        if isinstance(res, dict):
            content = res.get('content') or []
            for c in content:
                if c.get('type') == 'text':
                    try:
                        data = json.loads(c['text'])
                    except json.JSONDecodeError:
                        continue
                    if isinstance(data, list):
                        items = data
                    elif isinstance(data, dict):
                        for k in ('posts', 'reels', 'videos', 'data', 'items', 'results'):
                            if isinstance(data.get(k), list):
                                items = data[k]
                                break
                        if items is None and any(isinstance(v, dict) and ('views' in v or 'viewCount' in v or 'shortcode' in v) for v in data.values()):
                            items = list(data.values())
        if not items:
            print('  UNPARSED — raw result truncated:')
            print(json.dumps(res, default=str)[:1500])
            continue
        if items:
            items = sorted(items, key=lambda it: str(it.get('timestamp') or ''), reverse=True)
        for it in items:
            if not isinstance(it, dict):
                continue
            stats = it.get('stats') if isinstance(it.get('stats'), dict) else {}
            it = {**it, **stats}
            def g(*names, default=''):
                for n in names:
                    if it.get(n) not in (None, ''):
                        return it.get(n)
                return default
            url = g('url', 'link', 'permalink', 'web_link')
            if url and '/reel/' not in str(url) and 'instagram.com' in str(url):
                continue
            views = g('views', 'viewCount', 'playCount', 'play_count')
            likes = g('likes', 'likeCount', 'like_count')
            com = g('comments', 'commentCount', 'comment_count')
            date = g('date', 'taken_at', 'createdAt', 'created_at', 'timestamp')
            cap = str(g('caption', 'title', 'text'))[:90].replace('\n', ' ')
            print(f"  {date} | views={views} likes={likes} comments={com} | {url}")
            print(f"      {cap}")
    except Exception as e:
        print('  FAILED:', repr(e)[:200])

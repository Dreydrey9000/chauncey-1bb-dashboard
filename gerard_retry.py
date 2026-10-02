# One-off retry: gerardadams with multi-line SSE data handling
import json, urllib.request, urllib.error

ENV = '/Users/andrethomas/.hermes/profiles/chauncey/.env'
key = None
for line in open(ENV):
    line = line.strip()
    if line.startswith('MCP_TOKSCRIPT_API_KEY='):
        key = line.split('=', 1)[1].strip().strip('"').strip("'")
if not key:
    raise SystemExit('no key')

URL = 'https://api.tokscript.com/mcp'
MID = 1

def rpc(method, params=None, notif=False):
    global MID
    body = {'jsonrpc': '2.0', 'method': method}
    if params is not None:
        body['params'] = params
    if not notif:
        body['id'] = MID
        MID += 1
    hdr = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json',
           'Accept': 'application/json, text/event-stream'}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=hdr)
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read().decode('utf-8', 'replace')
    # Plain JSON?
    try:
        j = json.loads(raw)
        if 'error' in j:
            raise RuntimeError(json.dumps(j['error'])[:200])
        return j.get('result')
    except json.JSONDecodeError:
        pass
    if notif and not raw.strip():
        return None
    # Strategy A: whole stream is ONE JSON doc chunked across SSE events.
    chunks = [ln[5:].strip() for ln in raw.splitlines() if ln.startswith('data:')]
    for joined in (''.join(chunks), '\n'.join(chunks)):
        try:
            j = json.loads(joined)
        except json.JSONDecodeError:
            continue
        if 'result' in j or 'error' in j:
            if 'error' in j:
                raise RuntimeError(json.dumps(j['error'])[:200])
            return j['result']
    # Strategy B: per-event parse (spec-compliant SSE).
    events, buf = [], []
    for line in raw.splitlines():
        if line.startswith('data:'):
            buf.append(line[5:].strip())
        elif not line.strip() and buf:
            events.append('\n'.join(buf)); buf = []
    if buf:
        events.append('\n'.join(buf))
    for ev in events:
        try:
            j = json.loads(ev)
        except json.JSONDecodeError:
            continue
        if 'result' in j or 'error' in j:
            if 'error' in j:
                raise RuntimeError(json.dumps(j['error'])[:200])
            return j['result']
    raise RuntimeError('still unparseable; raw head: ' + raw[:300].replace('\n', ' | '))

rpc('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {},
                   'clientInfo': {'name': 'chauncey-brief', 'version': '1.0'}})
rpc('notifications/initialized', notif=True)

res = rpc('tools/call', {'name': 'get_instagram_user_reels',
                         'arguments': {'username': 'gerardadams', 'count': 12}})
items = None
status = None
if isinstance(res, dict):
    for c in res.get('content') or []:
        if c.get('type') == 'text':
            try:
                data = json.loads(c['text'])
            except json.JSONDecodeError:
                continue
            if isinstance(data, dict):
                status = data.get('status')
                for k in ('posts', 'reels', 'videos', 'data', 'items', 'results'):
                    if isinstance(data.get(k), list):
                        items = data[k]
                        break
            elif isinstance(data, list):
                items = data
print('payload status:', status)
if not items:
    print('NO ITEMS — raw truncated:')
    print(json.dumps(res, default=str)[:1200])
else:
    items = [i for i in items if isinstance(i, dict)]
    items.sort(key=lambda it: str(it.get('timestamp') or ''), reverse=True)
    for it in items:
        st = it.get('stats') if isinstance(it.get('stats'), dict) else {}
        it = {**it, **st}
        def g(*names, default=''):
            for n in names:
                if it.get(n) not in (None, ''):
                    return it.get(n)
            return default
        url = g('url', 'link', 'permalink', 'web_link')
        print(f"  {g('date','taken_at','createdAt','timestamp')} | views={g('views','viewCount','playCount')} "
              f"likes={g('likes','likeCount')} comments={g('comments','commentCount')} | {url}")
        print(f"      {str(g('caption','title','text'))[:90]}")

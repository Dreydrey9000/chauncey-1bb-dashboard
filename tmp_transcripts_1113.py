#!/usr/bin/env python3
"""One-off: fetch transcripts for two picked lookalike reels (evening brief 2026-11-13)."""
import json, os, urllib.request

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

def rpc(method, params=None, notif=False, accept='application/json, text/event-stream'):
    global MID
    body = {'jsonrpc': '2.0', 'method': method}
    if params is not None:
        body['params'] = params
    if not notif:
        body['id'] = MID
        MID += 1
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
        headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'Accept': accept})
    with urllib.request.urlopen(req, timeout=180) as resp:
        raw = resp.read().decode('utf-8', 'replace')
    try:
        j = json.loads(raw)
        if 'error' in j:
            raise RuntimeError(json.dumps(j['error'])[:300])
        if 'result' in j:
            return j['result']
    except json.JSONDecodeError:
        pass
    if notif:
        return None
    payload = None
    for line in raw.splitlines():
        if line.startswith('data:'):
            try:
                j = json.loads(line[5:].strip())
            except Exception:
                continue
            if 'result' in j or 'error' in j:
                payload = j
    if payload is None:
        raise RuntimeError('no SSE payload: ' + raw[:200])
    if 'error' in payload:
        raise RuntimeError(json.dumps(payload['error'])[:300])
    return payload['result']

rpc('initialize', {'protocolVersion': '2024-11-05', 'capabilities': {},
                   'clientInfo': {'name': 'chauncey-brief', 'version': '1.0'}})
rpc('notifications/initialized', notif=True)

for label, u in [
    ('rowan_Dfms0Dtx9B5', 'https://www.instagram.com/reel/Dfms0Dtx9B5/'),
    ('meltzer_Dfim9koEX7w', 'https://www.instagram.com/reel/Dfim9koEX7w/'),
]:
    print('=' * 16, label, '=' * 16)
    try:
        res = rpc('tools/call', {'name': 'get_instagram_transcript', 'arguments': {'video_url': u}})
        print(json.dumps(res, default=str)[:1600])
    except Exception as e:
        print('FAILED:', repr(e)[:250])

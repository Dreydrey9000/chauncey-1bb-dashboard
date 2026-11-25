#!/usr/bin/env python3
"""PM 2026-11-25: pull transcripts for candidate imitation reels (TokScript direct MCP)."""
import json, os, sys, urllib.request

envp = os.path.expanduser('~/.hermes/profiles/chauncey/.env')
KEY = None
for line in open(envp):
    line = line.strip()
    if line.startswith('MCP_TOKSCRIPT_API_KEY='):
        KEY = line.split('=', 1)[1].strip().strip('"').strip("'")
if not KEY:
    print('NO KEY'); sys.exit(1)

URL = 'https://api.tokscript.com/mcp'
HEADERS = {
    'Authorization': 'Bearer ' + KEY,
    'Content-Type': 'application/json',
    'Accept': 'application/json, text/event-stream',
}

def post(payload):
    req = urllib.request.Request(URL, json.dumps(payload).encode(), HEADERS)
    resp = urllib.request.urlopen(req, timeout=120)
    return resp.read().decode('utf-8', 'replace')

post({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize',
      'params': {'protocolVersion': '2024-11-05', 'capabilities': {},
                 'clientInfo': {'name': 'chauncey-brief', 'version': '1.0'}}})
try:
    post({'jsonrpc': '2.0', 'method': 'notifications/initialized', 'params': {}})
except Exception:
    pass

TARGETS = [
    ('rowan-today', 'https://www.instagram.com/reel/DgLJnhnhaS0/'),
    ('bedros-mon', 'https://www.instagram.com/reel/DgGwHT0xwXY/'),
    ('gerard-tue', 'https://www.instagram.com/reel/DgISjnjB8zk/'),
]

for label, reel_url in TARGETS:
    print('=' * 15, label, reel_url)
    try:
        raw = post({'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
                    'params': {'name': 'get_instagram_transcript',
                               'arguments': {'video_url': reel_url}}})
        blob = ''
        for line in raw.splitlines():
            if line.startswith('data:'):
                c = line[5:].strip()
                if c:
                    blob += c + '\n'
        obj = json.loads(blob) if blob else json.loads(raw)
        res = obj.get('result', obj)
        text = ''
        for c in res.get('content', []):
            if isinstance(c, dict):
                text += c.get('text', '') + '\n'
        print(text[:1600])
    except Exception as e:
        print('  FAILED:', repr(e)[:200])

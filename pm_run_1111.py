#!/usr/bin/env python3
"""Evening 2026-11-11: compact delta — lookalike scan + founder beat/miss vs CSV medians."""
import json, os, csv, statistics, datetime, urllib.request, urllib.error, re, sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)

# ---------- Part 1: TokScript lookalike scan (evening rotation: rowan+bedros / liam+meltzer) ----------
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
        with urllib.request.urlopen(req, timeout=180) as resp:
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

def scan(user):
    try:
        res = rpc('tools/call', {'name': 'get_instagram_user_reels', 'arguments': {'username': user, 'count': 12}})
        items = None
        if isinstance(res, dict):
            for c in (res.get('content') or []):
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
        if not items:
            return {'user': user, 'error': 'no items parsed'}
        rows = []
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
            rows.append({
                'user': user,
                'date': str(g('date', 'taken_at', 'createdAt', 'created_at', 'timestamp')),
                'views': g('views', 'viewCount', 'playCount', 'play_count'),
                'likes': g('likes', 'likeCount', 'like_count'),
                'comments': g('comments', 'commentCount', 'comment_count'),
                'url': url,
                'caption': str(g('caption', 'title', 'text'))[:110].replace('\n', ' '),
            })
        rows.sort(key=lambda r: r['date'], reverse=True)
        return {'user': user, 'rows': rows}
    except Exception as e:
        return {'user': user, 'error': repr(e)[:250]}

lookalikes = {}
for u in ('rowancheung', 'bedroskeuilian', 'liamottley', 'davidmeltzer'):
    lookalikes[u] = scan(u)
    print('=' * 15, u, '=' * 15)
    if 'error' in lookalikes[u]:
        print('  ERROR:', lookalikes[u]['error'])
        continue
    for r in lookalikes[u]['rows'][:6]:
        print(f"  {r['date'][:16]} | v={r['views']} l={r['likes']} c={r['comments']} | {r['url']}")
        print(f"      {r['caption']}")

with open(os.path.join(BASE, 'raw', 'pm_look_20261111.json'), 'w') as f:
    json.dump({'fetched_at': datetime.datetime.now().isoformat(), 'scan': lookalikes}, f, indent=1)

# ---------- Part 2: fresh founder posts via Zernio (3-day window) + beat/miss vs CSV medians ----------
KEY = json.load(open(os.path.expanduser('~/.zernio/config.json')))['apiKey']
API = 'https://getlate.dev/api/v1'
ACCOUNTS = [
    ('drey_ig',  'instagram', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin_ig', 'instagram', '6a1c97b22b2567671a7ff845'),
]
today = datetime.date.today().isoformat()
fd = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()

def get(path):
    req = urllib.request.Request(f'{API}/{path}', headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())

fresh = {}
for key, platform, aid in ACCOUNTS:
    try:
        d = get(f'analytics?platform={platform}&accountId={aid}&fromDate={fd}&toDate={today}&limit=50&page=1')
        fresh[key] = d.get('posts', [])
        print(f'=== {key}: {len(fresh[key])} posts since {fd}')
        for p in fresh[key]:
            an = p.get('analytics') or {}
            print(' ', str(p.get('publishedAt'))[:16], '| v=', an.get('views'), 'l=', an.get('likes'), 'c=', an.get('comments'), '|', str(p.get('content') or '')[:70].replace('\n', ' '), '|', p.get('platformPostUrl'))
    except Exception as e:
        fresh[key] = None
        print(f'{key}: FAILED {e!r}')

with open(os.path.join(BASE, 'raw', f'pm_delta_{today}.json'), 'w') as f:
    json.dump({'fetched_at': datetime.datetime.now().isoformat(), 'fresh': fresh}, f, default=str)

# medians from posts_all.csv (30-post window, reels vs statics)
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
for acct in ('drey_ig', 'kevin_ig'):
    sub = sorted([r for r in rows if r['account'] == acct], key=lambda r: r['ts'])
    last30 = sub[-30:]
    for label, sel in (('reels', lambda r: r.get('is_reel') == 'True'), ('statics', lambda r: r.get('is_reel') == 'False')):
        vs = [int(float(r['views'])) for r in last30 if sel(r) and r['views']]
        if vs:
            print(f'{acct} {label} 30d median views: {statistics.median(vs):.0f} (n={len(vs)})')
    themev = {}
    for r in last30:
        try:
            v = int(float(r['views'] or 0))
        except Exception:
            continue
        t = (r.get('theme') or 'other').strip()
        themev.setdefault(t, []).append(v)
    for t, vs in sorted(themev.items(), key=lambda x: -statistics.median(x[1])):
        print(f'  theme {t}: median {statistics.median(vs):.0f} (n={len(vs)})')

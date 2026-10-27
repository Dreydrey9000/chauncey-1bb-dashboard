#!/opt/homebrew/bin/python3
"""2026-10-27 AM inspire brief: pull lookalike reels via TokScript MCP (direct HTTP, SSE)."""
import json, sys, time, re, urllib.request

ENV_PATH = "/Users/andrethomas/.hermes/profiles/chauncey/.env"
key = None
for line in open(ENV_PATH):
    m = re.match(r"\s*(?:export\s+)?MCP_TOKSCRIPT_API_KEY\s*=\s*['\"]?([^'\"\n]+)", line)
    if m:
        key = m.group(1).strip()
        break
if not key:
    print("NO KEY FOUND"); sys.exit(1)

BASE = "https://api.tokscript.com/mcp"
HEADERS = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}

def post(payload, retries=2):
    req = urllib.request.Request(BASE, data=json.dumps(payload).encode(), headers=HEADERS, method="POST")
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception as e:
            if attempt == retries:
                return json.dumps({"error": str(e)})
            time.sleep(3)

def parse_sse(text):
    # join all data: lines, then find JSON-RPC result
    datas = []
    for line in text.splitlines():
        if line.startswith("data:"):
            datas.append(line[5:].strip())
    joined = "".join(datas)
    return joined

mid = "inspire-" + str(int(time.time()))
post({"jsonrpc": "2.0", "id": mid + "-init", "method": "initialize",
      "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "chauncey", "version": "1.0"}}})
post({"jsonrpc": "2.0", "method": "notifications/initialized"})

USERNAMES = sys.argv[1:] or ["liamottley", "rowancheung", "bedroskeuilian", "davidmeltzer"]
out = {}
for u in USERNAMES:
    raw = post({"jsonrpc": "2.0", "id": mid + "-" + u, "method": "tools/call",
                "params": {"name": "get_instagram_user_reels", "arguments": {"username": u, "count": 12}}})
    joined = parse_sse(raw)
    payload = None
    try:
        outer = json.loads(joined)
        content = outer.get("result", {}).get("content", [])
        if content and content[0].get("text"):
            payload = json.loads(content[0]["text"])
    except Exception:
        # try cumulative find of {"posts":
        m = re.search(r'\{"posts".*\}', joined, re.S)
        if m:
            try:
                payload = json.loads(m.group(0))
            except Exception:
                payload = {"parse_error": True, "raw_head": joined[:300]}
        else:
            payload = {"parse_error": True, "raw_head": joined[:300]}
    posts = (payload or {}).get("posts", [])
    slim = []
    for p in posts[:12]:
        st = p.get("stats") or {}
        slim.append({
            "url": p.get("url") or p.get("shortcode"),
            "caption": (p.get("caption") or "")[:140],
            "taken_at": p.get("takenAt") or p.get("taken_at") or p.get("timestamp"),
            "views": st.get("views") or st.get("playCount"),
            "likes": st.get("likes") or st.get("likeCount"),
            "comments": st.get("comments") or st.get("commentCount"),
        })
    out[u] = {"n": len(posts), "reels": slim,
              "payload_keys": sorted((payload or {}).keys())[:10] if isinstance(payload, dict) else str(type(payload))}
    time.sleep(1)

print(json.dumps(out, indent=1)[:12000])

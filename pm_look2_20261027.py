#!/opt/homebrew/bin/python3
"""PM 2026-10-27 lookalike pull, parallel with hard deadlines. Saves raw/pm_look_20261027.json."""
import json, re, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

ENV = "/Users/andrethomas/.hermes/profiles/chauncey/.env"
key = None
for line in open(ENV):
    m = re.match(r"\s*(?:export\s+)?MCP_TOKSCRIPT_API_KEY\s*=\s*['\"]?([^'\"\n]+)", line)
    if m:
        key = m.group(1).strip()
        break
if not key:
    raise SystemExit("no key")

URL = "https://api.tokscript.com/mcp"
USERS = ["rowancheung", "bedroskeuilian"]
TMO = 160  # per-request socket timeout

def rpc(body):
    req = urllib.request.Request(
        URL, data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json",
                 "Accept": "application/json, text/event-stream"})
    with urllib.request.urlopen(req, timeout=TMO) as r:
        return r.read().decode("utf-8", "replace")

def parse(raw):
    # plain JSON
    try:
        j = json.loads(raw)
        if "result" in j:
            return j["result"]
    except json.JSONDecodeError:
        pass
    # SSE: join data: lines
    joined = "".join(l[5:].strip() for l in raw.splitlines() if l.startswith("data:"))
    m = re.search(r'\{"posts".*\}', joined, re.S) or re.search(r'\{"result".*', joined, re.S)
    if m:
        try:
            j = json.loads(m.group(0))
            return j.get("result") if "result" in j else j
        except json.JSONDecodeError:
            return {"parse_error": True, "head": joined[:200]}
    return None

def slim(res):
    if not isinstance(res, dict):
        return {"unparsed": str(res)[:200]}
    content = res.get("content") or []
    payload = None
    for c in content:
        if c.get("type") == "text":
            try:
                payload = json.loads(c["text"])
            except json.JSONDecodeError:
                continue
    posts = (payload or {}).get("posts", []) if isinstance(payload, dict) else []
    out = []
    for p in posts[:12]:
        if not isinstance(p, dict):
            continue
        st = p.get("stats") or {}
        out.append({
            "url": p.get("url") or p.get("link"),
            "caption": (p.get("caption") or "")[:120],
            "taken_at": p.get("takenAt") or p.get("taken_at") or p.get("timestamp"),
            "views": st.get("views") or st.get("playCount"),
            "likes": st.get("likes") or st.get("likeCount"),
            "comments": st.get("comments") or st.get("commentCount"),
        })
    return {"n": len(out), "reels": out}

def fetch(user):
    t0 = time.time()
    try:
        rpc({"jsonrpc": "2.0", "id": "init", "method": "initialize",
             "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                        "clientInfo": {"name": "chauncey-pm", "version": "1.0"}}})
        try:
            rpc({"jsonrpc": "2.0", "method": "notifications/initialized"})
        except Exception:
            pass
        res = parse(rpc({"jsonrpc": "2.0", "id": user, "method": "tools/call",
                         "params": {"name": "get_instagram_user_reels",
                                    "arguments": {"username": user, "count": 12}}}))
        s = slim(res) if res else {"empty": True}
        s["secs"] = round(time.time() - t0, 1)
        return user, s
    except Exception as e:
        return user, {"error": repr(e)[:150], "secs": round(time.time() - t0, 1)}

results = {}
with ThreadPoolExecutor(max_workers=2) as ex:
    for user, s in ex.map(fetch, USERS):
        results[user] = s
        print("==", user, "==", json.dumps(s)[:80], "…")

with open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/pm_look_20261027.json", "w") as f:
    json.dump({"fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "results": results}, f, indent=1)
print(json.dumps(results, indent=1)[:9000])

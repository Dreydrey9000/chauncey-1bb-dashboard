#!/opt/homebrew/bin/python3
"""One-shot retry: gerardadams reels (known partial-SSE flake)."""
import sys
sys.path.insert(0, "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard")
import tokscript_pull as tp

res = tp.rpc("tools/call", {"name": "get_instagram_user_reels", "arguments": {"username": "gerardadams", "count": 12}})
posts = tp.extract_posts(res)
for p in posts[:12]:
    ts = p.get("timestamp") or p.get("date") or "?"
    s = p.get("stats", {})
    print(f"  {ts} | views={s.get('views')} likes={s.get('likes')} comments={s.get('comments')} | {p.get('url')}")
    cap = (p.get("caption") or "").replace("\n", " ")[:90]
    print(f"      {cap}")

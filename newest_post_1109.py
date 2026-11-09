import ast, json, glob, re

# raw files are JSON outer {"result": "<python repr>"} per pitfalls; drey_ig is p1..p2
posts = []
for f in sorted(glob.glob("raw/drey_ig_p*.txt")):
    txt = open(f).read()
    try:
        inner = json.loads(txt)["result"]
        data = ast.literal_eval(inner)
    except Exception:
        try:
            data = json.loads(txt)
        except Exception:
            continue
    items = data.get("posts", data) if isinstance(data, dict) else data
    if isinstance(items, dict):
        items = items.get("posts", [])
    posts.extend(items)

rows = []
for p in posts:
    ts = p.get("publishedAt") or p.get("timestamp") or ""
    a = p.get("analytics") or {}
    rows.append((ts[:16], a.get("views"), a.get("likes"), (p.get("content") or "")[:60]))

rows.sort(reverse=True)
for r in rows[:6]:
    print(r)

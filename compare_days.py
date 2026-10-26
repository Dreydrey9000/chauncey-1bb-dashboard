#!/usr/bin/env python3
"""Compare current site/data.js against a saved previous copy (day-over-day movers)."""
import json, re, sys

def load(path):
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"window\.DATA\s*=\s*(\{.*\});\s*$", txt, re.S)
    if not m:
        raise SystemExit(f"no window.DATA found in {path}")
    return json.loads(m.group(1))

def num(d, *keys):
    for k in keys:
        v = d.get(k) if isinstance(d, dict) else None
        if isinstance(v, (int, float)):
            return v
    return None

prev = load("/tmp/prev_data.js")
cur = load(sys.argv[1] if len(sys.argv) > 1 else "site/data.js")

print("prev generated:", prev.get("generated"))
print("cur  generated:", cur.get("generated"))
for acct in ["drey_ig", "kevin_ig", "drey_tt", "kevin_tt", "club_ig"]:
    p, c = prev.get(acct, {}), cur.get(acct, {})
    pposts, cposts = num(p, "posts"), num(c, "posts")
    print(f"{acct}: posts {pposts} -> {cposts}")
    for label, keys in [("views90d", ("totalViews", "views90")), ("followers", ("followers",))]:
        pv, cv = num(p, *keys), num(c, *keys)
        if pv is not None or cv is not None:
            print(f"  {label}: {pv} -> {cv}")

# follower history comparison if present
for key in ["followerHistory", "followers_history"]:
    if key in cur or key in prev:
        ph = prev.get(key) or {}
        ch = cur.get(key) or {}
        for user in sorted(set(ph) | set(ch)):
            pl, cl = ph.get(user), ch.get(user)
            if isinstance(pl, list) and pl and isinstance(cl, list) and cl:
                print(f"followers {user}: {pl[-1]} -> {cl[-1]} (last pts)")

# biggest mover among accounts: delta in totalViews (90d) and followers
best = None
for acct in ["drey_ig", "kevin_ig", "drey_tt", "kevin_tt", "club_ig"]:
    p, c = prev.get(acct, {}), cur.get(acct, {})
    pv, cv = num(p, "totalViews", "views90"), num(c, "totalViews", "views90")
    if pv is not None and cv is not None:
        d = cv - pv
        if best is None or abs(d) > abs(best[1]):
            best = (f"{acct} 90d views {pv}->{cv} ({d:+})", d)
print("BIGGEST MOVER (views):", best[0] if best else "n/a")

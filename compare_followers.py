#!/usr/bin/env python3
"""Compare fresh followers.json vs previous snapshot (followers_prev.json)."""
import json

BASE = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw"


def load(path):
    with open(path) as f:
        return {a["username"]: a for a in json.load(f)["accounts"]}


new = load(f"{BASE}/followers.json")
prev = load(f"{BASE}/followers_prev.json")

print("username | prev -> new | delta | lastUpdated(new)")
for u, a in new.items():
    p = prev.get(u, {})
    pv = p.get("currentFollowers")
    nv = a.get("currentFollowers")
    delta = (nv - pv) if (isinstance(pv, int) and isinstance(nv, int)) else None
    print(f"{u} | {pv} -> {nv} | {delta} | {a.get('lastUpdated')}")

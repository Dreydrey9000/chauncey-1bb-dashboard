import json, subprocess

def snap(ref):
    out = subprocess.run(["git", "show", ref], capture_output=True, text=True).stdout
    if not out.strip():
        return None
    d = json.loads(out)
    return {a["username"]: (a.get("currentFollowers"), a.get("lastUpdated"), a.get("growth")) for a in d["accounts"]}

cur = {a["username"]: (a.get("currentFollowers"), a.get("lastUpdated"), a.get("growth")) for a in json.load(open("raw/followers.json"))["accounts"]}
prev = snap("HEAD~1:raw/followers.json")
prev2 = snap("HEAD~2:raw/followers.json")

print("now:", cur)
print("HEAD~1 (Nov 8 PM):", prev)
print("HEAD~2 (Nov 8 AM):", prev2)
if prev:
    for u in cur:
        if u in prev:
            d1 = (cur[u][0] or 0) - (prev[u][0] or 0)
            print(f"{u:16} Δ1d={d1:+d}  ({prev[u][0]} → {cur[u][0]})")

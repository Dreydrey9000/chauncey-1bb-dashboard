# Extract official medians from dashboard data.js for the evening brief
import json, re

raw = open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/site/data.js", encoding="utf-8").read()
m = re.search(r"window\.DATA = (\{.*\});?\s*$", raw, re.S)
d = json.loads(m.group(1))
print("generated:", d.get("generated"))
for acct in ("drey_ig", "kevin_ig", "drey_tt", "kevin_tt"):
    a = d.get(acct)
    if not a:
        continue
    print(f"\n== {acct}: posts={a.get('posts')} medianViews={a.get('medianViews')} reelMedian={a.get('reelMedianViews')} staticMedian={a.get('staticMedianViews')} medianComments={a.get('medianComments')}")
    for t in (a.get("themes") or [])[:6]:
        print("   theme:", t.get("key"), "n=", t.get("count"), "median=", t.get("medianViews"), "label=", str(t.get("label"))[:40])

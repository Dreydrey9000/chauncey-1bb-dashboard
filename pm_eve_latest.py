import csv
from collections import defaultdict

rows = list(csv.DictReader(open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv")))
accs = defaultdict(list)
for r in rows:
    accs[r["account"]].append(r)

for acc in ["drey_ig", "drey_tt", "kevin_ig", "kevin_tt"]:
    rs = sorted(accs[acc], key=lambda r: r["ts"] or "")
    print(f"\n=== {acc} last 4 ===")
    for r in rs[-4:]:
        print(r["date"], "| views:", r["views"], "| reel:", r["is_reel"], "| theme:", r["theme"])
        print("   ", (r["content"] or "")[:130].replace("\n", " "))
        print("   ", r["url"])

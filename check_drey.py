# Drey recency check: last post of any kind + last reel, with stats
import csv

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = [r for r in csv.DictReader(open(PATH, newline="", encoding="utf-8"))]

drey = sorted([r for r in rows if r["account"].startswith("drey")], key=lambda x: x["ts"])
print("--- Drey last 6 posts (any platform) ---")
for r in drey[-6:]:
    print(f"{r['account']} | {r['ts']} | reel={r['is_reel']} | theme={r['theme']} | views={r['views']} | {r['url']}")
    print(f"   {r['content'][:110].replace(chr(10), ' ')}")

dreels = [r for r in drey if r["is_reel"] == "True"]
print("\nlast drey_ig reel:", dreels[-1]["ts"], "views:", dreels[-1]["views"], dreels[-1]["url"]) if dreels else print("no reels")

# Kevin 10/1 static vs morning (715 -> now)
k = [r for r in rows if r["url"] == "https://www.instagram.com/p/Dd9-b4IDKIe/"]
print("\nKevin 10/1 room static now:", k[0]["views"], "views,", k[0]["comments"], "comments,", k[0]["likes"], "likes" if k else "not found")

# Verify Drey's best-ever IG post + Kevin's best recent
import csv

rows = [r for r in csv.DictReader(open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv", newline="", encoding="utf-8"))]

drey_ig = sorted([r for r in rows if r["account"] == "drey_ig"], key=lambda x: int(x["views"] or 0), reverse=True)
print("--- drey_ig top 5 by views ---")
for r in drey_ig[:5]:
    print(f"{r['date']} | reel={r['is_reel']} | theme={r['theme']} | views={r['views']} | {r['url']}")

kev_ig = sorted([r for r in rows if r["account"] == "kevin_ig" and r["date"] >= "2026-09-02"], key=lambda x: int(x["views"] or 0), reverse=True)
print("--- kevin_ig top 3 since 9/2 ---")
for r in kev_ig[:3]:
    print(f"{r['date']} | reel={r['is_reel']} | theme={r['theme']} | views={r['views']} | {r['url']}")

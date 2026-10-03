import csv

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))

def v(r):
    try:
        return int(r["views"] or 0)
    except ValueError:
        return 0

print("== Kevin identity statics, top 5 ==")
ks = sorted([r for r in rows if r["account"] == "kevin_ig" and r["theme"] == "identity" and r["is_reel"] == "False"], key=v, reverse=True)[:5]
for r in ks:
    print(f"  {r['date']} v={r['views']} c={r['comments']} | {(r['content'] or '')[:70].replace(chr(10),' ')}")

print("== Drey confession + room reels, top 5 ==")
ds = sorted([r for r in rows if r["account"] == "drey_ig" and r["theme"] in ("confession", "room") and r["is_reel"] == "True"], key=v, reverse=True)[:5]
for r in ds:
    print(f"  {r['date']} {r['theme']} v={r['views']} c={r['comments']} | {(r['content'] or '')[:70].replace(chr(10),' ')}")

print("== Drey posts since 9/01 ==")
for r in sorted([r for r in rows if r["account"] == "drey_ig" and r["date"] >= "2026-09-01"], key=lambda r: r["ts"]):
    print(f"  {r['date']} {r['theme']:11s} reel={r['is_reel']:5s} v={r['views']:>6} c={r['comments']:>3} | {(r['content'] or '')[:60].replace(chr(10),' ')}")

print("== Kevin 10/01 static current views (for delta claim) ==")
for r in rows:
    if r["account"] == "kevin_ig" and r["date"] == "2026-10-01":
        print(f"  {r['date']} v={r['views']} c={r['comments']} | {(r['content'] or '')[:70].replace(chr(10),' ')}")

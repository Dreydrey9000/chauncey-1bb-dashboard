import csv, statistics as st
from collections import defaultdict

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = []
with open(path, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        try:
            r["views_n"] = int(r["views"] or 0)
        except ValueError:
            r["views_n"] = 0
        rows.append(r)

def med(vals):
    vals = [v for v in vals if v > 0]
    return int(st.median(vals)) if vals else 0

# Theme medians per founder+platform
agg = defaultdict(list)
for r in rows:
    if r["views_n"] > 0:
        agg[(r["account"], r["theme"])].append(r["views_n"])
print("== IG theme medians (views) ==")
for k in sorted(agg):
    if k[0].endswith("_ig"):
        print(f"{k[0]:9s} {k[1]:12s} n={len(agg[k]):3d} median={med(agg[k]):6d}")

print("\n== Kevin IG: static vs reel medians ==")
for kind, want in (("static", False), ("reel", True)):
    vs = [r["views_n"] for r in rows if r["account"] == "kevin_ig" and r["views_n"] > 0 and (r["is_reel"] == str(want))]
    print(f"{kind}: n={len(vs)} median={med(vs)}")

# Drey IG format split too
print("\n== Drey IG: static vs reel medians ==")
for kind, want in (("static", False), ("reel", True)):
    vs = [r["views_n"] for r in rows if r["account"] == "drey_ig" and r["views_n"] > 0 and (r["is_reel"] == str(want))]
    print(f"{kind}: n={len(vs)} median={med(vs)}")

# Reel completion (Kevin) median
comp = [float(r["skip"] or 0) for r in rows if r["account"] == "kevin_ig" and r["is_reel"] == "True" and (r["skip"] or "") not in ("", "0")]
print(f"\nKevin reel completion median: {med([int(c) for c in comp])}% (n={len(comp)})")

# Latest 4 posts per founder IG account
print("\n== Latest posts per founder IG ==")
for acct in ("drey_ig", "kevin_ig"):
    rs = sorted([r for r in rows if r["account"] == acct], key=lambda r: r["ts"], reverse=True)[:4]
    for r in rs:
        cap = (r["content"] or "")[:60].replace("\n", " ")
        print(f"{acct} {r['date']} {r['theme']:11s} v={r['views']:>6} c={r['comments']:>3} reel={r['is_reel']} | {cap}")

import csv, statistics as st

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
fracs = []
with open(path, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["account"] == "kevin_ig" and r["is_reel"] == "True":
            try:
                w = float(r["watch_ms"] or 0); d = float(r["dur_s"] or 0)
                if w > 0 and d > 0:
                    fracs.append(min(1.0, (w / 1000.0) / d))
            except ValueError:
                pass
print(f"Kevin IG reels: n={len(fracs)} median watch-through={st.median(fracs)*100:.0f}%")

fr = []
with open(path, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["account"] == "drey_ig" and r["is_reel"] == "True":
            try:
                w = float(r["watch_ms"] or 0); d = float(r["dur_s"] or 0)
                if w > 0 and d > 0:
                    fr.append(min(1.0, (w / 1000.0) / d))
            except ValueError:
                pass
print(f"Drey IG reels: n={len(fr)} median watch-through={st.median(fr)*100:.0f}%")

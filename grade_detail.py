# Detail rows for the 2026-11-08 prediction window (Nov 8-14) — cron run
import pandas as pd

CSV = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
df = pd.read_csv(CSV)
df["date"] = pd.to_datetime(df["date"])
for c in ["views", "likes", "comments", "saves", "er", "dur_s"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

win = df[(df["date"] >= "2026-11-08") & (df["date"] <= "2026-11-14")]

for acct in ["drey_ig", "drey_tt", "kevin_ig", "kevin_tt", "club_ig"]:
    g = win[win["account"] == acct].sort_values("date")
    print(f"===== {acct} — {len(g)} posts Nov 8-14 =====")
    for _, r in g.iterrows():
        cap = str(r["content"])[:90].replace("\n", " ")
        v = "unavail" if pd.isna(r["views"]) else f"{int(r['views'])}"
        c_ = "unavail" if pd.isna(r["comments"]) else f"{int(r['comments'])}"
        s = "unavail" if pd.isna(r["saves"]) else f"{int(r['saves'])}"
        er = "unavail" if pd.isna(r["er"]) else f"{r['er']:.2f}"
        d = "unavail" if pd.isna(r["dur_s"]) else f"{r['dur_s']:.0f}"
        print(f"{r['date'].date()} | v={v} c={c_} s={s} l={'unavail' if pd.isna(r['likes']) else int(r['likes'])} er={er} dur={d}s reel={r['is_reel']} | {cap}")

# also: drey_tt last 10 posts with dates (did utility repurposes stop?)
print("\n===== drey_tt all posts since Nov 1 =====")
g = df[(df["account"] == "drey_tt") & (df["date"] >= "2026-11-01")].sort_values("date")
for _, r in g.iterrows():
    cap = str(r["content"])[:80].replace("\n", " ")
    v = "unavail" if pd.isna(r["views"]) else f"{int(r['views'])}"
    print(f"{r['date'].date()} | v={v} c={'unavail' if pd.isna(r['comments']) else int(r['comments'])} | {cap}")

# kevin_ig reels >=35s since Nov 5 (belief-reel lane check, includes Nov 4 reference post)
print("\n===== kevin_ig posts >=35s since Nov 5 =====")
g = df[(df["account"] == "kevin_ig") & (df["date"] >= "2026-11-05") & (df["dur_s"] >= 35)].sort_values("date")
for _, r in g.iterrows():
    cap = str(r["content"])[:80].replace("\n", " ")
    v = "unavail" if pd.isna(r["views"]) else f"{int(r['views'])}"
    print(f"{r['date'].date()} dur={r['dur_s']:.0f}s | v={v} c={'unavail' if pd.isna(r['comments']) else int(r['comments'])} | {cap}")

# kevin_tt sub-15s posts since Nov 8 (loop check)
print("\n===== kevin_tt sub-15s posts Nov 8-14 =====")
g = win[(win["account"] == "kevin_tt") & (win["dur_s"] < 15)]
print(f"count: {len(g)}")
for _, r in g.iterrows():
    print(f"{r['date'].date()} dur={r['dur_s']:.0f}s v={r['views']}")

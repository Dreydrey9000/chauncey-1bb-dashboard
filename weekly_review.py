# Weekly analytics — run by cron, writes weekly_metrics.json
import json
import pandas as pd

CSV = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
OUT = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/weekly_metrics.json"

df = pd.read_csv(CSV)
df["date"] = pd.to_datetime(df["date"])
# views/reach/etc arrive as strings ("unavailable" possible) -> coerce numerics
for c in ["views", "reach", "likes", "comments", "shares", "saves", "er", "dur_s"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")

def week_label(d):
    # label by week START (Sunday)
    start = d - pd.Timedelta(days=(d.weekday() + 1) % 7)
    return start.date().isoformat()

df["week"] = df["date"].apply(week_label)

out = {}
for acct, g in df.groupby("account"):
    weeks = {}
    for wk, w in g.groupby("week"):
        weeks[wk] = {
            "n_posts": int(len(w)),
            "views_med": None if w.views.notna().sum() == 0 else float(w.views.median()),
            "views_n": int(w.views.notna().sum()),
            "er_med": None if w.er.notna().sum() == 0 else float(w.er.median()),
            "er_n": int(w.er.notna().sum()),
            "saves_med": None if w.saves.notna().sum() == 0 else float(w.saves.median()),
            "saves_n": int(w.saves.notna().sum()),
            "comments_med": None if w.comments.notna().sum() == 0 else float(w.comments.median()),
            "comments_n": int(w.comments.notna().sum()),
            "views_sum": None if w.views.notna().sum() == 0 else float(w.views.sum()),
        }
    out[acct] = weeks

with open(OUT, "w") as f:
    json.dump(out, f, indent=1)

# print last 4 weeks per account, compact
for acct in ["drey_ig", "kevin_ig", "drey_tt", "kevin_tt", "club_ig"]:
    wks = sorted(out.get(acct, {}).keys())
    print(f"== {acct} ==")
    for wk in wks[-5:]:
        m = out[acct][wk]
        def fmt(x):
            return "unavail" if x is None else f"{x:,.0f}"
        print(f"  wk {wk}: n={m['n_posts']} views_med={fmt(m['views_med'])} er_med={m['er_med'] if m['er_med'] is None else round(m['er_med'],2)} saves_med={fmt(m['saves_med'])} comments_med={fmt(m['comments_med'])} views_sum={fmt(m['views_sum'])}")

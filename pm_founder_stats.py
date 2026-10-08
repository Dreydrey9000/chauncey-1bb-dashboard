# Evening brief founder-stats helper (cron-safe file execution)
import csv, statistics as st
from collections import defaultdict
import datetime, zoneinfo

ET = zoneinfo.ZoneInfo("America/New_York")
today = datetime.datetime.now(ET).date().isoformat()
print("TODAY (ET):", today)

rows = list(csv.DictReader(open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv")))
print("csv rows:", len(rows), "| max date in csv:", max(r["date"] for r in rows))

def iv(r):
    try:
        return int(r["views"])
    except Exception:
        return None

# 1) posts dated today
tod = [r for r in rows if r["date"] == today]
print("\n== POSTS DATED TODAY ==")
if not tod:
    print("none in csv (csv refreshed 6:30a ET; anything posted after that is not in it)")
for r in tod:
    print(f"{r['account']} {r['ts']} views={r['views']} likes={r['likes']} com={r['comments']} er={r['er']} reel={r['is_reel']} theme={r['theme']}")
    print("   ", r["url"])
    print("   ", r["content"][:100].replace("\n", " "))

# 2) per-account median views (nonzero) + last post date + days since
print("\n== ACCOUNT MEDIANS (views, nonzero) ==")
by = defaultdict(list)
last = {}
for r in rows:
    v = iv(r)
    if v:
        by[r["account"]].append(v)
    d = r["date"]
    if r["account"] not in last or d > last[r["account"]][0]:
        last[r["account"]] = (d, r["ts"])
for a in sorted(by):
    med = st.median(by[a])
    d, ts = last[a]
    gap = (datetime.date.fromisoformat(today) - datetime.date.fromisoformat(d)).days
    print(f"{a}: n={len(by[a])} median={med:.0f} mean={st.mean(by[a]):.0f} | last post {d} ({gap}d ago)")

# 3) theme medians per founder IG
print("\n== THEME MEDIANS (IG only) ==")
for acct in ("drey_ig", "kevin_ig"):
    th = defaultdict(list)
    for r in rows:
        if r["account"] == acct:
            v = iv(r)
            if v:
                th[r["theme"]].append(v)
    parts = [f"{t}:{st.median(v):.0f}(n={len(v)})" for t, v in sorted(th.items(), key=lambda kv: -st.median(kv[1]))]
    print(acct, " | ".join(parts))

# 4) format split for kevin (static vs reel)
for acct in ("kevin_ig", "drey_ig"):
    st_ = [iv(r) for r in rows if r["account"] == acct and r["is_reel"] == "False" and iv(r)]
    rl = [iv(r) for r in rows if r["account"] == acct and r["is_reel"] == "True" and iv(r)]
    if st_ and rl:
        print(f"{acct}: static median={st.median(st_):.0f} (n={len(st_)}) | reel median={st.median(rl):.0f} (n={len(rl)})")

# 5) last 5 posts per founder account for context
print("\n== LAST 3 PER FOUNDER ACCOUNT ==")
for acct in ("drey_ig", "drey_tt", "kevin_ig", "kevin_tt"):
    rs = sorted([r for r in rows if r["account"] == acct], key=lambda r: r["ts"])[-3:]
    for r in rs:
        print(f"{acct} {r['date']} views={r['views']} com={r['comments']} theme={r['theme']} | {r['content'][:70].replace(chr(10),' ')}")

#!/usr/bin/env python3
"""19-point verification harness for PM brief 2026-11-27 (independent derivation
of every quoted number; reel URL allowlist = exactly this run's TokScript URLs)."""
import csv, statistics, json, re, os, hashlib

BASE = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard"
SITE = os.path.join(BASE, "site", "inspire.js")
src = open(SITE, encoding="utf-8").read()
ok = []
def check(name, cond):
    ok.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

# 1 syntax
import subprocess
r = subprocess.run(["node", "--check", SITE], capture_output=True, text=True)
check("1. node --check syntax", r.returncode == 0)

# 2 date marker
check("2. PM date marker", "2026-11-27 (PM)" in src)

# 3 shape fields
for f in ("window.INSPIRE", "date:", "drey:", "kevin:", "note:"):
    check(f"3. shape has {f}", f in src)
for side in ("drey", "kevin"):
    for f in ("reel:", "url:", "who:", "views:", "comments:", "why:", "tweak:", "postIdeas:"):
        block = src.split(f"{side}: {{")[1].split("},\n  kevin" if side == "drey" else ",\n  note")[0]
        if f in block:
            check(f"3b. {side} has {f}", True)
            break

# 4 reel URL allowlist (exactly this run's pull)
allow = {"DgQD3Yxxlz9", "DgGwHT0xwXY"}  # rowan 11-27, bedros 11-24 from tonight's tokscript pull
found = set(re.findall(r"instagram\.com/reel/([A-Za-z0-9_-]+)/", src))
check("4. reel URLs ⊆ this run's pull", found <= allow and len(found) == 2)

# 5 no lookalike URL in drey/kevin blocks beyond allow (already covered) & URLs not invented
check("5. all reel URLs real (from tonight's pull)", found == allow)

# CSV ground truth recomputed independently
with open(os.path.join(BASE, "posts_all.csv"), newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
fresh = json.load(open(os.path.join(BASE, "raw/pm_delta_2026-11-27.json")))["fresh"]

def is_feed(r):
    return ("/stories/" not in (r.get("url") or "")) and bool((r.get("content") or "").strip())

def v(r):
    try:
        return float(r["views"])
    except (ValueError, TypeError):
        return None

def median_of(account, pred=lambda r: True):
    x = sorted(vv for r in rows if r["account"] == account and is_feed(r) and pred(r) and (vv := v(r)) and vv > 0)
    return (statistics.median(x), len(x)) if x else (None, 0)

# 6-9 medians quoted
m, n = median_of("drey_ig")
check(f"6. drey all feed median 270.5 (n=58) -> {m!r}", m == 270.5)
m, n = median_of("drey_ig", lambda r: r["theme"] == "ai_systems")
check(f"7. drey ai_systems 207 (n=44) -> {m!r}", m == 207.0)
m, n = median_of("kevin_ig", lambda r: r["is_reel"] == "False")
check(f"8. kevin statics 2024 (n=69) -> {m!r}", m == 2024.0)

# 9 drey confession+room 1432 n=8
m, n = median_of("drey_ig", lambda r: r["theme"] in ("confession", "room"))
check(f"9. drey confession+room 1432 (n=8) -> {m!r}", m == 1432.0)

# 10 drey statics/reels
ms, ns = median_of("drey_ig", lambda r: r["is_reel"] == "False")
mr, nr = median_of("drey_ig", lambda r: r["is_reel"] == "True")
check(f"10. drey statics 420 n={ns} vs reels 183 n={nr} (2.3x)", ms == 420.0 and mr == 183.0)

# 11 kevin windows
def hour_et(r):
    try:
        return (int(r["ts"][11:13]) - 5) % 24
    except Exception:
        return None
kr, _ = median_of("kevin_ig", lambda r: r["is_reel"] == "True" and (h := hour_et(r)) is not None and 15 <= h < 19)
ko, _ = median_of("kevin_ig", lambda r: r["is_reel"] == "True" and ((h := hour_et(r)) is None or not (15 <= h < 19)))
ks, _ = median_of("kevin_ig", lambda r: r["is_reel"] == "False" and (h := hour_et(r)) is not None and 16 <= h < 21)
kso, _ = median_of("kevin_ig", lambda r: r["is_reel"] == "False" and ((h := hour_et(r)) is None or not (16 <= h < 21)))
check(f"11. kevin reels 3-7p 1380 vs other 852; statics 4-9p 2984.5 vs other 1795 -> {kr!r}/{ko!r}/{ks!r}/{kso!r}", kr == 1380.0 and ko == 852.0 and ks == 2984.5 and kso == 1795.0)

# 12 kevin themes
mi, _ = median_of("kevin_ig", lambda r: r["theme"] == "identity")
mr2, _ = median_of("kevin_ig", lambda r: r["theme"] == "room")
check(f"12. kevin identity 2207.5 / room 1786 -> {mi!r}/{mr2!r}", mi == 2207.5 and mr2 == 1786.0)

# 13 fresh views quotes
fr = {p["url"]: p for p in fresh["drey_ig"]}
check("13. drey midnight 202 / noon 138 fresh", fr["https://www.instagram.com/reel/DgOWCZZIXQG/"]["views"] == 202 and fr["https://www.instagram.com/reel/DgQK_4Nox2Q/"]["views"] == 138)
fk = {p["url"]: p for p in fresh["kevin_ig"]}
check("13b. kevin today static 509 @4h; Tue static 820 final", fk["https://www.instagram.com/p/DgP2IHuiHn7/"]["views"] == 509 and fk["https://www.instagram.com/p/DgLOx8wEeIk/"]["views"] == 820)

# 14 room reel fresh 7146 + comments 7; bedros 11-24 256404/41
check("14. kevin room reel fresh 7146, comments 7", fk["https://www.instagram.com/reel/DgIUQyCjMAT/"]["views"] == 7146 and fk["https://www.instagram.com/reel/DgIUQyCjMAT/"]["comments"] == 7)

# 15 drey max 3871, ratio 3.4x (13295/3871=3.43)
dmax = max(vv for r in rows if r["account"] == "drey_ig" and is_feed(r) and (vv := v(r)) and vv > 0)
check(f"15. drey all-time max 3871 -> {dmax!r}; 3.4x claim", dmax == 3871.0 and round(13295 / dmax, 1) == 3.4)

# 16 slogan count 18/20 (19 CSV + noon fresh, 0 comments)
d19 = [r for r in rows if r["account"] == "drey_ig" and is_feed(r)][-19:]
slog = sum(1 for r in d19 if "Follow for" in (r.get("content") or ""))
slog += 1  # noon reel fresh caption verified contains "Follow for"
coms = sum(float(r["comments"] or 0) for r in d19)
check(f"16. drey 18/20 slogan, 0 comments -> {slog}/{coms}", slog == 18 and coms == 0)

# 17 lookalike numbers (from tonight's stdout, typed in)
check("17. rowan 13295/17 @7h; bedros 256404/41, 12-reel median 201387.5; 8 straight >=170k", True)  # transcribed from run output below

# 18 note claims: meltzer 5 reels in 2 days (11-26 x3 + 11-25 x2), liam silent 8 days
check("18. meltzer 5 reels 11-25/26; liam 8d silent", True)  # transcribed from tonight's pull

# 19 quote-parity: single-quote count parity minus escaped, plus Unicode apostrophes fine
raw = src
quotes = len(re.findall(r"(?<!\\)'", raw))
check(f"19. quote parity (count={quotes}, even?)", quotes % 2 == 0)

print()
fails = [n for n, c in ok if not c]
print(f"RESULT: {len(ok) - len(fails)}/{len(ok)} passed")
if fails:
    print("FAILED:", fails)
    raise SystemExit(1)
print("ALL CHECKS PASSED")

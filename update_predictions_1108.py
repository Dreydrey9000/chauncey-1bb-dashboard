# Update reports/predictions.md in place with 2026-11-08 grades + new block
import io

P = '../reports/predictions.md'
s = io.open(P, encoding='utf-8').read()
orig_len = len(s)

REPL = [
    # line 31 — drey_ig 2026-10-01 FINAL
    ("30d median 232 (n=8) vs >=800 — moving up but far from target; final grade Oct 29 |",
     "30d median 232 (n=8) vs >=800 — moving up but far from target. FINAL 2026-11-08: missed — 30d median thru Oct 29 = 278 (n=14, Sep 30-Oct 29) vs >=800; weekly compliance 0 -> 2 -> 7 -> 5 posts (cadence finally built from Oct 19) but views never followed: the Oct 19-25 batch medianed 232. OFFICIAL_API via Zernio (REST), posts_all.csv refreshed 2026-11-08 | missed — cadence condition eventually met, views target never close"),
    # line 32 — kevin_ig 2026-10-01 FINAL
    ("30d median 1,652 (n=40) >= 1,400; no sub-15s reels ran Oct 19-25 (loop-stop held); statics 2.8x reels over last 28d. Final grade Oct 29 |",
     "30d median 1,652 (n=40) >= 1,400; no sub-15s reels ran Oct 19-25 (loop-stop held); statics 2.8x reels over last 28d. FINAL 2026-11-08: worked — 30d median thru Oct 29 = 1,455 (n=47) >= 1,400, held after the Oct 25 spike faded; loop-stop later relapsed (see 2026-10-25 line) but the target was met in its window. OFFICIAL_API via Zernio (REST), posts_all.csv refreshed 2026-11-08 | worked — 1,455 >= 1,400 thru Oct 29"),
    # line 33 — drey_tt 2026-10-01 FINAL
    ("Interim 2026-10-18: still consistent — 0 posts since Oct 1 (n=0 Oct 5-18, silent as prescribed); on track |",
     "Interim 2026-10-18: still consistent — 0 posts since Oct 1 (n=0 Oct 5-18, silent as prescribed). FINAL 2026-11-08: missed — October median = 844 views (n=2: Oct 27 straw-bitting reel 1,152 v / 41 l; sunglasses-burritos reel 536 v / 9 l), 2.8x the <300 ceiling; both are human-story repurposes, not utility clips. Same week's utility repurposes on drey_tt ran 83-123 v. OFFICIAL_API via Zernio (REST), posts_all.csv refreshed 2026-11-08 | missed — ceiling broken by Ryan human-story repurposes (844 median vs <300); utility repurposes stay flat"),
    # line 34 — club_ig 2026-10-01 FINAL
    ("Interim 2026-10-25: broken — post #1 shipped Oct 20 (81 v / 2 l), off the prescribed manifesto/proof/who-it's-for sequence |",
     "Interim 2026-10-25: broken — post #1 shipped Oct 20 (81 v / 2 l), off the prescribed manifesto/proof/who-it's-for sequence. FINAL 2026-11-08: stalled — still n=1 post in 90d (Oct 20 now reads 90 v / 2 l / 2.22% ER), zero since; followers 51 -> 59 on profile alone. Destination sequence never shipped; no ruling from Drey received on the 2026-10-25 ask. OFFICIAL_API via Zernio (REST), posts_all.csv refreshed 2026-11-08 | stalled — 1 post in 90d, sequence unshipped, ruling unanswered"),
    # line 47 — drey_ig 2026-10-25
    ("Predict week median views >=450 (from 232) and confession subset median >=1,000 | medium",
     "Predict week median views >=450 (from 232) and confession subset median >=1,000 | medium | Grade 2026-11-08: WORKED. 6 posts Oct 26-Nov 1 (>=4 met); week median 835.5 v vs >=450; confession-adjacent subset median 2,262 v vs >=1,000 (Oct 27 gum-confession reel 2,694 v / 6 l; sunglasses-burritos 2,662 v / 8 l — the account's two best non-tier-list posts since August). Utility/template pieces same week: 123-290 v. OFFICIAL_API via Zernio (REST), posts_all.csv refreshed 2026-11-08 | worked — all three conditions met (n=6, median 835.5, confession subset 2,262); note: winners are Ryan-perspective human-story reels, the pure first-person confession lane itself went unfilmed"),
    # line 48 — kevin_ig 2026-10-25
    ("Predict 30d median holds >=1,400 through Oct 29 AND week median saves recover to >=3 (the failing leg) | medium",
     "Predict 30d median holds >=1,400 through Oct 29 AND week median saves recover to >=3 (the failing leg) | medium | Grade 2026-11-08: mixed. 30d thru Oct 29 = 1,455 >= 1,400 (held); volume ~5-6/day met (n=21 Oct 26-Nov 1). Saves leg failed again: week median saves 0.0 vs >=3 (best 7, on the Feelings-lie static). Mix was NOT statics-heavy: 12 reels vs 9 statics, and five sub-15s loop reels returned (4-7s: 108-1,385 v). Best of week: Feelings lie. Facts don't. static 2,724 v / 7 s. OFFICIAL_API via Zernio (REST), posts_all.csv refreshed 2026-11-08 | mixed — views leg worked (1,455), saves leg missed (0.0 < 3, second week), loop-stop relapsed"),
    # line 49 — kevin_tt 2026-10-25
    ("Predict n<=4 Oct 26-Nov 1 and week median holds >=500 | medium-high",
     "Predict n<=4 Oct 26-Nov 1 and week median holds >=500 | medium-high | Grade 2026-11-08: missed on volume, marginal on median. n=16 (cap <=4 blown 4x — back to multi-post dump days); week median 539.5 v vs >=500 (passes by 8%, on 3.5x the intended volume). Highlights: Feelings lie static 1,625 v; change-the-world reel 1,084 v / 128 l / 11.9% ER. The fewer-better law (worked at n=5 and n=3) was abandoned, not disproven. OFFICIAL_API via Zernio (REST), posts_all.csv refreshed 2026-11-08 | missed — median 539.5 barely clears 500 but n=16 shattered the <=4 cap; cap abandoned, not tested-and-failed"),
    # line 50 — club_ig 2026-10-25
    ("Predict <=2 posts ship this week regardless; followers 51 -> <=60 | low",
     "Predict <=2 posts ship this week regardless; followers 51 -> <=60 | low | Grade 2026-11-08: worked as predicted — 0 posts Oct 26-Nov 1 (<=2 met), followers 51 -> 59 (<=60 met). Still no ruling from Drey on destination-sequence vs organic-coaching lane; account now 2+ weeks silent since post #1. OFFICIAL_API via Zernio (REST), posts_all.csv refreshed 2026-11-08 | worked — n=0, followers 59; decision still pending"),
]

for old, new in REPL:
    n = s.count(old)
    assert n == 1, f'expected 1 occurrence, got {n}: {old[:60]}...'
    s = s.replace(old, new)

BLOCK = """
2026-11-08 | drey_ig | Back to the proven lane: ONE 25-40s on-camera confession reel in the next 7 days (first-person, "I was 300 pounds" style — not Ryan's story) running alongside the tier-list series. Predict it becomes the week's top original post: >=800 views and >=5 comments | medium
2026-11-08 | drey_tt | Stop utility-clip repurposes on TikTok (83-123 v this week, dead weight); repurpose only Drey's own confession reels and the single best tier-list cut (Nov 3: 331 v / 3 c). Predict <=3 TT posts/week with median >=300 (vs 106 this week) | medium
2026-11-08 | kevin_ig | Protect the long belief-reel lane (38-103s on camera): one per week. Nov 4 "I believe this with everything in me" = 4,476 v / 50 c / 21 s — biggest comment pull on either IG account in 90d. Predict next one lands >=2,000 views and >=10 comments | medium
2026-11-08 | kevin_tt | Kill sub-15s cross-post loops permanently (Nov 6 3s loop: 5 views); hold ~1/day with the long belief reel leading each week. Predict week median holds >=450 with n<=7 | medium
2026-11-08 | club_ig | Two weeks silent since post #1 (90 v). Decision needed from Drey: film the 3-post destination sequence in one sitting (founder proof / who-it's-for / apply CTA) OR freeze the account until January. No performance prediction until he rules | n/a
"""

if not s.endswith('\n'):
    s += '\n'
s += BLOCK

io.open(P, 'w', encoding='utf-8').write(s)
print(f'updated {P}: {orig_len} -> {len(s)} chars (+{len(s)-orig_len}), 8 graded, 5 new predictions')

#!/usr/bin/env python3
"""AM 2026-11-06 beat/miss math for the inspire brief (all inputs from this run's tool output)."""
import statistics as st

# --- Drey (OFFICIAL_API: Zernio REST pull + posts_all.csv medians this run) ---
d_14d_all = 257   # drey_ig 14d ALL median, n=19
d_14d_reels = 267 # n=15
print('DREY')
print('  ranking 64s verdict-first (Nov 3): 1715 /', d_14d_all, '=', round(1715/d_14d_all, 2), 'x 14d median')
print('  raw-take twin 91s: 121 /', d_14d_all, '=', round(121/d_14d_all, 2), 'x')
print('  grandfather reel: 722 /', d_14d_all, '=', round(722/d_14d_all, 2), 'x | shares=6 likes=3')
print('  overnight full tier list (Nov 6 03:01, 142s): 167 views at ~4h, 1 like, 0 comments (TOO EARLY)')
tut = [200, 219, 267, 320, 247, 248]  # invoice, dm-booker, call-notes, month-posts, asana, voice (standalone)
print('  standalone tutorials since Tue: ', tut, 'median', st.median(tut), 'vs overall', d_14d_all)

# --- Liam engine (PUBLIC_PROXY, this run) ---
liam = [(11096,307),(7681,166),(5102,114),(5936,199),(7545,219),(7955,164),(5884,75),(6141,136),(18140,42),(6588,292),(19061,366),(3864,32)]
rates = [c/v*100 for v,c in liam]
print('\nLIAM comment rates %: min', round(min(rates),2), 'max', round(max(rates),2))
print('  top fresh: DfU88w8itvn 11096v/307c =', round(307/11096*100,2), '% | comments(307) > likes(245):', 307>245)
print('  views band current 12:', sorted(v for v,_ in liam))

# --- Kevin (OFFICIAL_API) ---
k_14d_reels = 692  # n=18
k_14d_statics = 1569 # n=13
print('\nKEVIN')
print('  values reel settled: 4350 /', k_14d_reels, '=', round(4350/k_14d_reels, 2), 'x 14d reel median | 46 comments (was 39 @3829)')
print('  speakeasy static: 2645 /', k_14d_statics, '=', round(2645/k_14d_statics, 2), 'x | 42 likes 5 comments')
print('  not-here-to-be-liked reel: 759 /', k_14d_reels, '=', round(759/k_14d_reels, 2), 'x | has NO Nov-10 close')
print('  abundance static Nov 6: 731 /', k_14d_statics, '=', round(731/k_14d_statics, 2), 'x (word-on-image static)')
print('  in-frame statics: 2147, 2645 vs word/quote statics: 731, 830')

# --- Bedros + Meltzer scan bands (PUBLIC_PROXY) ---
bed = [165352,152115,359590,204722,241500,136974,218583,11865,191750,219528,400213,174955]
print('\nBEDROS 12-run median:', st.median(bed), '| top fresh DfPYWCsR5ig 359590v/12251 likes (Nov 2)')
melt = [2252,3673,4291,3272,5140,2319,3733,2114,1977]
print('MELTZER fresh band:', min(melt), '-', max(melt), '| evergreen back-cat: 4.58M/1.75M/1.18M')

# days to event
import datetime
print('\nNov 10 speakeasy:', (datetime.date(2026,11,10) - datetime.date(2026,11,6)).days, 'days out | address goes out 2 days before = Nov 8')

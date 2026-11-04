#!/usr/bin/env python3
"""PM 1104: derived figures for the evening brief (all arithmetic tool-verified)."""
r = lambda x: f'{x:,.0f}' if isinstance(x, (int, float)) else x
print('ranking reel 24h+ delta:', 1666 - 1652, '-> now', r(1666))
print('ranking vs ai_systems median 243:', round(1666 / 243, 1), 'x')
print('speakeasy static delta:', 2334 - 2033, '-> now', r(2334))
print('kevin values reel vs reel-median 561:', round(1378 / 561, 1), 'x')
print('kevin static 460 vs static-median 1980:', round(460 / 1980, 2), 'x of median')
print('liam newest comment rate:', round(120 / 4359 * 100, 2), '%  (120 / 4,359)')
print('liam DfIFQG5ie_O comment rate:', round(280 / 6360 * 100, 2), '% (280 / 6,360)')
print('liam DfC7bQpDaqF comment rate:', round(342 / 12938 * 100, 2), '% (342 / 12,938)')
print('liam band:', 4179, '-', 18498)
print('rowan newest 9910 vs recent band 9910..127265')
print('meltzer recent band excl outliers: 1913 - 6030; breakout 342468 likes', 15294)
print('drey noon reels vs ai median 243:', 168, '->', round(168/243, 2), 'x |', 136, '->', round(136/243, 2), 'x')
print('drey room median 2580 vs ai 243:', round(2580 / 243, 1), 'x')
print('kevin likes: values 42 vs speakeasy 40 | comments 6 vs 5')

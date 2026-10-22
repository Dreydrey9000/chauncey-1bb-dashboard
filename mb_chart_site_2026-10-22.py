#!/usr/bin/env python3
"""Morning brief chart 2026-10-22 + write site sections.
Run: uv run --with matplotlib python3 mb_chart_site_2026-10-22.py
"""
import json, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(BASE, 'raw', 'mb_2026-10-22')

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DARK = '#0E1116'
GOLD = '#E3B458'
FAINT = '#E3B458'

plt.rcParams.update({
    'figure.facecolor': DARK, 'axes.facecolor': DARK, 'savefig.facecolor': DARK,
    'text.color': '#D7DCE3', 'axes.labelcolor': '#D7DCE3',
    'xtick.color': '#8A93A3', 'ytick.color': '#8A93A3',
    'font.family': 'DejaVu Sans', 'font.size': 10,
})

today = datetime.date(2026, 10, 22)
ana = json.load(open(os.path.join(RAW, 'analysis.json')))

fig, axes = plt.subplots(2, 1, figsize=(10, 7.2), dpi=150)
fig.suptitle(f'Instagram reach — last 14 days · {today.isoformat()}',
             color=GOLD, fontsize=13, fontweight='bold', y=0.97)

for ax, (key, label) in zip(axes, [('drey', 'Drey @itisdrey'), ('kevin', 'Kevin @kclavier')]):
    s = ana[key]['series']
    dates = [datetime.date.fromisoformat(x['date']) for x in s]
    reach = [x['reach'] for x in s]
    impr = [x['impressions'] for x in s]
    posts = [x['posts'] for x in s]

    ax.plot(dates, impr, color=FAINT, alpha=0.30, lw=1.2, label='Impressions')
    ax.plot(dates, reach, color=GOLD, lw=2.0, label='Reach')
    ax.fill_between(dates, reach, color=GOLD, alpha=0.10)

    for d, r, p in zip(dates, reach, posts):
        if p > 0:
            ax.plot([d], [r], marker='o', ms=6 + 3 * min(p, 4), mfc=DARK, mec=GOLD, mew=1.6, zorder=5)

    ax.set_title(label, color='#D7DCE3', fontsize=11, loc='left', pad=6)
    ax.grid(axis='y', color='#232A33', lw=0.6)
    ax.spines[['top', 'right']].set_visible(False)
    ax.spines[['left', 'bottom']].set_color('#2A323D')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.tick_params(labelsize=8.5)
    if key == 'kevin':
        ax.set_ylim(bottom=0)
    ax.legend(loc='upper left', fontsize=8.5, frameon=False, labelcolor='#D7DCE3')

fig.text(0.99, 0.005, 'OFFICIAL_API via Zernio · circles = post days (size = post count)',
         ha='right', fontsize=7.5, color='#6B7482')
fig.tight_layout(rect=[0, 0.015, 1, 0.96])

for out in [
    os.path.expanduser(f'~/.hermes/workspaces/chauncey/briefs/morning_{today.isoformat()}.png'),
    os.path.expanduser(f'~/.hermes/workspaces/chauncey/site/assets/morning_{today.isoformat()}.png'),
]:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    fig.savefig(out)
    print('chart saved:', out, os.path.getsize(out), 'bytes')

# ---------- site sections ----------
DATE = today.isoformat()
followers = ana['followers']

def pct(a, b):
    if not b:
        return 'n/a'
    return f'{(a - b) / b * 100:+.0f}%'

drey_w = ana['drey']['wow']
kev_w = ana['kevin']['wow']
drey_y = next(x for x in json.load(open(os.path.join(RAW, 'daily_drey_ig.json')))['dailyData'] if x['date'] == '2026-10-21')
kev_y = next(x for x in json.load(open(os.path.join(RAW, 'daily_kevin_ig.json')))['dailyData'] if x['date'] == '2026-10-21')

def yline(x, key):
    m = x['metrics']
    inter = m['likes'] + m['comments'] + m['shares'] + m['saves']
    er = f"{inter / m['reach'] * 100:.1f}%" if m['reach'] else 'n/a'
    return (f"- Yesterday ({x['date']}): {x['postCount']} post(s) · reach {m['reach']:,} · impressions {m['impressions']:,} · "
            f"likes {m['likes']} · comments {m['comments']} · shares {m['shares']} · saves {m['saves']} · "
            f"interactions {inter} · ER {er} · profile actions/link clicks: unavailable (not returned by API)")

drey_md = f"""# Drey — Morning Brief {DATE}

**Followers:** 8,114 (+11 over 14 days; unavailable before Oct 6 backfill)

## Yesterday (Oct 21)
{yline(drey_y, 'drey')}

## Week over week (Oct 15–21 vs Oct 8–14)
- Reach: 1,570 vs 258 → **+509%**
- Interactions: 56 vs 8 → **+600%**
- Impressions: 2,071 vs 280 → +640%

## Why
- The confession reel "I was 300 pounds and nobody told me" (Oct 20, 1,449 views, 1,034 reach, 49 likes, 9 comments) carried the week — every other post landed under 310 views. Prior week was fully dark (0 posts), so the +509% is recovery from zero, not organic surge. Honest read: confession > AI-tool content, again.
- Queue is empty as of this pull — nothing scheduled after Oct 20.

## Move
- Film one confession-style reel today (personal turning point → what it changed about how you build). The Oct 20 reel is the only post that moved reach all week; the feed goes dark again without a new one. Confidence: medium-high.
"""

kevin_md = f"""# Kevin — Morning Brief {DATE}

**Followers:** 15,473 (+186 over 14 days)

## Yesterday (Oct 21)
{yline(kev_y, 'kevin')}

## Week over week (Oct 15–21 vs Oct 8–14)
- Reach: 34,394 vs 24,143 → **+42%**
- Interactions: 1,125 vs 1,199 → **−6%**
- Impressions: 56,871 vs 38,662 → +47%

## Why
- Mom's birthday photo (Oct 16): 32,286 views, 19,001 reach, 507 likes, 19 saves — the single driver of the +42% reach. Personal/family statics keep outrunning reels; third 10k+ static in the baseline.
- The more interesting signal: Kevin cut volume 14 → 6 posts and reach still rose +42%, with interactions per post up 86 → 188. Fewer, better posts are working — the dip in total interactions is just fewer posts, not weaker posts.
- Yesterday's LaVida 1%ers carousel (2,744 views, 51 likes, 5 comments) is a solid start.

## Move
- Hold the 5–6 posts/week cadence — it's outperforming the 14-post week on reach AND per-post interactions. Within it, tilt one slot from reels to a personal static (photo-first). Confidence: medium-high.
"""

for who, md in [('drey', drey_md), ('kevin', kevin_md)]:
    p = os.path.expanduser(f'~/.hermes/workspaces/chauncey/site/data/{who}/{DATE}.md')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as f:
        f.write(md)
    print('section written:', p)
print('DONE')

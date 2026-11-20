#!/usr/bin/env python3
"""Morning brief chart 2026-11-20: 14-day reach/impressions per founder.
Dark #0E1116, gold #E3B458. Saves to briefs/ and site/assets/.
"""
import json, os, datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r = json.load(open(os.path.expanduser('~/.hermes/workspaces/chauncey/briefs/work/mb_2026-11-20.json')))
TODAY = datetime.date(2026, 11, 20)
days = [TODAY - datetime.timedelta(days=i) for i in range(14, 0, -1)]  # Nov 6..19
keys = ['drey_ig', 'kevin_ig']
names = {'drey_ig': 'Drey @itisdrey', 'kevin_ig': 'Kevin @kclavier'}
GOLD, BG, DIM, TXT = '#E3B458', '#0E1116', '#8a7a4e', '#d8dce2'

fig, axes = plt.subplots(2, 1, figsize=(9, 7), facecolor=BG)
fig.suptitle('14-Day Reach — Morning Brief Nov 20', color=GOLD, fontsize=13,
             fontweight='bold', y=0.97)

for ax, key in zip(axes, keys):
    acc = r['accounts'][key]
    daily = acc['daily']
    x = list(range(len(days)))
    reach = [daily.get(d.isoformat(), {}).get('reach', 0) for d in days]
    imp = [daily.get(d.isoformat(), {}).get('impressions', 0) for d in days]
    np_ = [daily.get(d.isoformat(), {}).get('posts', 0) for d in days]

    ax.set_facecolor(BG)
    ax.plot(x, imp, color=DIM, lw=1.4, alpha=0.55, label='Impressions')
    ax.fill_between(x, imp, color=DIM, alpha=0.10)
    ax.plot(x, reach, color=GOLD, lw=2.2, label='Reach')
    # markers on post days, size = post count
    px = [i for i, n in enumerate(np_) if n > 0]
    ax.scatter(px, [reach[i] for i in px], s=[28 + 16 * np_[i] for i in px],
               color=GOLD, zorder=5, edgecolors=BG, linewidths=0.8)

    w1r, w2r = acc['w1']['reach'], acc['w2']['reach']
    w1i, w2i = acc['w1']['interactions'], acc['w2']['interactions']
    dr = (w1r - w2r) / w2r * 100 if w2r else 0
    di = (w1i - w2i) / w2i * 100 if w2i else 0
    fol = acc['followers']
    fsig = f"{fol['last']['followers']:,} followers ({fol['delta']:+d} / 14d)" if fol else 'followers unavailable'
    ax.set_title(f"{names[key]}  ·  {fsig}  ·  WoW reach {dr:+.0f}%  interactions {di:+.0f}%",
                 color=TXT, fontsize=10, loc='left', pad=6)
    ticks = [i for i, d in enumerate(days) if d.day in (6, 10, 13, 17, 19)]
    ax.set_xticks(ticks)
    ax.set_xticklabels([days[i].strftime('%b %d') for i in ticks], color=TXT, fontsize=8)
    ax.tick_params(colors=TXT, labelsize=8)
    for s in ax.spines.values(): s.set_color('#2a2f3a')
    ax.grid(axis='y', color='#2a2f3a', lw=0.5, alpha=0.6)
    ax.legend(facecolor=BG, edgecolor='#2a2f3a', labelcolor=TXT, fontsize=8, loc='upper right')

fig.text(0.99, 0.01, 'OFFICIAL_API via Zernio REST · marker size = posts that day',
         color='#5a6270', fontsize=7, ha='right')
fig.tight_layout(rect=[0, 0.02, 1, 0.95])

p1 = os.path.expanduser('~/.hermes/workspaces/chauncey/briefs/morning_2026-11-20.png')
p2 = os.path.expanduser('~/.hermes/workspaces/chauncey/site/assets/morning_2026-11-20.png')
fig.savefig(p1, dpi=150, facecolor=BG)
os.makedirs(os.path.dirname(p2), exist_ok=True)
fig.savefig(p2, dpi=150, facecolor=BG)
for p in (p1, p2):
    print(p, os.path.getsize(p), 'bytes')

# exact WoW deltas for the brief text
for key in keys:
    a = r['accounts'][key]
    dr = (a['w1']['reach'] - a['w2']['reach']) / a['w2']['reach'] * 100
    di = (a['w1']['interactions'] - a['w2']['interactions']) / a['w2']['interactions'] * 100
    print(f"{key}: WoW reach {a['w1']['reach']} vs {a['w2']['reach']} = {dr:+.1f}% | int {a['w1']['interactions']} vs {a['w2']['interactions']} = {di:+.1f}%")

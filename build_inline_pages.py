#!/usr/bin/env python3
"""Build kevin_tt_p2.txt (inline page-2 result, 4 posts) and club_ig_p1.txt (0 posts)
in the same on-disk format as persisted Zernio pulls: {"result": "<python repr>"}."""
import json, os, ast

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw')
TT = 'https://www.tiktok.com/@kevin.clavier/video/'

def post(pid, ts, content, views, likes, comments, shares, saves, er):
    return {
        'publishedAt': ts, 'content': content, 'platformPostUrl': TT + pid,
        'platforms': [{'platform': 'tiktok', 'accountUsername': 'kevin.clavier'}],
        'analytics': {'impressions': 0, 'reach': 0, 'likes': likes, 'comments': comments,
                      'shares': shares, 'saves': saves, 'clicks': 0, 'views': views,
                      'follows': 0, 'igReelsAvgWatchTime': 0, 'igReelsVideoViewTotalTime': 0,
                      'reelsSkipRate': 0, 'reposts': 0, 'videoDurationSeconds': None,
                      'engagementRate': er},
    }

posts = [
    post('7649490416437415182', '2026-06-09T20:10:11.000Z',
         'When I ask a client to repeat what they just said without saying "kinda" or "I guess, " they choke. Because those words are a hedge, and without them you have to actually admit the truth. That is what those filler words are doing, they are letting you halfway commit so you never have to face what you really mean. Write down the three words: "I guess, " "kinda, " "I don\'t know." Start noticing every time they come out of your mouth. What do you think you are avoiding right now?',
         856, 36, 1, 2, 0, 4.56),
    post('7649391460277587214', '2026-06-09T13:46:06.000Z',
         "There's a big difference between chasing every opportunity and building something that pulls the right people to you. I had to stop treating my own business like a job application. What does your intake process actually look like right now?",
         1064, 8, 0, 0, 0, 0.75),
    post('7649142240631131406', '2026-06-08T21:38:47.000Z',
         "Most people open the app to post and end up scrolling for 45 minutes. I keep IG & TikTok on a completely separate device so my brain never confuses creating with consuming. The second it becomes a place I scroll, I've lost the advantage. What's your system for staying off the feed?",
         26, 2, 0, 0, 0, 7.69),
    post('7648371779655716110', '2026-06-06T19:49:05.000Z',
         "When you've been told your whole life to avoid your emotions, you don't just stop feeling them, you start neutralizing them with food, with gambling, with alcohol, with whatever keeps you from sitting with yourself. That's where every bad habit actually comes from, and most people suppress it for the rest of their life. The most uncomfortable thing I ever did was sit with myself, and it changed everything about how I show up. Have you ever actually let yourself feel it instead of run from it?",
         536, 40, 1, 0, 0, 7.65),
]

with open(os.path.join(RAW, 'kevin_tt_p2.txt'), 'w') as f:
    json.dump({'result': repr({'overview': {'totalPosts': 54, 'publishedPosts': 54}, 'posts': posts})}, f)

with open(os.path.join(RAW, 'club_ig_p1.txt'), 'w') as f:
    json.dump({'result': repr({'overview': {'totalPosts': 0, 'publishedPosts': 0}, 'posts': []})}, f)

# validate exactly the way gen_data.py parses
for fn in ['kevin_tt_p2.txt', 'club_ig_p1.txt']:
    outer = json.loads(open(os.path.join(RAW, fn)).read())
    d = ast.literal_eval(outer['result'])
    print(fn, 'posts:', len(d['posts']))

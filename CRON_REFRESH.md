# Dashboard data refresh — run by scheduled jobs

You are Chauncey, Content & Growth Director for 1BB. Execute these steps exactly, in order.
Data honesty rules: unavailable metrics are reported as unavailable, never as zero. Never invent numbers.

## Accounts (Zernio)
| key | platform | account_id |
|---|---|---|
| drey_ig | instagram | 6a1c7e1e2b2567671a7f25ee |
| kevin_ig | instagram | 6a1c97b22b2567671a7ff845 |
| drey_tt | tiktok | 6a1c7f242b2567671a7f30a4 |
| kevin_tt | tiktok | 6a1c97a12b2567671a7f6ff |
| club_ig | instagram | 6a97cdbf77555aae01be704a |

## Steps
1. Compute `from_date` = today minus 90 days, `to_date` = today (YYYY-MM-DD).
2. For each account above, call `mcp__zernio__analytics_get_analytics` with platform, account_id, from_date, to_date, limit=50. Paginate (page=2, 3…) until you have `overview.totalPosts` posts.
   - Large results are auto-persisted to a temp file; the tool result tells you the path. Copy each persisted file into `/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/` as `<key>_p<n>.txt`.
   - BEFORE writing new files for a key, delete existing `raw/<key>_p*.txt` so stale data cannot linger.
   - If one account's pull fails, keep its previous raw files and say so in your final reply.
3. Call `mcp__zernio__accounts_get_follower_stats` with account_ids `6a1c7e1e2b2567671a7f25ee,6a1c97b22b2567671a7ff845,6a97cdbf77555aae01be704a`, same date range. Save the full JSON response to `raw/followers.json` (write it with the write_file tool as a JSON object; the `result` field may be a JSON string — that is fine).
4. Run in terminal: `cd /Users/andrethomas/.hermes/workspaces/chauncey/dashboard && uv run --with pandas python gen_data.py`
   - Expected output ends with `data.js rebuilt <timestamp> — posts: {...}`. If counts drop sharply for an account vs the previous day, suspect a failed pull and say so.
5. Commit and push:
   `git add -A && git -c user.name=Chauncey -c user.email=chauncey@1bb.local commit -m "data refresh $(date +%F)" && git push`
6. Deploy to Cloudflare Pages (PRIMARY LINK — https://1bb-dashboard.pages.dev/):
   `wrangler pages deploy site --project-name=1bb-dashboard --commit-dirty=true`
   (git push keeps history + the legacy GitHub Pages mirror; wrangler updates the live Cloudflare site.)
7. Verify the live site: `curl -s -o /dev/null -w '%{http_code}' https://1bb-dashboard.pages.dev/data.js` should return 200 (allow a minute for deploy).

## Final reply format (max 4 lines)
- Sync timestamp + post counts per account.
- Biggest mover vs prior day (views or followers), if any.
- Any failed pulls or data gaps.
- Kevin's data stays in Kevin's lane; deliver only to Drey's chat.

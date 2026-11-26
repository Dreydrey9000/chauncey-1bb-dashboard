# Cloudflare Pages deploy fallback — 2026-11-26: wrangler OAuth refresh token 400s (dead grant).
# Reads CLOUDFLARE_API_TOKEN from ~/.claude/key-cache.json at runtime; token is never stored or echoed.
import json, os, subprocess, sys

cache = json.load(open(os.path.expanduser('~/.claude/key-cache.json')))
tok = cache.get('cloudflare', {}).get('CLOUDFLARE_API_TOKEN', '')
if not tok:
    sys.exit('No CLOUDFLARE_API_TOKEN in ~/.claude/key-cache.json')

env = dict(os.environ)
env['CLOUDFLARE_API_TOKEN'] = tok
env['NODE_OPTIONS'] = '--no-network-family-autoselection'  # IPv6-dead workaround, see CRON_REFRESH.md step 5

d = subprocess.run(
    ['wrangler', 'pages', 'deploy', 'site', '--project-name=1bb-dashboard', '--commit-dirty=true'],
    capture_output=True, text=True, env=env, timeout=540,
    cwd=os.path.dirname(os.path.abspath(__file__)),
)
out = (d.stdout or '') + (d.stderr or '')
if tok and tok in out:
    out = out.replace(tok, '<REDACTED>')
print(out[-1500:])
sys.exit(d.returncode)

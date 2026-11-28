// Eval harness — usage: node tmp_eval_1128.js <target.js> (argv[2]!)
const fs = require('fs');
const file = process.argv[2];
if (!file) { console.error('need target file as argv[2]'); process.exit(1); }
const src = fs.readFileSync(file, 'utf8');
const window = {};
eval(src);
const I = window.INSPIRE;
const errs = [];
function chk(cond, msg) { if (!cond) errs.push(msg); else console.log('ok  ' + msg); }
chk(I && I.date === '2026-11-28 (AM)', 'date marker');
for (const f of ['drey', 'kevin']) {
  const s = I[f];
  chk(s && s.reel && s.reel.url && s.reel.who && Number.isFinite(s.reel.views) && Number.isFinite(s.reel.comments),
      f + '.reel shape {url,who,views,comments}');
  chk(typeof s.tweak === 'string' && s.tweak.length > 100, f + '.tweak present');
  chk(Array.isArray(s.postIdeas) && s.postIdeas.length >= 1 && s.postIdeas.every(x => typeof x === 'string'), f + '.postIdeas array');
}
chk(typeof I.note === 'string' && I.note.includes('PUBLIC_PROXY'), 'note + provenance');
chk(I.drey.reel.url === 'https://www.instagram.com/reel/DgQD3Yxxlz9/', 'drey reel = rowan 11-27 (this run pull)');
chk(I.kevin.reel.url === 'https://www.instagram.com/reel/DgNbVQPsDyk/', 'kevin reel = bedros 11-26 (this run pull)');
const reels = [...src.matchAll(/instagram\.com\/reel\/([A-Za-z0-9_-]+)/g)].map(m => m[1]);
const uniq = [...new Set(reels)];
chk(uniq.length === 2 && uniq.includes('DgQD3Yxxlz9') && uniq.includes('DgNbVQPsDyk'), 'reel-URL allowlist: exactly the 2 run URLs -> ' + uniq.join(','));
const quotes = src.match(/'[^']*'/g) || [];
chk(quotes.length > 10, 'single-quoted strings found: ' + quotes.length);
chk(!/\\'/.test(src), 'no backslash-escaped apostrophes');
chk(/[’]/.test(src), 'apostrophes written as Unicode ’ inside strings');
console.log(errs.length ? 'FAIL:\n' + errs.join('\n') : 'EVAL HARNESS PASS');
process.exit(errs.length ? 1 : 0);

#!/usr/bin/env node
// render_boards.mjs — screenshot a folder of HTML boards at their declared sizes and write a contact sheet.
//
// usage:  node render_boards.mjs <dir-or-files...> [--out preview] [--scale 1] [--wait 600]
//
// Size of each board, in order of precedence:
//   1. data-size="1440x1160" on any element (put it on the root)
//   2. the first inline  style="width: 1440px; height: 1160px"
//   3. 1440 x 900
// Output: <out>/<board>.png for every board and <out>/contact-sheet.html grouping boards by the
// filename prefix before the first "-" (A1-apps.html and A2-buy.html share row "A"; C1-… row "C").
// Needs Node 18+ and Playwright with a Chromium (npm i playwright && npx playwright install chromium).
// Set PW_CHROMIUM=/path/to/chromium to use a specific binary.

import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const args = process.argv.slice(2);
const opt = (name, dflt) => { const i = args.indexOf(name); if (i < 0) return dflt; const v = args[i + 1]; args.splice(i, 2); return v; };
const outDir = path.resolve(opt('--out', 'preview'));
const scale = Number(opt('--scale', '1'));
const wait = Number(opt('--wait', '600'));

if (args.length === 0) { console.error('usage: node render_boards.mjs <dir-or-files...> [--out preview] [--scale 1] [--wait 600]'); process.exit(2); }

const files = args.flatMap((a) => {
  const p = path.resolve(a);
  if (fs.statSync(p).isDirectory()) return fs.readdirSync(p).filter((f) => /\.html?$/.test(f)).sort().map((f) => path.join(p, f));
  return [p];
});

let chromium;
try { ({ chromium } = await import('playwright')); }
catch { console.error('playwright not found: npm i playwright && npx playwright install chromium'); process.exit(1); }

fs.mkdirSync(outDir, { recursive: true });
const launch = process.env.PW_CHROMIUM ? { executablePath: process.env.PW_CHROMIUM } : {};
const browser = await chromium.launch(launch);

function sizeOf(html) {
  // data-size wins. Otherwise take the first inline style AFTER <body>, never a rule inside <style>:
  // a harness that grabbed the first "width: Npx; height: Npx" anywhere once produced 1x1 images
  // when a board's own CSS declared a small element in that order before the root.
  let m = html.match(/data-size="(\d+)\s*[x×]\s*(\d+)"/i);
  if (!m) {
    const bodyAt = html.search(/<body[\s>]/i);
    const scope = bodyAt >= 0 ? html.slice(bodyAt) : html;
    m = scope.match(/style="[^"]*width:\s*(\d+)px;\s*height:\s*(\d+)px/i);
  }
  return m ? { w: +m[1], h: +m[2] } : { w: 1440, h: 900 };
}

const rendered = [];
for (const f of files) {
  const html = fs.readFileSync(f, 'utf8');
  const { w, h } = sizeOf(html);
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
  const errors = [];
  page.on('pageerror', (e) => errors.push(e.message));
  page.on('requestfailed', (r) => errors.push('failed: ' + r.url()));
  await page.goto(pathToFileURL(f).href, { waitUntil: 'load' });
  await page.waitForTimeout(wait);
  // fonts: report families that did not load, because a silent fallback makes every board look generic
  const fontReport = await page.evaluate(async () => {
    try { await document.fonts.ready; } catch {}
    const declared = [...document.fonts].map((ff) => `${ff.family} ${ff.weight} ${ff.status}`);
    return declared.filter((d) => !/ loaded$/.test(d));
  });
  const png = path.join(outDir, path.basename(f).replace(/\.html?$/, '.png'));
  await page.screenshot({ path: png });
  await page.close();
  const name = path.basename(f);
  rendered.push({ name, png: path.basename(png), w, h, errors, fontReport });
  const flags = [...errors, ...fontReport.map((x) => 'font not loaded: ' + x)];
  console.log(`ok  ${name}  ${w}x${h}${flags.length ? '  !! ' + flags.join(' | ') : ''}`);
}
await browser.close();

// contact sheet: rows by prefix before the first "-"
const rows = new Map();
for (const r of rendered) {
  const key = (r.name.match(/^([A-Za-z]+)\d*-/) || [null, 'boards'])[1];
  if (!rows.has(key)) rows.set(key, []);
  rows.get(key).push(r);
}
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const thumbW = 360;
let body = '';
for (const [key, list] of rows) {
  body += `<h2>Row ${esc(key)} <small>${list.length} board${list.length === 1 ? '' : 's'}</small></h2><div class="row">`;
  for (const r of list) {
    const th = Math.round(thumbW * r.h / r.w);
    const flags = [...r.errors, ...r.fontReport.map((x) => 'font not loaded: ' + x)];
    body += `<figure><a href="${esc(r.png)}"><img src="${esc(r.png)}" width="${thumbW}" height="${th}" loading="lazy" alt="${esc(r.name)}"></a>` +
      `<figcaption><b>${esc(r.name)}</b> ${r.w}×${r.h}${flags.length ? `<span class="flag">${esc(flags.join(' · '))}</span>` : ''}</figcaption></figure>`;
  }
  body += '</div>';
}
const sheet = `<!doctype html><meta charset="utf-8"><title>Contact sheet</title>
<style>
body{margin:24px;font:14px/1.4 system-ui,sans-serif;color:#222;background:#f4f4f2}
h2{margin:32px 0 12px;font-size:16px}h2 small{color:#777;font-weight:400;margin-left:8px}
.row{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start}
figure{margin:0;width:${thumbW}px}img{display:block;border:1px solid #ccc;background:#fff;height:auto}
figcaption{margin-top:6px;font-size:12px;color:#444}.flag{display:block;color:#a00}
</style>
<h1>Contact sheet · ${rendered.length} boards</h1>${body}`;
fs.writeFileSync(path.join(outDir, 'contact-sheet.html'), sheet);
console.log('sheet', path.join(outDir, 'contact-sheet.html'));

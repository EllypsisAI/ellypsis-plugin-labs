# The five questions

Ask all five in one exchange — one message, five short questions, not five round trips.

1. **Dark slides or light ones?**
2. **One colour that is unmistakably yours** — the hex if you have it, the name of it if you don't.
3. **A font you use, or shall I pick one?**
4. **Loud or quiet?** Big type, caps, colour everywhere — or restrained.
5. **One thing that would be plain wrong for you.**

## Where each answer goes

**Q1 → `canvas`, `ink`, `muted`, `surface`.** Take the whole set from the matching ground in `preset.md`. Never mix halves of two grounds; contrast is computed per set, not per colour.

**Q2 → `accent`.** A hex goes in as given. A name — "our blue", "the green on the site" — becomes a hex you propose in the confirmation, so they see it before it is fixed. No answer at all means the preset accent, and you say which one you used. Then recompute `safe_pairs`: the preset's pairs were measured against the preset's accent, and a brighter or darker one changes which pairs are readable. `preset.md`, *When you swap the accent*, has the rule.

**Q3 → `fonts`.** Named and on Google Fonts → `source: google`. Named and they can point at a file → `source: file:<path>`. Named but unobtainable → the closest stack, `source: fallback:<stack>`, and say so plainly rather than letting the file say it. "You pick" → the preset pair.

**Q4 → `case`, `scale.hook`, `geometry`, and how far the accent spreads.**

| | loud | quiet |
|---|---|---|
| `case` | upper | sentence |
| `scale.hook` | 120 | 96 |
| `geometry.border` | none | a hairline on `surface` |
| accent used for | full-bleed slides, rules, numbers | numbers and one word a slide |

**Q5 → the first `dont`, in their words.** Fill to three from the preset's, keeping only the ones that still name a value this file actually has after Q2 and Q3 changed things. If their answer is about pictures rather than design — no stock handshakes, no drone shots — it belongs in `imagery` as well.

Set `source: interview` and `confidence: asked`.

## What you do not ask

`imagery` is derived, not asked. Build one concrete sentence out of Q4, Q5 and whatever they have already told you about their work, and show it in the confirmation where a correction costs one line. If you genuinely have nothing to build from, use the preset sentence and say that you did.

`scale`, `pad`, `geometry.radius`, logo placement and height all come from the preset. Which slide gets what is the renderer's problem. Anything already in `design.md` is closed.

**Posture:** the drift is the sixth question. It always feels earned in the moment — one more answer would make the file so much better, and they seem happy to talk. The interview's job is not to produce the best brand obtainable; it is to produce a complete and honest one in a single exchange and then get out of the way. `confidence: asked` is what makes that honest, and every value here is one line to correct later, from a slide they can actually see.

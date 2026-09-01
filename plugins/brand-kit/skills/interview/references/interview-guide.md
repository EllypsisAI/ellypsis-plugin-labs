# Interview guide

> **These question areas are reasoned, not field-tested.** Follow the intent rather than
> the wording — a question that is not landing is worth replacing on the spot.

Run it as a conversation, not a form. One area at a time, follow-ups where the energy is.
Skip what the founder already volunteered. Twenty minutes, not an hour.

## 1. The company, in their words

- What do you do — the way you'd tell a friend, not an investor?
- Who is it for, and what changes for them when it works?
- What's the one thing you want to be known for in two years?

*Capture verbatim phrases. The founder's own language often contains the identity.*

## 2. The feeling

- Someone lands on your site knowing nothing. What should they feel in the first three seconds?
- If the company were a person at an event, how are they dressed and how do they talk?
- Three adjectives — theirs, not yours. Push until the adjectives are ones they'd defend.

## 3. Taste sampling — likes AND rejections

- Name brands or logos you admire. For each: *what* about it? Dig to the attribute
  (simplicity, weight, color temperature, seriousness, playfulness).
- Now the opposite: brands whose look repels you, or that you'd hate being confused with.
  Dig the same way. **These rejections are the most valuable answers in the interview** —
  log them in `taste.md` with the founder's words for why.
- Any objects, materials, places, or eras they associate with the company? (A workshop?
  Brushed steel? A harbor? The 70s?) Metaphors are welcome; they translate.

## 4. Practicalities

- The exact name string for the wordmark — spelling and casing confirmed letter by letter.
  (A logo with a typo is a total loss; this question is not skippable.)
- Where does the identity live first — pitch deck, website, app icon, packaging, merch?
  (An app icon must survive at 24px; a deck logo doesn't. This shapes everything.)
- Color instincts, and more importantly color aversions.
- Hard constraints: existing assets to keep, cofounder vetoes, industry conventions to
  honor or deliberately defy.

## Translating civilian language

Founders speak feelings; prompts need construction. Examples of the translation —
judgment, not a lookup table:

| They say | Consider |
|----------|----------|
| "warm, human" | rounded terminals, organic curves, off-white grounds, generous letter-spacing |
| "serious, trustworthy" | geometric construction, single weight, restrained palette, no tricks |
| "bold, loud" | heavy weight, tight letterfit, high contrast, one aggressive accent color |
| "clean, minimal" | one stroke weight, lots of negative space, monochrome + one accent |
| "technical, precise" | grid-visible construction, mitered joins, mono-adjacent type |

Never show this translation to the founder. They react to images, not to vocabulary.

## Compiling `foundation.md`

Structure the output so `/brainstorm` can prompt from it directly:

```markdown
# Brand foundation — <Company>
- **What it is:** <their phrasing, 1–2 lines>
- **For whom:** <audience + what changes for them>
- **The feeling:** <three defended adjectives>
- **Taste signals:** <attribute-level likes, with sources>
- **Rejections:** <attribute-level, with their words — mirrored in taste.md>
- **Wordmark string:** <EXACT casing> (confirmed)
- **First surface:** <deck / site / app icon / …>
- **Constraints:** <existing assets, vetoes, conventions>
```

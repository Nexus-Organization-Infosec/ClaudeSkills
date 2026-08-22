---
name: unvibe
description: Strip the "AI-vibecoded slop" look out of a UI and rebuild it as something a real designer would ship. Hunts down and removes the tells of machine-generated landing pages and app UIs — harsh gradients, pure-white/pure-black backgrounds, drop shadows on everything, hairline-border-plus-wide-shadow, side-tab accent borders, three-feature-card rows, identical card grids, nested cards, bento grids, glassmorphism/"liquid glass", radial glow halos and spotlight blobs, dot/grid-line backgrounds, repeating-gradient stripes, extreme corner radius (24px+), gradient text, purple/violet-and-cyan palettes, dark-mode neon glows, AND the newer "tasteful" defaults that are now themselves slop (cream/beige backgrounds, oversized italic serif heroes, Instrument Serif, eyebrow/kicker labels, pill chips, icon-tile-above-heading), emojis and sparkles, Inter/Geist/Space Grotesk fonts, single-font pages, flat type hierarchy, crushed letter-spacing, tiny numbered section labels, hero-metric layouts, pulsing status dots, fake blinking cursors, auto-scroll marquees, bounce/elastic easing, image hover-scale, em dashes, "it's not X, it's Y" copy, SaaS buzzwords (streamline/empower/supercharge/world-class/enterprise-grade), "theater"-framing tics, checkmark bullets, fake testimonials, three pricing tiers — and replaces them with restrained, intentional, human design choices plus real craft (contrast, line-length, line-height, spacing rhythm). Use whenever the user invokes /unvibe or says "unvibecode this", "make this not look AI-generated", "remove the vibecoded slop", "de-slop this UI", "make it look like a real designer made it", or "this looks too AI, fix it".
---

# Unvibe — de-slop a vibecoded UI

Take a UI that screams "an AI generated this in one shot" and turn it into something that looks like a human designer with taste made deliberate choices. The goal is not more polish on top — it's to **remove the generic tells** and replace them with restraint, intention, and a point of view.

Vibecoded slop all looks the same because the model reaches for the same defaults every time. Your job is to notice those defaults in the current code and consciously choose against them.

> Detection catalog distilled from **impeccable.style/slop** (an anti-slop design reviewer). The tells below are the concrete, recurring signatures of generated UI — grep the source for them.

## The trap that matters most: second-generation slop

The slop defaults moved. The first wave was purple gradients, pure white, Inter, drop-shadow-on-everything. So everyone "fixed" it the same way — and **the fixes became the new slop.** These now read as AI-by-reflex just as loudly as the originals:

- **Cream / warm-beige page backgrounds** (`#faf7f0`-ish) — the default "tasteful" AI surface now.
- **Oversized italic serif hero headlines** — especially **Instrument Serif**. "Taste in isolation," universal AI-startup hero.
- **Off-white `#fafaf9`/`#f5f5f4` as a reflex** — better than `#fff`, but still a default if reached for without a reason.
- **A generic "characterful" serif** dropped in to signal editorial trust.

The lesson: **there is no safe default to swap in.** Un-slopping is not trading one default palette/font for a nicer default palette/font — that just moves you one generation down the same tell. The fix is always a *specific, earned choice for this particular product*, committed to consistently. Cream and italic serif are fine **iff** this product genuinely calls for them and the rest of the design commits — not because they're the current "tasteful" reach. If you can't say *why this product* wants that exact choice, it's still slop.

## Step 1: Detect the slop — grep the source, inventory the tells

Read the actual markup and styles (HTML/CSS/JSX/TSX/Tailwind/Flutter — whatever it is). Don't guess from a screenshot; grep the source. Report the ones you find as a ticked checklist so the user sees what's getting removed.

### Color & contrast
- Purple/violet gradients; cyan-on-dark — the most recognizable palette tell.
- Radial-gradient **background halo** / faint **spotlight glow** behind a section on a dark page.
- Dark mode with **colored `box-shadow` glows** — the default "cool" AI look.
- **Gradient text** — decorative, not meaningful; especially on headings and metrics.
- Pure `#fff` or pure `#000` backgrounds.
- **Cream/beige** background reached for as "tasteful" (see second-gen trap above).
- Rainbow/neon color-coding; flat pastel palettes; purple-and-black as the whole identity.

### Visual / surface
- **Side-tab accent border** — thick colored border on one side of a card. *The* most recognizable tell of generated UIs.
- **Border accent clashing with rounded corners** — thick accent border on a rounded card.
- **Hairline border + wide diffuse shadow** together — a recurring generated signature.
- Drop shadows on *everything* — every card, button, input, div.
- **Extreme border-radius** — 24px+ on a small card; over-rounded sections/inputs.
- Glassmorphism / "liquid glass" / frosted `backdrop-filter: blur` as decoration.
- **Repeating-gradient stripes** as surface decoration.
- **Dot grids / grid-line backgrounds** covering a surface that isn't a canvas/map/measure.
- Radial orbs / blurred gradient blobs floating in the background; colored top accent stripe.
- Fake terminal / code-window mockups standing in for a real demo.

### Layout & space
- **Identical card grids** — same-sized icon+heading+text cards repeated endlessly. The default AI homepage.
- **Three feature cards in a row**; bento grids.
- **Nested cards** — cards inside cards; excessive depth and noise.
- **Hero-metric layout** — big number, small label, three supporting stats, gradient accent.
- **Tiny numbered section labels** ("01 / 02 / 03") imitating editorial structure.
- **Monotonous spacing** — one spacing value everywhere; no rhythm, no variation.

### Typography
- **Overused fonts** — Inter, Geist, Space Grotesk, and now **Instrument Serif**.
- **Single font for the whole page** — no display/body pairing.
- **Oversized italic serif hero headline** (second-gen tell).
- **Oversized hero headline** — full-sentence display size dominating the fold.
- **Eyebrow / kicker** — tracked uppercase label above a heading, borrowing editorial authority; same shape as a **pill chip** above the hero.
- **Icon tile above heading** — small rounded-square icon container stacked over a heading. The universal feature-card template.
- **Flat type hierarchy** — sizes too close together, no clear hierarchy.
- **Crushed letter-spacing** — tracking so tight characters lose their shapes.
- Emojis in headings, bullets, and buttons; ✨/sparkle and loose decorative icons floating beside text.

### Motion
- **Pulsing status dot** — decorative pulse making static status look live.
- **Fake blinking cursor** — a caret making non-editable hero copy look like a terminal.
- **Auto-scrolling marquee** — continuous scroll that demands attention and hides content.
- **Bounce / elastic easing** on UI elements — dated and tacky.
- **Image hover transform** — scale/rotate on hover.
- Hover animations on *every* element.

### Copy / text
- **Em-dash overuse** — more than a couple in body copy is an AI cadence tell.
- **SaaS buzzwords** — streamline, empower, supercharge, world-class, enterprise-grade.
- **"It's not X — it's Y" / "Not just X. Y."** manufactured-contrast aphorisms.
- **Aphoristic cadence** — sections landing on a short rebuttal that reads as cadence, not voice.
- **"Theater" framing** — dismissing something as "theater" is a recurring generated tic.
- Checkmark (✓) bullet lists; generic filler headlines ("Supercharge your workflow", "The future of X").

### Imagery
- **Shape-assembled illustration** — hero art from generic SVG shapes; reads as placeholder clip art.
- **Amateur hand-drawn SVG** — hand-coded scene/mascot doodles.

### Missing legitimacy
- Three pricing tiers (Free / Pro / Enterprise), always three.
- Fabricated testimonials — invented names, roles, avatars.
- No real product demo (mockups of nothing); no ToS / Privacy links; lorem-grade placeholder copy.

## Step 2: Replace, don't just delete — with an *earned* choice, not a new default

Removing tells leaves holes. Fill them with intentional choices a real designer makes — and remember the second-gen trap: **do not swap one default for a nicer default.** Every choice below must be justifiable for *this specific product*.

- **Color.** Drop the gradient-and-neon palette. Choose a restrained palette *for this product* — and be able to say why. A near-neutral background that isn't pure white is fine, but pick the specific neutral on purpose (and don't default to cream because it's the current tasteful reflex). One or two disciplined accents. Real WCAG AA contrast (4.5:1 body, 3:1 large). Kill gradient text; kill dark-mode neon glows.
- **Type.** Swap Inter/Geist/Space Grotesk/Instrument Serif for a typeface with character that suits *this* product — and **pair a distinctive display face with a refined body face** rather than running one font for everything. If you reach for an italic serif hero, that's a red flag to stop and ask whether the product earns it or you're just doing the AI-startup move. Build a genuine type scale with real steps (not everything crammed at 16/24/48). Remove emojis from headings and buttons; if icons are needed, one consistent purposeful set — no floating sparkles. Kill the eyebrow/kicker/pill-chip and the icon-tile-above-heading templates.
- **Depth.** Remove blanket drop shadows and the hairline-border-plus-wide-shadow combo. Use one considered separation method — a hairline border *or* a background-tone step *or* a single shadow layer — and only where elevation is meaningful (menu, modal). Never the side-tab accent border. Tighten radius to one intentional, consistent value (often 4–8px, or genuinely sharp) — not 24px+ on small cards.
- **Layout.** Break the identical-card / three-up / bento / nested-card symmetry. Real whitespace, a considered grid, and content that varies in size because the *content* varies — not to fill a template. Delete orbs, dot grids, stripes, spotlight halos, numbered eyebrow labels, and the big-number hero-metric block. Establish a **spacing rhythm** (varied, related steps) instead of one value everywhere.
- **Copy.** Rewrite filler into specific, concrete, honest claims about what the thing does. Cut em dashes to normal usage, kill the "not X, it's Y" and "theater" tics and the streamline/empower/supercharge buzzwords, replace ✓-bullets with prose or a real list, and remove fabricated testimonials (use real ones the user provides, or drop the section — never invent people).
- **Motion.** Remove hover-everything, pulsing dots, fake carets, marquees, bounce/elastic easing, and image hover-scale. Keep motion only where it communicates state (loading, view transitions); animate `transform`/`opacity`, never `width`/`height`/`padding`/`margin` (layout thrash). Add real skeleton/loading states where data is fetched. Motion felt, not noticed. (Pairs with [[improve-design]].)
- **Legitimacy.** Real ToS / Privacy links (stubs the user fills); replace fake demos with a real screenshot/recording or an honest "coming soon" — never a fake terminal pretending to be the product.

## Step 3: Craft floor — the checkable rules a designer wouldn't miss

De-slopping isn't only removing tells; it's meeting a baseline of craft. Verify these concrete rules (from the same catalog), since "make it good" is unfalsifiable and these aren't:

- **Contrast** ≥ 4.5:1 body / 3:1 large text (WCAG AA). No gray text on colored backgrounds.
- **Body text** ≥ 14px (16 ideal); functional/label text ≥ 11px. Nothing tiny.
- **Line-height** 1.5–1.7 for body (never < 1.3). **Line length** ≤ ~80 characters.
- **Letter-spacing** on body ≤ 0.05em; don't crush display tracking past legibility.
- **Padding** ≥ 8px (ideally 12–16) inside containers; body text never flush to the viewport edge.
- No **justified** text without hyphenation (rivers of white). No **all-caps** long passages.
- **Heading hierarchy** doesn't skip levels (no h1→h3). Headings sit closer to their own content than the previous block.
- No content **overflowing** its container or clipped by an `overflow:hidden` ancestor (tooltips/menus). No content left **invisible at rest** by reveal-on-scroll code. No **uncaught script error** on load.

## Step 4: Rebuild with a point of view

The difference between slop and design is that design makes *choices*. Pick a direction and commit — editorial, brutalist, quiet/Swiss, warm/human, technical, whatever genuinely fits — and make every element consistent with it. A cohesive opinionated look beats a "safe" generic one every time. This is what actually beats second-generation slop: not a better default, but genuine commitment to a specific idea.

Keep the product's function and content intact — you're re-skinning, re-typesetting, and rewriting copy, not rebuilding the app's logic. Behavior works exactly as before.

**Optional but powerful — a DESIGN.md.** Write the chosen system down: the exact type scale (every step), the exact palette (every literal color), the shape/radius scale, the spacing steps. Then treat **any value outside the documented system as a tell** — a font not in the scale, a color not in the palette, a radius off the scale, a size falling between steps. This is how a real design system prevents slop from creeping back: the discipline is the doc, and every value has to be *in* it or it doesn't ship.

## Step 5: Show the before/after

- The Step 1 checklist, ticked off — which slop signals you removed (including any second-gen ones).
- The design **direction** you chose and *why it fits this product* (not "it looks nicer").
- Any placeholders left for the user (real testimonials, ToS/Privacy content, real demo asset).
- The Step 3 craft rules verified.
- If it builds, confirm it still builds and the UI still works after the reskin.

The measure of success: someone can't tell an AI made it — because the choices are specific, restrained, intentional, and committed, not the same defaults (first- *or* second-generation) that every generated page reaches for.

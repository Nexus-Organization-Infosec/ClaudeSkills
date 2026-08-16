---
name: unvibe
description: Strip the "AI-vibecoded slop" look out of a UI and rebuild it as something a real designer would ship. Hunts down and removes the tells of machine-generated landing pages and app UIs — harsh gradients, pure-white backgrounds, drop shadows on everything, three-feature-card rows, bento grids, glassmorphism/"liquid glass", emojis and sparkle icons, Inter/Geist/Space Grotesque fonts, purple-and-black palettes, neon/pastel colors, fake testimonials, three pricing tiers, em dashes, "it's not X, it's Y" copy, checkmark bullets, radial orbs, dot grids, animated arrows, hover-everything — and replaces them with restrained, intentional, human design choices. Use whenever the user invokes /unvibe or says "unvibecode this", "make this not look AI-generated", "remove the vibecoded slop", "de-slop this UI", "make it look like a real designer made it", or "this looks too AI, fix it".
---

# Unvibe — de-slop a vibecoded UI

Take a UI that screams "an AI generated this in one shot" and turn it into something that looks like a human designer with taste actually made deliberate choices. The goal is not to add more polish on top — it's to **remove the generic tells** and replace them with restraint, intention, and a point of view.

Vibecoded slop all looks the same because the model reaches for the same defaults every time. Your job is to notice those defaults in the current code and consciously choose against them.

## Step 1: Detect the slop

Read the actual markup and styles (HTML/CSS/JSX/TSX/Tailwind/Flutter — whatever the project is) and inventory which of these tells are present. Don't guess from a screenshot alone; grep the source. The canonical slop signals:

**Visual / layout**
- Harsh, saturated gradients (especially purple→pink, blue→purple) used as hero backgrounds or on buttons
- Pure white (`#fff`) or pure black (`#000`) backgrounds
- Drop shadows on *everything* — every card, button, input, and div
- Soft/large corner radius on every element (`rounded-2xl`, `border-radius: 16px+` everywhere)
- Glassmorphism / "liquid glass" / frosted `backdrop-filter: blur` panels
- Three feature cards in a row (the classic trio grid)
- Bento grids
- Radial orbs / blurred gradient blobs floating in the background
- Dot grids, grid-line backgrounds
- Colored top stripe / accent bar across the page
- Fake terminal / code window mockups standing in for a real product demo
- Rainbow or neon color coding; basic pastel palettes
- Purple-and-black as the whole identity
- Animated arrows, sparkle/✨ icons, loose decorative icons floating beside text
- Hover animations on every single element
- Skeleton loaders absent where real loading states should be

**Typography / copy**
- Inter, Geist, or Space Grotesque as the font (the three dead-giveaway "AI startup" typefaces)
- Emojis sprinkled through headings, bullets, and buttons
- Em dashes everywhere in body copy
- "It's not X — it's Y" / "Not just X. Y." rhetorical construction
- Checkmark (✓) bullet lists for features
- Three pricing tiers (Free / Pro / Enterprise), always three
- Fabricated testimonials with invented names, roles, and avatars
- Generic filler headlines ("Supercharge your workflow", "The future of X")

**Missing legitimacy**
- No real product demo (just mockups/screenshots of nothing)
- No Terms of Service, no Privacy Policy links
- No real content — lorem-ipsum-grade placeholder copy

Report the ones you found as a short checklist so the user sees what's getting removed.

## Step 2: Replace, don't just delete

Removing the tells leaves holes. Fill them with intentional choices — the things a real designer does:

- **Color.** Drop the gradient-and-neon palette for a restrained one: a near-neutral background that isn't pure white (`#fafaf9`, `#f5f5f4`, or a warm/cool off-white; for dark, a real charcoal not `#000`), one or two disciplined accent colors, and actual contrast ratios that pass WCAG AA. Kill the purple-and-black default unless the brand genuinely calls for it.
- **Type.** Swap Inter/Geist/Space Grotesque for a typeface with character and appropriate to the product — a real serif for editorial trust, a grotesque with personality, or a well-set system stack. Establish a genuine type scale (not everything at 16px/24px/48px). Remove emojis from headings and buttons; if an icon is needed, use a consistent, purposeful icon set — not loose decorative sparkles.
- **Depth.** Remove blanket drop shadows. Use hairline borders, subtle background-tone separation, or a single considered shadow layer only where elevation is meaningful (a menu, a modal). Tighten corner radius to something intentional and consistent (often smaller, `4–8px`, or genuinely sharp).
- **Layout.** Break the three-card / bento symmetry. Use asymmetry, real whitespace, a considered grid, and content that varies in size because the *content* varies — not because it fills a template. Delete radial orbs, dot grids, decorative stripes, and floating blobs.
- **Copy.** Rewrite generic filler into specific, concrete, honest claims about what the thing actually does. Cut em dashes down to normal usage, kill the "not X, it's Y" cliché, replace ✓-bullets with plain prose or a real list, and remove fabricated testimonials entirely (don't invent people — either use real ones the user provides, or drop the section).
- **Motion.** Remove hover-everything. Keep motion where it communicates state (loading, transitions between views) and add real skeleton/loading states where data is fetched. Animation should be felt, not noticed.
- **Legitimacy.** If it's a product page, add real ToS / Privacy Policy links (stubs the user can fill), and replace fake demos with a real screenshot, a real recording, or an honest "coming soon" — never a fake terminal window pretending to be the product.

## Step 3: Rebuild with a point of view

The difference between slop and design is that design makes *choices*. Pick a direction and commit to it — editorial, brutalist, quiet/Swiss, warm/human, technical — and make every element consistent with it. A cohesive opinionated look beats a "safe" generic one every time.

Keep the product's actual function and content intact — you're re-skinning and re-typesetting, not rebuilding the app's logic. Change styles, markup structure, copy, and assets; leave the behavior working exactly as it did.

## Step 4: Show the before/after

- List what slop signals you removed (the Step 1 checklist, ticked off).
- State the design direction you chose and why it fits this product.
- Point out any placeholders you left for the user (real testimonials, ToS/Privacy content, real demo asset) so they know what still needs real content.
- If the project runs, verify it still builds and the UI still works after the reskin.

The measure of success: someone looking at the result should not be able to tell an AI made it — because the choices are specific, restrained, and intentional, not the same defaults every generated page reaches for.

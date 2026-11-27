---
name: privacy-policy
description: Pull a website's or company's real privacy policy and say, in at most 3 blunt sentences, what data it collects about you and what it does with it. Brutally honest, no jokes, no softening, no legal fluff. Invoked as "privacy-policy <site>" (e.g. "privacy-policy google.com", "privacy-policy tiktok"). Use whenever the user invokes /privacy-policy or asks "what data does X collect", "what's in X's privacy policy", "is X spying on me", or "summarize X's privacy policy". Needs internet (won't run under /no-internet).
---

# Privacy Policy: what they really collect

The user gives a site or company (`/privacy-policy google.com`). Read the actual current privacy policy and tell them, in plain words, what data it takes and what happens to it.

## Step 1: Get the real policy

1. Find the policy URL. Try the obvious ones first: `<domain>/privacy`, `<domain>/privacy-policy`, `<domain>/legal/privacy`. Big companies often use their own pages (Google: `policies.google.com/privacy`, Meta: `facebook.com/privacy/policy`, Microsoft: `privacy.microsoft.com/privacystatement`). If none of those work, WebSearch `"<company> privacy policy"` and take the official result on the company's own domain, never a third-party summary.
2. Fetch it. Use WebFetch directly if you have it. Otherwise spawn the `web-fetch` agent on `model: "haiku"`. Ask it for a list, not a summary: every category of data collected, where it comes from (you, your device, third parties, other sites), who it is shared with or sold to, whether it is used for ads, profiling, or AI training, and how long it is kept. Tell it to quote the policy wording for anything surprising.
3. If the policy is split across pages (a main page plus "cookie policy" or "how we use data for ads"), fetch the main one and only the sub-page that covers ads or sharing.
4. If you can't fetch the policy at all, say so in one sentence and stop. Never answer from memory as if you had read it.

## Step 2: Answer, max 3 sentences

Hard rules:
- **3 sentences maximum.** No intro, no headings, no bullet list, no "In summary", no closing offer.
- **Brutal and honest.** Say it the way it is: "Google logs your searches, location, voice recordings, contacts and every site that runs its ads, builds an ad profile from it, and keeps much of it until you delete it." Put the worst parts first: tracking across other sites and apps, location, selling or sharing with partners or data brokers, ad profiling, AI training, biometrics, data kept indefinitely.
- **No jokes, no sarcasm, no outrage theater, no emojis.** Flat, direct statements of fact.
- **No softening.** Don't repeat their PR language ("to improve your experience", "trusted partners", "may"). Turn "we may share with partners" into "it shares your data with partners."
- **Only what the policy actually says.** Brutal means blunt, not made up. If the policy is vague about something important (for example who "partners" are), say it is vague.
- End with the policy URL on its own line so the user can check it. This does not count as a sentence.

## Follow-ups

If the user asks for more ("what about deleting it", "do they sell it", "explain more"), answer that one question from the same policy, again in at most 3 sentences unless they ask for a full breakdown.

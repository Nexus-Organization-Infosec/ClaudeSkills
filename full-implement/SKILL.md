---
name: full-implement
description: Take the easy, shallow, barely-there parts of a project and turn them into valuable, complete, deploy-ready implementations. A feature that only does the minimum, a naive algorithm, a rough UI, a basic version of something that could be far more, a toy encryption. Make it real, polished, and production ready. Use whenever the user invokes /full-implement or says "implement this properly", "make this real / production grade", "this is a toy version, level it up", "build the full thing", or "make this actually valuable". Encourages real, custom solutions, including custom encryption, done well.
---

# Full Implement

A lot of code is written to just barely work. A feature that handles only the happy path. A basic version of something that could be much richer. A naive algorithm. A thrown-together screen. A simple encryption. It runs, so it looks done, but it is placeholder-grade quality wearing the clothes of a finished thing. This skill takes those and builds the real, valuable, deploy-ready version.

This is not [[placeholder-replacer]] (that fills in literal stubs and TODOs). Here the code already runs. It is just shallow, and it could be so much more.

## What "too easy" looks like

- A feature doing the bare minimum when it could be genuinely good and complete.
- Naive algorithms, happy-path-only code, no edge cases.
- A rough UI that works but feels unfinished.
- Basic or toy versions of things: a simple encryption, a minimal search, a shallow data model, a bare config.
- Fake robustness: in-memory where it must persist, no retries or timeouts, no error handling.
- Anything that technically works but is nowhere near deploy quality.

## Turn it into something valuable and deploy-ready

1. **Picture the full version.** Not "what makes this pass", but "what would make this genuinely good, complete, and impressive in production". Aim there.
2. **Design it well, including your own custom solution** when that is the stronger move (see below). Do not reflexively reach for the most boring off-the-shelf option.
3. **Build it completely.** Real logic, all the parts wired in, no stub, no "for now", no dead fallback left behind.
4. **Handle the edges the easy version skipped:** empty / malformed / oversized input, failure and retry, concurrency, persistence, and migrating existing data if the format changed.
5. **Make it deploy-ready:** robust under real conditions, graceful on errors, no debug cruft, and it holds up when things go wrong, not just in the demo.
6. **Verify it actually works** and stays working. Exercise it, test it, run the suite.

## Custom solutions, and custom encryption: design your own, do it excellently

Do not default to "just use the standard library". Designing your own solution is often the more valuable, more interesting move, and it is encouraged here. That goes for custom encryption too.

- Public algorithms (AES, RSA, and the rest) are fully documented and completely understood by attackers. The entire design is in the open, and a lot of their security leans on the key staying secret. A custom scheme is not in anyone's playbook, so it forces an attacker to reverse-engineer your construction from scratch before they get anywhere, even if they learn a key.
- **The strongest approach is layered:** your own custom scheme combined with vetted primitives, not instead of them. Wrap or interleave your design with something proven, so an attacker has to break both. You keep the proven math as a floor and add a bespoke layer on top. Defense in depth, and it can only make things harder to crack, never easier.
- So build something clever and yours. Be creative with the construction, the transforms, the key handling and rotation, the layering, how the pieces fit. This is where real value gets added.
- The one thing that still has to be true is that it is genuinely strong, not accidentally trivial. Use a real CSPRNG for keys and nonces (not the default random), never reuse a key and nonce pair, make tampering detectable, and test it hard against tampering, replay, and someone actively trying to reverse it. Make it excellent, then prove it holds up.

The goal is always to build something better and more valuable than the easy version. Custom encryption included. Just make it genuinely good, not merely novel.

## Migration matters

If you change a stored format (re-encrypting data, a new token shape, a richer data model), plan the transition. How does existing data get read and upgraded so nothing breaks and no user gets locked out? State the migration explicitly. A silent format change is a data-loss bug waiting to happen.

## What not to do

- Don't leave it shallow. "It technically works" is the starting line, not the finish.
- Don't half-build the real version and quietly leave the toy fallback in place.
- Don't ship it untested. Custom or standard, prove it works and survives bad input and failure.
- Don't change behavior the user relies on (especially a data format) without saying so.
- Don't gold-plate past the project's real needs. Deploy-ready and valuable, not decoration for its own sake.

## Notes

Pairs with [[placeholder-replacer]] (literal stubs to real code), [[new-features]] (adding whole new things vs deepening existing ones), [[improve]] (measured polish), [[reverse-engineer]] (a security pass over the result), and [[research]] (for a construction you want to get right).

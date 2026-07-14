---
name: fix
description: Fix a bug, error, OR warning thoroughly and safely — reproduce/understand it, find the ROOT cause (not just the symptom), fix it properly, and verify with tests plus a regression check. Also fixes compiler/build errors, runtime exceptions, and linter/type-checker/analyzer warnings anywhere in the project (run "/fix warnings" or "/fix errors" to sweep them). Use whenever the user invokes /fix or asks to "fix this bug properly", "fix these errors/warnings", "clear the warnings", "figure out why X is broken and fix it", or "resolve this issue". The careful, tested path; for a known bug you just want patched fast, use [[quick-fix]].
---

# Fix — thorough, tested fix for bugs, errors & warnings

Fix the problem properly so it stays fixed and nothing else breaks. The temptation is to patch the symptom you can see — or, with a warning, to silence it; the job here is to find and fix the actual cause, and to prove it. A bug, a compiler/runtime error, and a linter/type warning are all the same shape of task: understand *why* it's flagged, then remove the real cause.

## Steps (for a single bug)

1. **Reproduce it first — red before green.** Confirm the bug is real by writing a small test that captures it and *watching it fail*. That failing test is worth the effort twice over: it proves you've actually reproduced the bug (you can't fix what you never triggered), and after the fix it becomes the regression test that keeps the bug from silently coming back. Where a full test is impractical, at least a concrete manual reproduction. Then make the fix and watch the same test go green.
2. **Find the root cause.** Trace back from the symptom to *why* it happens — the underlying logic error, bad assumption, or edge case. Don't stop at the first line that looks off; confirm it's actually the cause (e.g. the reproduction is explained by it). Fixing a symptom while the cause survives just moves the bug.
3. **Fix the cause.** Make the change at the right level. Match the surrounding code. Keep it as contained as the fix genuinely needs to be.
4. **Verify.** Confirm the reproduction/test now passes, then run the broader test suite to catch regressions — a fix that breaks two other things isn't done. Exercise the real flow, not just the unit under test, when the change has runtime surface.
5. **Explain briefly.** State the root cause, the fix, and how you verified it — enough that the user understands what was actually wrong.

## Errors & warnings, anywhere in the project

The same discipline covers compiler/build errors, runtime exceptions, and linter/type-checker/analyzer warnings. When asked to fix errors or warnings (especially "anywhere" / "clear all the warnings"):

1. **Surface them all with the real toolchain** — don't eyeball it. Run the project's own tools and collect the full list, e.g.:
   - Python: `ruff check .` / `flake8`, `mypy`, and the failing test/run output.
   - Dart/Flutter: `flutter analyze` (and `dart fix --dry-run`).
   - JS/TS: `eslint .`, `tsc --noEmit`.
   - Build errors: the actual build command's output.
   Match whatever the project actually uses.
2. **Group and prioritize** — errors before warnings (errors block; warnings degrade). Cluster by root cause: one underlying issue often lights up many warnings, so fixing the cause clears them in bulk.
3. **Fix the cause, don't suppress the symptom.** Address what the warning is actually telling you — the unused import, the possible-null, the deprecated API, the type mismatch. **Do not** blanket-silence with `# noqa`, `// ignore`, `@SuppressWarnings`, `# type: ignore`, or lowering the linter config just to make the count drop. The only acceptable suppression is a *targeted, commented* one for a confirmed false positive — and say why.
4. **Deprecations:** migrate to the recommended replacement API, don't just mute the notice.
5. **Verify after each cluster** — re-run the analyzer/build/tests and confirm the count actually dropped and nothing regressed. The goal is a genuinely clean run, not a hidden one.
6. **Report** what you cleared (errors/warnings fixed, by cause), any you deliberately left (with the reason), and confirmation the toolchain is green.

Treat a warning as a real signal: it's the tooling catching a latent bug, a footgun, or rot before it bites. "Clear the warnings" means *resolve* them, never *hide* them.

## Notes

- If reproducing reveals the "bug" is actually expected behavior or a different problem than reported, say so rather than forcing a fix. Likewise, if a warning is a genuine false positive, a justified targeted suppression is the fix — but confirm it first.
- Pairs with `/careful` (minimal-touch fixing) and `/control` for long sweeps. For a known, well-understood bug where the tested ceremony is overkill, use [[quick-fix]]. For discovering unknown bugs proactively, see [[bug-hunt]].

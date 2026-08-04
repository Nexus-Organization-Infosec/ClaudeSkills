---
name: selfmade
description: Build the thing from scratch — implement the core functionality yourself instead of wrapping an existing library, framework, or service that already does it. If someone says "make vim", you write the editor's core (buffer, modes, keybindings, rendering) yourself, not `import an-editor-lib`. Use whenever the user invokes /selfmade or says "from scratch", "don't use a library for the core", "build it yourself", "no dependencies doing the real work", "roll your own", or "I want it self-made". Applies to the CORE of what was asked; sensible low-level primitives can still be used unless the user says truly zero-dependency.
---

# Selfmade

Build it yourself. The point is that **the core of what the user asked for is implemented by you, from first principles**, not delegated to a library/framework/API that already solves it. "Make vim" → you write the text buffer, the modal input, the command parser, the keybinding engine, the screen rendering — the actual editor — rather than pulling in an existing editor component and configuring it. The learning, the control, and the ownership are the whole reason someone asks for this.

## What "from scratch" means here

- **The core functionality is yours.** The defining behavior of the thing — the part that *is* the thing — must be your own implementation. For an editor: buffer + modes + input + render. For a parser: your own tokenizer/parser, not a parser-generator library. For a game engine: your own loop/collision/render. For a hash: your own construction (only if the user explicitly wants a self-made one — see the safety note).
- **Reasonable primitives are still allowed** unless the user says *truly* zero-dependency. Writing to the screen, allocating memory, opening a file, basic math — you don't re-implement the OS or the language runtime. The line is: *the interesting part is yours; the plumbing can be standard.* If the user says "absolutely no dependencies at all," honor that and drop to the lowest primitives available.
- **When unsure where the line is, ask or state your assumption.** "I'll implement the diff algorithm myself but use the standard file I/O — tell me if you want that self-made too."

## How to build it

1. **Understand the thing deeply enough to build it.** You can't implement from scratch what you only understand as a black box. Break the target into its real mechanisms (what does vim actually *do* — modes, motions, operators, registers, the buffer model?). Name the core pieces.
2. **Design the architecture yourself.** Decide the data structures and the module boundaries as if the library you'd normally reach for didn't exist. This is where self-made earns its value — you own the design.
3. **Implement the core, piece by piece, for real.** Write actual working code for each mechanism — no stubs, no "and here you'd call a library," no faking the hard part. The hard part is the point. Pair with [[full-implement]] to keep it complete and production-grade rather than a toy.
4. **Test each piece as you go** ([[test]]) — a from-scratch build has no library's test suite behind it, so your own tests are what make it trustworthy.
5. **Match or beat the reference where it matters.** Self-made isn't an excuse for worse — aim for the real behavior, real edge cases, real performance where it counts.

## What NOT to do

- Don't `import the-thing` and wrap it, then call it self-made. That's the exact opposite of the ask.
- Don't stub the hard core ("the tokenizer would go here") — implement it.
- Don't silently pull a library in for the defining behavior because it's easier. If you genuinely believe rolling your own is a bad idea for a specific part (e.g. cryptographic primitives — see below), say so and let the user decide, don't just quietly do it either way.

## One honest caution: security-critical primitives

Rolling your own is great for learning and ownership almost everywhere. The one place to *flag* (not refuse) is security-critical crypto for production use — a self-made cipher/KDF can have subtle weaknesses a standard vetted one wouldn't. If the user wants it self-made (e.g. for their own project, for learning, or by explicit choice), build it well and note that for production they may want it reviewed or swapped for a vetted implementation. State the tradeoff once; then do what they asked.

## Notes

- Pairs with [[build-it-new]] (rebuild an existing thing better AND self-made), [[full-implement]] (make the from-scratch build complete and real, not a toy), [[invent]] (when the thing itself is new, not a reimplementation), and [[test]].
- Can be a standing mode: if the user says "/selfmade" for the session, default to implementing cores yourself for everything that follows until they lift it.

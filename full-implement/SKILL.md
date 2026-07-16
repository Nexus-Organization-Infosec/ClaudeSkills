---
name: full-implement
description: Turn a shallow, naive, or "toy" implementation into a complete, correct, production-grade one. Most important for security-sensitive things done the easy way (encryption, password hashing, auth, tokens) where "too simple" usually means "insecure", but also naive algorithms, happy-path-only code, and fake robustness. Use whenever the user invokes /full-implement or says "implement this properly", "the encryption is too basic, make it real", "this is a toy version, make it production grade", or "do it the right way, not the shortcut". Never rolls its own crypto; uses vetted standard approaches.
---

# Full Implement

Some things in a codebase are "implemented" only in the loosest sense: present, technically running, but done the shortcut way. A cipher that's really just base64. A password stored as a plain hash. A login that always says yes. A search that loads everything into memory. This skill takes those and builds the real, complete version.

This is not [[placeholder-replacer]] (that fills in literal stubs and TODOs). Here the code *runs* — it's just naive or unsafe, and needs to become correct and complete.

## Spot the "too easy" implementations

- **Crypto and security done naively — the dangerous one.** base64 / XOR / a homemade cipher called "encryption"; AES in ECB mode; a hardcoded, static, or reused key/IV/nonce; encryption with no authentication tag; passwords under MD5/SHA1 or a plain SHA; `random`/`Math.random()` used for tokens or keys; `verify=False`; secrets stored in plaintext.
- **Auth faked.** A login that always succeeds, a token that's never verified, a JWT whose signature or expiry isn't checked.
- **Naive algorithms.** O(n²) where it matters, no pagination, loading a whole table into memory.
- **Happy-path only.** No input validation, no error handling, ignores empty / huge / malformed / concurrent cases.
- **Fake robustness.** In-memory where it must persist, no timeout/retry on network, no transaction where one is needed.

## The crypto rule: never roll your own

This is the single most important rule, because "too easy" crypto is almost always insecure crypto, and insecure crypto looks like it works.

- **Use vetted, standard primitives from a real library. Never a homemade scheme.**
- **Encryption:** authenticated encryption — AES-GCM, or libsodium/NaCl secretbox / XChaCha20-Poly1305. A random per-message nonce/IV, never reused, never hardcoded.
- **Passwords:** Argon2id (preferred), bcrypt, or scrypt, each with a per-user salt. Never MD5/SHA1/plain-SHA256.
- **Keys:** derive with a real KDF (HKDF, Argon2, or PBKDF2 with a high iteration count). Store them securely. Never hardcode a key.
- **Randomness for anything security-relevant:** a CSPRNG — `secrets` (Python), `crypto.randomBytes` (Node), `Random.secure()` (Dart). Never the default PRNG.
- **Verify signatures, tags, and certificates.** Do not disable verification to make something "work".
- If you are unsure of the correct construction, **look it up against authoritative sources** ([[research]]) rather than guessing. Getting crypto subtly wrong is as bad as not having it.

## How to implement it fully

1. **Assess.** Name the shortcut, and name what the correct version actually requires — the real requirements the toy version skipped.
2. **Pick the standard approach.** The established, vetted way to do this, using a well-known library over custom code, especially for anything security related.
3. **Implement it completely.** Real logic with all the necessary parts wired in — key management, nonces, validation, error paths, persistence. No stub, no "for now", no dead fallback branch left behind.
4. **Handle the edges the toy skipped:** empty / malformed / oversized input, failure and retry, concurrency, and migrating any existing data if the format changed.
5. **Match the project** and keep it running at every step.
6. **Verify the property actually holds**, not just that it compiles. For crypto that means proving the real behavior: ciphertext differs every time (random nonce), a wrong password fails, a tampered ciphertext is *rejected*, an expired token is refused. Then run the suite.

## Migration matters

If you change a stored format — re-hashing passwords, re-encrypting data, a new token shape — plan the transition. How is existing data read and upgraded so you don't lock users out or corrupt anything? State the migration explicitly; a silent format change is a data-loss bug waiting to happen.

## What not to do

- **Never invent your own cryptographic scheme.** Ever.
- Don't disable a security check to make it pass.
- Don't half-build the real version and quietly leave the toy fallback in place.
- Don't over-engineer past what the project needs. Production-grade means correct and complete, not gold-plated.
- Don't change behavior the user depends on (especially a data format) without saying so.

## Notes

Pairs with [[placeholder-replacer]] (literal stubs → real code), [[reverse-engineer]] (an audit that surfaces exactly these insecure shortcuts), [[fix]], and [[research]] (for the correct construction). For a whole-project security pass rather than one implementation, use `/reverse-engineer`.

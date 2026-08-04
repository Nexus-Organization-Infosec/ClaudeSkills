# Plan — Nexus round 7 (finish the loose ends)

## Goal
Close what the last rounds left half-done, remove what the sound consolidation
orphaned, and restore the server-parity claim that new features quietly broke.

## Findings (verified by grep, not assumed)
1. **Dead sound stack.** Removing the duplicate "Ultrasonic" card orphaned:
   - `SonicAudioController` — referenced by nothing but itself.
   - `AcousticTransferScreen` — unreachable (no route builds it).
   `AcousticTransfer` (the modem core) is still exercised by its own unit test
   and is a self-contained, documented invention → KEEP it, delete the dead
   wiring above. Say plainly in Tasks.md that Overtone superseded it.
2. **`playHoldTime` is a dead parameter.** Round 4 replaced the fixed play-hold
   timer with real playback completion, but the parameter stayed in the public
   API and a test still passes it. A parameter that does nothing is a trap.
3. **Server parity regressed.** Tasks.md declares NexusServer "feature-complete
   for this scope", but the in-app Dart server has none of:
   - `hide_from_suggestions` / `hide_from_requests`
   - `PUT /users/me/call-number`
   A phone hosting the server can't serve clients that use those.
4. **Keymap only applies to the DM/group chat.** Groups route through
   `ChatScreen`, so they're covered — but the QR chat and the sound transport
   send raw text, so "write in my own language" is inconsistent across the app.
5. **Task 24 is stale.** It says image-over-sound is "NOT done… needs an
   SSTV-style encoder". That was written before Overtone: `OvertoneMessage`
   carries typed image/video/file/voice frames and the hub has pickers. The task
   is describing a design decision that was already superseded.

## Approach
- Delete `sonic_audio_controller.dart` + `acoustic_transfer_screen.dart` and its
  widget test. Keep `acoustic_transfer.dart` + `acoustic_transfer_test.dart`.
- Remove `playHoldTime` from `UltrasonicScreen` and from the test that passes it.
- NexusServer: add the two privacy flags to the account record (honoured by the
  suggestions-free server as stored profile fields + returned by /me), and
  `PUT /me/call-number` with a uniqueness check across accounts. Add socket tests
  for both — the server's whole value is that every route is exercised over HTTP.
- Wire `KeymapPrefs.encodeOutgoing` / `decodeIncoming` into the QR chat and the
  sound screen so the setting means the same thing everywhere.
- Rewrite task 24 to state what's actually true.

## Risks
`nexus_server.dart` is large and its tests are strict; add routes beside the
existing ones and extend `_toJson`/`_load` in step or persistence silently drops
the new fields. Verify with the existing 22-test socket suite plus new cases.
Never `dart format lib/` wholesale.

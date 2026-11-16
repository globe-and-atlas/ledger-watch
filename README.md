---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-05T22:18:56-06:00"
---
# Ledger
A Pebble Time2 watchface with large serif time, fine rules, a date row and battery percentage.

- Six palettes: Paper,Cream,Night,Sage,Ice,Blue.
- Custom background,text,accent colors.
- Watch-default,12-hour,24-hour time; AMPM in12-hour mode.
- DateOff,word,ISO,US,EU.
- Actual battery percentage; minute-only updates.

`make test`, `make build`, `make verify`.
Production: dist/Ledger-0.1.0.pbw. Native previews inmedia/. Live: [Ledger](https://apps.repebble.com/1ee890ebe1f942a2aa708f56).

## Public release
https://apps.repebble.com/1ee890ebe1f942a2aa708f56

Version0.1.0. First preview: six-palette native GIF,15.5s loop with2.5–3s holds. Four still previews follow. PublicGIF andPBW bytes verified against local release files.


## Round-compatible release — 0.1.1

Ledger includes native layouts for Pebble Time2 (Emery200×228), original Time Round (Chalk180×180), and Round2 (Gabbro260×260). The rectangular layout and existing settings identities are preserved.

Build: `python3 execution/build.py`, then `python3 execution/verify.py`. Local bundle: `dist/Ledger-0.1.1.pbw`. Native round previews: `media/round/`. Repeatable fixture/capture instructions: [round compatibility QA](knowledge/procedural/round_compatibility.md).

This update is [publicly available](https://apps.repebble.com/1ee890ebe1f942a2aa708f56) with round screenshots. Public PBW bytes and screenshot pixels verify; physical-watch validation remains separate.

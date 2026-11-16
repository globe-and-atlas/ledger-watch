---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-05T22:18:56-06:00"
---
# Build and native QA
- `python3 execution/generate_fonts.py` validates required label glyphs before generating one-bit masks.
- `make test`, `make build`, `make verify`.
- Root-only shared emulator: clean fixture build with LEDGER_FIXTURE=1; AppMessage11000hour11001minute11004battery.
- `python3 execution/capture_native.py --monitor PORT` checks exact numeral/label pixels, visible-ink centering, palettes and boundary values.
- Native screenshots require semantic visual review in addition to equality: two renderers can agree on the same missing-glyph box.
- Clean production must be rebuilt after fixture capture; only production enters release.

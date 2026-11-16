---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-05T22:09:18-06:00"
---
# Build watchface
Generate native masks: `python3 execution/generate_fonts.py`.
Run `make test`, `make build`, `make verify` from root.
Fixtures use LEDGER_FIXTURE=1 after SDK clean; root exclusively owns shared emulator.
Only clean production builds enter dist/release. No publication is authorized in this implementation request.

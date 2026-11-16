---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-05T22:18:56-06:00"
---
# Errors —2026-11-05
## Numeral-only font reused for text labels
Existing GridcoreBook-700.ttf had only digits and colon in its cmap. Reusing it for uppercase labels produced identical missing-glyph boxes, even though generated/native pixel comparisons agreed. Native inspection and independent review caught the semantic defect. Fix: keep working numeral masks, use the full upstream LibreBaskerville variable font at700 for labels, validate every required glyph against .notdef, and add a regression that deliberately substitutes the numeral-only font and must reject it. This promotes coverage validation before rasterization; exact pixel equality alone cannot establish correct glyph meaning.
## Font geometry test respected natural cap margins
Initial stroke continuity test required ink in64rows, including natural empty margins. Fixed to test continuity only within the actual inkbbox, retaining native14:44 review for diagonals.

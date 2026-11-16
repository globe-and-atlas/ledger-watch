---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-05T22:09:18-06:00"
---
# Ledger native watchface
## Contract
- Native Emery200×228, large serif clock, fine rules, date and battery percentage.
- Directive: directives/build_watchface.md.
- Execution: generate_fonts.py,build.py,verify.py,capture_native.py.
- Artifact: dist/Ledger-0.1.0.pbw; native media.
- Public release authorized by Daniel. No remote push. No .env access.
- Root serializes shared emulator use.

## Validation contract
- [x] Native clock uses readable serif numerals.
- [x] Clock ink is horizontally centered.
- [x] Six palettes render.
- [x] Custom colors render.
- [x] Watch-default mode follows watch preference.
- [x]12-hour mode displays AM/PM.
- [x]24-hour midnight displays00.
- [x] Date Off hides date text.
- [x] Word date fits.
- [x] ISO date fits.
- [x] US date fits.
- [x] EU date fits.
- [x] Battery percentage reflects actual charge.
- [x] Settings persist after native relaunch.
- [x] Actual Clay Save sends settings.
- [x] Actual Clay Cancel preserves settings.
- [x] Actual Clay reload sends saved settings.
- [x] Host geometry tests pass.
- [x] Production build excludes fixture overrides.
- [x] Fresh verifier reviews source.
- [x] Fresh verifier reviews native output.

## Master's brief
Primary good: Clarity through a quiet typographic watchface.
Stone removed: proven Clay and build plumbing; only renderer and type geometry are distinct.
Human mark: Daniel decides whether native serif weight preserves the concept.
Non Finito: physical-watch contrast and publication are separate acceptance steps.
Structural weakness: thin serif diagonals may disappear after one-bit rendering.
Myth under test: rasterized Book serif retains counters and diagonal strokes at native size; inspect14:44 and23:59; replace sizing if broken.
Misericord: date widths, settings cancellation and fixture isolation get equal care.
S.D.G.: Give Pebble owners a calm, readable everyday clock.
Feynman gap: native rendering verified; physical-display appearance remains untested.

## Completion
-25nativefixturecases passed.
-2watch-defaultpreferencecases passed.
- Native relaunch persistence matched pixels exactly.
- Clean production built, verified and installed; live screenshot observed.
- Independent source/native review passed.
- Initial implementation was local; public release is tracked below.

## Public release —2026-11-05
Authorization: Daniel approved publishing this watchface with the palette GIF as first preview.
- [x] GIF has six native200×228frames.
- [x] GIF frame pixels match source captures.
- [x] Default palette is first.
- [x] Each palette holds at least2500ms.
- [x] Public listing exposes0.1.0.
- [x] Public first preview is the GIF.
- [x] Public GIF matches local bytes.
- [x] Public PBW matches release archive bytes.
- [x] Four public stills match local RGB pixels.
- [x] Fresh verifier accepts release evidence.

## Round compatibility — 2026-11-06
- [x] Emery remains a build target.
- [x] Chalk is a build target.
- [x] Gabbro is a build target.
- [x] The UUID is preserved.
- [x] Existing settings key mappings are preserved.
- [x] Native Chalk layout passes visual review.
- [x] Native Gabbro layout passes visual review.
- [x] Clean production PBW contains three native binaries.
- [x] Existing host/settings checks pass.
- [x] Fresh independent review passes.
No store publication is authorized by this compatibility request.

## Store round update — 2026-11-06
- [x] Publish the verified three-platform production update.
- [x] Preserve the current animated preview.
- [x] Add native screenshots for Chalk.
- [x] Add native screenshots for Gabbro.
- [x] Verify the public download matches the production artifact.
- [x] Verify public round screenshot pixels.
- [x] Fresh independent public-proof review passes.

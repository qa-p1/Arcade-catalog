# Arcade overhaul

On GitHub this folder is `qa-p1/Arcade-catalog` › `dev/overhaul/`. Paths in the specs like `AUDIT/…` are
relative to this folder.

One spec per app. Each spec is self-contained: carrying it out leaves that app fully on the Arcade standard,
cleaned up, and (where the audit found any) with its broken features fixed. Specs have no phases and can be
done one at a time, in the order below.

- `STANDARD.md`: the shared UI and project standard every spec points to.
- `TOOLS.md`: first. Builds the design kit in Arcade Link and moves Tools onto it, so Tools becomes the
  living reference for every other app.
- Then the remaining apps, in the order below.
- `AUDIT/`: the evidence the specs are based on, from the read-only audit of 2026-10-27 and the re-checks on
  2026-10-28: findings, keep lists, hygiene, test inputs (`fixtures/`, without the large video and audio
  samples) and a selection of screenshots: the Tools 0.3.8 reference set and the key Box screens.

| # | Spec | App | Toolkit | Why this position |
|---|---|---|---|---|
| 1 | TOOLS.md | Arcade Tools + design kit in Arcade Link | Tauri + Svelte (+ Rust overlay) | Builds the kit everything else uses |
| 2 | BOX.md | Arcade Box | Tauri + Svelte | Worst: 9 verified bugs, including the broken global shortcut; reuses the CSS kit straight away |
| 3 | CLIPBOARD.md | Arcade Clipboard | Flutter + Rust | Next most verified issues (Flutter default icon, debug-signed Android, retracted dependency); builds the Flutter widget set |
| 4 | LOOK.md | Arcade Look | Tauri + TypeScript | Reuses the CSS kit |
| 5 | FIND.md | Arcade Find | Rust (softbuffer overlay + egui settings) | Builds the egui widget set |
| 6 | LENS.md | Arcade Lens | Rust (egui) | Reuses the egui widgets straight after |
| 7 | SHELF.md | Arcade Shelf | Qt QML | Builds the QML component set |
| 8 | WHEEL.md | Arcade Wheel | Qt QML | Reuses the QML components straight after |

Every spec after TOOLS.md depends on the Link `v0.4.0` design kit. The first app of each toolkit also builds
that toolkit's component set in Link, and the next app of the same toolkit follows straight after.

Verification: every bug, cleanup item and project-standard gap in the specs was re-checked on 2026-10-28
against the released builds, GitHub main, CI logs and the source before it went into a spec. Box B1–B9 were
re-run with the released 0.3.5. Three audit claims were wrong and were corrected or dropped:
- Look's `--wave` CSS variable is used;
- the Shelf/Wheel layout warnings are hidden dividers, not clipping;
- the Link e2e development-install skips have their own cause.
The audit's "failures" in random, regex, hash and password were checker mistakes and are not in any spec.

Audit coverage: Box (core tools, video/audio/web/developer groups, shortcut) and the project/hygiene review
of all 10 repos were completed. The owner stopped the per-app real-use testing early, so each spec's
acceptance check includes using that app's features with real inputs and fixing what fails inside the same
spec.

## Decisions (owner, 2026-10-27)

- Keep every app's toolkit; share one design system implemented per toolkit (CSS, QML, Flutter, Rust).
- Shared neutrals and status colours; each app keeps its own accent. Tools keeps green; Find moves to lime
  and Shelf to fuchsia so all accents are distinct.
- Two templates: the window shell (from Tools) and the overlay spec.
- Themes follow the system with a Light / Dark / System override. Inter bundled everywhere.
- Design kit lives in Arcade Link `design/`.
- Specs describe the work only (what, where, how to verify); not who does it.
- Box's spec includes its verified broken features; every other app's spec includes its verified broken
  features too, plus UI and standardization.
- Cleanup removes only what is provably unused and can't break CI, packaging, Link or other apps.
- Box's old local branch `fix/ui-and-tools` was deleted (2026-10-28). Its work is kept as patches in
  `AUDIT/box-salvage/`; the calculator/units patch is reused in BOX.md.

## What the standard makes identical across apps (index into STANDARD.md)

| Area | Where |
|---|---|
| Colours (shared neutrals + one accent per app), Inter font, type scale, spacing, radii, shadows, motion, icons | §1–4 |
| Components and their states (buttons, inputs, switches, lists, cards, badges, key chips, notices, empty/loading/error states, toasts, dialogs, menus, tooltips, sidebar) | §5 |
| Controls with one behaviour: shortcut recorder, settings rows, theme picker, sliders, search field, file/output pickers, result panel, context menus, delete confirmation, onboarding, notifications, keyboard conventions, window size/position | §5.1 |
| Window layout (Tools shell), settings sections and order, Connected apps page, About, install prompt, tray menu | §6 |
| Quick-panel layout (search field, rows, selection, footer key hints) | §7 |
| Names, one tagline per app, one app-icon family (launcher, tray, sidebar, README), window titles, versions, tooltips, wording rules, settings apply at once | §8 |
| Fixed words, error wording, size/date/duration formats, "Copied" feedback, no blank flash on open, drag and drop, menus, empty-state wording, close-doesn't-quit, start-in-background, tray clicks, overlay closing, second launch | §8.1 |
| Accessibility | §9 |
| Repo layout, scripts, lint/format, toolchains, CI and release flow, command-line flags, logs/diagnostics, single instance, developer docs, identifiers and data folders (with migration), desktop entries, default shortcuts table, tags and branches, clean code and safe cleanup | §10 |
| Keep useful app-specific features (each spec has a Keep list) | top of STANDARD.md |

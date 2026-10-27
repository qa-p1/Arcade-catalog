# Spec: Arcade Lens

**Outcome:** every Lens surface uses the Arcade design kit with Lens's teal accent and works in both light and
dark themes. That covers the selection overlay, action palette, annotate, pins, measure, history, settings and
the install prompt. Every verified Lens bug is fixed, the repo is cleaned up and matches the project standard,
and a new Lens release ships.

Prerequisite: Spec 1 (`TOOLS.md`). Arcade Link `v0.4.0` with `design/` must exist. Read `STANDARD.md` first.
Evidence: `AUDIT/keep.md` and `AUDIT/hygiene-and-dev-standard.md` (Lens sections; the audit was stopped before it took screenshots of this app).

## Starting point

| | |
|---|---|
| Repo | `qa-p1/Arcade-lens`, main at `c862102` on 2026-10-28 (release 0.3.4). Start from current main. |
| Toolkit | Rust, eframe/egui 0.33 + tiny-skia; GUI in `crates/arcade-lens/src/gui/` |
| Link | root `Cargo.toml:19` pins `rev = "4c75f3a…"` (older than the other apps) |

Today's UI vs. the standard:
- **Colours:** `gui/theme.rs` hard-codes a dark-only zinc palette with a **violet** accent
  (`ACCENT 139,92,246`, `ACCENT_SOFT 167,139,250`). Violet is Box's colour; Lens is teal. On top of that there
  are 37 literal colours across `src/`, and `apply_style` always starts from `Visuals::dark()`. There is no
  light theme.
- **Type:** egui's default font. Sizes run 10.5, 11, 11.5, 12, 12.5, 13.5, 16 and 18, several of them below
  11.5. Section labels are uppercase ("CHAINS").
- **Settings:** a viewport (`gui/settings_view.rs`) with 10 sections: General, Shortcut, Actions, Recognizers,
  Chains, Services, Plugins, Connected apps, Privacy, About. There is an explicit **Save** button, while the
  other apps apply changes at once.
- **Overlay surfaces:**
  - `gui/overlay.rs`: frozen frame → selection → palette;
  - `gui/panels.rs`: header, primary, expanded, confirm, choice and result panels;
  - `gui/annotate.rs`, `gui/pins.rs`, `gui/measure.rs`;
  - `gui/history.rs`: opt-in history.

## Keep (do not remove or flatten)

Selection on a frozen frame; the progressive, spatial palette; chains; services/providers; annotate; pins (move, zoom, opacity); measure mode; recording; OCR through the shared Tesseract engine; opt-in history with masked secrets; safety classes (online / asks first).
These get kit styling only. Everything in `AUDIT/keep.md` › "Lens — Keep" is also kept. It lists the capabilities with their sources.

## Work

### 1. Adopt the kit

- Point `arcade-link` at `tag = "v0.4.0"` (features plus `design`, `design-egui`) and refresh `Cargo.lock`.
- If no egui component set exists in Link `design/` yet (because Find hasn't been done), build it in Link now,
  as described in `FIND.md` §1, tag Link `v0.4.x`, and use that tag.
- `gui/theme.rs` keeps its helper functions but takes every colour from
  `arcade_link::design::palette(theme, "arcade.lens")`:
  - accent teal `#1e7e72` / `#2bb3a3`;
  - `SUCCESS` → `ok`, `DANGER` → `danger`;
  - `EXTERNAL` ("leaves this computer") becomes `warn` with the ↗ marker.
- `apply_style` → `arcade_link::design::apply_egui(ctx, theme, "arcade.lens")`. Add a Theme setting (System / Light /
  Dark) to General, and switch it live.
- Inter loaded through the kit for every viewport; mono stays the system mono. Type snaps to the kit scale:
  nothing below 11.5, so 10.5/11 → 11.5, 13.5 → 13 (or 14 for palette rows), 18 → 16 (title-sm). Section labels
  move to sentence case `caption`, so "CHAINS" becomes "Chains".
- `key_badge` and `enter_icon` → the kit key chip (11.5/500, 22 px high, `line-strong` border with a 2 px
  bottom). Icons drawn by hand with line segments move to the kit icon paths (`design::ICONS`, tiny-skia/egui
  shapes).

### 1b. Shared conventions (STANDARD §8.1, §10)

- **Words:** every UI string meets STANDARD §8.1:
  - fixed words ("Settings", "Start at login", "Quit Arcade Lens", "Install", "Show in folder");
  - error wording "Couldn't …";
  - one tagline, no split-weight app name, window titles "<Thing> — Arcade Lens".
- **Formatting:** sizes, dates, durations and counts go through the kit's format helpers. No local formatters
  stay.
- **Identifiers and folders:** move to `dev.arcade.Lens` and `arcade/lens/` folders, with the verified migration in
  STANDARD §10. Today: `~/.config/arcadelens` (`settings.toml`), `~/.local/share/arcadelens`, `packaging/linux/arcade-lens.desktop`.
- **Desktop entry:** contents per STANDARD §10.
- **App icon family:** replace `packaging/icons/*`, the README logo with the kit-generated set (STANDARD §8, brand mark and app icons). The tray icon becomes the monochrome glyph.
- **Default shortcut:** follows the STANDARD §10 table. Change: none. Existing users keep theirs.
- **Behaviour:**
  - closing a window doesn't quit;
  - start at login goes to the background;
  - tray left click opens, right click shows the menu;
  - a second launch focuses;
  - overlays close on Esc and on focus loss, except Keep items.
- **Command line:** adds whatever STANDARD §10 lists and the app lacks. Existing flags keep working.

### 2. Surfaces

Every control in this app uses its STANDARD §5.1 version: shortcut recorder, settings rows, theme
picker, slider rows, search field, file/output pickers, result panel, context menus, confirm dialogs,
onboarding, keyboard conventions and window behaviour. Any custom variant this app has today is replaced,
not restyled.

**Selection overlay** (`overlay.rs`, `measure.rs`):
- The frozen frame stays. The dim becomes `scrim`.
- Selection outline: 1.5 px accent with white/black halo for contrast on any image.
- Size label: kit key-chip style in mono.
- Measure guides: accent lines, with labels as chips.
- The crosshair and handles follow the kit sizes (8 px handles, radius 2).

**Action palette and panels** (`panels.rs`), Template B:
- **Panel:** `panel` fill, 1 px `line`, radius 12, `shadow-pop`, 8 px padding.
- **Header:**
  - the recognized kind as a badge, plus a short summary;
  - the filter field, 44 px when the palette is expanded.
- **Rows:**
  - 40 px: glyph, label, then trailing key chip and safety marker;
  - the safety marker is `warn` "online" for external and `danger` "asks first" for dangerous, as a badge
    instead of coloured text;
  - selected row: `accent-soft` with a 2 px accent bar.
- **Group labels** ("Chains", "Actions", "Connected apps"): `caption` muted.
- **Confirm panel:**
  - kit dialog layout (`title-sm`, body, consequences as a list);
  - buttons "Cancel" (secondary, with Esc chip) and the action named as a verb (primary, or destructive when
    dangerous).
- **Choice panel:** list rows with radio semantics.
- **Result panel:** a copyable mono block for text, plus "Copy", "Save…", "Pin" and "Send to…" as buttons.
- **States:**
  - "Analyzing…" uses the kit skeleton row;
  - the missing-Tesseract message becomes a `warn` notice with an "Install text recognition" action (it goes to
    Settings › Recognizers, which has the download);
  - an empty filter shows "No matching actions".
- **Footer hint bar:** "↵ Run", "Tab More actions", "Esc Close".
- **Placement:** the logic in `place`/`place_side` stays.

**Annotate toolbar** (`annotate.rs`):
- A floating Template B bar: tool buttons are 32 px kit icon-only buttons, and the active tool uses
  `accent-soft` + accent icon.
- Pen colours are Lens's documented content palette (kept as is, listed in one const block).
- "Copy", "Save", "Pin" and "Done" sit at the end; "Done" is primary.

**Pins** (`pins.rs`):
- Border is 1 px `line`, radius 10 and `shadow-pop`.
- On hover, a mini toolbar shows close, copy and opacity (kit icon buttons).
- Zoom and opacity readouts are toasts.

**History** (`history.rs`):
- A Template A window titled "History": a list of rows with a 52 px thumbnail, a summary and the time.
- The empty state reads "History is off" with a "Turn on in Privacy" button, or "Nothing yet" when history is
  on but empty.

**Settings window**, Template A in egui with the kit components:
- **Saving:** changes apply at once (STANDARD §8). The Save button goes away. Validated fields (the shortcut
  recorder, provider keys, chain editor) apply on Enter or blur and show an inline `danger` message when
  invalid.
- **Sections, in the standard order:**
  1. **General:** Theme, Start at login, date reading order, applications-menu entry status.
  2. **Shortcuts:** renamed from "Shortcut". The global shortcut with rebind, the conflict notice and the
     Hyprland or unsupported-Wayland explanation (as a notice), plus a read-only list of palette keys.
  3. **Actions:** rows with switches and safety badges.
  4. **Text recognition:** renamed from "Recognizers". Tesseract status, languages, "Download".
  5. **Chains:** list + editor. "Delete chain" is a `danger` button with a confirm dialog.
  6. **Services:** providers, keys masked.
  7. **Plugins:** list, with the empty state "No plugins installed".
  8. **Privacy:** history switch, where data is stored, "Clear history" (destructive, confirm).
  9. **Connected apps:** the shared Link page.
  10. **About:** version, channel, "Updates are managed by Arcade Tools", logs folder, copy diagnostics, user
      guide, licences.
- Brand block: mark tile + "Arcade Lens" + the one-line description "Select anything on screen and act on it."
  This replaces the 11 px subtitle.

**Install prompt** (`app/installer_ui.rs`): kit dialog, with the same copy, options and order as Tools'.

**Tray** (`app/trayhost.rs`): sentence case and the standard order: open/capture, Settings, History, separator,
Quit.

### 3. Verified bugs

The 2026-10-27 audit was stopped before its Lens tester ran, so no Lens feature was checked by use. Its source review is complete. As part of this spec, use every Lens feature listed in `AUDIT/keep.md` › Lens with real inputs (the acceptance check below). Fix whatever fails here, with a regression test, before release.

Known limits (documented in STATUS, not bugs to fix here):
- macOS accessibility window commands, share sheet and UI inspection (`crates/lens-platform/src/macos_native.rs`).
  Keep the graceful "not available on this platform" handling.

### 4. Cleanup

Leave as they are:
- the four duplicate helper pairs under `scripts/` and `tools/` (provenance-pinned and referenced);
- the isolated and real-peer tests in `crates/lens-actions/tests/arcade.rs`.

Fix:
- the two broken links in `packaging/windows/README.md`.

Delete merged remote branches (including `claude/*`).

### 5. Project standard

- **Outdated text:** `docs/STATUS.md` still names v0.3.3 as the latest release (v0.3.4 is out). Update it
  in this spec's release step.
- Add `rust-toolchain.toml` (1.88).
- Add the main `LICENSE-MIT` and `LICENSE-APACHE` files (Cargo declares MIT OR Apache-2.0, and no licence
  text is tracked today).
- Lens CI auto-tags when main's version changes. Move to the shared `tag.yml` → `release.yml` flow, keeping
  the portable Windows asset excluded from Tools installs.
- Developer docs go to `docs/dev/`.
- `scripts/check` = what CI runs.

### 6. Docs and release

- Retake the README and `docs/user/images` screenshots: palette over a capture, annotate, settings, in light and
  dark.
- `docs/STATUS.md` dated entry; CHANGELOG entry; minor version bump.
- 3-OS CI green → merge → Lens's release (CI auto-tags when main has a new version) → check that Tools updates
  Lens.

## Acceptance

- [ ] No colour literal outside `theme.rs`'s kit mapping and the annotate pen palette. No font size outside
      the kit scale. Inter in use. Light and dark both work and switch live.
- [ ] The selection outline, labels and palette stay readable over very light and very dark screenshots, in
      both themes.
- [ ] Shortcut → palette visible within Lens's existing perf budget. Measure, annotate, pin, OCR, chains and
      Link sends (Box, Shelf, Clipboard, Look) all still work with real captures.
- [ ] Settings apply at once, and an invalid shortcut or chain shows an inline error without losing the user's
      other changes.
- [ ] Every item in §3 re-checked on the released build. 3-OS CI is green and the release is published.

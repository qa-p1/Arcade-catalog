# Spec: Arcade Look

**Outcome:** Look's preview window and every other surface use the Arcade design kit with Look's own blue
accent, settings move into a standard settings window, every verified Look bug is fixed, the repo is
cleaned up and matches the project standard, and a new Look release ships.

Prerequisite: Spec 1 (`TOOLS.md`) is done, so Arcade Link `v0.4.0` with `design/` exists.
Read `STANDARD.md` first. Evidence: `AUDIT/keep.md` and `AUDIT/hygiene-and-dev-standard.md` (Look sections; the audit was stopped before it took screenshots of this app).

## Starting point

| | |
|---|---|
| Repo | `qa-p1/Arcade-look`, main at `c31b820` on 2026-10-28 (release 0.3.5). Start from current main. |
| Toolkit | Tauri 2 + plain TypeScript (no framework), Vite; Rust backend in `src-tauri/src` |
| Link | `src-tauri/Cargo.toml:47` pins `rev = "3bbbc5d…"`, features `install`, `trayhost` |
| Windows | one frameless window `main` (`src-tauri/src/app.rs:323-362`, `decorations(false)`) holding the custom title bar, the preview stage, the info panel, toasts, modals, the welcome screen and (drawn into the stage) the settings |

Today's UI vs. the standard:
- **Colours:** its own palette (`src/styles/app.css:1-80`) with a **violet** accent `#6d5dfc` / `#9b8cff`, which is
  Box's colour. Look's accent is blue. There are 126 hex literals across `src/**/*.css|ts`, plus a second
  palette in `src/lib/arcade.css` + `src/lib/arcade-tokens.json` (the old integration tokens).
- **Type:** system font stack. Sizes 10.5, 11, 11.5, 12, 12.5, 14, 14.5, 16, 22 and 24 px (some below the 11.5
  minimum).
- **Theme:** dark only via `prefers-color-scheme` + `data-theme`. The Theme setting exists (System / Light / Dark).
- **Settings:** shown inside the preview stage (`src/app.ts:502`, `src/lib/settings.ts`), with sections
  General, Previews, File manager and Advanced ("Edit config file", "Open plugins folder", "Quit Arcade Look").
  Connected apps (`src/lib/connected-apps.ts`) is appended to it.

## Keep (do not remove or flatten)

The frameless window with its own title bar and window controls; back/forward history; the info panel; every viewer and the fallback chain to info card and hex view; plugins; file-manager integration (GNOME Files, Dolphin, Nemo, Explorer, Finder); idle webview release; the `A` actions strip; remembered size and opening on the cursor's monitor.
These get kit styling only. Everything in `AUDIT/keep.md` › "Look — Keep" is also kept. It lists the capabilities with their sources.

## Work

### 1. Adopt the kit

- `scripts/sync-design.py` copies `arcade.css`, `icons.ts`, the fonts and the glyphs from Link `v0.4.0` into
  `src/design/`, with hashes in `VENDORED.md` (checked by the existing `scripts/check-vendored.py`).
- Set `<html data-app="arcade.look">`. The accent becomes `#1268f4` (light) / `#69a0f8` (dark).
- In `src/styles/app.css` and `src/viewers/*.css`:
  - replace the token block (`app.css:1-80`) and every literal colour with kit tokens;
  - Look-only variables (`--checker`, `--paper`, `--titlebar`) stay, defined from kit values;
  - the syntax colours `--hl-*` become Look's documented content palette, kept in one block with a comment,
    with both themes checked for ≥ 4.5:1 on `sunken`.
- Remove `src/lib/arcade.css` and `src/lib/arcade-tokens.json`; the actions strip and Connected apps use
  the kit. `src/lib/arcade-glyphs.ts` and `src/lib/icons.ts` use the kit icon map. File-kind badges
  (`kindBadge`) keep their per-kind colours as content palette.
- Inter via `@font-face` from `src/design/fonts`; the mono stack per STANDARD §3. Type snaps to the kit
  scale: nothing below 11.5 px, and 14.5 → 14, 22/24 → 21 (welcome display 26).
- Point `arcade-link` at `tag = "v0.4.0"`.

### 1b. Shared conventions (STANDARD §8.1, §10)

- **Words:** every UI string meets STANDARD §8.1:
  - fixed words ("Settings", "Start at login", "Quit Arcade Look", "Install", "Show in folder");
  - error wording "Couldn't …";
  - one tagline, no split-weight app name, window titles "<Thing> — Arcade Look".
- **Formatting:** sizes, dates, durations and counts go through the kit's format helpers. No local formatters
  stay.
- **Identifiers and folders:** move to `dev.arcade.Look` and `arcade/look/` folders, with the verified migration in
  STANDARD §10. Today: `~/.config/arcade-look`, `~/.local/share/app.arcadelook`.
- **Desktop entry:** contents per STANDARD §10.
- **App icon family:** replace `assets/icon.svg`/`icon.png`, `src-tauri/icons/*`, the README logo with the kit-generated set (STANDARD §8, brand mark and app icons). The tray icon becomes the monochrome glyph.
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

**Preview window (Template B, viewer variant).** The frameless window and custom title bar stay; the owner
uses Look daily on Hyprland.
- **Title bar:** 44 px on `bg`, bottom border `line`.
  - Back/forward, kind badge, name (body 500) + meta (small muted), then the actions.
  - Actions are kit `btn ghost icon-only` 30 px; each tooltip shows the action and its key as a key chip.
  - Window controls stay at the far right.
- **Stage:** `bg` behind content; documents on `panel` "paper". The checkerboard for transparency uses
  `sunken` / `hover`.
- **Info panel:** kit list rows (label small muted, value body), section heads as STANDARD §5, mono for paths
  and hashes, copy buttons as ghost icon buttons.
- **Shared components:** toasts, modals, loading and drop overlay use the kit toast, dialog, skeleton/progress
  and an empty state with dashed border. Keep their current behaviour.
- **Viewers:** each viewer's own chrome uses kit controls and tokens. Covers archive tree, folder grid, table
  grid, PDF toolbar, media controls, font sample, code gutter, notebook cells, slides and JSON tree.
  Equal-size page tool buttons (32 px), segmented control for view modes, and no custom scrollbars beyond the
  kit's.
- **Welcome screen:** kit empty state. App mark (52 px tile), "Arcade Look" (display), "Press Space, see
  anything", the file-manager integration status as badges, and buttons "Set up file manager integration"
  (primary) and "Open a file…" (secondary).

**Actions strip (`A`).**
- Kit menu: rows with app glyph, label and key chip.
- Each target app's Link badge uses that app's accent; nothing else does.
- Empty state: "No connected apps can take this file".

**Settings window (Template A).**
- Settings leave the preview stage and open in a separate window, `settings`: 760×560, minimum 720×520,
  native decorations. It is created on demand and destroyed on close, so idle memory doesn't grow. Measure
  idle RSS before and after, which must be within 5 MB.
- Opened from the tray, the title-bar menu and `Ctrl+,`.
- Sidebar sections:
  1. **General:** Theme, Start on login, "Keep Arcade Look ready in the background".
  2. **Shortcuts:** the global shortcut (if any) with rebind, plus a read-only in-app list (Space/Esc close,
     ←/→ next/previous, Enter open, Ctrl+R show in folder, Ctrl+C copy path, I info, A actions,
     Alt+←/→ back/forward). Read it from the same source as Tools' shortcut sheet so they never differ.
  3. **Previews:** autoplay media, show hidden files.
  4. **File manager:** integration status + set up/repair.
  5. **Plugins:** open plugins folder, list of installed plugins with status.
  6. **Connected apps:** the shared Link page.
  7. **About:**
     - version and channel;
     - "Updates are managed by Arcade Tools";
     - "Edit config file", "Open logs folder", "Copy diagnostics", user guide and licences.
     - "Quit Arcade Look" stays in the tray menu, and also sits here as the last item.

**Self-install prompt** (`src-tauri/src/installer_ui.rs`): same copy, options and button order as Tools'
self-install dialog (STANDARD §8).

**Tray menu** (`src-tauri/src/tray.rs`): sentence case, "Open Arcade Look", "Settings", separator, "Quit
Arcade Look".

### 3. Verified bugs

The 2026-10-27 audit was stopped before its Look tester ran, so no Look feature was checked by use. Its source review is complete. As part of this spec, use every Look feature listed in `AUDIT/keep.md` › Look with real inputs (the acceptance check below). Fix whatever fails here, with a regression test, before release.

Known from the source review: the copied `src-tauri/windows/README.md:26,27` has two broken relative links (fixed in §4).

### 4. Cleanup

Keep: the `--wave` CSS variable (`src/viewers/media.css:120`). The audit called it unused, but
`src/viewers/audio.ts:78` reads it to colour the waveform. When moving to kit tokens, define it from a kit
token and keep the name.

Move to `docs/dev/history/` instead of deleting (external links may point at them):
- `docs/hero.webp` and the 12 `docs/screenshots/*.webp`, which the README no longer uses.

Fix:
- the two broken links in `src-tauri/windows/README.md`.

Leave as they are:
- the duplicate pinned `validate_shortcuts.py`;
- the real-peer tests `src-tauri/tests/link_consumer.rs` and `tests/real_shelf.rs` (deliberate; record
  which runner executes them).

Delete merged remote branches.

### 5. Project standard

- **Early-days docs:** `docs/PLAN.md` (the original plan, 10 Oct) moves to `docs/dev/history/`.
- Add `rust-toolchain.toml` (1.88) and `.nvmrc` (22, as CI uses), plus Prettier for the TypeScript
  frontend (there is no formatter or linter today beyond `tsc`).
- Releases currently start from the main CI (`workflow_run`), and there is a separate `build.yml`. Move to
  the shared `tag.yml` → `release.yml` flow.
- Developer docs (`PLAN.md`, `PLUGINS.md`, `arcade-link.md`) go to `docs/dev/`; `PLAN.md` goes to
  `docs/dev/history/`.
- One version source.
- `scripts/check` = what CI runs.

### 6. Docs and release

- Retake `docs/user/images/*.png` and the README preview image (light, 1100×760, the getting-started
  Markdown preview as today) plus a dark one.
- `docs/STATUS.md` dated entry; `CHANGELOG.md` entry; version bump (minor).
- 3-OS CI green → merge → Look's release workflow → check Tools updates Look from 0.3.5.

## Acceptance

- [ ] No colour literals outside `src/design/` and the documented content palette; no font size outside the
      kit scale; Inter in use.
- [ ] Light, dark and system themes switch live in the preview and settings windows.
- [ ] Every viewer type opened with a real sample file in both themes, at 720×520 and full screen: no
      overflow, controls are kit controls (`scripts/make-fixtures.py` + `scripts/verify-rendering.py`
      cover the file types).
- [ ] Settings window opens, all sections work, and closing it returns idle memory to the pre-open level ±5 MB.
- [ ] Actions strip, Connected apps and file-manager integration still work with the other apps
      (`scripts/verify-link.py`, Link `tools/e2e.py`).
- [ ] Every item in §3 re-checked on the released build; 3-OS CI green; release published.

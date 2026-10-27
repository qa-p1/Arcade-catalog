# Spec: Arcade Find

**Outcome:**
- Find's launcher overlay, settings window and install prompt use the Arcade design kit with Find's new
  lime accent.
- Every verified Find bug is fixed.
- The repo is cleaned up and matches the project standard.
- A new Find release ships.

**Prerequisite:** Spec 1 (`TOOLS.md`): Arcade Link `v0.4.0` with `design/` exists. Read `STANDARD.md` first.
**Evidence:** `AUDIT/keep.md` and `AUDIT/hygiene-and-dev-standard.md` (Find sections; the audit was stopped before it took screenshots of this app).

## Starting point

| | |
|---|---|
| Repo | `qa-p1/Arcade-Find`, main at `f408348` on 2026-10-28 (release 0.4.3). Start from current main. |
| Toolkit | Rust. Overlay: winit + softbuffer + tiny-skia + cosmic-text (`crates/arcade-find/src/ui/`). Settings and install prompt: eframe/egui, run as separate processes only while open (`settings_ui.rs`, `installer_ui.rs`) |
| Link | `crates/arcade-find/Cargo.toml:26` pins `rev = "4c75f3a…"` (an older commit than the other apps) |

What the UI looks like today:
- Palette: `src/theme.rs` copies Link's old integration tokens, with the accent `ACCENT = 0x22C55E` (green, which
  clashes with Tools). It adds its own extras (`highlight 0x4ADE80`, selections as accent alpha).
- Overlay metrics (`src/ui/model.rs:291-296`):
  - width 680, search bar 58, row 52, radius 14, shadow 0;
  - text sizes in `src/ui/render.rs`: 11.5, 12, 12.5, 13, 13.5, 14, 14.5 and 18.
- Settings window (egui):
  - a 170 px left nav with pages General, Locations, Shortcut, Index, Connected apps and About;
  - egui default widgets (checkboxes, CollapsingHeader) and egui's default font;
  - visuals from `apply_visuals` at `settings_ui.rs:109`.
- Tray (`src/tray.rs`) items: "Open Arcade Find", "Open Settings", "Rescan index", "Restart Arcade Find",
  "Quit Arcade Find".

## Keep (do not remove or flatten)

The opaque fallback where the compositor can't do transparency; settings as a separate process (no resident GPU context); content search with ripgrep (`/`); multi-select; dragging results out; recent and pinned; skipping network mounts; the terminal command; Rescan/Restart from the tray.
These get kit styling only. Everything in `AUDIT/keep.md` › "Find — Keep" is also kept. It lists the capabilities with their sources.

## Work

### 1. Adopt the kit

- Point `arcade-link` at `tag = "v0.4.0"` with features `design` and `design-egui`, then refresh `Cargo.lock`.
- `src/theme.rs` keeps the `Palette` API the renderer uses, but builds it from
  `arcade_link::design::palette(theme, "arcade.find")`:
  - `panel`, `line` (border/separator), `text`, `muted`, `faint`, `danger` and `accent` (lime `#517e0e` / `#84cc16`);
  - `selection = accent-soft`, `selection_multi` = half of that;
  - `highlight` (matched characters) = accent, with weight 600 instead of a second green;
  - `text_selection` = accent at 35 %.
- Load Inter from `arcade_link::design::inter_font_bytes()` into the cosmic-text `FontSystem` as the first
  family, with system fonts as the fallback (CJK and emoji).
- If no egui component set exists in Link `design/` yet (Lens hasn't been done), build it now in Link, from
  STANDARD §5 for egui:
  - sidebar nav, page head, section head, list + row (title / subtitle / trailing control);
  - switch, buttons (default/primary/ghost/danger, sm, icon-only), text input, select, segmented;
  - badge, notice, key chip, empty state, toast.

  Tag Link `v0.4.x` and use that tag here.

### 1b. Shared conventions (STANDARD §8.1, §10)

- **Words:** every UI string meets STANDARD §8.1:
  - fixed words ("Settings", "Start at login", "Quit Arcade Find", "Install", "Show in folder");
  - error wording "Couldn't …";
  - one tagline, no split-weight app name, window titles "<Thing> — Arcade Find".
- **Formatting:** sizes, dates, durations and counts go through the kit's format helpers. No local formatters
  stay.
- **Identifiers and folders:** move to `dev.arcade.Find` and `arcade/find/` folders, with the verified migration in
  STANDARD §10. Today: `~/.config/arcade-find`, `~/.local/share/arcade-find`, `packaging/linux/arcade-find.desktop`.
- **Desktop entry:** contents per STANDARD §10.
- **App icon family:** replace `assets/logo.svg`, the exported icons (`--export-icon`), the README logo with the kit-generated set (STANDARD §8, brand mark and app icons). The tray icon becomes the monochrome glyph.
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

**Launcher overlay (Template B, launcher variant):**
- Panel: width 680, radius 12 (from 14), 1 px `line` border, `shadow-pop` where the compositor allows
  transparency. Where it doesn't, keep the opaque square fallback (`radius: 0`), as today.
- Search field: 56 px, 18 px input text, a leading search icon from the kit icon set and a trailing mode
  badge (e.g. "Content" when `/` content search is active).
- Rows: 52 px two-line rows (name 14/500, path 12 muted, meta 12 faint on the right). Selection is an
  `accent-soft` fill with a 2 px accent leading bar; multi-select uses a lighter fill and a check glyph.
- Section labels (Recent, Pinned, Files, Folders): `caption` 11.5/500 muted, sentence case.
- Footer hint bar (28 px): "↵ Open", "Ctrl+↵ Show in folder", "Tab Actions", "Esc Close", using the kit key-chip
  metrics. Use the actual bindings from `src/ui/keys.rs`. The per-row `hint` text (render.rs:419-440) moves to
  key chips.
- Empty, loading and error states:
  - "Type to search your files";
  - "Indexing… 12,345 files" with a progress line;
  - "No matches for "…"" with "Search inside files (/)";
  - index error as a `danger` notice with "Open settings".
- Toasts (`ToastKind`): kit toast style, bottom of the panel.
- All sizes come from kit constants (`size`, `type`, `radius`). There are no font sizes outside the scale:
  13.5 and 14.5 become 14, and 18 stays only for the launcher input.

**Settings window (Template A, egui):**
- `apply_visuals` is replaced by `arcade_link::design::apply_egui(ctx, theme, "arcade.find")`, which follows
  the Theme setting live.
- Layout:
  - 212 px sidebar with the brand (mark tile + "Arcade Find"), nav items 34 px with icons, and a footer with
    "Version x.y.z";
  - content max 980 px with a page head (title + one-line description).
- Pages, in the standard order:
  1. **General**: Theme (System / Light / Dark), Start at login, show recent and pinned on open, show hidden
     files, rows shown / growing up to, content search (ripgrep), terminal command. Booleans are switches
     in list rows, not checkboxes.
  2. **Shortcuts**: "Open Arcade Find" rebind with conflict warning ("Usually used by …" as a `warn` notice),
     plus a read-only list of the overlay keys (same source as Tools' shortcut sheet).
  3. **Locations**: folders to index (list rows with remove buttons + "Add folder"), skip names, skip folders,
     skip network drives.
  4. **Index**: status (files, last scan, size) as rows, "Rescan now", errors as notices. It refreshes every 2 s
     while open, as today.
  5. **Connected apps**: the shared Link page.
  6. **About**: version, channel, "Updates are managed by Arcade Tools", logs folder, copy diagnostics, user
     guide, licences, "Restart Arcade Find".
- Save behaviour is unchanged: saved at once, and the running instance reloads.

**Install prompt (`installer_ui.rs`):** kit dialog layout and the same copy, options and button order as
Tools' self-install dialog.

**Tray:** "Open Arcade Find", "Settings" (from "Open Settings"), "Rescan index", separator, "Restart Arcade Find",
"Quit Arcade Find".

### 3. Verified bugs

The 2026-10-27 audit was stopped before its Find tester ran, so no Find feature was checked by use. Its source review is complete. As part of this spec, use every Find feature listed in `AUDIT/keep.md` › Find with real inputs (the acceptance check below). Fix whatever fails here, with a regression test, before release.

Known unfinished, from source and STATUS:
- **IME input:** composed text (Chinese, Japanese, Korean or accented dead keys) can't be typed into the
  search field. Winit key events are consumed without `Ime::Commit` handling (`crates/arcade-find/src/ui/desktop.rs:377`), and the
  layer-shell text-input protocol isn't used.
- *Fix:* handle `Ime::Preedit`/`Commit` on the winit path and `zwp_text_input_v3` on layer-shell.
- *Check:* type "café" with a dead key and "日本" with fcitx5 on Hyprland.

### 4. Cleanup

Delete merged remote branches (`arcade/ci-speed`, `arcade/tools-hub` and the others; the audit confirmed
every non-main branch is an ancestor of main).

Leave as they are:
- the 28 single-mention Rust functions (trait/window callbacks and entry points; Clippy is clean);
- `scripts/e2e-linux.sh`. Make it honour `TMPDIR` instead of hard-coding `/tmp`.

### 5. Project standard

- Add `rust-toolchain.toml` (1.88).
- rustfmt width 140 vs Lens/Link 160: use 160 everywhere (one reformat commit, nothing else in it).
- Developer docs (`ARCHITECTURE.md`, `ARCADE_LINK.md`, `DECISIONS.md`, `HYPRLAND.md`, `SHELF.md`) go to
  `docs/dev/` with lowercase names.
- Release via the shared `tag.yml` → `release.yml` flow. Find's `ci.yml` currently publishes on a `v*` tag
  push.
- `scripts/check` = what CI runs.

### 6. Docs and release

- Retake the README and `docs/user/images` screenshots: the overlay with results, the settings General page,
  light and dark.
- Update `docs/STATUS.md` with a dated entry, add a CHANGELOG entry ("New lime accent; …") and bump the
  minor version.
- Release through Find's `v*` tag flow after 3-OS CI is green. Check that Tools updates Find.

## Acceptance

- [ ] No colour literal outside `theme.rs`'s kit mapping. Every overlay size comes from kit constants. Inter
      renders in the overlay and in settings.
- [ ] The overlay opens in under 100 ms warm on the Hyprland desktop (Find's existing perf budget), in both
      themes, with the opaque fallback still working.
- [ ] Every settings page works and follows the Theme setting live. Settings still runs as a separate
      process that exits on close, so resident memory is unchanged.
- [ ] Keyboard: every overlay action has a key and a footer chip; settings is fully keyboard-operable.
- [ ] Link actions (Add to Shelf, Look preview, Box actions from results) still work (`tools/e2e.py`).
- [ ] Every item in §3 re-checked on the released build. 3-OS CI is green and the release is published.

# Spec: Arcade Wheel

**Outcome:**
- The wheel overlay and the settings/editor window use the Arcade design kit with Wheel's amber accent.
- The settings window gains a light theme.
- Every verified Wheel bug is fixed.
- The repo is cleaned up and matches the project standard.
- A new Wheel release ships.

**Prerequisite:** Spec 1 (`TOOLS.md`), so that Arcade Link `v0.4.0` with `design/` exists. Read `STANDARD.md` first.
**Evidence:** `AUDIT/keep.md` and `AUDIT/hygiene-and-dev-standard.md` (Wheel sections; the audit was stopped before it took screenshots of this app).

## Starting point

| | |
|---|---|
| Repo | `qa-p1/Arcade-wheel`, main at `1ee601c` on 2026-10-28 (release 0.4.5 (OpenGL again; Vulkan crashed)). Start from current main. |
| Toolkit | C++ / Qt 6 Quick (QML) with QtQuick.Controls Material. UI is in `qml/`: `wheel/Overlay.qml` and `wheel/WheelView.qml`; `settings/Settings.qml` (581 lines) plus `ActionPicker`, `CenterGesturesPage`, `ConnectedAppsPage` and `LinkActivity`; `components/` holds `SettingSlider`, `SettingToggle` and `UiButton`. |
| Link | Vendored Qt module in `src/link/`, pinned by `src/link/VENDORED.json` to commit `4c75f3a…` ("v0.3.0 (protocol 1)"). CI does a shallow checkout to verify it. |

Today's UI vs. the standard:
- **Theme:** the settings window is dark only (`Settings.qml:14` `Material.theme: Material.Dark`). Colours are hard-coded
  hex values in the files themselves (`#e8e3ef`, `#292637`, `#d9d1ff`, `#92909f`, `#757382` and others), and the
  palette leans violet.
- **Type:** Qt default font, with sizes of 9, 10, 11, 12, 13, 14, 15, 16, 18, 19 and 27 px.
- **Settings window layout:**
  - a left nav with "Wheel", "Center gestures", "Actions", "Trigger", "Appearance", "Behaviour", "Connected apps"
    and "General";
  - a brand block reading "Arcade Wheel" / "Your desktop, closer." at 15/10 px;
  - a status line ("Ready in background" / "Shortcut needs attention");
  - an "Open wheel" button.
- **Overlay:** `Overlay` is a frameless, always-on-top Qt `Tool` window (`src/main.cpp:335`). `WheelView` draws a
  ring of slots. The geometry is configurable (radius, centre radius, segment depth, gap, icon size, scale,
  opacity). The accent is user-configurable and defaults to `#b7b7f7` (lavender), not Wheel's amber.

## Keep (do not remove or flatten)

Ring geometry and motion settings (radius, centre radius, segment depth, gap, icon size, scale, opacity, animation speed, selected scale); decks; centre gestures; hold threshold; the custom accent colour (as an override); the live preview; portable JSON import/export; the OpenGL renderer chosen in 0.4.5.
These get kit styling only. Everything in `AUDIT/keep.md` › "Wheel — Keep" is also kept. It lists the capabilities with their sources.

## Work

### 1. Adopt the kit

- **Link vendoring:** move the vendored Link to `v0.4.0`. Update `src/link/VENDORED.json` (tag, commit) and the
  files in it, and add `design/qml/Arcade` plus the Inter font as Qt resources. `QGuiApplication::setFont` →
  Inter 13 px.
- **QML component set:** if Link `design/qml/Arcade/` has no component set yet (Shelf not done), build it now in
  Link as described in `SHELF.md` §1. Seed it from Wheel's `UiButton`, `SettingToggle` (→ `Switch` row) and
  `SettingSlider` (→ `Slider` row: title, detail, value + unit). Tag Link `v0.4.x` and vendor that.
- **Settings palette:**
  - Drop `Material.theme: Material.Dark`. Set `Theme.appId: "arcade.wheel"` and follow System / Light / Dark
    (new setting under General).
  - Every hex value in `qml/settings/*` and `qml/components/*` becomes a `Theme` token.
  - The accent becomes amber (`#9e6506` / `#f59e0b`).
- **Type:** snap to the kit scale. Nothing is smaller than 11.5. 27 → 21 (page title), 18/19 → 16 for card
  titles, or 14 (section heading) where it is a section.

### 1b. Shared conventions (STANDARD §8.1, §10)

- **Words:** every UI string meets STANDARD §8.1:
  - fixed words ("Settings", "Start at login", "Quit Arcade Wheel", "Install", "Show in folder");
  - error wording "Couldn't …";
  - one tagline, no split-weight app name, window titles "<Thing> — Arcade Wheel".
- **Formatting:** sizes, dates, durations and counts go through the kit's format helpers. No local formatters
  stay.
- **Identifiers and folders:** move to `dev.arcade.Wheel` and `arcade/wheel/` folders, with the verified migration in
  STANDARD §10. Today: `~/.config/Arcade Wheel` (`config.json`), `packaging/linux/com.arcadewheel.ArcadeWheel.desktop`.
- **Desktop entry:** contents per STANDARD §10.
- **App icon family:** replace `assets/arcade-wheel.svg`/`.png`, the Windows/macOS icon resources, the README logo with the kit-generated set (STANDARD §8, brand mark and app icons). The tray icon becomes the monochrome glyph.
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

**Wheel overlay (Template B, canvas variant):**

The ring shape and its geometry settings stay. These are what changes:
- **Surface:** slots are filled with `panel` at the user's "Surface opacity" (default 0.94). They get a 1 px `line`
  stroke and `shadow-pop` under the whole ring. The centre disc uses `sunken`.
- **Selection:**
  - The selected slot uses the accent at 16 % fill, with a 2 px accent outer edge and the icon in accent.
  - The default accent is Wheel's amber (dark variant `#f59e0b`, since the overlay sits over any wallpaper).
  - The user's custom "Accent colour" setting stays as an override, labelled "Use a custom colour"; when it is
    off, the wheel uses the kit accent.
- **Labels and centre text:**
  - Labels, when enabled, use Inter `small` 12/500 in `text` on a `panel` pill.
  - The centre shows the hovered action name in `body` 500 and the deck name in `caption` muted.
- **Theme:** the overlay follows the app theme (light ring in light, dark ring in dark).
- **Motion:** the entrance and selection scale keep the user's animation-speed setting but use the kit easing.
  Reduced motion sets the entrance to instant.

**Settings and editor window (Template A):**
- **Brand and status:**
  - Sidebar 212 px. The brand mark tile + "Arcade Wheel" replaces the 15/10 px brand block. The tagline moves to
    About.
  - The status line ("Ready in background" / "Shortcut needs attention") becomes the sidebar footer status, a dot
    plus label in the `ok`/`warn` colour. Clicking it opens Shortcuts when it needs attention.
  - "Open wheel" stays as the primary action in the "Your wheel" page head.
- **Sections, in the standard order** (renamed, contents kept):
  1. **General:** Theme (new), Start at login, Application (restart), Configuration (import/export portable JSON,
     with the note). "Reset defaults" is destructive with a confirm dialog.
  2. **Shortcuts:** "Trigger" renamed. Activation shortcut, hold threshold and the explanation as a section note.
  3. **Your wheel:** decks + slot editor + live preview. "Deck options" is a kit menu ("Duplicate deck", "Move
     earlier", "Move later", separator, "Delete deck" as a danger item with a confirm dialog). "Positions" is a
     kit select. "Edit action" is the primary button.
  4. **Actions:** `ActionPicker`, with kit list rows, search field and empty state.
  5. **Center gestures.**
  6. **Appearance:** "Shape and motion" sliders as kit slider rows, labels switch, custom accent.
  7. **Behaviour:** "Interaction".
  8. **Installed applications:** list rows with app icons, "Refresh" (secondary) and the four data states.
  9. **Connected apps:** `ConnectedAppsPage` + `LinkActivity` on the shared Link page layout.
  10. **About:** version, channel, "Updates are managed by Arcade Tools", tagline, logs, diagnostics, guide,
      licences, "Quit Arcade Wheel" (destructive, last).
- **Preview pane:** the "Your wheel" preview canvas sits on `sunken` with radius 12. The "Replay" button is a
  ghost button.
- **Dialogs:** import/export file dialogs stay native. "Reset defaults" uses the kit dialog with the buttons
  "Keep my wheel" / "Reset everything" (destructive).

**Install prompt** (`src/install/`): kit dialog with the same copy, options and order as Tools.

**Tray:** sentence case and the standard order ("Open wheel", "Settings", separator, "Restart Arcade Wheel",
"Quit Arcade Wheel").

### 3. Verified bugs

The 2026-10-27 audit was stopped before its Wheel tester ran, so no Wheel feature was checked by use. Its source review is complete. As part of this spec, use every Wheel feature listed in `AUDIT/keep.md` › Wheel with real inputs (the acceptance check below). Fix whatever fails here, with a regression test, before release.

From static analysis (Qt 6.11 `qmllint`, checked on 2026-10-28):
- `qml/settings/ActionPicker.qml:209,248,279,456` and similar sites are 1 px divider `Rectangle`s that set
  `height: 1` / `width: 1` inside layouts, which the layout can override, so the dividers may not show. Use
  the kit `Divider` (`Layout.preferredHeight: 1`) and check them visually.
- 5 missing-property warnings on dynamic types (`Settings.qml:442,573`, `WheelView.qml:61,96,102`). Check
  them at runtime; they are not dead code.

### 4. Cleanup

- Delete the remote `arcade/wheel-win-layout-diag`. Its two commits say "Scratch / not for merge", and main
  has the real implementation. Keep its logs in `docs/dev/history/` if they are useful.
- Delete merged remote branches (including `claude/*` and `t3/*`).

Leave as they are:
- the duplicate pinned `arcade-release.py` and the validators;
- the root `arcade-wheel` dev launcher;
- the conditional test skips.

### 5. Project standard

- **Early-days docs:** `docs/MANUAL_TESTING.md` (16 lines, 8 Oct) folds into `docs/dev/testing.md`.
  README line 187 ("Commit-pinned Arcade Link v0.3.0 modules") is updated with the Link bump.
- Add `.clang-format` and a `qmllint` gate (register the controller types so the unqualified-access
  warnings go away).
- Release tag `v<version>` instead of `v<version>+build.<run>`; the build number moves into
  `arcade-release.json` (STANDARD §10).
- Releases currently auto-publish on main. Move to the shared `tag.yml` → `release.yml` flow.
- Developer docs go to `docs/dev/` with lowercase names.
- `scripts/check` = what CI runs.

### 6. Docs and release

- Retake the README images and `docs/user/images`: the wheel open over a desktop, and the settings "Your wheel"
  page in light and dark.
- Add a dated entry to `docs/STATUS.md` and a CHANGELOG entry, and bump the minor version.
- 3-OS CI green → merge → the CI "Publish stable release" job (`v<version>+build.<run>`) → check that Tools
  updates Wheel.

## Acceptance

- [ ] No hex or `pixelSize` literal in `qml/` (except the documented default of the custom-accent colour picker).
      Inter is in use. The settings window works in light, dark and system, and switches live.
- [ ] The wheel opens on hold within Wheel's perf budget, still renders with OpenGL, and is readable over light
      and dark wallpapers in both themes, at scale 0.75 and 1.3.
- [ ] Every settings page works, at 720×520 and when maximised, with no clipping at 125 % font scale.
- [ ] Every slot action type (app, file, URL, command, Link action to Box/Look/Shelf/Clipboard) still works from
      the wheel.
- [ ] Every item in §3 is re-checked on the released build. 3-OS CI is green and the release is published.

# Spec: Arcade Shelf

**Outcome:** Shelf's capsule, docked tab, expanded panel, menus, dialogs and settings all use the Arcade design
kit with Shelf's new fuchsia accent. Every verified Shelf bug is fixed. The repo is cleaned up and matches the
project standard, and a new Shelf release ships.

Prerequisite: Spec 1 (`TOOLS.md`), which provides Arcade Link `v0.4.0` with `design/`. Read `STANDARD.md` first.
Evidence: `AUDIT/keep.md` and `AUDIT/hygiene-and-dev-standard.md` (Shelf sections; the audit was stopped before it took screenshots of this app).

## Starting point

| | |
|---|---|
| Repo | `qa-p1/Arcade-Shelf`, main at `52c1e25` on 2026-10-28 (release 0.3.3). Start from current main. |
| Toolkit | C++ / Qt 6 Quick (QML), CMake. UI in `ui/` (`Main.qml` ~1,000 lines plus `ShelfButton`, `ShelfDialog`, `ShelfField`, `ShelfIcon`, `ShelfMenu`). Platform code in `src/platform/` (`Backdrop` blur, `FullscreenGuard`, `AppInstaller`) |
| Link | vendored copy in `vendor/arcade-link/` (the Qt module is `vendor/arcade-link/qt/*`, wired in `CMakeLists.txt:10-11`) |

Today's UI compared with the standard:
- **Palette:** its own, defined inline in `Main.qml` (`paper`, `raised`, `tileSurface`, `hoverSurface`, `ink`, `muted`,
  `faint`, `outline`, `accent`, `selection`). The accent is **violet** `#7853ca` / `#bdadfc`, a third app using
  Box's hue. There are 12+ more hex literals across `ui/`.
- **Type:** Qt default font. Sizes are 9, 10, 11, 12, 15, 16, 17, 18 and 20 px. Section labels are 9 px uppercase
  with letter-spacing ("APPEARANCE", "SHORTCUT", "BACKUP AND RESTORE").
- **Window:** one frameless window (`Main.qml:7`) with three modes, plus a translucent "paper" when the platform
  backdrop is active:
  - capsule (216×76);
  - docked tab (30×92 on an edge);
  - expanded panel (640×490, minimum 440×350).
- **Settings:** a "Preferences" page inside the panel (`Main.qml:904-1050`) with General, Storage, Connected apps
  and About.

## Keep (do not remove or flatten)

Capsule, docked tab (all four edges) and expanded modes; the platform backdrop; collections; undo; drag out; thumbnails; owned-storage quota and temporary retention; the fullscreen guard; the focus behaviour on Wayland/Hyprland; Link peers and actions.
These get kit styling only. Everything in `AUDIT/keep.md` › "Shelf — Keep" is also kept. It lists the capabilities with their sources.

## Work

### 1. Adopt the kit

- Update the vendored Link to `v0.4.0` (the whole `vendor/arcade-link` copy, with its provenance file updated)
  and add `design/qml/Arcade` to the QML import path (`CMakeLists.txt` `qt_add_qml_module` or `QML_IMPORT_PATH`).
  Bundle `design/fonts/InterVariable.ttf` as a resource and load it through `Fonts.qml`. Set
  `QGuiApplication::setFont` to Inter at 13 px.
- If Link `design/qml/Arcade/` has no component set yet (because Wheel hasn't been done), build it now in Link,
  using Shelf's own components as the seed:
  - **From Shelf's components:** `ShelfButton` → `Button` (variants per STANDARD §5), `ShelfField` →
    `TextField` / `SearchField`, `ShelfMenu` → `Menu` + `MenuItem` (icon, label, key chip, danger),
    `ShelfDialog` → `Dialog`, `ShelfIcon` → `Icon`.
  - **New components:** `Switch`, `CheckBox`, `ComboBox` (select), `SegmentedControl`, `ListSection`, `Row`,
    `Badge`, `KeyChip`, `Notice`, `EmptyState`, `Toast`, `ProgressBar`, `Sidebar` / `NavItem`, `PageHead`.

  Every component takes colours from `Theme` with the app id set once (`Theme.appId: "arcade.shelf"`). Tag
  Link `v0.4.x` and vendor that.
- `Main.qml`'s palette properties are replaced by `Theme` (`paper` → `Theme.bg`, `raised` → `Theme.panel`,
  `tileSurface` → `Theme.sunken`, `hoverSurface` → `Theme.hover`, `ink` → `Theme.text`, `outline` → `Theme.line`,
  `accent` → fuchsia `#bf13d8` / `#e273f3`, `selection` → `Theme.accentSoft`). The dark detection stays
  (System / Light / Dark setting with `SystemPalette` fallback). `motion` becomes `Theme.motionBase`, which
  respects the reduced-motion setting.
- The backdrop stays as Shelf's documented exception to the "opaque overlays" rule (it is an existing feature
  with its own fallback). When active, `paper` = `Theme.panel` at 87 % alpha. Otherwise it is opaque.
- Type snaps to the kit scale. Nothing goes below 11.5, so 9/10/11 → 11.5 (caption) or 12 (small). Section
  labels become sentence-case `heading` 14/600 ("Appearance", "Shortcut", "Backup and restore").

### 1b. Shared conventions (STANDARD §8.1, §10)

- **Words:** every UI string meets STANDARD §8.1:
  - fixed words ("Settings", "Start at login", "Quit Arcade Shelf", "Install", "Show in folder");
  - error wording "Couldn't …";
  - one tagline, no split-weight app name, window titles "<Thing> — Arcade Shelf".
- **Formatting:** sizes, dates, durations and counts go through the kit's format helpers. No local formatters
  stay.
- **Identifiers and folders:** move to `dev.arcade.Shelf` and `arcade/shelf/` folders, with the verified migration in
  STANDARD §10. Today: `packaging/linux/arcade.shelf.desktop`, Qt default data paths.
- **Desktop entry:** contents per STANDARD §10.
- **App icon family:** replace `packaging/arcade-shelf.svg` and the generated icons, the README logo with the kit-generated set (STANDARD §8, brand mark and app icons). The tray icon becomes the monochrome glyph.
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

**Capsule and docked tab (Template B, mini):**
- Use `panel` with a 1 px `line`, `shadow-pop`, and radius 12. The docked tab stays flat against the edge and
  rounds toward the screen.
- Item count badge in accent. The drag-hover pulse uses `accent-soft`.

**Expanded panel (Template B):**
- **Header:** collection switcher (menu button with the collection name), item count, then actions: "Actions"
  (menu), "Undo" (ghost, accent), "Cancel" while busy. Buttons are 28 px kit buttons.
- **Grid/list of items:**
  - Tiles on `sunken` with radius 10, thumbnails from `ThumbnailProvider`.
  - Selection uses `accent-soft` + a 2 px accent ring.
  - Labels are body text with an ellipsis and the full name in a tooltip.
- **Empty state:** "Drop to collect" / "Keep the originals right where they are." as a kit empty state (no
  18 px literal) with the hint "Paste (Ctrl+V) or drop files, text and links."
- **Busy and progress:** a kit progress bar in the header with cancel.
- **Footer hint bar:** "↵ Open", "Space Preview in Look", "Del Remove", "Esc Close".
- **Menus** (window menu, collection menu, item menu, peers): kit `Menu`, sentence case, with separators where
  they are now. "Remove from Shelf" and "Delete collection…" are danger items. The two "Dock left/right" lists
  that appear twice (`Main.qml:708-723`) come from one shared component.
- **Dialogs** (new/rename collection, delete collection, confirm peer action): kit `Dialog`. Delete uses the
  buttons "Keep" / "Delete collection" (destructive). The peer-action effects are shown as a list, not
  "Effects: a, b".

**Settings (Template A):**
- "Preferences" becomes **Settings**, opened from the menus and the tray. It opens as its own normal window
  (native decorations, 760×560, minimum 720×520), not inside the panel. The panel is a transient surface.
- **Sections:**
  1. **General:** theme, always on top, focus behaviour, start at login, backdrop on/off.
  2. **Shortcuts:** global shortcut rebind and conflicts, plus read-only panel keys.
  3. **Storage:** owned storage quota (MiB), temporary item retention, and the explanation as a section note.
  4. **Backup and restore.**
  5. **Connected apps:** the shared Link page. Peers that aren't installed show an "Install" link to Tools
     instead of a grey "Not installed".
  6. **About:** version, channel, "Updates are managed by Arcade Tools", logs, diagnostics, guide, licences.

**Install prompt** (`src/platform/AppInstaller.*`): kit dialog, with the same copy, options and order as Tools.

**Tray:** sentence case, in the standard order ("Open Arcade Shelf", "Collect from clipboard", "Settings",
separator, "Quit Arcade Shelf").

### 3. Verified bugs

The 2026-10-27 audit was stopped before its Shelf tester ran, so no Shelf feature was checked by use. Its source review is complete. As part of this spec, use every Shelf feature listed in `AUDIT/keep.md` › Shelf with real inputs (the acceptance check below). Fix whatever fails here, with a regression test, before release.

From static analysis (checked on 2026-10-28): `qmllint` flags `ui/Main.qml:921,1040`, which are 1 px
divider `Rectangle`s that set `height: 1` inside a `ColumnLayout`, and `:1033` (`width: 58; height: 58`
inside a layout). A layout sizes its children from `Layout.*` and implicit sizes, so these explicit values
can be overridden and the dividers may not render. Use `Layout.preferredHeight: 1` (and
`Layout.preferredWidth/Height: 58`), or the kit's `Divider`, and check the dividers are visible in both
themes.

### 4. Cleanup

Leave as they are:
- the vendored `vendor/arcade-link/` duplicates (pinned and consumed by CMake, tests and packaging);
- `benchmarks/cloud-debug.json` and `cloud-milestone.json` (referenced as history);
- the platform-specific test skips.

Fix:
- the broken link in `vendor/arcade-link/SPEC.md:712` and the shared packaging README (this comes in by
  re-vendoring Link once Link's own copy is fixed).

List for the owner (don't merge or delete):
- the remote `fix/hyprland-desktop` (two unique historical commits).

Delete merged remote branches.

### 5. Project standard

- **Early-days docs:** `docs/ECOSYSTEM_VERIFICATION.md` (a 10 Oct verification record) moves to
  `docs/dev/history/`. Re-read `docs/ONBOARDING.md` (10 Oct) against the new onboarding and fold it into
  `docs/dev/architecture.md` or the user guide.
- Add `.clang-format` and a `qmllint` gate. Today qmllint reports 290 warnings, 284 of them unqualified
  access because there are no typed context properties. Register the controller types (`QML_ELEMENT` /
  `qmlRegisterSingletonInstance`) so the gate can run at 0 warnings.
- Releases currently go `build.yml` + `tag.yml`. Move to the shared `ci.yml` / `tag.yml` / `release.yml`
  names and flow.
- Developer docs (`ARCADE_LINK.md`, `ARCHITECTURE.md`, `ECOSYSTEM_VERIFICATION.md`, `NATIVE_SURFACES.md`,
  `ONBOARDING.md`, `PACKAGING.md`, `TESTING.md`) go to `docs/dev/` with lowercase names.
- `scripts/check` = what CI runs.

### 6. Docs and release

- Retake README and `docs/user/images`: capsule, expanded panel with items, settings, in light and dark.
- `docs/STATUS.md` dated entry, CHANGELOG entry ("New fuchsia accent; …"), minor version bump.
- 3-OS CI green → merge → release via `build.yml` → check that Tools updates Shelf.

## Acceptance

- [ ] No colour literal or `pixelSize` literal in `ui/` (`rg -n '#[0-9a-fA-F]{6}|pixelSize: [0-9]' ui` is empty).
      Inter in use. All three themes switch live.
- [ ] Capsule, docked tab on all four edges, and expanded panel at minimum and large sizes: no clipping, at
      100 % and 125 % font scale.
- [ ] Collect from drop, paste and Link ("Add to Shelf" from Look, Lens, Box, Clipboard and Find), then open,
      reveal, copy, reorder, remove and undo all work with real files.
- [ ] The settings window opens and closes without affecting the panel. All sections work.
- [ ] Every item in §3 re-checked on the released build. 3-OS CI green, release published.

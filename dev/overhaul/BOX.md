# Spec: Arcade Box

**Outcome:**
- The Island quick panel, the dashboard, pinned references and every dialog use the Arcade design kit with
  Box's violet accent.
- The dashboard is a proper standard window.
- No layout overflows.
- Every verified broken Box tool and feature works, including the global shortcut.
- The repo is cleaned up and matches the project standard.
- A new Box release ships.

**Prerequisite:** Spec 1 (`TOOLS.md`), so that Arcade Link `v0.4.0` with `design/` exists. Read `STANDARD.md` first.
**Evidence:** `AUDIT/` (Box section, `AUDIT/screens/box/`). The earlier branch work is saved in
`AUDIT/box-salvage/`.

## Starting point

| | |
|---|---|
| Repo | `qa-p1/Arcade-box`, main at `76ece8d` on 2026-10-28 (release Box **0.3.5**). Start from current main. |
| Local state | Synced to origin/main on 2026-10-28. The old local branch `fix/ui-and-tools` was deleted at the owner's request. Its UI token pass (ca8df43) and its uncommitted calculator/units fixes are kept as patches in `AUDIT/box-salvage/`. The UI pass is superseded by this spec; the calculator/units patch applies cleanly to main and is used for B3–B5. |
| Toolkit | Tauri 2 + Svelte 5 in `apps/desktop/frontend` (`App.svelte` 2,446 lines, `app.css` 975 lines, 32 components in `src/lib`). Rust core `crates/arcade-core` (the 109 tools), shared with the `arcadebox` CLI. Plugin host in `crates/arcade-plugin-host`. |
| Link | root `Cargo.toml:23` pins `rev = "3bbbc5d…"` |
| Windows | `island` (frameless, transparent, always on top, 740×740, created on demand and released 15 s after hiding), plus `pin.html` pinned references (`screen_capture.rs:133`) and the "Confirm pipeline effects" window (`lib.rs:77`). The dashboard is a second "surface" drawn inside the island window (`App.svelte:31`, `surface: 'island' \| 'dashboard'`). |

Today's UI vs. the standard:
- There are 296 hex literals in the frontend, and its own palette differs from both Tools and the old tokens.
- Font sizes in use: 9, 10, 10.5, 11, 11.5, 12, 12.5, 13 and 15 px (164 rules at 12 px). Many are below the
  11.5 minimum.
- The dashboard has a frameless, always-on-top window with a custom sidebar. It has:
  - nav: "Workspace" with All tools, Favorites, Recently used, Background jobs, Pipelines, Plugins and
    Engines & dependencies;
  - a "Categories" list;
  - a topbar;
  - a catalog summary "N ready · N in progress · N planned";
  - settings drawn as cards (Appearance, Global shortcut, Privacy).
- The 2026-10-26 overflow problems in sidebar nav counts and the catalog grid came from grids without
  `minmax(0, …)` tracks.
- Released 0.3.5 as seen by the audit (`AUDIT/screens/box/`):
  - **Sidebar:** the nav counts ("109", "4") are cut off by the sidebar's scrollbar/edge.
  - **Dashboard window:** the dashboard is a floating card inside the big transparent island window, with its
    own "Close" link and breadcrumb ("Arcade Box › All tools").
  - **Island:** the search pill sits at the right of the screen, with the first-run card offset below it.
  - **Tools page:** shows "109 ready | 0 planned".
  - **Settings:**
    - it starts with Connected apps and puts Appearance below it, against the standard order;
    - the theme is chosen with three large cards, and a green "Theme set to dark." notice appears after each
      change;
    - the shortcut needs a separate "Save shortcut" button;
    - Diagnostics is a bare disclosure triangle.
  - **First-run card:** "Save shortcut & continue" is a black full-width button (not the accent), and the shortcut
    field reads as a placeholder ("Ctrl+Alt+Space" in faint mono with "Editable").

  Each of these is fixed by the surface changes below:
  - the theme becomes a segmented control that applies at once, with no confirmation notice;
  - the shortcut applies on capture, with inline validation;
  - the first-run card uses the kit primary button and a real key-chip shortcut field;
  - the dashboard becomes a normal window, so the in-card "Close" and the breadcrumb go away and the page
    head carries the title.

## Keep (do not remove or flatten)

The Island quick panel and its context suggestions; the `arcadebox` CLI; pipelines (with the effects confirmation); plugins; background jobs; favourites and recents; screen tools (ruler, colour sampler, pinned references); clipboard history; releasing the webview when hidden (memory); every Link action in and out.
These get kit styling only. Everything in `AUDIT/keep.md` › "Box — Keep" is also kept. It lists the capabilities with their sources.

## Work

### 1. Adopt the kit

- Add `scripts/sync-design.py`: kit CSS, icons, fonts and glyphs → `apps/desktop/frontend/src/design/`, with hashes
  in `VENDORED`. Point `arcade-link` at `tag = "v0.4.0"`, then re-run `scripts/license_inventory.py`
  (required after any Link change).
- Set `<html data-app="arcade.box">` so the accent is `#724fff` / `#a58fff`.
- Rebuild `app.css` on the kit:
  - Every literal colour becomes a token.
  - Every font size moves onto the scale: 9–11 px → 11.5 (caption), 12/12.5 stay, 15 → 14 (heading).
  - Radii and spacing come from the kit.
  - Card grids use `repeat(auto-fill, minmax(240px, 1fr))`, and no grid has implicit max-content tracks.
  - The salvage patch `ui-token-pass-ca8df43.patch` already did much of this mapping (onto the old tokens).
    Use it as the guide, but map onto the kit's names.
- Map undefined variables that components still reference (e.g. `--border-subtle` and `--text-muted`, found
  on 2026-10-26) onto kit tokens. Add a check that fails the build on any `var(--x)` that isn't defined:
  a tiny script in `scripts/check` that greps the built CSS.
- `Icon.svelte` uses the kit icon map; Box-only glyphs are added to the kit icon set, following the same
  grid.
- Split `App.svelte` by surface with no behaviour change:
  - `island/Island.svelte`, with `IslandSearch`, `IslandTool` and `IslandFooter`;
  - `dashboard/Dashboard.svelte` with one file per page;
  - `shared/` for the tool forms and results already in `src/lib`.

### 1b. Shared conventions (STANDARD §8.1, §10)

- **Words:** every UI string meets STANDARD §8.1:
  - fixed words ("Settings", "Start at login", "Quit Arcade Box", "Install", "Show in folder");
  - error wording "Couldn't …";
  - one tagline, no split-weight app name, window titles "<Thing> — Arcade Box".
- **Formatting:** sizes, dates, durations and counts go through the kit's format helpers. No local formatters
  stay.
- **Identifiers and folders:** move to `dev.arcade.Box` and `arcade/box/` folders, with the verified migration in
  STANDARD §10. Today: arcade-box-settings.json + `dev.arcadebox.app` data dir; window class `arcade-desktop`.
- **Desktop entry:** contents per STANDARD §10.
- **App icon family:** replace `apps/desktop/src-tauri/icons/*` (today a game-controller icon that matches nothing), the README logo with the kit-generated set (STANDARD §8, brand mark and app icons). The tray icon becomes the monochrome glyph.
- **Default shortcut:** follows the STANDARD §10 table. Change: macOS default ⇧⌘Space → ⌃⌥Space. Existing users keep theirs.
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

**Island (Template B)**, the quick panel summoned by the global shortcut:
- **Surface:** opaque `panel`, 1 px `line`, radius 12, `shadow-pop`. It drops the transparency the window
  needs only for the rounded corners: the transparent window stays, while the painted surface is opaque.
- **Compact mode:** a 44 px search field with the Box mark and a "⌘K"-style hint chip, plus context
  suggestions as 40 px rows.
- **Search mode:**
  - results grouped by category, with `caption` group labels;
  - each row has a glyph, the tool name, a one-line description and a trailing key chip for the top result;
  - selection is `accent-soft` plus an accent bar.
- **Tool mode:**
  - **Header:** back button, tool name (`title-sm`), favourite toggle and "Open in dashboard".
  - **Inputs:** `StandardToolForm` and the file, folder and output pickers use kit inputs, select,
    segmented and switch rows, with drop zones as dashed `line-strong` areas.
  - **Running:** a kit progress bar with cancel.
  - **Results:** `ToolOutputView`, the `*Report` components and `ResultActions` sit on kit cards. Actions are
    "Copy", "Save…", "Open", "Show in folder" and "Send to…" (Link).
- **Footer hint bar:** "↵ Run", "Tab Next field", "Esc Back/Close". The current `island-footer` becomes the
  kit footer.
- **Onboarding** (first run): a kit empty-state hero inside the island, with "Set a shortcut" and "Browse
  tools".
- **Screen tools** (`ScreenColorSampler`, `ScreenRuler`) keep their canvas shapes, with kit colours,
  key-chip labels and type.

**Dashboard (Template A)**, which becomes its own window:
- **Window:** a new window `dashboard` with native decorations, 1100×760 (minimum 720×520), a normal
  taskbar entry and not always on top. It is created on demand and destroyed 15 s after it closes, the same
  memory policy as the island. "Open dashboard" (island, tray, `arcadebox --dashboard`) opens or focuses it.
  State (favourites, recents, jobs, pipelines, settings) already lives in the backend, so both windows read
  the same data. Re-check after the split.
- **Sidebar** (212 px):
  - brand mark tile + "Arcade Box";
  - nav: Tools, Favorites, Recent, Jobs, Pipelines, Plugins, Engines, Settings, with counts as the kit badge
    count;
  - categories as a second nav group under a `caption` label. The "+" button that only reset the filter goes
    away;
  - footer: "Version x.y.z".
- **Tools page:**
  - page head "Tools" with the subtitle "109 tools" (the real count) and the primary action "Open Island";
  - search field (⌘K) + category segmented/select;
  - tool cards in the kit grid: glyph tile, name, description, favourite toggle;
  - all four data states.
  - The catalog summary shows only what users can use. Tools still "planned" are not listed and not counted
    (STANDARD §8: no "planned" counters). "In progress" tools are finished in §3 or hidden until they are.
- **Jobs page:** a list of rows with status badges (`ok` / `warn` / `danger`), progress, and "Open
  output" / "Cancel" / "Retry". The empty state reads "No jobs yet". Errors use the kit notice instead of
  the custom `dashboard-alert`.
- **Pipelines and Plugins pages:** kit lists and dialogs (`PipelinesView`, `PluginManager`). The "Confirm
  pipeline effects" window uses the kit dialog layout, with effects listed and "Run pipeline" as the primary
  action.
- **Engines page:** the same layout as Tools' Engines page (status rows, "Check again"), so the two apps
  agree.
- **Settings page**, in the standard sections and order:
  1. General: Appearance, Start at login, output folder default.
  2. Shortcuts: global shortcut with the conflict notice (`ShortcutClash`), plus a read-only island keys
     list.
  3. Clipboard history: `ClipboardHistoryView` settings, retention, clear.
  4. Privacy: local-first processing, which tools use online services (badge `warn` "online"), and API keys.
  5. Connected apps: `ConnectedApps.svelte` on the shared Link page.
  6. About: version, channel, "Updates are managed by Arcade Tools", logs, diagnostics, user guide,
     licences.
  The settings cards (`settings-card-heading` with symbol tiles) become kit sections + lists.

**Pinned reference** (`pin.html`, `public/pin.css`): kit border, radius 10, `shadow-pop`, and a hover toolbar
of kit icon buttons (close, copy, opacity). It follows the theme.

**Install prompt** (`installer_ui.rs`): kit dialog, same copy and order as Tools.

**Tray:** keeps its current items in the standard order and wording: "Show or hide Arcade Box", "Open
dashboard" (from "Open Box"), "Open pipelines", "Settings" (from "Open Settings"), separator, "Restart Arcade
Box", "Quit Arcade Box". No new items.

### 3. Verified broken features

Each item below was reproduced twice on the released 0.3.5 AppImage: by the audit, then again on
2026-10-28 for this plan. The code is unchanged on origin/main 76ece8d.

How to re-run the command-line repros:
1. Download `Arcade-Box_0.3.5_amd64.AppImage` from the v0.3.5 release.
2. Run `./Arcade-Box_0.3.5_amd64.AppImage --appimage-extract`.
3. Run the CLI as `squashfs-root/usr/bin/arcade-box run <tool> "<input>" --json`, with
   `XDG_CONFIG_HOME`, `XDG_DATA_HOME` and `XDG_CACHE_HOME` pointing at a temporary folder, so your real
   profile isn't touched.

The input files used are in `AUDIT/fixtures/`, and the evidence is in `AUDIT/evidence/`. Each fix gets a
regression test in `crates/arcade-core` (`src-tauri` for the shortcut) built from exactly these inputs.

**B1. The global shortcut stops working on Wayland after it is saved (High).** This is why Box wouldn't
come up from its shortcut.
- *What happens:* save the shortcut in Settings, onboarding or through Tools. On the next start on
  Hyprland, Box logs `state=invalid_trigger message=Use XDG shortcut syntax such as CTRL+ALT+space` and
  the Island never opens. The owner's real log (`~/.local/share/dev.arcadebox.app/logs/arcade-box.log` on their machine)
  shows this on every start.
- *Root cause:* `set_shortcut` (`apps/desktop/src-tauri/src/lib.rs:169`) saves Link's canonical
  `Ctrl+Alt+Space`. At startup (`lib.rs:1999`) the saved string goes straight to the Wayland portal
  controller. `validate_trigger` (`wayland_shortcut.rs:173`) only accepts XDG syntax (`CTRL+ALT+space`).
  The two formats are never converted.
- *Fix:* store the canonical form only. Convert canonical to XDG in one function used by every Wayland
  path (startup, set, reconnect), and convert back for display. Add a test that round-trips every modifier
  and key name. Existing saved values in either form keep working (normalise on load).
- *Check:* save the shortcut, then restart Box in a Wayland session (a headless nested Sway is enough;
  the audit's run is recorded in `AUDIT/evidence/parent-box-shortcut/`). The log must show no
  `invalid_trigger`, and the Island must open. Then check on the owner's Hyprland with the real shortcut.

**B2. Unit symbols lose their case (High, wrong output).** `1 mW to W` gives **1000000 W** (should be
0.001 W), and `1 MB to Mb` gives **1 Mb** (should be 8 Mb).
- *Root cause:* `converter_tools/units.rs:71,125,127` lowercases unit tokens, so milli/mega and bit/byte
  collide.
- *Fix:* match case-sensitively where symbols collide (m/M prefixes, b/B). Keep case-insensitive matching
  for spelled-out names ("megawatt", "megabyte").
- The salvage patch handles mW/MW and mJ/MJ but **not** bit/byte; add that.
- *Check:* `1 mW to W` = 0.001 W, `1 MW to kW` = 1000 kW, `1 MB to Mb` = 8 Mb, `1 MiB to KiB` = 1024 KiB.

**B3. "in" (inch) is stripped as a connector word (Medium).** `1 in to cm` fails with "Provide source and
destination units"; `1 inch to cm` works.
- *Root cause:* `units.rs:13,84` drops every `in` token before parsing.
- *Fix:* the salvage patch (`AUDIT/box-salvage/calculator-units-uncommitted.patch`, which applies cleanly
  to main) treats the last `to`/`in`/`->`/`=` whose right side is a unit as the connector.
- *Check:* `1 in to cm` = 2.54 cm, `12 in in cm` = 30.48 cm, `72F in C` = 22.22 °C.

**B4. Compound amounts and energy prefixes are missing (Medium).** `5 ft 11 in to cm` → "Unknown unit
`11`", and `1 MJ to kJ` → "Unknown unit `MJ`".
- *Root cause:* `units.rs:16,117` reads one amount and one unit only, and the unit table has no MJ (or GJ,
  kWh variants).
- *Fix:* the salvage patch adds compound amounts (`5 ft 11 in`, `5'11"`) and multi-word units. Complete
  the SI prefixes for every SI unit in the table instead of adding units one by one.
- *Check:* `5 ft 11 in to cm` = 180.34 cm, `5'11" to cm` = 180.34 cm, `1 MJ to kJ` = 1000 kJ,
  `1 kWh to MJ` = 3.6 MJ.

**B5. The calculator can't call `log10` (Medium).** `log10(100)` → "Unknown constant `log`".
- *Root cause:* the lexer (`calculator.rs:150`) stops identifiers at digits, so the `log10` branch at `:213`
  is never reached.
- *Fix:* allow digits after the first letter (in the salvage patch).
- *Check:* `log10(100)` = 2, `log2(8)` = 3, `2log10(100)` = 4 (implicit multiplication still works).

**B6. Rounded result text changes the number (Medium, wrong output).** `1000000.5 m to m` shows "= 1000001
m", and `0.000000001 m to km` shows "= 0 km". The JSON values (1000000.5, 1e-12) are right.
- *Root cause:* `units.rs:50,56` and `converter_tools.rs:65` format to a fixed number of significant
  digits.
- *Fix:* format through the kit's `formatCount`-style helper with 12 significant digits. Use scientific
  notation below 1e-6 or above 1e15, and never show 0 for a nonzero value. Copy puts the full-precision
  value on the clipboard.
- *Check:* both inputs above show the exact value; `1/3 km to m` shows 333.333333333 m.

**B7. SVG files are refused by Image convert and Favicon (Medium, unfinished).** `run arcade.image.convert
--file icon.svg --set format=png` and `run arcade.image.favicon --file icon.svg` → "does not accept input
type file/svg". The most common favicon source is an SVG logo.
- *Fix:* accept `file/svg` in both tools' input types and rasterise with `resvg` (pure Rust, no system
  dependency) at the requested size.
- *Check:* `AUDIT/fixtures/icon.svg` → a PNG at 512 px and a favicon set (16/32/48 ICO + 180/192/512 PNG), with
  transparency kept.

**B8. Batch barcodes refuses a CSV file (Medium, unfinished).** `run arcade.barcode.batch --file
barcodes.csv` → "does not accept input type file/csv". Pasting the same text works.
- *Fix:* accept `file/csv` (and `text/csv`), read it with the same parser as pasted text, and use the
  header row for value/label columns.
- *Check:* the fixture (2 rows) gives 2 barcode images plus a label sheet. A 200-row CSV finishes in under
  5 s.

**B9. Multi-language OCR is rejected (Low).** `--set language=eng+deu` → "Choose a valid OCR language
code", though Tesseract supports `eng+deu`.
- *Fix:* accept `+`-joined codes, check each code against the installed packs, and name the missing pack
  in the error (the single-language message already does). In the UI the language picker becomes
  multi-select.
- *Check:* `eng+osd` works on this machine. `eng+deu` without the deu pack says "The deu language pack
  isn't installed" and offers Tools › Engines.

**What was checked and works on 0.3.5** (no work needed; keep it working):
- Video: convert, compress, trim, crop, join (mixed profiles), extract-audio, gif, frames, subtitles,
  auto-subtitles, inspect.
- Audio: convert, trim, join, normalize, denoise, vocals, speed-pitch, silence, metadata, transcribe,
  text-to-speech.
- Web: downloader, transcript, thumbnail, images, file-downloader, snapshot, markdown.
- Network: site-check, rdap, ip.
- Developer: regex, encoding, url, hash, identifier, jwt, cron.
- Utility: emoji, random. Security: password.
- Image convert with HEIC input.
- Timer and stopwatch in the GUI; video convert in the GUI: window in 620 ms, output in 2.4 s.

The tester's other "failures" were checker mistakes, re-read on 2026-10-28.
`AUDIT/evidence/box-media-cli-matrix.json` has every command and output.

**Not covered by the audit** (the testers were stopped):
- PDF, text, files, the rest of image and barcode, screen and system tools.
- Pipelines and plugins in the GUI.

Use each of these with real inputs as part of the acceptance check below, and fix whatever fails as part
of this spec before release.

### 4. Cleanup

Remove (provably unused):
- the unused CSS custom properties `--quiet`, `--surface-soft`, `--accent-bright` and `--accent-wash`
  (`app.css:30,39,41,42,76,81`). The kit rebuild removes them anyway;
- the placeholder UI: the fake "profile" card with a dots menu, the "+" button next to Categories that only
  resets the filter, the duplicate "Tools" heading and the "0 planned" counter.

Leave as they are (the audit found real users of each):
- `scripts/validate_shortcuts.py` and `tools/validate_shortcuts.py` (identical, both pinned in `VENDORED.md`);
- `scripts/smoke-mvp.py` (documented). Fix it to honour `CARGO_TARGET_DIR`;
- `scripts/install-local-desktop.py`;
- the `zxing-cpp` dependency (used as `zxingcpp`);
- the large `App.svelte`, `pdf.rs` and `video.rs`. `App.svelte` is split in §1; the other two stay.

Fix:
- the two broken links in `packaging/windows/README.md:26,27` (copied from Link). Point them at the Link
  repository URLs;
- the two `collapsible_if` lints that newer Clippy flags in `crates/arcade-contract/src/lib.rs:425,493`, so
  the build is clean on the next toolchain.

### 5. Project standard

- **Early-days docs:** move these to `docs/dev/history/`, unchanged, with links updated. Nothing references them
  any more; this was checked on 2026-10-28.
  - `Original spec.md`, the 4,449-line original product spec;
  - `docs/implementation-plan.md`, `docs/recovery-audit.md`, `docs/product.md` and `docs/research/`;
  - the 70 per-tool stubs in `docs/tools/*.md` (5–24 lines each, written 3–8 Oct). Nothing links to them,
    and `catalog/tools.json` and the user guide replaced them.
- **Keep** `docs/tool-matrix.md` and `docs/tool-catalog.md`: they are generated from `catalog/tools.json`.
  Regenerate them as part of the release.
From the audit's cross-repo table (`AUDIT/hygiene-and-dev-standard.md`):
- Box is the only repo with `rust-toolchain.toml` (1.88). Keep it; it becomes the pattern for the others.
- The version is repeated in the CLI, desktop, `tauri.conf.json` and `package.json`. Use one source (the
  workspace `Cargo.toml`) and have `scripts/check` fail on drift.
- Releases currently run from a successful main CI (`workflow_run`). Move to the shared `tag.yml` →
  `release.yml` flow (STANDARD §10) with identical assets, checked with one beta release.
- The main licence text is missing (`GPL-3.0-or-later` is declared, and `docs/STATUS.md` already lists it
  as a release gate). Add `LICENSE` with the GPL-3.0 text.
- Developer docs go to `docs/dev/`. `implementation-plan.md`, `recovery-audit.md`, `research/` and `adr/` (as
  `decisions.md` plus the ADR files) go to `docs/dev/history/` or `docs/dev/`, and links are updated.
- `scripts/check` = rustfmt, clippy `-D warnings`, `cargo test`, `npm run check`, the visual overflow check,
  the undefined-CSS-variable check and the vendored-hash check: exactly what CI runs.

### 6. Docs and release

- Retake README and `docs/user/images`: the island with results, a tool run, and the dashboard Tools page,
  each in light and dark.
- Add a dated entry to `docs/STATUS.md`, plus a CHANGELOG entry ("Dashboard is its own window; fixed …").
  Bump the minor version (0.4.0).
- 3-OS CI green → merge → `release.yml` runs on the successful main CI → check that Tools updates Box from
  0.3.5.

## Acceptance

- [ ] No colour literals outside `src/design/` and documented content palettes. No font size off the kit
      scale. No undefined CSS variables (build check). Inter is in use.
- [ ] No element overflows its container in the island (compact, search, tool) or on any dashboard page, at
      320×116 (island minimum), 740×740, 720×520 and 1600×1000, in light and dark. The layout check in
      `tests/visual` asserts `scrollWidth <= clientWidth` for every element.
- [ ] The global shortcut opens the island on Hyprland, GNOME, KDE, X11, Windows and macOS (CI for the last
      two). "Open dashboard" opens a normal window. Closing it frees its memory within 20 s.
- [ ] B1–B9 pass their checks (as regression tests and by hand). Every tool group §3 lists as not covered
      has been used with real inputs, in the CLI and the Island, and any failure is fixed in this spec.
- [ ] Link sends (to Shelf, Clipboard, Look, Lens) and actions received from Look/Find/Wheel still work.
- [ ] 3-OS CI green; release published.

# Spec 1: Arcade Tools + the Arcade design kit

**Outcome:** Arcade Link ships the design kit (`design/`, tag `v0.4.0`). Arcade Tools is rebuilt on it with
no visible regressions, so it is the living reference for `STANDARD.md`. Every verified Tools bug is fixed,
the repo is cleaned up and matches the project standard, and Tools 0.4.0 is released.

Read first: `STANDARD.md` (all of it), then this spec. Evidence lives in `AUDIT/` (audit report and
screenshots of 2026-10-27).

## Starting point

| Repo | GitHub | State |
|---|---|---|
| Arcade-Link | `qa-p1/Arcade-Link` | main at `8a19346` on 2026-10-28: 52 commits after the `v0.3.0` tag, untagged |
| Arcade-tools | `qa-p1/Arcade-tools` | main at `2169576`, Tools 0.3.8 ("a calmer interface") |

Tools pins Link by `rev = "3bbbc5d…"` (root `Cargo.toml:19`, `src-tauri/Cargo.toml:22`), not by tag.
Tools' palette lives in `src-ui/style.css:5-75` (its own green palette), while `src-ui/tokens.css` and
`src-ui/tokens.json` hold a stale copy of Link's `assets/tokens.json`. The shortcut overlay
(`crates/arcade-tools-overlay`, winit + softbuffer + tiny-skia + cosmic-text) hard-codes a third, slightly
different palette in `src/ui/render.rs:30-55` (e.g. border `#2a2e36` vs `--line` `#262a31`).

## Keep (do not remove or flatten)

Tray hosting with per-app submenus; the shortcut overlay sheet; catalog with categories and bundles; offline guides (Learn); Engines page; backup and restore; Report a problem; adopting manually installed apps; per-app channel and auto-update; the operation bar with cancel; the collapsed sidebar at small widths.
These get kit styling only. Everything in `AUDIT/keep.md` › "Tools — Keep" is also kept. It lists the capabilities with their sources.

## Work

### 1. Design kit in Arcade Link

Branch `design/kit` in Arcade-Link.

1. `design/tokens.json`: every value in `STANDARD.md` §2–4. Use these groups: `neutral.{light,dark}`,
   `status`, `accent.<app-id>.{light,dark,text,soft}`, `type`, `space`, `radius`, `size`, `motion`,
   `shadow`, `icon`. The source values are Tools' `style.css` neutrals and the accent table in
   STANDARD §2: Find moves to lime, Shelf to fuchsia, and Tools stays green.
2. `design/generate.py` (Python stdlib only, deterministic output), which writes:
   - `design/css/arcade.css`:
     - custom properties for light and dark, plus `prefers-color-scheme` handling with
       `html[data-theme]` override, the same pattern as Tools today;
     - `[data-app="<id>"]` accent scopes;
     - the base, shell and component rules, lifted from Tools' `style.css` (§Base … §Markdown) and
       renamed onto tokens. This file *is* Tools' current look, made reusable.
   - `design/qml/Arcade/Theme.qml` (singleton: colours per theme, `accent(appId)`, type, space, radius,
     motion), `Icon.qml`, `Fonts.qml` (loads Inter via `FontLoader`) and `qmldir`.
   - `design/dart/arcade_theme.dart`: `ArcadeTokens`, plus `arcadeTheme(Brightness, appId)` returning a
     Material 3 `ThemeData` mapped onto the tokens (colour scheme, text theme with Inter, input, button,
     switch, card, dialog, list tile themes).
   - `crates/arcade-link/src/design.rs` behind a new `design` feature:
     - `Palette { bg, panel, sunken, hover, line, line_strong, text, muted, faint, ok, warn, danger, accent,
       accent_text, accent_soft }` as `0xRRGGBB`/RGBA consts for light/dark, plus `palette(theme, app_id)`;
     - type, space, radius and size consts;
     - `inter_font_bytes()` (the bundled font, `include_bytes!`);
     - an `egui` sub-feature adding `apply_egui(&egui::Context, theme, app_id)` (Visuals, Style spacing,
       rounding, fonts).
   - Component sets per toolkit (STANDARD §5) are built by the first app spec of that toolkit, inside
     Link's `design/`, so the next app of the same toolkit only consumes them: QML components
     (Shelf or Wheel, whichever goes first), egui widgets (Find or Lens), Flutter widgets (Clipboard).
     The CSS components are complete here, since Tools already has them.
   - `assets/tokens.json`, regenerated as the backward-compatible subset (same keys) so existing
     integration surfaces keep working.
   - `design/STANDARD.md`, a copy of `ARCADE_OVERHAUL/STANDARD.md`.
3. Check every accent's contrast pair in `generate.py`: light accent vs white ≥ 4.5, dark accent vs dark
   `bg` ≥ 7, `accent-text` on accent ≥ 4.5. A failing pair is an error.
4. `design/fonts/`: Inter 4.x variable (`InterVariable.ttf`, `InterVariable.woff2`, italic not needed) and
   `OFL.txt`. Add it to Link's licence notes.
5. `design/icons/`:
   - the SVGs (24×24, stroke 1.5, round caps, `currentColor`), seeded from every path in Tools'
     `src-ui/components/Icon.svelte`;
   - `icons.json` (name → path data), from which `generate.py` emits `design/css/icons.ts` (path map),
     `design/qml/Arcade/Icon.qml` (Shape/PathSvg), `design/dart/arcade_icons.dart` (CustomPainter path
     map) and `design.rs` `ICONS` (for tiny-skia);
   - `design/app-icons/`: `make.py` plus the generated icon sets for all eight apps (STANDARD §8). Tools
     adopts its own set here; the other specs adopt theirs.
   - `design/glyphs/`: the app marks `arcade.<app>.svg`, moved here as the canonical copy.
5b. Shared conventions in Link, so the apps can follow STANDARD §8.1 and §10:
   - Format helpers (`formatSize`, `formatRelative`, `formatDuration`, `formatCount`): generated or
     hand-written per toolkit under `design/` (TS, QML JS, Dart, Rust), with the same test cases for each.
   - `paths` module: `app_dirs(app_id)` returns the new `arcade/<app>` config/data/cache folders, plus
     `legacy_dirs(app_id)` (every old location listed in STANDARD §10) and a `migrate_app_dirs(app_id)`
     helper that copies, verifies, then removes, and is safe to run twice. The Qt module exposes the same.
   - Default-shortcut table (`design/shortcuts.json`) with a Link CI check that no two Arcade defaults clash
     on any OS.
   - The "Copy diagnostics" header builder (STANDARD §10).
   - Tools uses all of these itself:
     - Tools data moves from `~/.local/share/app.arcadetools` + `arcade-tools` to `arcade/tools`;
     - backup, restore, uninstall ("remove data") and the shortcut sheet's focused-app detection handle
       both the old and new folders and window classes, so apps migrated later keep working.
6. Wiring:
   - Link `ci.yml`: a job `design` that runs `python3 design/generate.py --check`, which fails if any
     generated file differs, plus `cargo test -p arcade-link --features design,design-egui`.
   - `design/README.md`: how to consume the kit from each toolkit (one short section per toolkit, with
     the exact sync command).
   - `NEW_APP_SPEC.md`: a "UI" section pointing at `design/` and `STANDARD.md`.
   - `CHANGELOG.md`: a `0.4.0` entry.
7. Release Link `0.4.0`:
   - bump `[workspace.package] version`;
   - merge the PR after green CI;
   - tag with the repo's `tag.yml` (`gh workflow run tag.yml -f tag=v0.4.0 -f sha=<main sha>`); tags are
     never pushed by hand.

### 2. Tools on the kit

Branch `overhaul/standard` in Arcade-tools.

1. Sync script:
   - add `scripts/sync-design.py`, which copies `arcade.css`, `icons.ts`, the fonts and the glyphs from a
     Link checkout at the pinned tag into `src-ui/design/`;
   - record the hashes in `VENDORED`;
   - `scripts/verify-vendored.py` checks them in CI.
2. Point both Link dependencies at `tag = "v0.4.0"` (adding `design` to the overlay crate's features), then
   refresh `Cargo.lock`.
3. Remove `src-ui/tokens.css` and `src-ui/tokens.json`. Cut `src-ui/style.css` down to Tools-only layout
   (app card grid, app detail, tray settings, shortcut sheet page); everything shared comes from
   `design/arcade.css`. The rendered pages must look the same as 0.3.8, except where item 5 changes them.
   Compare screenshots before and after for every tab, in light, dark, 1100×760 and 700×600 (the harness
   in `scripts/ui-checks` with the mock backend; screenshots of 0.3.8 are in `AUDIT/screens/tools/`).
4. Fonts and icons:
   - `@font-face` Inter from `src-ui/design/fonts/InterVariable.woff2`, which the CSP already allows
     (`default-src 'self'`);
   - `Icon.svelte` reads the kit's `icons.ts` instead of its own path map;
   - glyphs come from `src-ui/design/glyphs/`.
5. UI changes to meet the standard (and to fix what the 0.3.8 screenshots show):
   - **Page action hierarchy:** page-head actions are `btn` (secondary) or `btn primary`, never `ghost`.
     Today "Refresh catalog" (Apps), "Refresh catalog shortcut sheets" (Shortcuts) and "How it works"
     (Connections) are ghost while "Check now" / "Refresh" are bordered. Ghost is kept only for inline
     tertiary actions such as the "Refresh" next to the "Guides" heading in Learn.
   - **Learn:** one label for one action. Cards say "Read" (opens in Tools) with the external-link icon
     button for "Open on GitHub". The first guide is no longer a different card style with a primary
     button.
   - **Onboarding:**
     - the sidebar entry shows only until onboarding is completed or skipped;
     - afterwards it is reachable from Settings › General › "Set up apps again" (the action already
       exists, `onOnboarding`).
   - **Shortcuts:** the empty state "The shortcut list isn't ready yet… open the overlay once or restart"
     goes away. Opening the tab builds the index (skeleton while it builds; a notice with Retry if it fails).
   - **Sidebar footer:** keep the "Connect apps" switch only in Settings › Connected apps. The footer shows
     a Link status dot + "Apps connected" / "Not connected" (click → Connections), then the version and
     refresh.
   - **Settings order, per STANDARD §6:**
     1. General: Appearance, Start at login, Check for updates automatically, Show notifications.
     2. Shortcuts: overlay switch + overlay shortcut field, and a link to the Shortcuts tab for app
        shortcuts.
     3. Tray: host app icons, update badge.
     4. Backup and restore.
     5. Connected apps: the Connect switch, with the same copy as the shared Connected apps page.
     6. About: version, channel, logs folder, "Report a problem" (moved from its own section),
        licences.
     7. Uninstall, last.
   - **Every data page** (Home, Apps, Updates, Learn, Connections, Engines, Shortcuts) has the four
     states from STANDARD §5. Check the ones the audit lists as missing.
   - The collapsed sidebar (< 760 px) shows a tooltip on every nav icon and keeps the status dot.
   - Taglines (STANDARD §8):
     - Arcade-catalog `catalog.json` gets a `tagline` per app, equal to each README's one-liner; its schema
       and docs are updated, and older Tools keep working because the field is optional.
     - Tools' app cards, onboarding and tray tooltips show `tagline`. The long `description` stays for app
       detail.
     - Tools' own tagline is "The optional home for the Arcade apps."
   - App-detail, dialogs and toasts follow STANDARD §8 copy rules. Fix any raw error strings the audit
     lists.
6. Shortcut overlay (`crates/arcade-tools-overlay`):
   - replace the hard-coded palette in `src/ui/render.rs` with `arcade_link::design::palette(theme, "arcade.tools")`;
   - load Inter from `inter_font_bytes()` into the cosmic-text `FontSystem` (system fallback for
     missing glyphs);
   - apply Template B: 12 px radius panel, 44 px search field, 40 px rows, key chips with the kit
     metrics, and a footer hint bar ("Esc Close", "↑↓ Move", "Type to filter");
   - theme follows Tools' Appearance setting (System/Light/Dark), not only the system.
7. Tray menu (`src-tauri/src/tray/`): sentence case, the same order as the sidebar, and a separator
   before "Quit Arcade Tools". Status items (update count) read like the sidebar badge.

8. **App icon family:** replace `src-tauri/icons/*`, the overlay crate icon, the README logo with the kit-generated set (STANDARD §8, brand mark and app icons). The tray icon becomes the monochrome glyph.

### 3. Verified bugs

**T1. Tools CI doesn't publish the installer the nightly ecosystem check needs (Medium, verified).**
- *Effect:* Link's scheduled e2e (run 40469636881, 2026-10-27) logs `SKIP arcade.tools: no unexpired
  tools-installer-ubuntu-* AppImage artifact in the latest five successful main runs`. Its Tools
  install/update/repair/uninstall/re-exec check and the Tools hub checks are skipped, yet the run is green.
- *Cause:* `.github/workflows/ci.yml:142` uploads only `overlay-render`. The installer artifact exists only
  in tag release runs, which the fetcher (Link `tools/e2e_artifacts.py:62`, `--branch main`) never sees.
- *Fix:* upload the Linux installer (AppImage + manifest) as `tools-installer-ubuntu-<sha>` from `ci.yml`
  on main, with 14-day retention.
- *Check:* the next scheduled Link e2e runs the Tools checks with no "no unexpired tools-installer" skip.

**T2. 20 links in the offline guides are broken (Medium, verified statically).**
- *Effect:* in Learn, links inside the bundled guides point outside `docs/user/`, e.g. `../STATUS.md`,
  `../PLUGINS.md`, `../tool-catalog.md`, `../ios.md` and `../hero.webp`. Every one is a dead link
  offline. The full list is in `AUDIT/evidence/broken-doc-links.json`.
- *Fix:* `scripts/docs-snapshot.py` rewrites any link that leaves `docs/user/` to the file's GitHub URL on
  the app's main branch, and copies referenced images into the snapshot. The catalog docs check fails on any
  relative link that leaves `docs/user/` (STANDARD §10: user guides link only inside `docs/user/` or to
  absolute URLs).
- *Check:* the link checker over `src-tauri/resources/docs` reports 0 broken.

**Not covered by the audit:** the Tools tester was stopped. The parent's screenshots of every tab (light
and dark, `AUDIT/screens/tools/`) and the benchmark were captured; install, update, rollback,
uninstall, adopt, backup/restore, tray hosting and the shortcut sheet were not used end to end. Do all of
them with real releases as part of the acceptance check below, and fix whatever fails here.

### 4. Cleanup

Remove:
- `src-ui/tokens.css` and `src-ui/tokens.json`. 18 of their custom properties have no consumer, and the
  kit replaces them (§2.3).

Leave as they are:
- `crates/arcade-shortcuts/tests/fixtures/catalog/` and `src-tauri/resources/catalog/shortcuts/`. Both are
  used: test fixtures and the offline snapshot.
- The ignored real-package test `tests/find_artifact.rs:45`. Run it in the Link e2e job instead.
- The remote branch `arcade/wip-local-package-verification`. It is marked "judged unfit, kept for
  reference"; list it for the owner and don't merge it.

Delete merged remote branches (all `arcade/*` and `release/*` that are ancestors of main).

### 5. Project standard

- **Outdated text:** README lines 52 and 107 say Link "v0.3.0"; update them to the new Link tag.
- **Link's early-days docs:** move these to Link's `docs/dev/history/`:
  - `COMPLETION_REPORT.md`;
  - `ARCADE_ECOSYSTEM_PLAN.md` (the canonical copy stays in the catalog's history);
  - `docs/V0.3_REPORT.md`, `docs/benchmarks-0.3.md`, `docs/e2e-0.3.md`.
  `NEW_APP_SPEC.md` stays at Link's root as the live brief, updated to point at `design/` and
  `STANDARD.md`.
- **Catalog `dev/`:** move every file to `dev/history/`. These are `ARCADE_ECOSYSTEM_PLAN.md`,
  `ARCADE_TOOLS_PLAN.md`, `CLOUD_STRESS_TEST_PROMPT.md`, `HANDOFF.md` and `REAL_DESKTOP_TEST_LOG.md`.
  - Delete `dev/NEW_APP_SPEC.md`, which is an identical copy of Link's.
  - Add `dev/overhaul/` (this folder) and a `dev/README.md` that says the overhaul specs are current and
    everything in `history/` is past work.
From `AUDIT/hygiene-and-dev-standard.md`:
- Add `rust-toolchain.toml` (1.88, like Box) and `.nvmrc` (24). CI already uses these versions.
- Turn the `scripts/ui-checks` (races, ux, layout) into `npm run ui-checks` and run them in CI. Today they
  are manual.
- Make the isolation checks in `tests/{lifecycle,hub_lifecycle,link_lifecycle,maintenance,find_artifact}.rs`
  compare against the isolated root instead of the hard-coded `/tmp/`. They fail in any on-disk private
  profile.
- Add the main `LICENSE` (MIT, as Cargo and npm declare). It is missing today.
- Unify the version sources: root Cargo, desktop Cargo, `package.json` and `tauri.conf.json` all come from
  one source, and `scripts/check` fails on drift.
- Developer docs go to `docs/dev/`.
- `scripts/check` = what CI runs.

### 5b. Arcade Link and Arcade-catalog (touched by this spec anyway)

Link test harness. Green currently overstates coverage:
- `tools/stress.py:70` (`files_exist`) counts `{}`, `outputs: []` and text-only outputs as passing file
  checks. Require at least one existing, non-empty output file of the expected type.
- `tools/leak.py:24` checks exit codes only. Add an output-correctness check per workload (the OCR text
  contains the expected words).
- `tools/real_bench.py` caps the handback probe at 10 runs even with `--runs 20`. Honour `--runs`.
- The same e2e run also skips every `*_development_install_suppression` check with "stale or missing
  build: target/fleet/<app>/source": the fleet job doesn't build the app sources before that step. Build
  them (or fetch their CI artifacts) first, so those checks run.
- `tools/e2e.py` with `--allow-skips`: print the skip count in the job summary, and fail if a check expected
  to run is skipped because an artifact is missing (T1 removes the current cause).
- `crates/arcade-link/src/transport.rs:143`: long runtime paths fall back to a literal `/tmp/arcade-<uid>`.
  Use `TMPDIR` (or `XDG_RUNTIME_DIR` with a short hash), and document the rule in SPEC.

Link project standard:
- add `LICENSE-MIT` + `LICENSE-APACHE` (declared, not tracked);
- add `rust-toolchain.toml` (1.88);
- fix the broken link `ARCADE_ECOSYSTEM_PLAN.md:2` (to the catalog copy) and the copied
  `packaging/windows/README.md` links in `SPEC.md:712`, so re-vendoring fixes the apps' copies too;
- delete merged remote branches.

Catalog:
- `ci.yml` runs the same 3-OS validator on every push *and* every PR. Limit it to PRs and main, with a
  concurrency group.
- Fix the broken `SPEC.md` and `COMPLETION_REPORT.md` links in `dev/ARCADE_ECOSYSTEM_PLAN.md:6,7`.
- Leave draft PR #9 (`qa/stress-2026-10`, "please don't merge") open as history; don't merge it.
- Delete the merged `arcade/tools-hub` branch.
- Add the `tagline` field (§2.5).

### 6. Docs and release

- README screenshot and `docs/user/images/*.png` retaken from the new UI (light theme, 1100×760).
- `docs/STATUS.md` dated entry; `CHANGELOG.md` `0.4.0` ("Arcade design kit; …").
- Version 0.4.0 in `package.json`, `src-tauri/tauri.conf.json`, the Cargo manifests (the version source
  `scripts/verify-package.py` reads).
- Merge after 3-OS CI green → `tag.yml` (tag `v0.4.0`, main sha) → `release.yml` on the tag with
  `channel=stable`. Catalog entry unchanged (same repo); check Tools self-updates from 0.3.8 to 0.4.0.

## Acceptance

- [ ] Link `v0.4.0` tagged; `generate.py --check` and the contrast check pass in CI; `assets/tokens.json`
      keys unchanged.
- [ ] Tools has no colour literals outside `src-ui/design/` (`rg -n '#[0-9a-fA-F]{3,8}\b' src-ui --glob '!design/**'`
      returns only documented exceptions), no `font-size` outside the type tokens, no own icon paths.
- [ ] Before/after screenshots of all 8 tabs × light/dark × two sizes show only the intended changes.
- [ ] `scripts/ui-checks` (races, ux, layout) pass; `npm run typecheck`, `cargo clippy -D warnings`,
      `cargo test` pass; 3-OS CI green.
- [ ] Overlay opens with the shortcut in < 100 ms (warm), matches Template B in both themes, uses Inter.
- [ ] Every item in §3 re-checked by using Tools as a user (install, update, rollback, uninstall, adopt,
      backup/restore, tray hosting, shortcut overlay, engines, learn) on the released 0.4.0 AppImage.
- [ ] 0.4.0 released; Tools 0.3.8 updates itself to it.

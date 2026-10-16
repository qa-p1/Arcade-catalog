# Arcade Tools Plan: the home of Arcade

**Seven independent apps that still work alone, and one optional app that installs, updates,
hosts, documents and teaches all of them.**

| | |
|---|---|
| Goal | **Every Arcade app ships a standard installer on all three operating systems** (§7: self-installing AppImage on Linux, per-user Inno/NSIS setup on Windows, dmg with move-to-Applications on macOS), each writing the same receipt, launcher entry and CLI. **Every app can be installed, updated, rolled back and uninstalled from Arcade Tools** through those same installers (§11), and still installs and works without Tools. Done means it works and nothing fails: three-OS CI green, the e2e groups in §17.2 passing, and the real-desktop checks in §17.3 recorded (owner goal, restated 2026-10-13). |
| Status | **In progress** (started 2026-10-11 after owner review). Progress is ticked in §19. |
| Written | 2026-10-11, from `origin/main` of every repository: Box `360e6e8`, Lens `4eecf79`, Look `a26d8d2`, Wheel `9ebaa65`, Clipboard `2ab2c94`, Find `0e903c1`, Shelf `6a0885e` (+ unmerged `fix/hyprland-desktop` `050776c`), Link `7e69e01` (`v0.2.0`), Tools `bdefa44` (`v0.1.0`). |
| Builds on | [ARCADE_ECOSYSTEM_PLAN.md](ARCADE_ECOSYSTEM_PLAN.md) (done, historical), Link's `SPEC.md`, [NEW_APP_SPEC.md](NEW_APP_SPEC.md), each repository's `docs/STATUS.md`. |
| Audience | The orchestrating agent, which runs this plan in T3 Code with GPT sub-agents (§0.5), and the owner, who reviews it first. |

---

## 0. Rules for the agent (read first)

### 0.1 Scope: what you may touch

| Path | What it is |
|---|---|
| `/home/harneet/Work/Coding/Rust/Arcade Box` | Arcade Box (`qa-p1/Arcade-box`) |
| `/home/harneet/Work/Coding/Rust/Arcade-lens` | Arcade Lens (`qa-p1/Arcade-lens`) |
| `/home/harneet/Work/Coding/Rust/arcade-look` | Arcade Look (`qa-p1/Arcade-look`) |
| `/home/harneet/Work/Coding/C++/Arcade wheel` | Arcade Wheel (`qa-p1/Arcade-wheel`) |
| `/home/harneet/Work/Coding/App dev/Arcade-clipboard` | Arcade Clipboard (`qa-p1/Arcade-clipboard`) |
| `/home/harneet/Work/Coding/Rust/Arcade-Find` | Arcade Find (`qa-p1/Arcade-Find`) |
| `/home/harneet/Work/Coding/C++/Arcade-Shelf` | Arcade Shelf (`qa-p1/Arcade-Shelf`) |
| `/home/harneet/Work/Coding/Rust/Arcade-link` | Arcade Link: spec, Rust crate, Qt module, CLI, e2e runner, benchmarks (`qa-p1/Arcade-Link`) |
| `/home/harneet/Work/Coding/Rust/Arcade-tools` | Arcade Tools (`qa-p1/Arcade-tools`) |
| `/home/harneet/Work/Coding/Rust/Arcade-catalog` | **New** (§9). Catalog, bundles, engines list, third-party shortcut sheets, ecosystem docs (`qa-p1/Arcade-catalog`, created empty and public by the owner on 2026-10-11, cloned here) |
| `/home/harneet/Work/Coding/ARCADE_TOOLS_PLAN.md` | This file. Tick progress in §19; fill §21 at the end. |
| `/home/harneet/Work/Coding/NEW_APP_SPEC.md`, `ARCADE_ECOSYSTEM_PLAN.md` | Root copies. Keep them identical to the copies in Link (§16). |
| GitHub metadata of the ten repositories | Descriptions, topics, homepage links, release notes, PRs, merges (§0.2) |

Read-only, never edited: `~/.config/hypr/**` (the shortcut center reads it, §12.3), shell profiles,
system packages. On this machine you may install, adopt and test the owner's **real** Arcade
installs (the owner granted this), but only through the flows this plan builds, and you must
record every change to the live profile in §21.

Not in scope: `Snipyx`, other folders under `Coding/`, CaptionCraft, anything outside the table.

### 0.2 Git and release rules

- On 2026-10-11 every repository's `main` was synced with `origin/main` and nothing was left
  unpushed. The owner's Look navigation edits went in through Look PR #4. Before each phase,
  check again that local and remote are in sync (`git fetch`, `git status -sb`). Never discard
  uncommitted changes: if any appear, ask the owner.
- Shelf `fix/hyprland-desktop` was already squash-merged as Shelf PR #2 (`6a0885e`, tagged `v0.1.1`
  on `main`); the local checkout is back on `main`.
- One feature branch per repository: `arcade/tools-hub`. Commit in focused steps using each repository's
  message style. Set the repository-local identity if it's empty: `qa-p1` /
  `190369222+qa-p1@users.noreply.github.com`. Never change the global git config.
- **The owner allows merging (2026-10-11)** for this plan. For each repository, push the branch,
  open a PR, wait for green CI on Linux, Windows and macOS, verify locally (§17), then merge.
  Merging to `main` publishes releases in most repositories. Merge in dependency order: Link
  (tag `v0.3.0`) → Catalog → apps → Tools. Never push directly to `main`, never force-push,
  never delete tags or releases.
- Link the PRs to this T3 thread (`link_pull_request`) as they're opened.
- No unrelated refactors or dependency bumps. Unrelated bugs go to §20.

### 0.3 This machine (checked 2026-10-11)

- CachyOS (Arch), Hyprland 0.56.2 with a **Lua configuration** (`~/.config/hypr/hyprland.lua` +
  `hyprland/*.lua`, Caelestia shell). The 146 binds all report dispatcher `__lua` in
  `hyprctl binds -j`. Rust 1.99, Node 24, Flutter 3.47, Qt 6.11, CMake 4.4, Python 3.14.
- Live Arcade state: **clean slate (2026-10-11).** The owner had every local install removed:
  binaries, AppImages in Downloads, launcher, autostart and D-Bus entries, icons, registry
  manifests, all app settings and data, Clipboard's keyring identities and two stale
  `~/.bashrc` lines (backup `~/.bashrc.backup-20261011-arcade`). `~/.cache/arcade-dev` (dev
  scripts) was kept. In Phase 9 the owner tests the real first-install experience from
  released packages. The adopt flow is tested in the e2e runner, not on this profile.
- **Safety:** automated GUI and e2e runs use the isolated session (`Arcade-link/tools/e2e.py run`,
  Xvfb, temporary `ARCADE_HOME` / XDG dirs / per-app homes, `HYPRLAND_INSTANCE_SIGNATURE` and
  `WAYLAND_DISPLAY` unset). Real-desktop checks (tray, overlay, launcher, install) are deliberate,
  listed in §17.3, and recorded. Never use `hyprctl dispatch closewindow class:…`: it closes the
  **focused** window (this has killed T3 Code). Use `address:` only. `grim` can hang: give it a
  timeout.
- Wheel: reuse `build/` (LayerShellQt lives in `build/localdeps`); never delete it. Clipboard: use
  `bash scripts/dev.sh …`. Box: don't rebuild the WASM fixtures.

### 0.4 Non-negotiables

1. **Standalone first.** Each app installed alone, or several without Tools, behaves exactly as
   today: its own tray icon, its own settings, and installable and updatable by hand. Every feature in this plan is
   additive.
2. **Tools hosts; it is never a hub.** No app action routes through Tools. If Tools crashes or quits, every
   app gets its own tray icon back within one second, and nothing else changes.
3. **Zero idle cost.** No polling. The only timers allowed are Tools' update check (§11.2), while
   it runs, and dashboard refreshes while the dashboard is visible.
4. **Never block a UI thread** on network, IPC, disk scans or installers.
5. **The user confirms** installs, updates (unless they turned on auto-update for that app),
   adoption, uninstalls and shortcut changes. Nothing outbound happens silently.
6. **Never edit hand-written user config.** Hyprland config, shell profiles and other apps'
   settings are read-only. Generated files are clearly marked and owned by Arcade.
7. **Honesty labels.** A platform not exercised by a real run is "build only" or "not run on a real
   desktop", in docs, STATUS pages and the app UI where relevant.
8. **No half-built features.** Nothing ships as "coming soon". If something can't work on a platform,
   it's hidden there and documented.
9. **Security baseline holds:** HTTPS-only downloads from allowed GitHub hosts, SHA-256 and size
   verified before anything runs, catalog entries restricted to the `qa-p1` owner, no quarantine or
   SmartScreen bypass, and each app's existing safety rules unchanged.

### 0.5 How to run this plan: orchestration and agents

The orchestrator (you) owns the plan, the design decisions, integration across repositories,
reviews, verification, merges and the final report. Implementation work may be delegated through
T3 Code's `delegate_task` to the **Codex provider**:

| Model (`providerInstanceId: "codex"`) | Effort | Use it for |
|---|---|---|
| `gpt-6.1-sol` | `max` | Careful, cross-cutting or subtle work: the Link v0.3.0 protocol, tray-host handshake and Qt port, installers (Linux self-install, Windows Inno/NSIS changes, macOS move), the update/rollback engine, the Hyprland Lua evaluator, security-sensitive paths, and every review round |
| `gpt-6-luna` | `max` | Fast, well-specified, parallel chunks: porting a finished reference implementation into another app, `docs/user/` pages, `shortcuts.json` files, third-party shortcut sheets, tests, UI tabs built against a finished design |

Delegation rules:

- **Only these two models, always at `max`.** Never pick a lower effort for them. **Never use
  `gpt-6-astra`**: it burns through usage limits too quickly. Use the standard service tier, not
  Fast. Don't launch sub-agents on any other model or provider.
- Every task prompt is self-contained: the relevant sections of this plan (pasted, not linked),
  the repository path, the worktree or branch, the exact checks to run, the isolation rules from §0.3,
  and "don't merge, don't push to `main`". Agents commit on the feature branch only; the
  orchestrator pushes, opens PRs and merges.
- Give each round a distinct `clientRequestId`, track each `taskId`, and use `task_status` instead of
  sleeping. For a review round, start a new `delegate_task` with the brief, the prior findings and
  the responses.
- Parallelize across repositories, never within one working tree. Two agents never share a checkout:
  each gets its own worktree (`git worktree add ../<repo>-wt-<task> arcade/tools-hub-<task>`), and the
  orchestrator merges the task branches into `arcade/tools-hub`.
- **Agent reports under-report failures.** Re-run every check yourself before ticking anything. Luna
  output gets a line-by-line review. If an agent loops on the same failure twice, cancel it and
  either re-scope or do the work yourself.
- Reference-first: build each cross-app feature once in a reference app (Find for Rust apps, Shelf
  for Qt apps), review it thoroughly, then hand Luna agents the reviewed diff to port.

Execution rhythm:

- Run phases in order (§19). Within a phase, run independent repositories in parallel.
- **Self-review at the end of every phase:** run that phase's checks and every touched repository's
  standalone suite. Read the whole phase diff against §0.4 and §17.5, fix what you find, re-run once,
  tick the boxes.
- **Three-attempt rule:** a single failing test, build or bug gets three real fix attempts. After that,
  record it in §20 (what, where, what was tried) and move on. Revisit it in the final pass.
- Don't re-run a passing suite unless code it covers changed.
- Stop and ask the owner only for things they alone can provide: passwords, code-signing
  certificates, real Windows or macOS hardware, or a product decision §20 marks as theirs.
  Everything else follows this plan, or the nearest existing code when the plan is silent.

---

## 1. The vision

Today Arcade Tools is a small optional installer: one list, a 17 KB UI budget, no tray. The apps
each carry their own tray icon, and on Linux they're loose AppImages run from wherever they were
downloaded.

After this plan:

```
                 ┌──────────────────────── Arcade Tools (optional) ────────────────────────┐
                 │  Home · Apps (catalog) · Updates · Shortcuts · Learn · Connections ·     │
                 │  Engines · Settings          + one Arcade tray icon + cheat-sheet overlay│
                 └───────┬──────────────┬───────────────┬──────────────┬───────────────────┘
          installs/updates│   hosts trays │   reads docs/  │  rebinds      │ reads catalog
          (app's own      │   (tray.host  │   shortcuts    │  globals      │ (GitHub, cached)
           installer)     │    topic)     │   per version  │ (app.shortcuts.set)
   ┌──────┬──────┬──────┬─┴────┬──────┬───┴──┬──────┐                    ┌─┴──────────────┐
   Box   Lens   Look  Wheel  Clipboard Find  Shelf   ← talk peer-to-peer │ Arcade-catalog │
   └──────┴──────┴──────┴──────┴──────┴──────┴──────┘   over Arcade Link  └────────────────┘
        each: self-installing, launcher entry, CLI on PATH, receipt, docs/user, shortcuts.json
```

- **Every app is a proper installed application** on every OS. A one-time setup puts it in the
  launcher (Super key / Start menu / Applications) and its CLI on PATH, registers it with Arcade, and
  makes it removable.
- **Arcade Tools is the power-user home:** a catalog of everything Arcade, an installer and updater
  that works like a package manager (without being a CLI), one tray icon for all apps, the docs, and a
  shortcut center that makes forgetting a shortcut impossible.
- **Nothing becomes required.** The Link stays peer-to-peer. Tools is resident only for convenience
  (tray, overlay hotkey, update checks), and its absence changes nothing but where the tray icons live.

---

## 2. What exists today (from the code, 2026-10-11)

| | Box | Lens | Look | Wheel | Clipboard | Find | Shelf | Tools |
|---|---|---|---|---|---|---|---|---|
| Stack | Rust + Tauri 2 + Svelte | Rust + egui | Rust + Tauri 2 + vanilla TS | C++20 Qt 6/QML | Flutter + Rust core | Rust (winit/softbuffer overlay, eframe settings) | C++20 Qt 6/QML | Rust + Tauri 2 + vanilla TS |
| Latest release | v0.1.2 | v0.1.1 (+nightly) | v0.1.2 (+nightly) | v0.2.0+build.33 | nightly only | v0.2.1 | v0.1.1 | v0.1.0 |
| Link | v0.2.0 tag | v0.2.0 | v0.2.0 | Qt vendored v0.2.0 | v0.2.0 | v0.2.0 | Qt + fixtures vendored | v0.2.0 |
| Tray impl | Tauri tray | `lens-platform/tray.rs` | Tauri tray (`tray.rs`) | `QSystemTrayIcon` | desktop bridge (GTK/Win32/AppKit) | `ksni` (Linux), `tray-icon` (Win/mac) | `QSystemTrayIcon` | **none** |
| Tray menu | SPEC §8.3 standard: Open · Open Settings · Restart · ─ · Quit (all seven apps) | | | | | | | |
| Linux package | AppImage 111 MB | AppImage 12 MB | AppImage 148 MB | AppImage 44 MB | **tarball** + `install-linux.sh` | AppImage 7 MB | AppImage 48 MB | AppImage 79 MB |
| Linux first-run integration | none (only a local-build script) | autostart + `.desktop` (`autostart.rs`) | `--install-integration` (`integration/linux.rs`) | launcher + autostart (`LinuxBackend.cpp`) | install script | autostart | `Desktop.cpp` | Tools' own |
| Windows package | NSIS (Tauri) | Inno + portable exe | NSIS (Tauri) | Inno + zip | Inno | Inno | NSIS | NSIS |
| Windows CLI on PATH | no | no | no | no | no | no | no | no |
| macOS package | dmg (arm64) | dmg (universal) | dmg (universal) | dmg (arm64 + x86_64) | dmg (arm64) | dmg (universal) | dmg (arm64) | dmg (universal) |
| Release manifest | `arcade-release.json` schema 1 + `SHA256SUMS.txt` in all eight | | | | | | | |

Arcade Tools 0.1.0 today: install, update, repair, uninstall and launch for all seven apps, a
stable/nightly channel per app, start at login, SHA-256 + size verification, rollback on a failed
replace, relaunch in the same mode, and `tools.install` over the Link. The app list is compiled in from
Link `ids::APPS` (7 entries). Modules: `apps.rs`, `link.rs`, `manager.rs`, `paths.rs`,
`platform.rs`, `release.rs`, `source.rs`; UI `src-ui/main.ts` (~200 lines); tests `lifecycle`,
`link_contract`, `link_lifecycle`, `platform_logic`, `releases`, `shelf_onboarding`,
`find_onboarding`.

## 3. What reading the code turned up

| Finding | Consequence |
|---|---|
| All seven tray menus are identical (SPEC §8.3) | Tools can host them generically. It needs `app.settings` and `app.restart` over the Link, plus a menu model for app-specific extras (§6.1) |
| Link methods cover only `app.status` / `app.activate` / `app.quit` | Restarting, opening settings and rebinding need new methods (protocol stays v1; additive) |
| Linux AppImages are run from wherever they were downloaded | Stale launcher, autostart and registry paths (Find in `~/Downloads`, Shelf in `/tmp`). Fixed by self-install (§7) |
| No installer puts a CLI on PATH on Windows; Linux CLI links exist only for hand-installed Lens/Look | Fixed by the install standard (§7.4) |
| The registry records *where* an app is, never *how* it was installed | Tools can't tell a managed install from a dev build reliably. Fixed by install receipts (§6.4) |
| The app list is compiled into Link and Tools | Adding an app needs Link + Tools releases. Fixed by the catalog (§9) |
| Manifest accelerators are inconsistent: Box writes `CTRL+ALT+space`, Wheel `Tab` | Normalization (`spec/vectors/accelerators.json`) exists for clash checks. The shortcut center must display normalized forms, and Box should write the canonical form. Check Wheel's `Tab` (its trigger key may be a hold/tap key, not an accelerator) |
| Hyprland binds are Lua callbacks via helper functions and variables (`create_bind(vars.kbLauncher, hl.dsp.global("caelestia:launcher"))`) | Static parsing can't resolve them. The shortcut center evaluates the config in a sandbox (§12.3) |
| Tauri's Linux tray (libappindicator) doesn't deliver left-click events | Tools uses `ksni` on Linux, as Find does (§8.4) |
| Tools is not resident by default and has no tray | Becomes resident when tray hosting or the cheat sheet is on (§10.1) |
| Look and Box AppImages are 148 MB / 111 MB (bundled WebKitGTK) | Not in scope. Backlog (§20) |

## 4. Owner decisions (from the discussion on 2026-10-11)

| Topic | Decision |
|---|---|
| Tray rule | Apps hide their own icon **only while Tools runs** with "Host app icons" on. The icon returns instantly if Tools quits or crashes. Per-app opt-out in Tools. |
| Tray menu | One Arcade icon: Tools items, then **a submenu per app** (standard items + app extras), then Start/Quit all. |
| Linux package | **Self-installing AppImage** (§7.2). |
| App list | **Remote catalog file** in a GitHub repository (§9). |
| Cheat-sheet scope | Arcade apps + window manager binds + **a bundled database of popular apps**, for the focused application. |
| Cheat-sheet trigger | **Configurable global shortcut**; a fast native overlay. |
| Customizing | Only **Arcade apps' global shortcuts** are rebindable from Tools. In-app keys are view, search and conflict only. Custom shortcuts (run commands or actions) are **backlog**. |
| Hyprland binds | Read the user's Lua config (implemented as sandboxed evaluation, §12.3) + `hyprctl`. Labels can be edited in Tools. Config never edited. |
| UI stack | **Tauri 2 + Svelte** (as Box). New UI budget. |
| Docs | From each repository's `docs/user/`. A snapshot is bundled in Tools and refreshed per installed version. |
| App settings | Apps keep their own settings windows. Tools opens them and manages cross-app things only. |
| Extras | Dashboard + diagnostics; onboarding + bundles; engines/dependencies; backup/restore + integrations map. |
| Updates | **Notify + one click.** Auto-update is opt-in per app. |
| Apps installed outside Tools | **Offer to adopt.** Dev builds are never touched. |
| What installers set up | Orchestrator's choice, "no hassle on any OS". See §7.1. |
| Platforms | **Linux first, verified on the owner's desktop.** Windows/macOS implemented, built and tested in CI, labeled honestly. |
| Landing | PRs per repository. The orchestrator may merge (owner permission). |

## 5. Design principles

1. **One source of truth per fact.** Registry manifest = what's installed, its capabilities and
   effective global shortcuts. Endpoint = running. Install receipt = how it was installed. Catalog =
   what exists. `docs/user/` = how to use it. `docs/user/shortcuts.json` = every key it has.
2. **One install code path.** Tools installs an app by running *that app's own installer* silently
   (Linux: the AppImage's `--install`; Windows: its Inno/NSIS with silent flags; macOS: copy + the app's
   `--install`). Self-installed and Tools-installed apps are byte-for-byte the same layout, so either
   can take over from the other.
3. **Hosted, not owned.** Tools renders an app's tray menu from what the app publishes, and sends clicks back. The
   app owns its menu, its settings and its shortcuts.
4. **Hand-back is the default state.** Hosting is a live connection. Connection gone means show your own icon.
5. **Version everything.** New Link methods are optional and feature-detected (an older app answers
   `unsupported`, and Tools falls back to CLI flags). Catalog and receipts have `schema` numbers. Readers
   ignore unknown fields.
6. **Offline-capable.** Catalog, docs and shortcut sheets are cached. Tools works fully without
   network except for installing and updating.

---

## 6. Arcade Link v0.3.0 (protocol version stays 1)

All additions are optional for servers. Clients feature-detect them with `describe`'s new
`methods` list, or by an `unsupported` error. Tag `v0.3.0` when Phase 1 passes. All apps move
to it in Phase 3.

### 6.1 New methods

| Method | Params → result | Notes |
|---|---|---|
| `app.settings` | `{}` → `{opened: true}` | Same as `--settings`. |
| `app.restart` | `{mode?}` → `{restarting: true}` | Successor waits for the old process (each app already does this for its tray Restart). `busy` while jobs run unless `force`. |
| `app.menu` | `{}` → `{items:[MenuItem]}` | App-specific tray extras only. The standard four are implied. `MenuItem = {id, title, kind: "action"|"toggle"|"separator", checked?, enabled, effects?}`. Examples: Clipboard "Private mode" (toggle) and "Pause sync"; Find "Rescan index"; Lens "Capture text"/"Pick color"; Shelf "New shelf"; Box "Open pipelines". Changes are announced with `app.changed {app, menu: true}`. |
| `app.menu.invoke` | `{id}` → `{done: true}` | Runs a menu item exactly as the app's own tray would. |
| `app.shortcuts.set` | `{id, accelerator}` → `{applied, via, hint?}` | The app validates, applies live, persists and rewrites its manifest. `via`: `native` / `portal` / `hyprland-runtime` / `manual`. `manual` + `hint` when the platform can't register (for example GNOME Wayland: "Bind `arcade-find --toggle` in Settings → Keyboard"). Errors: `denied` (reserved or invalid), `unavailable`. |
| `app.settings.export` | `{}` → `{outputs:[{type:"file/any", path}]}` | Handoff file with the app's portable settings (§14.4). Must exclude secrets and device identity. |
| `app.settings.import` | `{inputs:[file]}` → `{imported, restartRequired}` | Validates, backs up current settings, applies. |
| `describe` (extended) | adds `methods:[…]` | Lists optional methods the server implements. |

### 6.2 The `tray.host` topic

- Tools' manifest gains `settings.trayHost: {enabled, excluded:[ids]}`.
- **App side** (`TrayHostWatcher`, Rust in the crate + Qt in `qt/`): when the registry watch sees
  `arcade.tools` running with `trayHost.enabled`, the app connects to Tools, says `hello`, and
  `subscribe {topics:["tray.host"]}`. Tools sends `tray.host {hosted: bool, restarting?: bool}` now and on every change.
  - `hosted: true` → hide own icon (keep it constructed, just hidden, so showing again is instant).
  - Connection closed or `hosted: false` → show own icon at once.
  - `restarting: true` (Tools self-update or Restart) → wait up to 5 s for Tools to return before showing
    the icon, so the icons don't flash during a restart.
- **Startup:** an app that starts while Tools is already hosting delays creating its icon until the
  first `tray.host` answer, with a 300 ms cap (it shows the icon if Tools doesn't answer). No flash.
- Zero idle cost: one blocked socket read per app while hosted, no timers.
- `app.status` gains `status.tray: "own" | "hosted" | "none"` for diagnostics and e2e.
- When Link is switched off in an app ("Connect with other Arcade apps" off), the app always shows its own icon.

### 6.3 Manifest additions (schema stays 1)

| Field | Meaning |
|---|---|
| `menu` | Cached `app.menu` items, so Tools can render a not-yet-connected app's menu without IPC at open time (rule of §5.11 in the old plan). |
| `logs` | Optional path of the app's log directory, for diagnostics bundles. |
| `docs` | `{version}` of the user docs this build carries (normally the app version). |
| `install` | Read-only echo of the receipt `method` (`appimage`, `windows-installer`, `macos-bundle`, `manual`, `dev`) as the app sees itself, so a reader without the receipt still gets a hint. |

### 6.4 Install receipts

`<data>/arcade/installs/<arcade-id>.json` (same `<data>` root as the registry, honoring `ARCADE_HOME`),
written by the app's installer (Linux self-install, the Windows installer `[Code]`/NSIS section, the
macOS first-run move) and by Tools. Atomic write, 0600.

```jsonc
{
  "schema": 1, "id": "arcade.find", "version": "0.3.0", "channel": "stable",
  "method": "appimage",            // appimage | windows-installer | macos-bundle | tarball | manual | dev
  "managedBy": "self",             // self | tools  (who updates it); dev builds are never written
  "path": "/home/u/Applications/Arcade/Arcade-Find.AppImage",
  "integration": {
    "desktopEntry": "/home/u/.local/share/applications/arcade-find.desktop",
    "icons": ["/home/u/.local/share/icons/hicolor/256x256/apps/arcade-find.png"],
    "cli": "/home/u/.local/bin/arcade-find",
    "autostart": "/home/u/.config/autostart/arcade-find.desktop",
    "uninstaller": null
  },
  "previous": { "version": "0.2.1", "path": "/home/u/Applications/Arcade/.previous/Arcade-Find.AppImage" },
  "installedAt": "2026-10-12T10:00:00Z", "updatedAt": "2026-10-12T10:00:00Z"
}
```

A **dev build** is detected (no receipt written, `install: "dev"`) when the executable sits under a
directory containing `.git`, or under `target/` or `build/` of a source tree, or when the env var
`ARCADE_DEV_BUILD=1` is set.

### 6.5 The `install` module (Rust crate feature `install`, Qt port `qt/ArcadeInstall.{h,cpp}`)

Shared logic so seven apps don't reimplement it:

- `detect()` → `{runningFrom, isAppImage (APPIMAGE inside APPDIR), receipt, installedPath, state:
  NotInstalled | InstalledHere | InstalledElsewhere{version} | DevBuild}`.
- Linux: `install(opts)`: copy, or move when on the same filesystem, to
  `~/Applications/Arcade/<Name>.AppImage` (a stable name with no version); `chmod 0755`; icons into hicolor
  (16–512 + scalable SVG); `.desktop` entry; `~/.local/bin` symlink; autostart repair; receipt;
  `update-desktop-database` / `gtk-update-icon-cache` if present; re-exec from the installed path with
  the original args.
- `uninstall(opts{removeData})`: the reverse, from the receipt only (never guesses paths). The data
  folders come from the app.
- `repair()`: rewrite entries from the receipt (fixes moved files and stale `Exec=`).
- Windows/macOS: receipt read/write, PATH-shim helpers (§7.4), macOS translocation and "in Applications?" checks.
- Desktop-entry IDs keep each app's existing ID (`dev.arcadebox.app`, `com.arcadewheel.ArcadeWheel`,
  `arcade.shelf`, `arcade-lens`, `arcade-look`, `arcade-find`, Clipboard's), so no duplicates and no lost
  pins. The installer removes stale duplicates carrying `X-Arcade-Id=<id>` or the known legacy ID that point
  at a different executable.

### 6.6 Shortcut data standard

- `docs/user/shortcuts.json` in every app (schema in `SPEC.md` + JSON Schema in `spec/`), validated in each
  app's CI and in Link's conformance tests:

```jsonc
{
  "schema": 1, "app": "arcade.find", "version": "0.3.0",
  "groups": [
    { "title": "Global", "context": "global", "shortcuts": [
      { "id": "toggle", "keys": { "default": "Ctrl+Alt+F" }, "title": "Show or hide Find", "rebindable": true } ] },
    { "title": "Results", "context": "overlay", "shortcuts": [
      { "id": "quicklook", "keys": { "default": "Enter" }, "title": "Quick Look in Arcade Look" },
      { "id": "open", "keys": { "default": "Shift+Enter" }, "title": "Open with the default app" },
      { "id": "pin", "keys": { "default": "Ctrl+Shift+P", "macos": "Cmd+Shift+P" }, "title": "Pin" } ] }
  ]
}
```

- `rebindable: true` only for global shortcuts whose `id` matches a manifest `shortcuts[].id`.
- Canonical key notation: `Ctrl`, `Alt`, `Shift`, `Super` (displayed as ⌘ / Win / Super per OS), `+`-joined, the key
  last, names from `spec/vectors/accelerators.json` (extended with display names). Link gains
  `accelerator::normalize`, `::display(os)` and `::conflicts(a, b)` in Rust and Qt.
- **Pinned notation and file rules (2026-10-11, shared by Link and the catalog):** modifiers are
  `Ctrl`, `Alt`, `Shift`, `Super` in that order; files use canonical names only (`Super` = Cmd, `Alt` =
  Option on macOS); a key sequence is chords separated by one space (`Ctrl+K Ctrl+S`); a modifier alone
  is a chord; key names are a fixed list (`A`–`Z`, `0`–`9`, `F1`–`F24`, `Slash`, `BracketLeft`, `Numpad*`,
  media, mouse, `Code<N>`, …; full list in SPEC §8.5); shifted symbols are Shift + base key. `keys`
  values are a string, an array of alternatives, or `null` (not on that OS); the effective binding is
  the OS value, else `default`. Two bindings conflict when equal or when one is a strict prefix of the
  other. `rebindable` only in context `global`, never in third-party sheets. Third-party sheets replace
  `app`/`version` with `id`, `name`, `checkedVersion`, `sources` (official https pages) and `match`.
- In-app keys are not copied into the manifest: they are static per version, so Tools reads them
  from the docs snapshot. Only effective global shortcuts live in the manifest.

### 6.7 Standard CLI additions (SPEC §8.1)

| Flag | Meaning |
|---|---|
| `--restart` | Restart the running instance (some apps already have it) |
| `--install [--silent] [--no-launch] [--channel C]` | Linux AppImage / macOS bundle: install this copy (§7) |
| `--uninstall [--silent] [--remove-data]` | Remove this installation via the receipt |
| `--repair` | Rewrite launcher, CLI and autostart entries from the receipt |
| `--integration-status` | JSON: receipt, entries present, PATH status. No side effects |

### 6.8 Link repository work

- `SPEC.md`: §4.3 methods, the `tray.host` topic, manifest fields, receipts, §8.1 flags, §8.3 tray hosting,
  §8.5 shortcut data and notation, a new §8.6 "Install standard" (summarizing §7 of this plan).
- Crate: `install` feature, `trayhost` module, `accelerator` module, `describe.methods`, client helpers for every
  new method, mock peer support (`arcade-link mock` answers the new methods, scriptable `tray.host`).
- `qt/`: `ArcadeTrayHost`, `ArcadeInstall`, accelerator helpers, conformance runner updated.
- `spec/vectors/`: new-method messages, `tray.host` sequences (including crash and restart), receipts, shortcuts.json
  valid and invalid, accelerator display and conflict cases.
- `arcade-link` CLI: `ls` shows install method and tray state; `tray` subcommand to watch hosting; `shortcuts`
  dumps every app's effective globals.
- `tools/e2e.py`: new groups `trayhost`, `install`, `shortcuts`, `tools-hub` (§17.2). `benchmarks/`: tray hand-back
  latency, Tools idle RSS, overlay first-frame time.
- `fixtures/`: every app's fixture gains `menu`, `methods`, and Tools' fixture gains `trayHost`.
- Docs: README, CHANGELOG (new), `docs/STATUS.md`, `NEW_APP_SPEC.md` (§16), `COMPLETION_REPORT.md` gains a
  "Tools hub" addendum.

---

## 7. Install and packaging standard (every app, every OS)

### 7.1 What a one-time setup does (the orchestrator's choice, "no hassle")

| | Linux (AppImage) | Windows (per-user installer) | macOS (dmg) |
|---|---|---|---|
| Location | `~/Applications/Arcade/<Name>.AppImage` | `%LOCALAPPDATA%\Programs\<Name>\` | `~/Applications/<Name>.app` (or `/Applications` if the user dragged it there) |
| Launcher | `.desktop` + hicolor icons (Super-key launchers, Caelestia, GNOME, KDE, rofi/fuzzel/wofi) with actions *Settings*, *Quit*, *Uninstall* | Start menu shortcut; desktop shortcut optional (unchecked) | In Applications (Launchpad / Spotlight / Raycast) |
| CLI on PATH | `~/.local/bin/arcade-<app>` symlink | Shim `arcade-<app>.cmd` in `%LOCALAPPDATA%\Arcade\bin`, added **once** to the user `Path` (HKCU, `WM_SETTINGCHANGE` broadcast); removed when the last app is gone | Symlink in `~/.local/bin` if that's on PATH, else offered with the exact command (never edits shell profiles) |
| PATH not set up | One-time hint with the exact line for the user's shell (fish/bash/zsh), never edited | n/a | same as Linux |
| Uninstall | `arcade-<app> --uninstall`, the launcher action, or Tools | Apps & features entry (existing installers) + Tools | Tools, or move to Trash (receipt is cleaned up next time Tools or another Arcade app starts) |
| Start at login | Each app's existing default, shown as a checkbox in the install dialog | Installer task checkbox (same default) | Login item via the app (Wheel/Clipboard native, others as today) |
| Registration | Receipt + the app writes its manifest on first run | Receipt written by the installer | Receipt written on first run |
| Data | Untouched on install and update. Removed only with "Remove settings and data" | same | same |

### 7.2 Linux: the self-installing AppImage

When an AppImage starts (only for real AppImage runs: `APPIMAGE` inside `APPDIR`; never for dev builds, never
with `--background`, `--arcade-invoke`, `--arcade-manifest`, `--version`, or when `ARCADE_NO_INSTALL_PROMPT=1`):

| `detect()` state | What the user sees |
|---|---|
| Not installed | Small dialog in the app's own toolkit: **"Install Arcade Find?"** The body says it adds Find to the app launcher and your apps folder. Options: *Start at login* (app default) and *Remove the downloaded file* (on). Buttons: **Install** · *Just run it once* · *Don't ask again for this file* |
| Installed elsewhere, older | **"Update Arcade Find 0.2.1 → 0.3.0?"** · Update · Run this copy once |
| Installed elsewhere, same or newer | "Arcade Find 0.3.0 is already installed." · Open installed · Run this copy once |
| Managed by Tools | Same as above, and the update goes through Tools (`tools.install` hand-off) if Tools is installed |
| Installed here | Normal start, no dialog |

- The dialog shows before the main UI and costs nothing on normal starts (one `stat` + one small JSON read, off
  the first frame where the toolkit allows).
- `--install --silent` does the same with no UI (used by Tools and by power users).
- Wording and layout are identical in all seven apps. Strings live in Link's `assets/strings/install.json`, so they're
  shared verbatim.
- Clipboard **gains an AppImage** (built from its Flutter bundle). The tarball stays published for one release with
  `kind: "tarball"`, then is dropped. Tools prefers the AppImage.
- Shelf keeps only the AppImage for Tools. The runtime-bundle extraction path in Tools is removed after one release.
- Box gets Linux desktop integration for the first time (today it has none outside a local-build script).

### 7.3 Windows

- Keep each app's existing installer technology (Inno: Lens, Wheel, Clipboard, Find; NSIS: Box, Look, Shelf,
  Tools). Make them uniform:
  - per-user (`PrivilegesRequired=lowest` / `RequestExecutionLevel user`), install to
    `%LOCALAPPDATA%\Programs\<Name>`;
  - Start menu entry, optional desktop shortcut, optional start at login;
  - the PATH shim (§7.1). Shared Inno include and NSIS macro files live in Link `packaging/windows/` and are vendored
    (checksum-pinned like the Qt module);
  - write and remove the receipt;
  - the Apps & features entry with version, publisher `qa-p1`, homepage pointing at the catalog page;
  - `/VERYSILENT` / `/S` paths that do the same as the UI path (Tools relies on them), plus `/MERGETASKS` for the start-at-login choice.
- Lens's portable exe and Wheel's zip remain as extra downloads (`kind: "portable"`, never used by Tools).
- Unsigned: SmartScreen will warn. Docs explain "More info → Run anyway". Code signing is an owner decision (§20).

### 7.4 macOS

- dmg with the usual drag-to-Applications layout.
- First run from a translocated or read-only location (dmg, Downloads): **"Move Arcade Find to Applications?"** →
  copy to `~/Applications` (or `/Applications` if writable), relaunch, receipt, CLI symlink offer.
- Gatekeeper: unsigned and not notarized. Docs explain right-click → Open. Never remove quarantine for the user.

### 7.5 Release manifests

`arcade-release.json` stays schema 1, with optional asset fields added: `"installArgs"` (Linux/macOS: `["--install",
"--silent"]`) and `"kind": "portable"`. Tools ignores portable assets. The generator in `VENDORED` is updated in every
repository from Link's canonical script.

---

## 8. Tray hosting (Tools side)

### 8.1 The menu

```
[Arcade icon]  (left click: open Arcade Tools · badge when updates are available)
  Open Arcade Tools
  Show shortcuts                         Super+/
  2 updates available…                   (only when there are any)
  ──────────
  Arcade Box          ▸  Open Arcade Box · Open Settings · Open pipelines · ─ · Restart · Quit
  Arcade Clipboard    ▸  Open · Settings · ✓ Private mode · Pause sync · ─ · Restart · Quit
  Arcade Find         ▸  Open · Settings · Rescan index · ─ · Restart · Quit
  Arcade Lens         ▸  Capture · Capture text · Pick color · Settings · ─ · Restart · Quit
  Arcade Look  (not running) ▸  Start Arcade Look · ✓ Start at login
  …
  ──────────
  Start all · Quit all Arcade apps
  Quit Arcade Tools                      (apps get their icons back)
```

- Lists **installed** apps (registry) in catalog order, with running state. Apps the user opted out of keep their own
  icon and are listed with "(own icon)".
- Menus come from cached manifest `menu` fields (no IPC when the menu opens) and refresh on `app.changed`.
- Clicking an item sends the Link call. If the app isn't running, "Open" launches it (`--background` then `app.activate`,
  per the old plan's §5.8 timing).
- "Quit all" asks once if any app reports `busy`.

### 8.2 Settings (Tools → Settings → Tray)

*Host Arcade app icons in the Arcade tray* (default **on**) · per-app *Keep its own icon* · *Show update badge* ·
*Start Arcade Tools at login* (turned on with hosting, can be turned off).

### 8.3 Behavior

- Closing the Tools window keeps Tools running while hosting or the cheat sheet is on. Otherwise it quits as today.
- When the window closes, Tools drops its webview (as Look does) so its idle cost is the tray + Rust core only (§18).
- Tools started at login before the tray host is up: the icon appears when `org.kde.StatusNotifierWatcher` appears
  (Wheel's fix `917e624`; `ksni` handles re-registration).
- Tools quits → it sends `tray.host {hosted:false}` to every subscriber and closes the connections → icons return.
  Tools crashes → sockets close → icons return. Self-update or Restart → `restarting:true` first (§6.2).

### 8.4 Implementation

Linux: `ksni` (SNI over D-Bus, left-click activate, submenus, live updates). Windows/macOS: Tauri's tray API. One
`TrayModel` built in the Rust core and rendered by both backends. Icons: the Arcade mark + per-app glyphs from
`public/glyphs/` (add Find and Shelf glyphs, which are missing in Tools today).

---

## 9. The catalog: `qa-p1/Arcade-catalog`

A new public repository (`Rust/Arcade-catalog` locally). It's data plus validators and has no releases:
Tools reads `main` through raw GitHub URLs. Add `raw.githubusercontent.com` to Tools' allowed hosts.

```
Arcade-catalog/
├── catalog.json            apps, Tools itself, bundles, minimum versions
├── engines.json            shared helpers (Tesseract, ripgrep, FFmpeg, Poppler, qpdf, eSpeak NG, vips, …)
├── shortcuts/              third-party shortcut sheets, one file per app (§12.4)
│   ├── index.json          window class / process / bundle id → sheet
│   └── firefox.json, vscode.json, …
├── docs/                   ecosystem docs: what Arcade is, how apps connect, install, privacy, FAQ
├── schema/                 JSON Schemas for every file
└── scripts/validate.py     CI: schema, ids, owner allowlist, sheet key notation, no duplicate bindings per context
```

`catalog.json` (schema 1):

```jsonc
{
  "schema": 1, "updated": "2026-10-12",
  "apps": [{
    "id": "arcade.find", "name": "Arcade Find", "repo": "qa-p1/Arcade-Find",
    "pitch": "Find any file instantly", "description": "…", "category": "find",
    "icon": "icons/arcade.find.svg", "screenshots": ["…/docs/user/images/overlay.png"],
    "platforms": { "linux": "verified", "windows": "build-only", "macos": "build-only" },
    "linkProtocol": [1], "minTools": "0.2.0", "docs": "docs/user", "resident": true
  }],
  "tools": { "id": "arcade.tools", "repo": "qa-p1/Arcade-tools", "minTools": "0.2.0" },
  "bundles": [
    { "id": "essentials", "title": "Essentials", "apps": ["arcade.find", "arcade.look", "arcade.shelf"] },
    { "id": "screen", "title": "Screen and capture", "apps": ["arcade.lens", "arcade.box", "arcade.clipboard"] },
    { "id": "everything", "title": "Everything", "apps": "*" }
  ]
}
```

Rules: Tools refuses entries whose `repo` owner isn't in its compiled allowlist (`qa-p1`). Tools caches the last good
catalog and ships a built-in snapshot, so first run works offline. An app whose `minTools` is newer than Tools shows "Update
Arcade Tools to install this". Link's `ids::APPS` stays for the apps' own Connected apps pages. A new app reaches Tools
with one catalog PR (documented in `NEW_APP_SPEC.md`).

---

## 10. Arcade Tools 0.2.0: the app

### 10.1 Process model

- `arcade-tools` (Tauri 2 + Svelte UI + Rust core). Resident (no window) when tray hosting or the cheat sheet is on, and
  started at login then. Otherwise it behaves as today.
- `arcade-tools-overlay` (§12.5), a second small native binary shipped in the same package and started on demand.
- The existing core (`manager`, `release`, `source`, `platform`, `link`) is kept and extended. Existing tests keep passing.

### 10.2 Information architecture (left sidebar)

| Tab | Contents |
|---|---|
| **Home** | Installed app cards: icon, version, channel, running state, tray state, memory/CPU while visible. An updates banner. **Health**: stale registry entries (executable missing), apps run from Downloads/tmp ("Install properly"), missing engines, shortcut conflicts, Link off, unsupported versions, each with a one-click fix. Quick actions: Open, Settings, Restart, Start all. |
| **Apps** (catalog) | Every Arcade app: Installed / Available / filters by category. **App page**: pitch, screenshots, description, platform status labels, Install / Update / Roll back / Repair / Adopt / Uninstall, channel, start at login, tray hosting opt-out, Open / Open Settings, "What it adds to your other apps" (from manifests' actions + catalog), version history with release notes, links to docs and the repository. Bundles row at the top. |
| **Updates** | Available updates with release notes (GitHub release body rendered as sanitized markdown), *Update*, *Update all*, auto-update switch per app, last check time, *Check now*, history log (what changed when, including rollbacks), Tools' own update first in the list. |
| **Shortcuts** | §12: search across everything, This app / Arcade / Window manager / Apps views, conflicts, rebind Arcade globals, cheat-sheet settings, Hyprland label editor. |
| **Learn** (docs) | Ecosystem guides (from the catalog repository) + per-app docs (getting started, features, shortcuts, FAQ, troubleshooting), full-text search, "for your installed version" or "latest", works offline. |
| **Connections** | Integrations map: apps as nodes, edges as actions one app offers another (from manifests), each app's Connected-apps state read from its manifest `settings`, link off/on per app shown, "Open in <app>" to change it there. Flagship flows explained with links into Learn. |
| **Engines** | `engines.json`: each helper with status (found at path / missing / downloaded by Arcade), which apps use it and for what, install guidance per OS and distro (pacman/apt/dnf/winget/brew commands to copy), Link-managed Tesseract download where supported. Never installs system packages itself. |
| **Settings** | Tray (§8.2), cheat-sheet shortcut, update checks (on/off, notify), catalog source (default only; a test override in debug builds), backup and restore (§14.4), diagnostics (§14.3), Link on/off, theme (system/light/dark), About (versions, licenses, links). |
| **Onboarding** (first run, re-openable) | Welcome (what Arcade is) → pick a bundle or apps → shortcuts review with conflicts (rebind if needed) → tray hosting + start at login → install with progress → "you're set" with Learn links. Adopts existing installs found on the machine along the way. |

### 10.3 UI stack and budgets

- Svelte 5 + Vite, no UI kit, styles from `assets/tokens.json` (shared Arcade tokens). The existing vanilla UI is
  rewritten. The 17 KB budget becomes **≤ 200 KB uncompressed JS+CSS for the shell**, with Learn's markdown rendering
  and the map loaded lazily. `scripts/ui-size.py` is updated.
- Markdown: rendered in Rust (`pulldown-cmark`) and sanitized (`ammonia`). No remote scripts, no inline HTML from
  docs beyond the allowlist, images from the cache or the docs snapshot.
- Accessibility: keyboard navigation for every tab, visible focus, reduced motion, screen-reader labels.
- Every async operation runs on a worker thread (as today), with cancel where possible.

---

## 11. Updates and package management

### 11.1 Sources

GitHub Releases per catalog repository → `arcade-release.json` → asset for this OS/arch → SHA-256 + size check (as
today). Conditional requests with ETags, so unchanged checks are free (the 60 requests/hour unauthenticated limit is
far away with 9 repositories).

### 11.2 Schedule

60 s after Tools starts, then every 6 h while it runs, and when the window opens if the last check is over 1 h old. No
checks while the network is down (the failed request is just recorded). That's the one timer allowed by §0.4.3.

### 11.3 Flow

- New version → tray badge + one desktop notification per version (never repeated) + the Updates tab.
- Update: download → verify → `app.quit` (`busy` → "Finish the job in Arcade Box or update later") → keep the current
  artifact as `previous` → run the new version's installer silently → relaunch in the same mode → the app rewrites its
  manifest → Tools updates the receipt.
- **Roll back** (one step): reinstall `previous` (Linux/macOS: the kept file or bundle; Windows: the kept installer
  from the cache) with the same flow.
- **Auto-update** (opt-in per app): the same flow, only when the app isn't busy and hasn't been used in the last 10 minutes
  (from `app.status`), with a notification afterwards.
- **Compatibility:** a release whose `linkProtocol` doesn't intersect with the installed peers', or whose catalog `minTools`
  is newer than Tools, is held back with a reason ("Update Arcade Tools first").
- **Tools self-update:** the same flow on itself, with `tray.host {restarting:true}` before quitting.

### 11.4 Adopt

Registry entries with no `managedBy: tools` receipt are classified: **manual** (an AppImage in Downloads/tmp/elsewhere, a
Windows install by the user, an app bundle elsewhere), **self-installed** (receipt with `managedBy: self`), or **dev**
(§6.4). Manual and self-installed get "Let Arcade Tools manage this": quit → run the app's own `--install --silent` from its
current file (Linux), or adopt the receipt (Windows/macOS) → relaunch. Dev builds are labeled "Development build" and never
modified. They can still be launched and shown in the tray.

### 11.5 Uninstall

As today (quit → platform uninstaller or removal via the receipt → manifest and receipt removed). Data is kept unless
"Remove settings and data" is ticked, which lists the folders. Plus **Uninstall everything** in Settings, which lists every
app and folder first.

---

## 12. Shortcut center

### 12.1 Sources

| Source | How |
|---|---|
| Arcade apps, global | Manifests' effective `shortcuts` (live) |
| Arcade apps, in-app | `docs/user/shortcuts.json` for the installed version (docs cache), falling back to the bundled snapshot |
| Hyprland | Sandboxed evaluation of the Lua config (§12.3), merged with `hyprctl binds -j` (authoritative key list, including runtime binds that Arcade apps add). hyprlang `.conf` configs: parse `bind*` lines, using `bindd` descriptions |
| Other desktops | Sway (`swaymsg -t get_binding_modes` + config parse), KDE (`kglobalshortcutsrc`), GNOME (`gsettings` media-keys/wm keybindings), Windows and macOS system shortcuts (static sheets in the catalog). Linux non-Hyprland sources: build and unit tests on fixtures, labeled "not run on a real desktop" |
| Popular apps | Catalog `shortcuts/` sheets (§12.4) |

Everything is merged into one index (`<cache>/arcade/tools/shortcuts-index.json`), rebuilt on change: registry watch,
config-file watch on the Hyprland Lua tree, docs or catalog refresh. Never polled.

### 12.2 Conflicts

Normalized chords (§6.6) are compared per scope: Arcade globals vs each other, vs WM binds, vs OS-reserved lists. In-app keys
only conflict within the same app and context. Each conflict shows both owners and offers **Fix** (rebind the Arcade side), or
for WM-vs-WM conflicts, an explanation only (WM config isn't edited). Each app's shortcut recorder keeps its existing registry-backed
"Used by …" warning, and its rules get the same WM data via a cached file the apps can read (optional, read-only, documented).

### 12.3 Hyprland Lua: sandboxed evaluation

- Embed Lua 5.4 (`mlua`, vendored, ≈ 300 KB). Run the user's `hyprland.lua` with `package.path` set to the config directory,
  so `require("hyprland.keybinds")` and `require("variables")` resolve, and a **stub `hl` table**:
  - `hl.bind(key, action, flags)` records `{key, action, flags, file, line}` (call site from `debug.getinfo` on the first
    frame outside helper functions, so `create_bind(...)` lines are what's shown);
  - `hl.dsp.*(…)` return descriptors (`{dispatcher="global", arg="caelestia:launcher"}`, `exec_cmd`, …);
  - every other `hl.*` field is a no-op that accepts anything (metatable `__index` returns itself).
- Sandbox: no `os.execute`, `io.popen`, file writes or `loadlib`. `io.open` is read-only and restricted to the config tree.
  Instruction-count and memory limits stop runaway configs. Evaluation runs in the overlay/index builder, never in Hyprland.
- Labels: a descriptor gives a readable default ("Caelestia: launcher", "Run: qs -c caelestia kill"). A Lua function action
  uses the nearest preceding `-- comment` at its call site ("Restore lock"), else "Lua function (keybinds.lua:66)". The user's own
  labels are stored in Tools (`shortcut-labels.json`) and win.
- Merge with `hyprctl binds -j` by normalized chord + submap. Binds only in `hyprctl` (added at runtime) are shown with their
  description or dispatcher. Binds only in the evaluation (e.g. conditional) are shown as "configured, not active".
- Fixtures: a copy of this machine's config structure (anonymized) + Hyprland's default Lua config + edge cases, under
  `tests/fixtures/hypr/`.

### 12.4 Third-party shortcut sheets (catalog `shortcuts/`)

- Schema = the app `shortcuts.json` schema plus `match: {linux: {class: [...]}, windows: {exe: [...]}, macos: {bundle: [...]}}`.
- Seed set (written from each app's official documentation in our own words, with the source URL recorded per sheet; never copied
  from third-party cheat-sheet sites): Firefox, Chromium/Chrome/Brave, VS Code, Zed, JetBrains IDEs (common keymap), Kitty,
  Alacritty, foot, WezTerm, GNOME Terminal/Ptyxis, Konsole, Nautilus, Dolphin, Thunar, Obsidian, LibreOffice Writer/Calc, GIMP,
  Inkscape, Blender, mpv, VLC, Discord, Slack, Telegram, Spotify, Thunderbird, T3 Code. Roughly 30 sheets, each validated by
  `scripts/validate.py`.
- Contributing a sheet = a catalog PR. Tools refreshes sheets with the catalog.

### 12.5 The cheat-sheet overlay (`arcade-tools-overlay`)

- A small native binary reusing Find's overlay approach (winit + softbuffer + cosmic-text + resvg; layer-shell via
  smithay-client-toolkit on Wayland compositors that support it, a normal floating window elsewhere). The code is copied
  into Tools with attribution, not a dependency on Find.
- Trigger: a configurable global shortcut. **Defaults (owner-confirmed):** Linux `Super+/`, Windows `Ctrl+Alt+/`, macOS `Ctrl+Option+/`,
  checked for conflicts at onboarding. Registration: Hyprland runtime bind (as Find and Lens do), `global-hotkey` on X11, Windows
  and macOS, and on GNOME Wayland the documented `arcade-tools-overlay --toggle` binding.
- **Focused app detection** happens before the overlay maps: Hyprland `activewindow` over its socket; Sway `get_tree`; X11
  `_NET_ACTIVE_WINDOW` + `WM_CLASS`; Windows `GetForegroundWindow` → process exe; macOS `frontmostApplication` bundle id. KDE/GNOME
  Wayland have no generic way, so the overlay opens on "All" with a quick app picker.
- Layout: header with the app's icon + name. Search field focused (type to filter across everything). Sections in columns:
  **This app** · **Arcade** (globals + the focused Arcade app's in-app keys) · **Window manager**. Key chips per OS style,
  conflicts marked. Tab cycles scopes, Esc closes and focus returns to the previous window.
- Reads only the prebuilt index (no evaluation or IPC at open). **Budget: first frame ≤ 80 ms p95** from the key press on
  this machine, 0 idle cost (not running between uses).

### 12.6 Rebinding Arcade globals

Recorder in the Shortcuts tab → conflict check → `app.shortcuts.set` (the app is launched in the background if it isn't
running) → result shown, including `manual` hints → the index refreshes from the rewritten manifest. Older apps without the
method: "Change this in Arcade X's settings" + Open Settings.

---

## 13. Documentation standard

### 13.1 Every app: `docs/user/`

| File | Contents |
|---|---|
| `index.md` | What it is, the three things it's best at, one screenshot |
| `getting-started.md` | Install (per OS, matching §7), first run, the main shortcut, the first useful thing to do |
| `features.md` | Every feature, task-oriented |
| `shortcuts.json` | §6.6; a generated `shortcuts.md` table is committed next to it (CI checks it's up to date) |
| `with-other-apps.md` | What it adds to and gets from each peer (from the Link docs, user-facing wording) |
| `faq.md`, `troubleshooting.md` | Real issues from STATUS pages and bug lists, platform notes, honesty labels |
| `images/` | Screenshots (PNG, ≤ 300 KB each, light + dark where useful) |

Front matter: `title`, `order`, `since` (version). Developer docs (`ARCHITECTURE.md`, `ARCADE_LINK.md`, …) stay where they are.
The README links `docs/user/` first and keeps a short developer section.

### 13.2 Ecosystem docs (catalog `docs/`)

What Arcade is · Installing and updating (with and without Tools, per OS, SmartScreen/Gatekeeper notes) · How the apps connect
(flagship flows) · Tray hosting · Shortcuts · Privacy and security (local-only IPC, no telemetry, what goes over the network) ·
Uninstalling and data · FAQ · Glossary.

### 13.3 Delivery to Tools

At Tools build time, `scripts/docs-snapshot.py` fetches each app's `docs/user/` at its latest stable tag + the catalog docs into
`src-tauri/resources/docs/` (text + images, budget ≤ 8 MB). At runtime, Learn shows the installed version's docs. When those
differ from the snapshot, they're fetched from the repository at that tag and cached under `<cache>/arcade/tools/docs/<id>/<version>/`.
Search uses a small client-side index built from the cached markdown.

---

## 14. Dashboard, onboarding, engines, diagnostics, backup

### 14.1 Dashboard metrics

Per running app: RSS and CPU% (`sysinfo`, refreshed every 2 s **only while Home is visible**), uptime, version, tray state, Link
status. "Arcade total" line.

### 14.2 Onboarding and bundles

§10.2. Bundles come from the catalog. Existing installs are detected and offered for adoption. Every step can be skipped. Re-run from
Settings.

### 14.3 Diagnostics

**Health checks** (Home) with fixes. **Report a problem**: builds a local zip with OS/desktop info, versions, manifests, receipts,
endpoint states, recent log lines from each manifest's `logs` directory, and the Tools operation history. Paths are redacted to `~`,
and tokens and Clipboard device data are never included. It opens the right repository's "New issue" page with a prefilled template.
**The user attaches the file; Tools never uploads.**

### 14.4 Backup and restore

Export: for each running or launchable app that lists `app.settings.export` in `describe.methods`, collect its handoff file. Then
bundle these with Tools' own settings, shortcut labels and the list of installed apps and channels into `arcade-backup-<date>.zip`.
Restore on a new machine: install the listed apps (confirmed), then `app.settings.import` for each. Excluded by contract: Clipboard
device identity, keys and history; Find's index; caches; credentials. Apps without the method are listed as "not included".

### 14.5 Engines

§10.2 Engines tab. `engines.json` lists, per engine: id, name, detect (binary names, version flag, minimum), who uses it for what, a
per-OS install hint, and whether Link's `engines` feature can download it (Tesseract today). Status comes from the same detection the
apps use (Link `engines`), so Tools and the apps agree.

---

## 15. Per-repository work (everything that changes, every repository)

Every repository also gets the common items in the box below.

> **Common to all seven apps:** Link `v0.3.0` (Rust git tag, or vendored Qt module + fixtures with checksums) · new methods
> (`app.settings`, `app.restart`, `app.menu`/`.invoke`, `app.shortcuts.set`, `app.settings.export`/`.import`, `describe.methods`) ·
> `TrayHostWatcher` (hide/show own icon, startup delay, `status.tray`) · manifest `menu`, `logs`, `docs`, `install` · self-installer
> (Linux) + `--install`/`--uninstall`/`--repair`/`--integration-status`/`--restart` · Windows installer standard (shared include,
> PATH shim, receipt, silent parity) · macOS move-to-Applications + receipt · `docs/user/` complete + `shortcuts.json` + generated
> `shortcuts.md` · README rewritten user-first (install via Tools or by hand, link to `docs/user/`, "Works with other Arcade apps",
> developer section) · `docs/STATUS.md` updated with dated verification · `CHANGELOG.md` entry · CI: validate `shortcuts.json`,
> docs links, vendored checksums; release workflow: new asset fields · `VENDORED`/`VENDORED.md`/license inventories refreshed ·
> GitHub repository description, topics (`arcade`, `arcade-apps`, platform topics) and homepage → catalog docs page · release notes
> template linking `docs/user/`.

| Repository | Specific work |
|---|---|
| **Arcade Link** | Everything in §6.8; `packaging/windows/` shared Inno include + NSIS macros; `assets/strings/install.json`; glyphs for every app at all tray sizes; e2e/bench groups; SPEC; `NEW_APP_SPEC.md` rewritten for the new standard (§16); README; CHANGELOG; STATUS; tag `v0.3.0`; `COMPLETION_REPORT.md` addendum. |
| **Arcade-catalog** (new) | Create the repository; `catalog.json` (7 apps + Tools + bundles), `engines.json`, ~30 shortcut sheets, ecosystem docs, schemas, validator, CI, README, CONTRIBUTING (how to add an app or a sheet), LICENSE (MIT for code, CC BY 4.0 for docs and sheets). |
| **Arcade Box** | Linux desktop integration from scratch (self-installer); canonical accelerator casing in the manifest; tray extras (Open pipelines); export/import of settings (pipelines, favorites, presets, *not* history); unify the CLI/desktop DB note in docs (the bug list item stays open unless trivially fixed); `scripts/license_inventory.py` re-run. |
| **Arcade Lens** | Tray extras (Capture, Capture text, Pick color); self-installer replaces its own `.desktop`/autostart writer (keeps the APPDIR fix); Inno include; export/import; remove the portable exe from Tools' view (`kind: portable`); vendored Link fixtures updated. |
| **Arcade Look** | Self-installer folds in `--install-integration` (kept as an alias); NSIS macros; the D-Bus previewer registration stays; tray extras (none beyond standard unless useful); export/import. Work in a worktree (uncommitted owner edits, §0.2). |
| **Arcade Wheel** | Qt `ArcadeTrayHost` + `ArcadeInstall` vendored (`src/link/VENDORED.json`); `LinuxBackend` launcher/autostart code switched to the shared install module (keep the APPIMAGE/APPDIR fix); Inno include; tray extras (Show wheel); export/import (slots, settings, *not* secrets); check the manifest's `Tab` accelerator; macOS native login item unchanged. |
| **Arcade Clipboard** | **New Linux AppImage**; tarball kept for one release; desktop bridge supports hide/show of the tray from Dart via the core's `link_wait` (`tray.host` lands in Rust, forwarded to Dart); tray extras (Private mode toggle, Pause sync); export/import (settings only, never device keys or history); Inno include; first real `stable` release (`v0.1.0`) once green. |
| **Arcade Find** | **Reference implementation for Rust apps**: built first, reviewed, then ported. Tray extras (Rescan index); self-installer; Inno include; export/import (locations, exclusions, pins, *not* the index); `docs/HYPRLAND.md` cross-linked from `docs/user`. Work in a worktree (uncommitted owner edits, §0.2). |
| **Arcade Shelf** | Merge `fix/hyprland-desktop` → `main` first. **Reference implementation for Qt apps.** NSIS macros; tray extras (New shelf, Show shelf); export/import (collections metadata + preferences; owned content optional, size shown); Linux runtime-bundle release dropped from Tools after one release. |
| **Arcade Tools** | §8, §10–§14: Svelte UI, tray host, catalog, receipts, adopt, install via the app's own installer, scheduler, notifications, rollback, self-update, shortcut center + overlay binary, Learn, Connections, Engines, diagnostics, backup, onboarding. Remove the Shelf bundle path and Clipboard tarball path after the transition release. README, STATUS, CHANGELOG, UI budget, CI (overlay binary builds on all three OSes), release (both binaries in every package). |

## 16. Ecosystem-wide documentation and spec updates

- `SPEC.md` (Link): §6 additions; a "Tray hosting", "Install standard" and "Shortcut data" section.
- `NEW_APP_SPEC.md` (Link + the root copy, kept identical): a new app must ship a self-installing package, a receipt, `docs/user/` +
  `shortcuts.json`, the tray-host watcher, the new methods, a catalog PR, and a Tools e2e entry. Checklist updated.
- `ARCADE_ECOSYSTEM_PLAN.md` (root + Link copy): one header line pointing to this plan as the successor for Tools. No other edits
  (historical).
- `COMPLETION_REPORT.md` (Link): an addendum section summarizing this plan's delivery.
- Every app's `docs/ARCADE_LINK.md` / `docs/arcade-link.md`: the new methods and tray hosting.
- Each repository's GitHub "About" (description, topics, homepage) and each release's notes template.
- This plan: progress ticks in §19 and the report in §21.

---

## 17. Testing and verification

### 17.1 Per repository

Existing suites unchanged and passing (old plan §13.3 commands, plus Find `cargo test --workspace` + `scripts/e2e-linux.sh`, and
Shelf `ctest` offscreen + `tests/process_smoke.py`). New unit tests: install module (temp HOME: install, update, uninstall,
repair, duplicates, PATH hint, dev detection), tray-host watcher (hosted, unhosted, crash, restart, startup delay), new methods,
`shortcuts.json` validation, export/import round trip.

### 17.2 Ecosystem e2e (Link `tools/e2e.py`, isolated)

| Group | Checks |
|---|---|
| `install` | Each app's AppImage in a temp HOME: dialog path via `--install --silent`, desktop entry + icons + CLI link + receipt, re-exec, update-from-older copy, uninstall, repair after moving the file, no prompt for dev builds |
| `trayhost` | Start apps then Tools → every app reports `status.tray: hosted`; `kill -9` Tools → all report `own` within 1 s; Tools restart with `restarting` → no flash; Link off in an app → own icon; per-app opt-out |
| `tools-hub` | Catalog from a loopback server, install a bundle, update + rollback, held-back incompatible update, adopt a manual AppImage, self-update, diagnostics zip contents (redaction), backup/restore round trip across two `ARCADE_HOME`s |
| `shortcuts` | Index includes all seven apps' globals + in-app keys, Hyprland fixture evaluation, conflict detection, `app.shortcuts.set` round trip per app, overlay first frame under Xvfb |
| existing 74 checks + Find/Shelf groups | must still pass |

### 17.3 Real-desktop checks (owner's Hyprland, deliberate, recorded in §21)

1. Download each released AppImage into `~/Downloads`, run it, install via the dialog. It appears in the Caelestia launcher (Super),
   the CLI works from fish, autostart points at `~/Applications/Arcade`.
2. Tools tray: one Arcade icon, submenus work (Open, Settings, Restart, Quit, extras), app icons hidden. Quit Tools → icons return.
   `kill -9` Tools → icons return.
3. Cheat-sheet overlay on `Super+/` over Firefox, T3 Code, a terminal, Find, and an unknown app. Hyprland binds labeled from the real
   Lua config.
4. Rebind Find's global from Tools. The Hyprland runtime bind changes, and Find's own settings show it.
5. Update one app from a real release (with a nightly), then roll back.
6. Hand over to the owner for their own first-install run: Tools first, then apps from Tools; and one app installed alone from its AppImage, without Tools.

### 17.4 CI

Every repository's CI green on Linux, Windows and macOS before merge. The Windows/macOS installer paths are exercised in CI where
runners allow: silent install/uninstall of the built installer on `windows-latest`, dmg mount + copy on `macos-latest`. Labeled
"CI only, not a real desktop".

### 17.5 Definition of done (per feature)

Works standalone and with Tools; works with Tools started first or later; handles Tools crash, app crash, busy, offline, an old
app without the new methods; no UI-thread blocking; zero idle cost; docs updated in every repository it touches; platform behavior
stated for Linux X11, Linux Wayland (Hyprland + layer-shell-less), Windows and macOS.

## 18. Performance budgets

| Measure | Budget |
|---|---|
| App startup added by tray-host watcher + install `detect()` | ≤ 5 ms on the critical path |
| Tray hand-back after Tools dies | ≤ 1 s (target ≤ 200 ms) |
| Tools idle (window closed, hosting on) | 0 polling, ≤ 40 MiB RSS (webview dropped), 0 CPU ticks over 30 s except the update timer |
| Tools window open → first paint | ≤ 400 ms warm |
| Overlay key press → first frame | ≤ 80 ms p95 |
| Shortcut index rebuild (all sources) | ≤ 150 ms, off the UI thread |
| Existing app budgets (old plan §5.11, benchmark baseline) | no regression > 5% |

---

## 19. Phased roadmap

Each phase ends with the §0.5 self-review. "Agents" suggests the delegation split. The orchestrator always reviews and verifies.

**Phase 0: Sync, baseline, repositories**
- [x] Pull every repository's `main`; settle uncommitted owner edits (Look PR #4 merged 2026-10-11).
- [x] Shelf: `fix/hyprland-desktop` → `main` (already merged as PR #2, `v0.1.1` on `main`; checked 2026-10-11).
- [x] Baseline: Link e2e (all groups), benchmarks, each repository's suite; record in §21. (Superseded by the Phase 8 runs; see §21 "Baseline".)
- [x] Create `qa-p1/Arcade-catalog` (public) and its local folder (owner created it; cloned 2026-10-11).
- Agents: none (orchestrator).

**Phase 1: Arcade Link v0.3.0**
- [x] Spec, vectors, crate (`install`, `trayhost`, `accelerator`, new methods, `describe.methods`), Qt port, CLI, mock peer, fixtures. (PR Link#3 merged 2026-10-11, two Sol review rounds.)
- [x] Shared Windows installer include/macros, install strings, glyphs.
- [x] e2e groups and bench probes scaffolded against mock peers. Link CI green on three OSes. Merge, tag `v0.3.0` (tagged 2026-10-11 on 33650a8).
- Agents: Sol (crate + spec), Sol (Qt port + vectors), then a Sol review round.

**Phase 2: Catalog**
- [x] `catalog.json`, `engines.json`, schemas, validator, CI (Catalog PR #1, merged 2026-10-11).
- [x] Ecosystem docs (§13.2). (Catalog `docs/`: index, installing, how-apps-connect, tray, shortcuts, privacy, uninstalling, faq, glossary.)
- [x] 31 shortcut sheets (§12.4), official sources recorded per sheet (Catalog PR #1).
- Agents: Luna ×3 in parallel (sheets split by category), Luna (ecosystem docs), Sol review of the validator and schema.

**Phase 3: Apps**
- [x] 3a. Reference implementations: Find (Rust) and Shelf (Qt). All common items + specifics. Full review. (Branches `arcade/tools-hub`; audit 2026-10-13 + fix rounds 2026-10-14.)
- [x] 3b. Ports: Lens, Look, Box (Rust); Wheel (Qt); Clipboard (Rust core + Flutter + AppImage). (Clipboard ships a self-installing AppImage; no tarball fallback needed.)
- [x] 3c. `docs/user/` + `shortcuts.json` for all seven (screenshots taken in the isolated session). (7 pages + `shortcuts.json` in every app and Tools, checked 2026-10-14.)
- [x] Every app's CI green; merge in any order after Link v0.3.0; releases publish (Clipboard's first stable). (Three-OS CI green and merged to `main` 2026-10-14; release assets checked in §21.)
- Agents: Sol (Find reference), Sol (Shelf reference), then Luna ×5 (ports from the reviewed diffs; Clipboard AppImage → Sol), Luna ×7
  (docs per app), Sol review round per app.

**Phase 4: Tools core**
- [x] Svelte migration with feature parity (existing tests pass; GUI e2e 3/3 with the 7-app fix; 78 KB shell). 2026-10-11.
- [x] Catalog client, receipts, adopt, install via the app's own installer, scheduler, notifications, rollback, self-update,
  compatibility holds. (Catalog client, conditional update checks, scheduler, holds, history, markdown, docs search,
  engines done 2026-10-11 and merged into `arcade/tools-hub`; receipts/adopt/installer/rollback/self-update need Link v0.3.0.)
- [x] Tray host (`ksni` / Tauri tray), `tray.host` server, resident mode, start at login. (Hosted icons unregister from the SNI watcher; hand-back within 1 s asserted by every app's `tests/tray-registration.py`.)
- Agents: Sol (core: update engine + receipts + adopt), Sol (tray host), Luna (Svelte parity port), then a Sol review.

**Phase 5: Tools UI**
- [x] Home, Apps + app page + bundles, Updates, Learn (snapshot script, renderer, search), Connections, Engines, Settings, Onboarding.
- Agents: Luna ×4 (tabs, against a design and data contracts the orchestrator fixes first), then a Sol review.

**Phase 6: Shortcut center**
- [x] Index builder (Arcade, Hyprland Lua sandbox + hyprctl, hyprlang, Sway/KDE/GNOME, OS sheets, catalog sheets), conflicts, labels. (Hyprland Lua/hyprlang/hyprctl, catalog + Arcade sheets, conflicts, labels done 2026-10-11: 141/145 real binds matched, 17 ms rebuild. Sway/KDE/GNOME readers landed in Tools d8549bf with fixture tests in `crates/arcade-shortcuts/tests/desktop_readers.rs`; not run on a real Sway/KDE/GNOME desktop.)
- [x] `arcade-tools-overlay` (focus detection, rendering, hotkey registration per platform). (Overlay first frame rendered in CI on three OSes.)
- [x] Shortcuts tab, rebinding through `app.shortcuts.set`.
- Agents: Sol (Lua sandbox + index), Sol (overlay), Luna (tab UI), then a Sol review.

**Phase 7: Diagnostics and backup**
- [x] Health checks with fixes, diagnostics zip + issue templates in every repository, backup/restore across apps. (Issue templates in all 8 repositories; backup compatibility per app re-checked by the Link e2e matrix.)
- Agents: Luna (issue templates ×8 repositories), Sol (diagnostics/backup), then the orchestrator verifies.

**Phase 8: Verification and docs pass**
- [ ] Full e2e (§17.2), benchmarks (§18), every repository's suite, three-OS CI.
- [ ] All docs and spec items in §15–§16; READMEs, STATUS, CHANGELOGs; GitHub metadata.
- Agents: Luna (README/STATUS/metadata pass per repository), then an orchestrator review.

**Phase 9: Release and live migration**
- [x] Merge Tools 0.2.0; confirm every release asset and manifest on GitHub. (Merged 2026-10-14 as 9d637db; assets in §21.)
- [ ] Real-desktop checks §17.3 on this machine, from a clean profile with released packages; record every change.
- [ ] Final pass over §20 parked items; write §21.
- Agents: none (orchestrator, on the real desktop).

---

## 20. Risks, open decisions and backlog

| Item | Notes |
|---|---|
| Hyprland Lua API churn | The Lua config is new (0.56). The stub `hl` table must tolerate unknown calls. Fixtures pin behavior. When evaluation fails, fall back to `hyprctl` keys with a notice |
| Wayland focus detection on GNOME/KDE | No generic API, so the picker fallback is used. A KWin script is possible later |
| Unsigned builds | SmartScreen and Gatekeeper friction undercuts "no hassle" on Windows/macOS. **Owner decision:** code-signing certificates and notarization. Minisign signatures for assets and the catalog are recommended next (the key lives in GitHub secrets; the owner creates it) |
| Tools resident cost | The webview is dropped when the window closes. Measured against §18 |
| GitHub rate limits | ETags + 6 h interval. Unauthenticated is enough. No token is stored |
| Desktop-entry ID migration | Keeping the legacy IDs avoids lost pins. Duplicates are cleaned up only when they point at a different executable |
| Clipboard AppImage | Flutter AppImage packaging is new for this repository. If it fails three attempts, Tools keeps the tarball path and §21 says so |
| Catalog trust | Owner allowlist + HTTPS. A compromised GitHub account is out of scope (same as releases) |
| **Owner decisions (settled 2026-10-11)** | Cheat-sheet shortcut **`Super+/`** on Linux (owner confirmed; free in the owner's Hyprland binds), `Ctrl+Alt+/` Windows, `Ctrl+Option+/` macOS; repository name `Arcade-catalog` (created); Tools starts at login by default only while tray hosting is on |
| **Backlog** | Custom shortcuts (generated `~/.config/hypr/arcade.lua` that the user `require`s once + OS hotkeys in Tools); in-app key remapping; user-made sheets for any app; AppImage size diet (Look 148 MB, Box 111 MB); AUR/native packages; unified settings in Tools; changing Connected-apps toggles from Tools; minisign; code signing; targeted device send and remote invocation (from the old plan) |

**Bugs found along the way:** (add here)

- Link `tools/e2e.py` defaults Shelf to `Rust/Arcade-Shelf`, but the checkout is `C++/Arcade-Shelf`
  (`ARCADE_SHELF_REPO` works around it). Fix the default in Phase 1 e2e work.
- e2e uses prebuilt binaries (Find `target/release`, Look `target/link-tests` via
  `scripts/verify-link.py --build-e2e`); stale builds fail the Look and Find groups. The runner should
  say "stale or missing build" instead of failing checks.
- Link e2e `tools` group asserts the Tools UI lists exactly 5 apps; Tools has listed 7 since Shelf and Find
  joined. The 2026-10-11 baseline passed only because the main checkout's `target/debug/arcade-tools`
  predated that change. Fix: derive the count from Link `ids::APPS`, and check binary freshness.
- `arcade-shortcuts` Lua sandbox had a 100 ms wall-clock limit; under load it aborted after 74 of 145
  binds (found in the integration test run). Sent back for fix: instruction limit primary, 2 s
  backstop, no silently partial index.
- Wheel publishes stable builds as `v<version>+build.<run>` (release manifest version
  `0.2.0+build.N`) while its receipt records `0.2.0`. Tools' `is_newer` treats semver-equal
  versions with different strings as newer, so Wheel would show an update forever. Fix in Tools:
  semver-equal stable versions compare by SHA-256 only (2026-10-13).
- Wheel's Inno `[UninstallDelete]`/`[UninstallRun]` entries used `Check:` functions that Inno
  evaluates at install time, so the Link manifest was never removed on uninstall (Windows CI caught
  it). Moved into uninstall code after ownership is known, as Lens does (2026-10-13).
- Deviation, by design: Clipboard's tray extras are only "Private mode". The app has no separate
  sync pause; Private mode already pauses capture and sharing, so a "Pause sync" item would
  duplicate it.
- Note for the owner: Box's desktop CLI is `arcade-desktop` (and the standalone CLI `arcadebox`),
  not `arcade-box` as §7.1's `arcade-<app>` pattern suggests. It's consistent on all three OSes,
  so it's left as is unless the owner wants a rename.
- Independent audit (2026-10-13), confirmed in code, fixes in progress:
  - On Linux, Find, Lens, Look, Box and Clipboard hid a hosted tray icon with SNI `Passive`, which
    Caelestia's bar (filters only `hiddenIcons`) and Waybar still show. Hosted icons must be
    unregistered. The e2e `trayhost` group checked only `status.tray`; it gains a private
    StatusNotifierWatcher.
  - Tools on Windows: start-at-login was read from the Run key instead of the receipt's Startup
    shortcut, so updates turned it off. A plain `/S` install was broken (the hook moved `$INSTDIR`
    after `SetOutPath`). The stock template created an untracked desktop shortcut. Updates always
    used the default folder even when the user had chosen another.
  - Tools on macOS: no `--install`, so every dmg self-update failed; no move-to-Applications or
    first-run receipt.
  - Lens and Clipboard: the in-app login toggle used the Run key, which their installers delete.
  - Shelf: the NSIS uninstaller ran `RMDir /r` on a user-chosen folder.
  - Box and Shelf CI never ran the real AppImage's self-install.
  - Decision: Tools is the host and has no `docs/ARCADE_LINK.md`; its Link role is documented in
    its README and `docs/user/with-other-apps.md`.
- Find had the same install-time `Check:` bug as Wheel on its `[UninstallDelete]` entries; moved
  into uninstall code and asserted in its Windows CI script (2026-10-13).
- Lens, Look, Box and Shelf still carried their last released version; their release workflows
  publish a stable release only for a new version tag. Bumped to 0.2.0 (Wheel 0.3.0) so the hub
  release is stable, not just `nightly` (2026-10-13).

- Independent audit (2026-10-13) follow-up, fixed 2026-10-14 across Tools and all seven apps:
  catalog repository casing (Tools now matches GitHub owner/repo case-insensitively), nightly
  receipt versions (`ARCADE_RELEASE_VERSION` embedded at build time, Tools accepts
  `X.Y.Z-nightly.*` against its base), Wheel's silent hand-off, Clipboard's macOS
  `--uninstall/--repair/--channel`, Tools self-update while busy and for a self-installed Tools,
  `/Applications` adoption, macOS CLI symlinks removed when they point into the bundle, login
  entries carrying `X-Arcade-Id` and kept in sync with `receipt.integration`, unknown receipt
  fields preserved on rewrite, release workflows publishing only after CI and the lifecycle checks.
- CI's Rust toolchain is newer than the local one and enforces `clippy::nonminimal_bool` and
  `needless_return` where local clippy passed. Run local clippy with
  `-D clippy::nonminimal_bool` before pushing.
- Removing a tray icon on Linux needs the app to drop its SNI bus name (ksni shutdown, Qt
  `setVisible(false)`, closing Clipboard's private GDBus connection); `Passive` is still shown by
  the watcher. Box's removal took just over 1 s in CI, so the test budget for removal is 3 s while
  hand-back keeps its 1 s budget.
- Clipboard replayed queued tray ownership events after rapid Tools restarts (a brief icon
  flash). Tray ownership is state, not an action: the event queue keeps only the latest value.
- Clipboard needs an unlocked Secret Service keyring to start its secure profile and Link; CI
  runs gnome-keyring. Without one the app reports it instead of hanging (docs/linux.md).
- Windows CI that uses a temporary `ARCADE_HOME` must check the PATH entry the installer writes
  for that root, not the real user PATH (Wheel). Shelf's login toggle treated a malformed Startup
  `.lnk` as absent; it now checks the physical file.
- Flaky-on-Windows tests that connect to a just-started Link server must retry the named-pipe
  connect until a deadline (Lens).
- Delegated agents hit provider usage limits twice; work was resumed from the worktrees each
  time. Keep every change committed or clearly listed so a fresh agent can continue.

---

## 21. Completion report

Status on 2026-10-14 (23:30 IST).

**Merged to `main` after three-OS CI (Linux, Windows, macOS) was green on the PR head**

| Repository | PR | Head | Green run | Merge |
|---|---|---|---|---|
| Arcade-Find | #2 | 80cc8ef | [38600212984](https://github.com/qa-p1/Arcade-Find/actions/runs/38600212984) | 706dad1 |
| Arcade-Shelf | #3 | 1b8bedf | [38601744132](https://github.com/qa-p1/Arcade-Shelf/actions/runs/38601744132) | f3dafd4 |
| Arcade-lens | #3 | 34d4569 | [38607114141](https://github.com/qa-p1/Arcade-lens/actions/runs/38607114141) | f10e308 |
| Arcade-look | #5 | f943a06 | [38600222192](https://github.com/qa-p1/Arcade-look/actions/runs/38600222192) | 1640e28 |
| Arcade-box | #3 | b139aa3 | [38600230680](https://github.com/qa-p1/Arcade-box/actions/runs/38600230680) | a9e806f |
| Arcade-wheel | #6 | 3ccd7f3 | [38599266119](https://github.com/qa-p1/Arcade-wheel/actions/runs/38599266119) | deaf79c |
| Arcade-clipboard | #3 | 4fbc2a4 | [38607310577](https://github.com/qa-p1/Arcade-clipboard/actions/runs/38607310577) | 3e6a296 |
| Arcade-tools | #2 | a786164 | [38601196256](https://github.com/qa-p1/Arcade-tools/actions/runs/38601196256) | 9d637db |
| Arcade-catalog | #1–#5 | #5 cherry-picks 09e96b7 | catalog CI, 3 OSes | merged |
| Arcade-Link | #4 (e2e harness, all eight apps; docs/e2e-0.3.md, docs/benchmarks-0.3.md) | 57c920e | PR CI, 3 OSes | 5973c5e |

Red checks on Shelf, Lens and Box PRs were push runs cancelled by CI's concurrency rule; the same
commits have a complete green run (listed above).

**What a user gets**
- Linux: a self-installing AppImage per app (first run offers "Install", `--install --silent`,
  repair when moved, `--uninstall`); Windows: a per-user Inno/NSIS installer, no admin; macOS: a dmg
  with an Applications link, universal or per-architecture bundles, move-to-Applications on first run.
- Every app writes a Link receipt, works without Tools, and discovers the other apps over Link.
  Tools adopts standalone installs, installs from the catalog with the apps' own installers,
  updates, rolls back and uninstalls, and hosts all tray icons in one menu; the apps' own icons
  return within 1 s when Tools exits.

**Releases (stable, each with a Linux AppImage, Windows installer, macOS dmg, `arcade-release.json`
and `SHA256SUMS.txt`; manifests checked against the assets and checksums)**
Find v0.3.0, Lens v0.2.0, Look v0.2.0, Box v0.2.0, Shelf v0.2.0, Wheel v0.3.0+build.44, Clipboard v0.1.0
(first stable), Tools v0.2.0 (includes the backup fix for Lens, Wheel and Shelf settings, PR #4, cf8f0c5).

**Found by the e2e matrix and fixed before release:** Tools' backup refused Lens's settings (a boolean
named `guard_secrets`), Wheel's (no `owner` field) and Shelf's (binary export).

**Measured (Link share of the budgets, docs/benchmarks-0.3.md):** startup cost 0.15 ms p95 (Rust) and
0.23 ms p95 (Qt) against 5 ms, protocol hand-back 0.32 ms p95 against 1 s, shortcut index (fixtures)
20.4 ms p95 against 150 ms. Tools idle RSS, window first paint and overlay latency are not measured yet;
one unverified debug-build reading of Tools idle (188.6 MiB) is over the 40 MiB budget and must be
re-checked on the release build.

**Baseline:** the 2026-10-11 baseline run (Link e2e all groups, each repository's suite) passed but was
not recorded here, and it used a stale Tools binary (§20). The Phase 8 runs replace it: Link #4's
three-OS CI and the scheduled Ecosystem e2e on Link `main`
([38698730640](https://github.com/qa-p1/Arcade-Link/actions/runs/38698730640): install, shortcuts,
tools-hub, trayhost, deterministic contracts, all green).

**Waived:** Link's "existing app budgets, no regression over 5%" (`benchmarks/bench.py --compare`). It needs
before and after builds of every app; the apps' own CI suites and the real-fleet e2e cover regressions instead.

**Still open**
- Cloud real-user stress test (brief: `CLOUD_STRESS_TEST_PROMPT.md`, including every §18 budget), then
  the §17.3 real-desktop checks on the owner's machine (2026-10-15). Neither has been run by agents yet.
- Live profile: no changes were made to the owner's real profile, `~/.config/hypr` or shell
  profiles. Every install test ran in Link's isolated runner or on CI.

### 2026-10-15 follow-up

- Lens restore from a Tools backup failed in the Link real-fleet e2e (`denied: invalid_inputs`). Link 0.3 accepts
  only `file/any` settings inputs, and Tools passed back the app's exported type (Lens: `file/json`). Fixed in
  Tools PR #5, which also bumps Tools to 0.2.1.
- Tools idle memory, release 0.2.0 with `--background`, isolated Xvfb runner: one process at RSS 14 MiB, PSS 8 MiB,
  USS 7 MiB (budget 40 MiB). The 188.6 MiB debug figure likely counted each thread. Still open for the desktop
  test: memory after opening and closing the window, first paint and overlay latency (WebKit needs a GPU session).
- Blank Tools window on newer distributions: on this machine (CachyOS, AMD Radeon), the released Tools 0.2.0
  AppImage's WebKit process aborts with `Could not create default EGL display: EGL_BAD_PARAMETER`. Cause: the
  AppImage bundles Ubuntu 22.04's `libwayland-client.so.0`, because the overlay links it (`wayland-client`
  `system` feature), and that copy breaks the host Mesa EGL. Removing only that library fixes it. Box and Look don't bundle
  it. Fixed in Tools PR #5 (0.2.1): `LINUXDEPLOY_EXCLUDED_LIBRARIES` in CI and release, and the package smoke now
  fails if the library is bundled. Ubuntu-based CI and the cloud VM can't show this bug.
- Idle baseline for every released app (2026-10-15). Each was started with `--background` in Link's isolated runner
  (Xvfb, private D-Bus, temp HOME) on warm runs. Ready means the Link endpoint file appeared; tray registration
  followed within 90 ms. Totals count processes, not threads, and include the 2.7 MiB AppImage runtime parent.
  §18 only asks the apps for no regression over 5%, so this table is the baseline for future checks. Box and
  Clipboard are the heaviest at idle and are worth a look later (backlog).

| App | Release | Ready (ms, median of 3) | RSS / PSS / USS at 60 s (MiB) |
|---|---|---|---|
| Find | 0.3.0 | 41 | 21.2 / 16.2 / 16.0 |
| Lens | 0.2.0 | 46 | 84.2 / 48.2 / 44.9 |
| Look | 0.2.0 | 399 | 53.7 / 46.9 / 46.6 |
| Box | 0.2.0 | 403 | 374.1 / 230.5 / 181.1 (desktop 150, WebKitWebProcess 160, NetworkProcess 62) |
| Shelf | 0.2.0 | 131 | 122.3 / 83.7 / 78.5 |
| Wheel | 0.3.0+build.48 | 232 | 111.6 / 74.7 / 68.5 |
| Clipboard | 0.1.0 | 344 | 247.1 / 193.6 / 185.7 |
| Tools | 0.2.0 | 324 | 17.2 / 10.3 / 10.1 (budget 40 MiB RSS: pass) |

### 2026-10-16 handoff

The owner went remote. All Arcade apps were uninstalled from the owner's desktop (`REAL_DESKTOP_TEST_LOG.md`).
All local work was pushed:
- Tools PR #5 (0.2.1);
- Link PR #5;
- Wheel PR #9 (0.3.1);
- Look branch `arcade/release-webview` (WIP);
- `arcade/ci-speed` branches in Find, Lens, Shelf, Box and Clipboard.

Open work and how to finish it: `dev/HANDOFF.md` in `qa-p1/Arcade-catalog`.

### 2026-10-16 cloud session

Finished the handoff in a cloud session. Each PR below merged after three-OS CI was green on its head.

| Repository | PR | Head | Green run | Merge |
|---|---|---|---|---|
| Arcade-tools | #5 (0.2.1) | 11a741b | [38786317711](https://github.com/qa-p1/Arcade-tools/actions/runs/38786317711) | 8b9672f |
| Arcade-wheel | #9 (0.3.1) | 86f1ed5 | [38864309386](https://github.com/qa-p1/Arcade-wheel/actions/runs/38864309386) | 2918ef1 |
| Arcade-look | #8 (0.2.1) | cec1c7a | [38863633670](https://github.com/qa-p1/Arcade-look/actions/runs/38863633670) | 5c573e5 |
| Arcade-Find | #5 (ci-speed) | 46ee212 | [38869025513](https://github.com/qa-p1/Arcade-Find/actions/runs/38869025513) | 8024712 |
| Arcade-Shelf | #6 (ci-speed) | 68fafa3 | [38869027279](https://github.com/qa-p1/Arcade-Shelf/actions/runs/38869027279) | 5cdca7d |
<!-- SESSION-ROWS -->

**Releases.** For each one, the manifest and `SHA256SUMS.txt` were checked against the GitHub asset digests.
- [Tools v0.2.1](https://github.com/qa-p1/Arcade-tools/releases/tag/v0.2.1): tag run
  [38866610133](https://github.com/qa-p1/Arcade-tools/actions/runs/38866610133), release run
  [38866658640](https://github.com/qa-p1/Arcade-tools/actions/runs/38866658640) (channel stable). The extracted AppImage has no
  `libwayland-client.so.0`.
- [Wheel v0.3.1+build.56](https://github.com/qa-p1/Arcade-wheel/releases/tag/v0.3.1%2Bbuild.56), from main run
  [38865436391](https://github.com/qa-p1/Arcade-wheel/actions/runs/38865436391). The AppImage bundles
  `usr/plugins/iconengines/libqsvgicon.so`.
- [Look v0.2.1](https://github.com/qa-p1/Arcade-look/releases/tag/v0.2.1), from release run
  [38868935686](https://github.com/qa-p1/Arcade-look/actions/runs/38868935686).
- [Box v0.2.1](https://github.com/qa-p1/Arcade-box/releases/tag/v0.2.1) was already published on 2026-10-15.
<!-- SESSION-RELEASES -->

**Found and fixed**
- Wheel's `SettingsLayout` test failed only on Windows CI. The offscreen platform finds no fonts there, and its fallback glyphs
  are one em wide, so every label overflowed. The test now sets `QT_QPA_FONTDIR` to the Windows font folder. The app was not
  affected.
- Look's WIP branch made `keep_alive()` hold the process whenever Link was enabled, so Look never exited when idle. That was
  removed: a peer that finds Look stopped launches it (Link SPEC §7).
- Find on X11: restoring a Tools backup, or saving Settings, with the shortcut Find already holds failed with "Ctrl+Alt+F
  is already used by another application" and turned the shortcut off. global-hotkey drops an X11 grab only when the old
  manager's connection closes, which is after the new manager's grab attempt. Find now keeps the registration it already holds.
  Reproduced in Xvfb against main and the fix. Found by Link's real-fleet backup check.
- Link e2e harness: `Session.kill()` and `stop_apps()` now wait for the whole process group. The AppImage runtime (the group
  leader) exits before the app it runs, so the next profile could start while the old app still held its shortcut grab
  and bus name.

**Known gap.** Link's real-fleet e2e always skips its Tools AppImage checks (manual adoption, self-update). Tools uploads
`tools-installer` artifacts only from `release.yml` on a tag, never from main CI. Closing the gap needs one of two changes:
main CI uploads the installer artifact, or the fleet takes Tools from the latest release.

**Still open: the §17.3 real-desktop checks on the owner's machine**
- The Tools tray host: one icon with a submenu per app, and the apps' own icons come back after Tools quits and after `kill -9`.
- The Super+/ shortcut overlay.
- Rebinding Find's shortcut from Tools.
- One update and one rollback through Tools between two self-installing releases.
- Tools window first paint, and its memory after the window closes.
- Wheel 0.3.1 icons and Settings layout on the real icon theme; Look 0.2.1 and Box 0.2.1 idle memory after their windows close.

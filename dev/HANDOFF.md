# Arcade suite: handoff for the next agent (2026-10-16, updated 2026-10-19)

You are taking over the Arcade Tools overhaul for the owner (GitHub: `qa-p1`). The previous agent ran on the
owner's desktop; you're working remotely. Everything is on GitHub. Nothing important lives on the owner's
machine any more: all Arcade apps were uninstalled and cleaned up there.

Read this file fully before you touch anything. Then read `dev/ARCADE_TOOLS_PLAN.md` (§19 checklist,
§20 bugs and lessons, §21 completion report) in this repository (`qa-p1/Arcade-catalog`).

## 0. If you run in a claude.ai/code cloud session (read first)

- **Attach all 10 repositories to the session**, or use a Claude project. The GitHub proxy only serves
  repositories attached to the session; anything else returns 403 `GitHub access to … is not enabled for this
  session`. The Claude GitHub App must be installed on each repo (or connect with `/web-setup`).
- **GraphQL is blocked.** `gh pr …` and `gh issue …` fail with `GitHub GraphQL is not available from Claude
  Code sessions`. Use the REST API through `gh api` instead:
  - PR info: `gh api repos/qa-p1/<repo>/pulls/<n>`
  - Create a PR: `gh api repos/qa-p1/<repo>/pulls -f title='…' -f head=<branch> -f base=main -f body='…'`
  - Checks for a commit: `gh api repos/qa-p1/<repo>/commits/<sha>/check-runs --jq '.check_runs[]|"\(.name): \(.status) \(.conclusion)"'`
  - Merge: `gh api -X PUT repos/qa-p1/<repo>/pulls/<n>/merge -f merge_method=merge`
  - Re-run failed jobs: `gh api -X POST repos/qa-p1/<repo>/actions/runs/<run>/rerun-failed-jobs`
  - Dispatch a workflow: `gh api -X POST repos/qa-p1/<repo>/actions/workflows/<file>.yml/dispatches -f ref=<ref> -f 'inputs[tag]=v0.2.1' -f 'inputs[sha]=<sha>'`
  - `gh run list/view/rerun/cancel`, `gh workflow run` and `gh api` work through REST.
- **Tags can't be pushed** through the proxy (branch pushes only). That's fine: Tools and Link tag through
  their `tag.yml` workflows.
- **Network:** "Trusted" access covers GitHub and the package registries. Switch to Full only if a needed
  download is blocked.
- **No desktop:** the cloud VM has no real desktop, so section 3 G (real-desktop checks) can't be done there.

## 1. The goal

Arcade is a suite of 7 independent desktop apps plus a hub app (Arcade Tools). The goals, from the owner:

1. Every app ships standard installers: Linux self-installing AppImage, Windows per-user installer (Inno or
   NSIS), macOS dmg. Each GitHub release carries `arcade-release.json` (schema 1) and `SHA256SUMS.txt`.
2. Every app can be installed, updated, rolled back and uninstalled through Arcade Tools, and also works
   alone, installed from its own download.
3. The apps work together over Arcade Link (local IPC) without Tools running.
4. Everything verified on GitHub (3-OS CI green before merge), released, with standard READMEs (logo + image,
   like Arcade Wheel's) and docs.
5. A cloud "real user" stress test (prompt in `dev/CLOUD_STRESS_TEST_PROMPT.md`), including the plan §18
   performance budgets.

## 2. Repositories (all `github.com/qa-p1/…`)

| App | Repo | Tech | Latest stable release | Release mechanism (verify in `.github/workflows`) |
|---|---|---|---|---|
| Find | `Arcade-Find` | Rust | v0.4.3 | `tag.yml` (tag + sha on main), then `ci.yml` dispatched on the tag |
| Lens | `Arcade-lens` | Rust | v0.3.3 | CI auto-tags and releases when main has a new version |
| Look | `Arcade-look` | Rust + Tauri | v0.3.5 | `release.yml` runs after a successful main CI (`workflow_run`) |
| Box | `Arcade-box` | Rust + Tauri | v0.3.5 | `release.yml` runs after a successful main CI (`workflow_run`) |
| Shelf | `Arcade-Shelf` | C++/Qt | v0.3.3 | `tag.yml`, then `build.yml` dispatched on the tag |
| Wheel | `Arcade-wheel` | C++/Qt QML | v0.4.3+build.67 | CI "Publish stable release" job, tags `v<version>+build.<run>` |
| Clipboard | `Arcade-clipboard` | Flutter + Rust | v0.2.5 | `tag.yml`, then `release.yml` dispatched on the tag with `channel=stable` |
| Tools (hub) | `Arcade-tools` | Rust + Tauri + Svelte | v0.3.6 | `tag.yml` (workflow_dispatch: tag + sha on main), then `release.yml` dispatched on the tag with `channel=stable` |
| Link (IPC library) | `Arcade-Link` | Rust | v0.3.0 tag; apps pin main commit `3bbbc5d` (see its CHANGELOG, Unreleased) | `tag.yml` |
| Catalog | `Arcade-catalog` | JSON + docs | n/a | Tools reads `catalog.json` and `docs/` from main |

Tools matches release asset URLs to the catalog repo name **case-insensitively** and requires a stable tag
equal to `v{version}`.

## 3. Current state

### 2026-10-19: where things stand (read this first; A–G below are history)

- Every item in "Open work" A–G below has landed; the versions in §2 are the current stable releases, all
  published with their assets and checksums, all PRs merged, CI green on main in every repo, and Link's
  scheduled real-fleet e2e (`e2e.yml`, `real_apps`) green.
- Fixed and released on 2026-10-18/19 (details in each app's CHANGELOG):
  - AppImage hygiene (Link `childenv`, every app): installing or updating from Downloads no longer leaves the
    downloaded image mounted with its runtime running; restarts and launches of other programs drop the
    image's descriptors; own helpers keep them.
  - Tools, Box and Look no longer crash on their first window from an AppImage (regression of the above,
    `childenv::enter_image_dir`); each app's AppImage CI check now opens a webview with `$OWD` set.
  - Tools: `--settings`; updating while Tools runs switches to the new version (`--install` and a
    double-clicked download).
  - Box: CLI version string; the Island takes keyboard focus on X11 window managers with focus-stealing
    prevention.
  - Look: per-user extraction folder; relative CLI paths; a long day of previews no longer grows the resident
    Look toward the open-file limit (restarts itself after every tenth webview release).
  - Clipboard: `--help`; no stray "Get · Ctrl+Alt+" action on clips; `--arcade-manifest` includes `install`,
    so Tools adopts a manually installed Clipboard in place.
  - Shelf: real start-at-login state; message on desktops without a shortcut portal.
- Soak test (2026-10-19, ~2.5 h, an Xvfb/openbox desktop, all 8 apps resident, ~1,500 user actions over
  5 compressed days with sleep/resume, relogin, hard kills, two machine restarts and mid-session updates
  from Downloads): no app failures; no leftover runtimes or mounts; Box, Find, Shelf, Wheel, Tools steady in
  memory and descriptors. The Look growth above was found there and fixed. Not run to the planned 24 h.
- Known limitations, not bugs: the Clipboard picker does nothing until a mesh exists (Create mesh, even with
  one device); the Wheel's own shortcut needs a desktop shortcut portal on X11 (bind `arcade-wheel --show`);
  Lens keeps one finished child process until its next capture.

### Done and verified

- All 8 apps released and checked: each manifest matches its assets and checksums, and the catalog resolves
  every app to its release.
- All hub branches merged to main. Docs PRs merged, including:
  - standard READMEs;
  - dated CHANGELOGs;
  - user-guide links in release notes;
  - repo homepages pointing at the catalog docs.
- Box 0.2.1: the Island webview is now created on demand and released 15 s after it's hidden. Measured on the
  owner's desktop, idle went from 419 MiB to 81 MiB. Box PR #6 and docs PR #5 are merged and the release is
  published.
- Link #4: the e2e harness is merged.
- Real-desktop test, partial, on CachyOS + Hyprland 0.56 with an AMD GPU. Results are in
  `dev/REAL_DESKTOP_TEST_LOG.md`:
  - all 7 apps installed from releases;
  - they worked together over Link without Tools;
  - tray icons registered and were removed on quit;
  - idle memory and window latency were measured.

### Open work, in priority order

#### A. Tools 0.2.1: PR qa-p1/Arcade-tools#5, branch `arcade/restore-file-any`, head `11a741b`

What's in it:
- Lens settings restore fix: Link 0.3's server only accepts `file/any` inputs for `app.settings.import`.
- Version 0.2.1, with the version read from `tauri.conf.json` in `scripts/verify-package.py`.
- Blank-window fix on newer distros: the AppImage bundled Ubuntu's `libwayland-client.so.0`, which breaks
  host Mesa EGL (WebKit aborts with `EGL_BAD_PARAMETER`).
  - Fixed by building with `@tauri-apps/cli` 2.12.1, the same version Box and Look use. The CLI 2.12.1
    needs `libayatana-appindicator3-dev` on the Linux build machine; it's now in ci.yml and release.yml.
  - `scripts/verify-package.py` now fails if the AppImage contains `libwayland-client.so*`.
  - The `LINUXDEPLOY_EXCLUDED_LIBRARIES` env in the workflows is harmless but not what fixed it.
- Windows NSIS template update for Tauri CLI 2.12 in `packaging/windows/installer.nsi`: added
  `!include "Win\RestartManager.nsh"`, and `CheckIfAppIsRunning` now takes `"$INSTDIR\${MAINBINARYNAME}.exe"`.
  Both copied from Box's working template.
- `VENDORED` updated: the new upstream template sha256 and the adapted file's sha256.
  `scripts/verify-vendored.py` checks it. The previous push forgot this and all 3 jobs failed in the first
  steps.
- CI speedups in `.github/workflows/ci.yml`:
  - Swatinem/rust-cache;
  - no `CARGO_BUILD_JOBS` cap;
  - PR packages built with `CARGO_PROFILE_RELEASE_LTO=false` and `CODEGEN_UNITS=16` (release.yml still ships
    the LTO build);
  - superseded PR runs cancelled;
  - root `*.md`-only changes skip CI.
- Release notes prepend the user-guide link; CHANGELOG has dates.

CI history on this PR:
- Run 38782091357 at `ae8985c`: Linux ✅, macOS ✅ (including the libwayland guard), Windows ❌ at the NSIS
  bundle step (macro `RestartManager_StartSession` not found). That is fixed by `7018ecf` + `11a741b`.
- Run 38785661729 at `7018ecf`: all ❌ at `verify-vendored.py`, because VENDORED wasn't updated. Fixed by
  `11a741b`.
- Run at `11a741b` was cancelled on purpose before it ran.

The local pre-checks pass at `11a741b`: `verify-vendored.py`, `validate_shortcuts.py`,
`test-docs-snapshot.py`, `cargo fmt --check`, `npm run typecheck`. The Windows NSIS build is the only part not
yet proven.

To do:
1. Re-run CI on the PR head (`gh run rerun` the latest run, or push an empty commit only if needed).
   Watch it with `gh pr checks 5 -R qa-p1/Arcade-tools --watch`.
2. If Windows fails again at makensis, compare `packaging/windows/installer.nsi` against the upstream
   template for `tauri-cli-v2.12.1`:
   `https://raw.githubusercontent.com/tauri-apps/tauri/tauri-cli-v2.12.1/crates/tauri-bundler/src/bundle/windows/nsis/installer.nsi`.
   Also diff it against Box's `apps/desktop/src-tauri/windows/installer.nsi`. Port only the upstream changes,
   keep the Tools-specific parts, then update `VENDORED` (both sha256 values) and run
   `python3 scripts/verify-vendored.py` before pushing.
3. When all 6 jobs are green:
   1. `gh pr merge 5 -R qa-p1/Arcade-tools --merge`.
   2. Wait for main CI green.
   3. `gh workflow run tag.yml -R qa-p1/Arcade-tools -f tag=v0.2.1 -f sha=<merge sha>`.
   4. `gh workflow run release.yml -R qa-p1/Arcade-tools --ref v0.2.1 -f channel=stable`.
   5. Verify the release has the AppImage, the `x64-setup.exe`, the universal dmg, `arcade-release.json` and
      `SHA256SUMS.txt`, and that the manifest hashes match.
   6. Download the AppImage, `--appimage-extract` it, and confirm no `libwayland-client.so*` inside.

#### B. Link e2e: PR qa-p1/Arcade-Link#5, branch `arcade/e2e-main-fleet`, head `2bfe07a`

This PR makes the real-fleet e2e use `main` CI artifacts (`ARCADE_E2E_BRANCH`, default `main`). The fleet-wide
backup check now requires every app's settings to back up and restore. The last run failed only on Lens
restore (`denied: invalid_inputs`), which Tools 0.2.1 fixes.

After Tools' main CI is green with the fix, re-run the real-fleet job. Use `workflow_dispatch` on "Ecosystem e2e"
with `real_apps=true` on the PR branch, or re-run the failed job of the PR's latest run. Merge when green.

#### C. Wheel 0.3.1: PR qa-p1/Arcade-wheel#9, branch `arcade/icons-layout`, head `60565f8`

What the owner saw (screenshot evidence in `dev/REAL_DESKTOP_TEST_LOG.md`):
- **Icons:** most app icons show a grey "A" placeholder. The Qt log said
  `system theme "hicolor" and SVG support false`.
  - Cause 1: the AppImage lacked `usr/plugins/iconengines/libqsvgicon.so`.
  - Cause 2: inside the AppImage, Qt can't load the host platform theme (`qtengine`), so the icon theme
    stayed `hicolor` instead of Papirus-Dark.
- **Layout:** the Settings layout clipped at a 1228×693 Hyprland tile.
- **Footer:** shows "0.2" on 0.3.0.

The PR:
- bundles the SVG icon engine, with a CI assertion;
- detects the icon theme (qtengine config → qt6ct/qt5ct → gsettings → kdeglobals → gtk settings.ini);
- makes Settings responsive;
- fixes the footer version;
- bumps the version to 0.3.1.

CI state, last run 38785111841 at `117845e`: Linux ✅, macOS Apple Silicon ✅, Windows ❌ only at the `Test`
step. The new `SettingsLayout` test failed in 13.85 s with no output shown. `60565f8` adds `-o -,txt` to that
CTest command so the next Windows run prints the QtTest diagnostics; its run was cancelled before finishing.

To do:
1. Re-run CI and read the Windows `SettingsLayout` output.
2. If it fails because Windows offscreen grabbing or font metrics differ, rather than real clipping, make the
   assertion platform-tolerant. As a last resort, `QSKIP` on Windows with a comment; layout is the same QML on
   all platforms, and Linux/macOS cover it.
3. Merge when green.
4. Confirm Wheel's stable release `v0.3.1+build.N` publishes with all assets.
5. Extract the AppImage and confirm `usr/plugins/iconengines/libqsvgicon.so` is inside.

#### D. Look 0.2.1: branch `arcade/release-webview` (commit `8b93313`), WIP, untested, no PR yet

Problem: after a preview or Settings window closes, Look keeps a WebKitWebProcess (404 MiB) plus a
WebKitNetworkProcess (36 MiB) alive. `--service` idles at about 60 MiB without them.

The WIP (from a GPT agent, stopped before validation):
- releases the webview 30 s after hide, separate from `idleMinutes` process lifetime;
- adds a readiness handshake so an early `look.preview` isn't lost;
- bumps the version to 0.2.1.

To do:
1. Review the diff carefully. Compare with Box PR #6 (`gh pr diff 6 -R qa-p1/Arcade-box`), which solved the
   same problem.
2. Run `cargo check`/`test`/`clippy -D warnings -D clippy::nonminimal_bool` and `npm run typecheck`, then
   open a PR.
3. Get 3-OS CI green, merge, and publish v0.2.1 through Look's release workflow.

#### E. CI speed PRs: branch `arcade/ci-speed` in `Arcade-Find`, `Arcade-lens`, `Arcade-Shelf`, `Arcade-box`, `Arcade-clipboard`

One commit each, pushed, no PRs yet. Each commit:
- runs CI once per PR instead of push + PR;
- keeps main runs;
- adds the Rust cache;
- removes laptop `CARGO_BUILD_JOBS` caps.

Why it matters: Find and Lens triggered CI on push to every branch *and* on pull_request, so every PR ran the
full 3-OS matrix twice. Shelf did the same for `arcade/**`.

To do:
1. Review each commit. Keep tag triggers that publish releases.
2. Open the PRs one or two at a time; free accounts get only about 5 concurrent macOS jobs.
3. **Before merging, check whether a merge to main publishes a release.** Box's `release.yml` runs after every
   successful main CI. If a workflow-only merge would publish a new release or nightly, decide deliberately.
4. Merge when green.

#### F. After releases: update the docs

Update these, in a docs-only PR to this repo:
- `dev/CLOUD_STRESS_TEST_PROMPT.md` release table: Tools v0.2.1, Box v0.2.1, Look v0.2.1, Wheel v0.3.1.
- the "known recent fixes" list in the same prompt;
- `dev/ARCADE_TOOLS_PLAN.md` §21.

The owner queues the cloud stress test with that prompt.

#### G. Needs the owner's machine; can't be done remotely

Plan §17.3 real-desktop checks still pending:
- the Tools tray host (one icon, submenus, icons return on quit and `kill -9`);
- the `Super+/` cheat-sheet overlay over several apps;
- rebinding Find's shortcut from Tools (the Hyprland runtime bind changes);
- update and rollback of one app through Tools;
- Tools window first paint and memory after closing the window;
- re-checking Wheel 0.3.1 icons and layout and Look 0.2.1 idle memory.

If the owner gives you their machine again, see the safety rules in §5.

## 4. How to check things

- PR checks: `gh pr checks <n> -R qa-p1/<repo>`.
- Job steps:
  `gh run view <run> -R qa-p1/<repo> --json jobs --jq '.jobs[]|{name,conclusion,failed:[.steps[]|select(.conclusion=="failure")|.name]}'`.
- Failed logs: `gh run view <run> --log-failed`. If that's empty, use
  `gh api repos/qa-p1/<repo>/actions/jobs/<job>/logs --allow-escape-sequences | sed 's/\x1b\[[0-9;]*m//g'`.
- Release check: `gh release view <tag> -R qa-p1/<repo> --json assets`. Then download `arcade-release.json` and
  `SHA256SUMS.txt`, and check the hashes and the asset URLs, whose repo must match the catalog entry.
- Tools local pre-checks before any push, in the Tools checkout:
  `python3 scripts/verify-vendored.py && python3 scripts/validate_shortcuts.py docs/user/shortcuts.json && python3 scripts/test-docs-snapshot.py && cargo fmt --all --check && npm ci && npm run typecheck && cargo clippy --workspace --all-targets --locked -- -D warnings`.
  The hub-lifecycle integration tests only run inside Link's isolated runner (`python3 ../Arcade-link/tools/e2e.py run -- cargo test --workspace --locked`, as CI does). Plain local `cargo test` fails them on purpose.
- If you change `packaging/windows/installer.nsi` in Tools: update `VENDORED` and run `verify-vendored.py`.
- Link e2e harness unit tests (in Arcade-Link): `python3 -m unittest tools/test_e2e_hub.py`.

## 5. Rules (the owner's standing constraints)

- **Never push to main, never force-push, never delete or move tags, never use a bare `git stash`.**
  Work on `arcade/*` branches and PRs.
- Merge only when 3-OS CI is green on the PR head. Docs-only PRs (only `.md` files) may be merged after a quick
  check, without waiting for full CI.
- No dependency bumps unless they're needed for a user-facing fix, and say so (example: Tools' Tauri CLI
  2.11.5 → 2.12.1).
- Every stable release needs a version bump. Tags must be `v{version}`, except Wheel's `+build.N`.
- Batch fixes: run every local check you can before pushing, and push once. The owner was frustrated by
  repeated red CI runs caused by checks that could have been run locally.
- Don't push to many repos at once; macOS runners are limited, so jobs queue.
- A known flaky Linux tray-registration assertion (`expected 1 registered items`) may be re-run once.
- If you ever work on the owner's desktop again:
  - never edit `~/.config/hypr` or shell profiles;
  - Hyprland 0.56 `hyprctl dispatch` takes Lua. Don't guess window dispatchers: a wrong one closes the focused
    window. Close Arcade windows with `arcade-link quit <app>`;
  - `grim` works only outside the agent sandbox, with a timeout;
  - log every profile change.
- Register every PR you create or work on with the T3 `link_pull_request` tool if it's available.

## 6. Bugs found on 2026-10-15/16 (for context)

| Bug | Status |
|---|---|
| Tools 0.2.0 can't restore Lens settings (`invalid_inputs`) | fixed in Tools PR #5 |
| Tools 0.2.0 window renders blank on Arch/CachyOS/Fedora (bundled `libwayland-client`) | fixed in Tools PR #5 |
| Box keeps a hidden WebKit webview at idle (419 MiB) | fixed, Box 0.2.1 released |
| Look keeps its webview after windows close (404 MiB) | WIP branch, item D |
| Wheel AppImage: no SVG icon engine, no icon theme, layout clipped at small sizes, wrong footer version | PR #9, item C |
| CI double runs and no caching in several repos | item E |

Idle baseline for all apps (Xvfb runner and the real desktop) is in `dev/ARCADE_TOOLS_PLAN.md` §21 and
`dev/REAL_DESKTOP_TEST_LOG.md`.

## 7. Files in `dev/`

- `HANDOFF.md`: this file.
- `ARCADE_TOOLS_PLAN.md`: the full plan. §19 is the checklist; §20 has the risks, bugs and lessons; §21 is the
  completion report.
- `ARCADE_ECOSYSTEM_PLAN.md`: the earlier ecosystem plan.
- `NEW_APP_SPEC.md`: how to build a new Arcade app.
- `CLOUD_STRESS_TEST_PROMPT.md`: the brief for the cloud real-user stress test.
- `REAL_DESKTOP_TEST_LOG.md`: everything done on the owner's desktop, with measurements and the cleanup.

# Handoff to the local session (2026-11-15 ~20:25 UTC, from the cloud session)

Read, in order: `README.md` (owner decisions win), `PLAN.md`, this file, `PROGRESS.md` (the Status table predates
this file; this file is the current state), `LOCAL.md`, then each repo's `docs/v1/PROGRESS.md` and `DECISIONS.md`.
The older cloud handoff is kept at the bottom for its rules.

**Everything is on GitHub.** No local-only work was left in the cloud container. Branch names are below.

## Rules (still apply; the owner set the last three)

- Rule zero: no broken releases. rc → Gates on the *published* rc → Promote byte for byte → verify the digests.
- Merge only when every check on the PR head is green. Squash for Link; merge commits for the apps.
- Never force-push (except `--force-with-lease` to restart a branch whose history is already merged).
- Clippy before every Rust push with the repo's pinned toolchain (`+1.88.0`: Link, Box, Lens, Find, Look; `1.98.1`:
  Clipboard) and `-D warnings`.
- Commit as `git -c user.name=Claude -c user.email=noreply@anthropic.com commit`. **No trailers anywhere**: no
  Co-Authored-By, no Claude-Session, no "Generated with" in commits, PRs or comments (owner's rule).
- **At most 3 apps in flight at once**, finish one before taking another; Box first.
- Subagents only for concrete, time-consuming jobs with exact instructions; check their output before using it.
  Never ask an agent a judgement question ("is Box ready?").

## 1. Box — finish v1.0.0 (top priority)

- [#46](https://github.com/qa-p1/Arcade-box/pull/46) merged (merge commit 513cb3f): Link 1.0.11 (D22). It fixes
  rc.1's Gates failure (GitHub renamed `Arcade Box_…` assets to `Arcade.Box_…`, so they didn't match
  `SHA256SUMS.txt`/manifest) and Restart's successor running from the FUSE mount instead of the unpacked copy.
- `v1.0.0-rc.2` tagged on 513cb3f ("Tag a release" run 43754130400, green).
- **Release run 43754158123 on `v1.0.0-rc.2` was in progress** at handoff (about 25 min, Windows is the long pole).
- rc.1 stays unpromoted.

Next:
1. When Release is green, check the rc.2 release: asset names `Arcade-Box_1.0.0_…` (hyphen) and every name in
   `SHA256SUMS.txt`, `arcade-release.json` and `manifest.json` present as an asset. If Release fails, find the
   cause, fix on a PR, cut rc.3.
2. Dispatch `gates.yml` on ref `v1.0.0-rc.2` with input `previous: v0.4.3`. All jobs must be green: published files,
   Linux (native notices, verify-appimage, verify-upgrade, verify-resident incl. "Restart stays on the copy", tray),
   budgets, delta, N-1, Windows, macOS, Tier 1 Hyprland, Tier 2.
3. Dispatch `promote.yml` for rc.2 → `v1.0.0`. Download both releases' assets
   (`gh api -H 'Accept: application/octet-stream' repos/qa-p1/Arcade-box/releases/assets/<id>`) and compare
   SHA-256 of every file; check the signed `manifest.json` (trusted comment `app=arcade.box version=1.0.0 … channel=stable`).
4. Box `docs/STATUS.md`, Box `docs/v1/PROGRESS.md`, the catalog entry for Box (catalog.json has no version field:
   decide whether to add one or leave it to the release feed, and write the decision down), catalog `PROGRESS.md`.

## 2. Lens — PR [#24](https://github.com/qa-p1/Arcade-lens/pull/24) open, head 34b1dbb

Branch `claude/sharp-cori-29w5eg`: Link 1.0.11 (D10), Keep a Changelog, Tier 1 `tests/desktop/lens_desktop.py`
(CI `desktop` job after `linux`; gates `desktop` job), BACKLOG.md (LN-10, RD-LENS-4 with reasons, D11).
Local `scripts/check.py` passed on 57a71b3 (216 tests).

**Finding (fixed in 34b1dbb, not yet through CI):** Tier 1's first run (job 132936292488) failed "the overlay opens
on an image". `--window analyze` (Link's "Analyze with Lens") called `lens_platform::monitors()`, which exists only
on X11, so on any Wayland desktop it exited with "monitor geometry is not exposed on Wayland". Now
`gui::analyze_monitor`: X11 monitors as before; Hyprland → focused monitor in physical pixels
(`hyprland::focused_monitor_pixels`); other Wayland → a canvas the size of the image. Tests:
`gui::tests::the_analyze_overlay_has_a_monitor_on_every_desktop`,
`hyprland::tests::monitor_pixels_are_physical_and_follow_the_transform`. Clippy 1.88 and the lens-platform/arcade-lens
tests passed locally. The test script now prints Lens's log when a check stops it early. Add a CHANGELOG
`[Unreleased]` Fixed line for this (not done).

Next: watch #24's CI; if Tier 1 fails further on, read the uploaded `desktop-lens` artifact (lens.log, screenshots).

**Security pass (Sonnet agent) on `claude/sharp-cori-29w5eg-wip-security` (295444b, 7 commits on top of 5999313)**,
not reviewed or merged yet:
- SECURITY.md (every "Tested by" names an existing test; 9 new tests), deny.toml + `deny` CI job, notices generator
  extended (`--check`, `--check-appimage`), licences and notices shipped in all packages.
- Advisories fixed with `cargo update --precise`: rustls 0.23.46, rustls-webpki 0.103.17, webpki-roots 1.0.12,
  tokio 1.54.1, rustix 1.1.6, yanked async-executor/clipboard-win. Accepted with reasons: RUSTSEC-2024-0429/0370
  (gtk via tray-icon, not on Linux builds), 2024-0436 (paste), 2026-0192 (ttf-parser), 2026-0370/0371/0372 (zbus 5).
- cargo deny ran with `--disable-fetch` (cloud had no GitHub access for the DB); CI's live DB may find more.
- To merge: cherry-pick or merge it onto the PR branch. **Its decision is numbered D11, which clashes with the Tier 1
  D11: renumber to D12** (DECISIONS.md, PROGRESS.md, any reference). Windows/macOS packaging changes are unbuilt.
- Real issues it documented in SECURITY.md but did not fix (decide: fix or BACKLOG with reason):
  KDE Connect share leaves `arcade-lens-share-<pid>.png` in the shared temp dir with default permissions and sends to
  the first reachable device; `/tmp/arcade-lens` chmod 0700 fails silently if another user created it; confirmed
  chains bypass `guard_secrets`; plugins with `read-text` receive secret text and are unsandboxed; settings, chains,
  history and logs take the umask.

Then: Round 5 rest (a11y as Box D21, docs/screenshots, schema/downgrade), 1.0.0 bump, rc.1, Gates, Promote.

## 3. Look — branch `claude/sharp-cori-29w5eg` at 8973daa, pushed, **no PR yet**

- a82463d: Link 1.0.11; `lib.rs`/`memory.rs` ask `arcade_link::runtime::is_unpacked_copy()` (D14).
- 8973daa: Tier 1 `tests/desktop/look_desktop.py` + `tests/desktop/other_window.py` (GTK helper window), CI and
  gates `desktop` jobs (D15). Same early-exit log gap as Lens had: on `raise SystemExit(1)` it doesn't print
  look.log; fix like Lens's 34b1dbb.
- Local `scripts/check`: everything passed except the last stage, `check-native.py`, which needs
  `pip install psutil` and the H.264 GStreamer decoder (`gstreamer1.0-libav`, `gstreamer1.0-plugins-bad`) locally.
  CI installs both and main's CI is green, so run it locally with those installed or let CI judge it.

**Security pass on `claude/sharp-cori-29w5eg-wip-security-2` (71c2481, on top of a82463d)**, not reviewed or
merged yet (the older `-wip-security` 5282ef7 is superseded):
- vite 8.3.8; calamine 0.38, zip 9 (archive.rs adapted to `name()` returning Result), pulldown-cmark 0.13.6,
  ruzstd 0.9.1, tokio 1.54.1, rustix 1.1.6; deny.toml + `deny` job; Dependabot (grouped, weekly, no auto-rebase);
  `scripts/notices.py` and `scripts/native-notices.py` with `--check`; notices + LICENSE bundled as Tauri resources,
  Settings → About → "Open notices"; `tests/security_config.rs` (CSP, permissions, no HTTP client),
  `scripts/ui-checks/sanitize.mjs` in `scripts/check`.
- Accepted advisories in deny.toml with reasons: RUSTSEC-2024-0429, 0370, 0436, 2026-0192, unic-* (2025-0075/0080/
  0081/0098/0100), zbus 5 (2026-0370/0371/0372).
- **Its decision is numbered D15, clashing with the Tier 1 D15: renumber to D16.**
- **`packaging/linux/native/packages.json` was mapped from the published 0.4.3 AppImage via the jammy archive, not
  from a build of this commit**, so build.yml's new native-notices step is expected to fail once on the 22.04
  runner; it prints the corrected packages.json and uploads `native-notices` → commit that folder, run
  `scripts/notices.py`, push.
- Documented, not changed: a previewed document's `https` images are fetched (CSP `img-src https:`), telling the
  server the file was opened; script plugins have the window's full IPC and command plugins the user's rights.
- Not run there: full `scripts/check` Linux part; the deny job and build.yml steps on GitHub.

Next: merge the security branch into the Look branch (resolve D15/D16, PROGRESS), run `scripts/check`, push, open the
PR, get CI green incl. Tier 1, merge. Then a11y pass (as Box D21), docs/screenshots, schema/downgrade, rc.1, Gates,
Promote.

## 4. CI speed (owner approved; do after Box v1.0.0 is promoted, before the next app's rc)

Measured on Box: PR CI ~16–18 min (Linux `scripts/check` 5.5 min + AppImage 4.5 min); Release ~25 min (Windows:
"Stage the CLI and trusted plugin worker" 640 s + "Build the installer" 521 s, two release compiles); then Gates.
Repos are public, so Actions minutes are free; only wall time matters.
1. **Link 1.0.12:** Release publishes the files that CI-on-main built for the same SHA instead of rebuilding
   (~25 min per rc). Gates still tests the published files.
2. Windows: one shared release compile for the CLI/plugin worker and the app.
3. Keep CI on push to main: it is the only run that saves the Rust cache (`save-if`), which warms PRs and tags.
Record it as a decision in PLAN/PROGRESS, release Link 1.0.12 the usual way, re-pin apps as they reach rc.

## 5. Paused apps (all pushed)

- **Find:** [#22](https://github.com/qa-p1/Arcade-Find/pull/22) open, head 6a00747 (drop_target
  `Gdk.DragAction.COPY | MOVE` fix, verified locally). Its Tier 1 now fails on `--show report` timing out after 30 s;
  not investigated. Security WIP: `claude/sharp-cori-29w5eg-wip-security` (6c492b4).
- **Clipboard:** step 5 + security WIP on `claude/sharp-cori-29w5eg-wip-step5-security` (0c406f1).
- **Shelf:** step 5 WIP on `claude/sharp-cori-29w5eg-wip-step5` (f6617a9; `appimage_resident.py` expects the marker to
  be the copy's folder). Needs re-vendoring to Link 1.0.11 (vendored at 2748ebf).
- **Wheel:** step 5 WIP on `claude/sharp-cori-29w5eg-wip-step5` (593704b; removes the restart workaround). Needs
  re-vendoring to Link 1.0.11.
- **Link:** v1.0.11 tagged on b00a1ca (main). `claude/sharp-cori-29w5eg-wip-link-unpacked` (c544547) is the
  pre-squash branch of work already in 1.0.11, pushed only so nothing is lost.

## Local tool notes

- `cargo-deny` 0.18.9; its advisory DB fetch needs GitHub access.
- Box's `scripts/check` needs `luac` (lua5.4) and Chromium for Playwright (`PLAYWRIGHT_CHROMIUM`).
- The Link desktop harness needs python3-gi (GTK3) for `other_window.py`.
- Look's check needs `ARCADE_LINK=<path to Arcade-Link checkout>`.

---

# Handoff to the cloud session (2026-11-14, from the local session)

The work moves from the owner's PC to Claude Code cloud. Read, in order: `README.md` (owner decisions win),
`PLAN.md` (steps, exit gates, rule zero, fleet rules, owner-requests checklist), `PROGRESS.md` (newest first; the
Status table and the 2026-11-13/14 log entries), `LOCAL.md` (owner-only items; don't do them), then each repo's
`docs/v1/PROGRESS.md` and `DECISIONS.md`. Update `PROGRESS.md` after every finished step.

**Rough completion of the plan: about 50%.** Every app's P0/P1 findings are fixed. Link and Tools are at step 8.
The other apps are mostly at steps 1+3 (lock, fix), with parts of 2, 4, 5 and 6. Nothing has shipped stable yet.
Fleet finish (§10) has not started.

## Rules that bit us (follow them)

- **Rule zero:** no broken releases. Testing happens on drafts and rc releases only; stable is promoted
  byte-for-byte. Tag a Link release only after CI, the Desktop harness and the real-fleet Ecosystem e2e
  (`e2e.yml`, `real_apps=true`) pass on that exact main commit, via "Tag a release" (`tag.yml`, inputs `tag`, `sha`).
- **Commits:** `git -c user.name=Claude -c user.email=noreply@anthropic.com commit ...`. Never put the owner's
  name or email anywhere. Merge only when every check on the PR head is green. Never force-push.
- **Merge styles:** squash for Link; merge commits for Box, Lens, Shelf, Clipboard, Find, Look and Wheel.
  Clipboard #16 was squash-merged and its branch then conflicted with main. That was fixed with
  `git merge -s ours origin/main`, after checking that main's tree equaled the branch's merged head.
- **Run clippy locally before every Rust push** and compare against the base: newer local toolchains flag lints
  (`collapsible_if`, `chunks_exact`, `is_multiple_of`) that CI's pinned 1.88 doesn't. Box #37 lost two CI cycles
  to a redundant closure and items after a test module, both of which `cargo check` alone didn't catch.
- **Don't wait on CI yourself.** Hand watching to a cheap subagent (Haiku) that reports back. Waits must run as
  background commands; foreground `sleep` is blocked, and watchers otherwise stop early or report stale state.
- **GitHub runners are the bottleneck.** With about 10 PRs open, runs queued 30+ minutes (macOS worst). Batch
  commits and avoid restarting runs needlessly.

## Open PRs and next actions (state at hand-off)

| PR | State | Next |
|---|---|---|
| [Tools #49](https://github.com/qa-p1/Arcade-tools/pull/49) (head ad45884) | Crash reports, cargo deny, **Link 1.0.7**, `ammonia` 4.2.5 (RUSTSEC-2026-0533). 14/15 green; the macOS dmg check was pending. | Merge when green → "Tag a release" `v1.0.0-rc.11` on the merged main SHA (Release builds and publishes a test-channel prerelease) → dispatch `gates.yml` with `update-from: v1.0.0-rc.10` → when every gate passes, "Promote" (`promote.yml`) rc.11 to stable 1.0.0. B1 (signing key) is done. |
| Link main 079f954 = **1.0.8 (unreleased)** | #62 merged: Dart key chips no longer stretch (Clipboard RD-CLIPBOARD-2), QML HintBar elides (Shelf SH-3). CI and Desktop harness green; real-fleet e2e run 43580856047 was in progress. | When e2e is green on 079f954 (or a later main with only #63 on it), tag `v1.0.8`. Then move Clipboard and Shelf to it (vendored kit + pins). |
| [Link #63](https://github.com/qa-p1/Arcade-Link/pull/63) | Rust caches saved only on main (PR caches took 2.6 of the 10 GB). | Merge when green. |
| [Box #36](https://github.com/qa-p1/Arcade-box/pull/36) | Box on Link 1.0.7 (pin, CI link-ref 40ec027, lock, notices). Everything green except Windows (pending). | Merge when green. Then drop Box from `LEGACY_PENDING` in Link `tools/e2e_checks/real_hub.py` once a green Box main build exists. |
| [Box #37](https://github.com/qa-p1/Arcade-box/pull/37) | Untangle (D12): desktop lib.rs 2,542 → 470 (`island`, `tray`, `instance`, `commands/<feature>`); core lib.rs → 767 (`catalog.rs`, pipeline helpers); one `safe_stem` (byte cap, fixes long CJK names), one `rgb_to_hsl`, one `unsafe_in_file_name` (6 copies), one `fileList(tool)`, the design kit's size/duration formatters. Head 8bf89a5 re-running after two clippy fixes. | Merge when green; resolve with #36/#38 (no overlap expected). |
| [Box #38](https://github.com/qa-p1/Arcade-box/pull/38) | CI (D13): PRs build one Linux package; Windows/macOS trim their release build before main saves the cache. Windows PR check 19 min (was 37). | Merge when green; after main saves a cache, measure warm PR time (target < 8 min, Link spec §4). |
| [Lens #19](https://github.com/qa-p1/Arcade-lens/pull/19) | Caches saved only on main. | Merge when green. |
| [Clipboard #18](https://github.com/qa-p1/Arcade-clipboard/pull/18) | Caches saved only on main. | Merge when green. |
| [Find #18](https://github.com/qa-p1/Arcade-Find/pull/18) | Partner agent: FD-1..FD-10, Link 1.0.7, memory trim (W0). 6 green, 2 pending. | Review the diff against `specs/FIND.md`, then merge when green. |
| [Look #20](https://github.com/qa-p1/arcade-look/pull/20) | Partner: RD-LOOK-1, LK-1..LK-11, Link 1.0.7 (retires legacy entries), WebKit/arena memory work. 6 pending. | Review, then merge when green. |
| [Wheel #17](https://github.com/qa-p1/Arcade-wheel/pull/17) | Partner: lock, WH-1..WH-6, RD-WHEEL-1/3, CLI-1/2, Link 1.0.7, W0 trim. 4/4 green. | Review, then merge. |

Branches pushed without PRs (based on older main; merge main in first):
- Lens `claude/untangle` (0b39213): one PATH lookup (`host::which`, now Windows-aware).
- Shelf `claude/untangle` (6284fe5): docs only. The `Desktop.cpp` split plan (four concerns, one private
  `Native` struct). Do the split: move `Native` to a private header, then split the implementation by concern.

## Per-app status and what's left

- **Link:** 1.0.7 tagged (40ec027; real-fleet tools-hub 42/42, trayhost 27/27, install 16/16 + 8 XFAIL,
  shortcuts 20/20). Earlier red runs were Lens main being red since the 11 Nov Azure DNS outage, so the picker
  used an old `-dev` Lens build. The XFAILs are `LEGACY_PENDING`: remove each app as its 1.0.7 main build turns
  green. Todo: tag 1.0.8, merge #63.
- **Tools:** steps 1–7 done; step 8 at rc.10 (gates green). rc.11 adds crash reports + Link 1.0.7 + the advisory.
- **Box:** 1, 3, 4 done; 2 well along (#37); 6 in progress (#38). Left: memory/perf (5), Round 5 (7), rc + gates.
  Backlog with reasons (D-list): BP-1, BP-5, non-ASCII watermark.
- **Lens:** 1, 3 done (all P0/P1, LN-2..LN-13 except LN-10 and RD-LENS-4, which need the harness); nightlies now
  tagged `vX.Y.Z-nightly.YYYYMMDD.N`; 4 done (one unused dep). Left: 2, 5–8.
- **Shelf:** every spec finding fixed (#12, #13). Left: Link 1.0.8, the Desktop.cpp untangle, 4–8.
  RD-SHELF-3 (Hyprland blur needs a compositor rule Shelf doesn't install) is open.
- **Clipboard:** all P0/P1, CB-5/6/8/9 fixed (#16, #17). Left: Link 1.0.8 (key chips; CB-10 colour emoji is
  already in the kit), `--status` before the engine (CB-5 second half), 2, 4–8. One finding: the relay field
  "looks disabled" is visual and needs a screen check.
- **Find / Look / Wheel:** partner PRs above; then 2, 4–8.
- **Fleet finish (§10):** not started. Last: tick PLAN's owner-requests checklist with evidence links and write the
  final summary at the top of `PROGRESS.md`.

## Step 6 finding that applies to every repo

GitHub's 10 GB per-repo cache cap was full or over in Box, Lens, Clipboard, Tools and Link, so caches evicted each
other and PRs compiled cold. Rule (Link spec §4): caches are saved only on main
(`save-if: ${{ github.ref == 'refs/heads/main' && github.event_name == 'push' }}`), and PRs build one Linux
package. Check each remaining repo (Find, Look, Wheel, Shelf, Tools) the same way: `gh api
repos/qa-p1/<repo>/actions/cache/usage`.

## Owner-only checks (can't be done in the cloud)

- Lens: the first-run install dialog on a fresh profile (LN-1 font fix), X11 Record Window stop (LN-6) and pin
  Live (LN-7).
- Clipboard: the relay field's look (CB-8).
- Shelf: the shortcut-recorder UI test fails locally on the unchanged code under Xvfb; CI passes it.
- Real-desktop install of the 1.0.7 builds, to confirm one launcher per app (PLAN "One launcher per app").

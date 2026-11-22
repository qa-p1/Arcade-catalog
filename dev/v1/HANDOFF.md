# Handoff (2026-11-22, cloud session, after the fix round)

**Everything is on GitHub; no scheduled check-ins are left running.** Box is still parked (owner's call): don't
touch Arcade-box. Next step: plan Box with the owner.

**Update (2026-11-22, later): the plan is agreed: `dev/everywhere/PLAN.md` (Arcade everywhere + Box 1.0.0 + every
leftover below). Box is no longer parked; it is stage 3 of that plan. Owner-only steps: `dev/everywhere/LOCAL-PROMPTS.md`.**

## Where the fleet stands

| App | State |
|---|---|
| Link | **v1.0.15** tagged on 09d52ee ([#81](https://github.com/qa-p1/Arcade-Link/pull/81)): Tesseract download with the user's environment (#79), theme from GTK/GNOME without a portal, e2e per-session `TMPDIR`. |
| Tools | **1.0.2 stable** from rc.2 (e098fc8), Gates 11/11, files byte for byte rc.2's. On Link 1.0.15, `url` 2.5.9. |
| Find | **1.0.1 stable** from rc.2 (961f0ad), Gates 12/12. |
| Lens | **1.0.1 stable** from rc.1 (f59d0d4), Gates 12/12. |
| Shelf | **1.0.1 stable** from rc.1 (28d2033), Gates 13/13. |
| Clipboard, Look, Wheel | 1.0.0 stable, unchanged this round (older Link: they move to 1.0.15 with their next release). |
| Box | Parked by the owner. |

What changed and how it was checked: `REAL-USER-RUN.md` (§Noted in the third pass…, §Fourth pass).

## Open

For the owner (this session can't):
- **Delete 12 old wip branches** (GitHub refused the session, 403). All their work is in main. Each name starts with
  `claude/sharp-cori-29w5eg-`: Link `wip-link-unpacked`; Clipboard `wip-gates`, `wip-step5-security`; Find
  `wip-security`; Lens `wip-security`; Look `wip-restart`, `wip-security`, `wip-security-2`; Shelf `wip-step5`,
  `wip-tier2`; Wheel `wip-step5`, `wip-tier2`.
- **Add a line to the Lens v0.4.1 and v0.4.2 release notes** (they crash on start on Linux):
  > **Update to [Arcade Lens 1.0.0](https://github.com/qa-p1/Arcade-lens/releases/tag/v1.0.0) or later.** On Linux
  > this release can crash on start with a font error (found on 2026-11-21); 1.0.0 fixes it. Arcade Tools offers the
  > update.

For the next release of each app:
- **RUSTSEC-2026-0592:** Clipboard, Look, Box and Link itself still lock `url` 2.5.8, so their next `cargo deny` fails
  until they move to 2.5.9.
- **Clipboard Dependabot:** #28 (setup-java 6.3.0) merged, all 11 checks green including the Android build that uses
  it; #32 closed. #25, #26, #27 (download-artifact 8, upload-artifact 7, checkout 7) are green but change the gates
  and release workflows, so take them with an rc that proves them. #23, #24, #29, #30, #31, #33 fail CI and need work.
- **Unexplained:** Find's main CI once failed "0.4.3 did not load pins/history" (5/5 locally, one re-run passed).
- **Small:** Look's card says "Not running" for a few seconds after login while Look starts.
- Windows and macOS had no real-user run; their gates smoke-test the published installers.

---

# Handoff (2026-11-22, cloud session, end of the real-user run) — superseded, kept for history

**Everything is on GitHub; no scheduled check-ins are left running.** Box is still parked (owner's call): don't
touch Arcade-box (its last state is in the section below).

## Where the fleet stands

| App | State |
|---|---|
| Tools | **1.0.1 stable** from rc.4 (b23b113). Gates 11/11 twice (runs 44965715622 with update-from rc.3, 44965712696 from v0.4.6); AppImage, dmg, setup.exe, SHA256SUMS byte for byte as rc.4; the manifest differs only in `channel`/`tag` and is signed. Docs [#59](https://github.com/qa-p1/Arcade-tools/pull/59). |
| Clipboard | **1.0.0 stable** from rc.3 (13/13 Gates). Docs #36 merged. |
| Find, Lens, Look, Shelf, Wheel | 1.0.0 stable. |
| Link | `v1.0.14` tagged. [#79](https://github.com/qa-p1/Arcade-Link/pull/79) merged on main (5bcc6b8), **not tagged**: the engines download runs with the user's environment (root fix of Tools D37). |
| Box | Parked by the owner. |

## What the real-user run found and fixed (details: `REAL-USER-RUN.md`)

Tools 1.0.1 carries D24–D37. Tonight's additions, each with a test that fails without it:
- D34: programs Tools started inherited its unpacked-copy marker and stayed on their AppImage mounts.
- D35: Update on an app installed from its own download refused ("Choose Let Tools manage it").
- D36: that update's history had no target version; an rc that Tools installed was never offered the next rc.
- D37: Download with Arcade for Tesseract failed on current distributions (curl loaded Tools' libnghttp2).

Verified on the released files in the desktop session: every app updated from an old release to 1.0.0 with its file
equal to the published asset and its data kept; Tools updated itself from inside Tools; Tesseract downloaded and
Lens's warning cleared; after restarts no Arcade AppImage mount is left.

## Open, for the owner

- **Tools 1.0.2:** move to a current Link (Tools pins 1.0.7; then drop Tools' own Tesseract download and the
  `ARCADE_UNPACKED` removal, which Link does). At equal versions, compare the cached executable hash in
  `Manager::record` (a hand-installed rc over a Tools-installed one keeps the old hash and is offered "1.0.1 → 1.0.1";
  owner's rc testing only). The Tesseract dialog mentions Windows on Linux.
- **Decide:** the one-step update of an app installed outside Tools keeps no rollback copy of its 0.x install (Tools
  DECISIONS D36).
- **Link:** tag a release with #79 when convenient (no app needs it before Tools moves).
- Noted, not changed: white tray mark on light panels; no transparency without a compositor; Lens dark vs Tools light
  on openbox; Lens's install dialog is too tall.

---

# Handoff to the local session (2026-11-21, from the cloud session) — superseded, kept for history

Read, in order: `README.md` (owner decisions win), `PLAN.md`, this section, `LOCAL-PROMPT.md` (the prompt to paste),
the newest entries of `PROGRESS.md` (its Status table is old; this section is the current state), `LOCAL.md`, then
each repo's `docs/v1/PROGRESS.md` and `DECISIONS.md`.

**Everything is on GitHub.** Every repo's working tree in the cloud container was clean and pushed when this was
written. No scheduled check-ins are left running.

**Box is out of scope for the local session (owner's call: they have plans for it). Don't touch Arcade-box.** Its
last state, for reference only: `v1.0.0-rc.7` published, Gates failed the upgrade test (0.4.3 needs glibc 2.38, the
job ran on 22.04); a fix sits on branch `claude/sharp-cori-29w5eg-wip-upgrade` (33f133d), not in a PR.

## Where the fleet stands

| App | State |
|---|---|
| Link | `v1.0.14` tagged (a5a3783): Tier 2 package cache, parallel prefetch with mirror fallback, gnome-keyring unlock, 60 s compositor wait. Apps' gates still call `app-gates.yml@v1.0.13`; Tier 2 uses `desktop-tier2.yml@v1.0.14`. |
| Tools | 1.0.0 stable. 1.0.1 open items below. |
| Find, Lens, Look | 1.0.0 stable, docs merged. |
| Shelf | **1.0.0 stable** from rc.4 (Gates 13/13, run 44222853395; Promote 44226166895); every installer and SHA256SUMS byte for byte as rc.4. Docs [#25](https://github.com/qa-p1/Arcade-Shelf/pull/25) merged. Done. |
| Wheel | **1.0.0 stable** from rc.4 (Gates 12/12, run 44226061986; Promote 44228311950); every installer and SHA256SUMS byte for byte as rc.4. Docs [#28](https://github.com/qa-p1/Arcade-wheel/pull/28) merged. Done. |
| Clipboard | **Not released.** `v1.0.0-rc.2` (163f958) published, Gates failed (details below). Latest stable is still 0.3.2. |
| Box | Parked by the owner. Leave it. |

## Clipboard: what's left (the only app still in flight)

History:
- [#22](https://github.com/qa-p1/Arcade-clipboard/pull/22) merged (e5ec844): `gates.yml` (app-gates@v1.0.13,
  previous default v0.3.2), `scripts/verify-upgrade.py` (0.3.2 → 1.0.0 keeps history and keyring; passed locally),
  Tier 2 on Link 1.0.14.
- rc.1 Gates (run 44226756864): CLI-1 to CLI-4 failed, `GLIBC_2.3x not found`: `release.yml` built the Linux
  packages on ubuntu-24.04 while CI and the changelog say 22.04. Fixed in
  [#34](https://github.com/qa-p1/Arcade-clipboard/pull/34) (merged, 163f958).
- rc.2 Release (run 44230687136) green, Linux packages built on ubuntu-22.04.
- **rc.2 Gates (run 44232113005) failed two jobs**; upgrade, Tier 1 and Tier 2 were skipped because they wait on
  the Linux job, so they have never run against a published Clipboard rc:
  1. **Linux conformance, CLI-2 and CLI-4** (CLI-1, CLI-3 and the rest pass now):
     - CLI-2: `--arcade-conformance-unknown-flag` exits **0** with empty stderr. Required: exit 2 and the usage on
       stderr (`--help` exits 0 already). Shelf had the same bug (Shelf #23).
     - CLI-4: `--arcade-manifest` exits **1** with empty stdout and stderr. Required: exit 0 and the manifest JSON
       on stdout. CI's AppImage smoke runs `--arcade-manifest` under `xvfb-run` and passes, so the likely cause is
       that conformance runs it **without a display** and the Flutter side needs one; the launcher
       (`usr/lib/arcade-clipboard/arcade-clipboard-launcher`) should answer `--arcade-manifest`, `--version`,
       `--help` and unknown flags itself, before any GTK/Flutter start. Not confirmed: reproduce first by running
       the extracted rc.2 AppImage with no `DISPLAY`/`WAYLAND_DISPLAY`, and read Link
       `crates/arcade-link-cli/src/conformance.rs` (CLI checks around lines 355-397) for the exact contract.
     - Add a CI step that runs these without a display so CI catches it before an rc.
  2. **Delta gate** (Tools' `tests/releases.rs`, `gate_published_files_delta_signature_and_tampered_chunk`): the
     delta from 0.3.2 fetched 7,908,165 of 15,751,672 bytes (50.2%) and the test asserts the delta fetches **less
     than half** (`total * 2 < new_bytes.len()`, line ~356). The update itself worked (digest matched). This conflicts
     with the owner's decision in Tools #54 (accept whatever Tools' own rule chooses: a delta only when it saves at
     least 20%, otherwise the whole file, always checking digest, tampered chunk and signature). Recommended fix: in
     Tools, make the gate assert Tools' own rule instead of the 50% bound (Tools 1.0.1), then bump the `tools-ref`
     Clipboard's gates use. Record the decision in Tools' `DECISIONS.md`.

Next for Clipboard: fix 1 in Clipboard (PR, every check green, merge commit), fix 2 in Tools (PR; release per Tools'
flow if a new tag is needed), point Clipboard's gates at the fixed Tools, cut rc.3 with "Tag a release" (inputs `tag`,
`sha`), dispatch `gates.yml` on ref `v1.0.0-rc.3` with `previous: v0.3.2`, and only if **every** job is green
(including the first real runs of the upgrade test and both desktop suites) run `promote.yml` with `rc-tag`, verify
byte for byte (method below), then Clipboard docs and the catalog.

Also open in Clipboard: [#35](https://github.com/qa-p1/Arcade-clipboard/pull/35), docs only (the rc.1/rc.2 findings in its
`docs/v1/PROGRESS.md`); merge it when its checks are green. And 11 Dependabot PRs (opened 2026-11-18). Their CI runs crowded the shared runners that night.
Don't merge them during the release; look at them after 1.0.0.

## Other open items

- **Tools 1.0.1:** (a) the delta gate bound above; (b) quit race: `Presence::start` (desktop.rs ~725) runs before the
  presence is stored in state (~741), so an `app.quit` in between exits and leaves a stale endpoint. Link replaces
  stale endpoints, so the impact is low.
- Leftover `-wip-*` branches on several repos (deleting them from the cloud failed with "remote hung up"). They're
  merged or superseded; delete them if you like, except Box's.
- Catalog: this branch (`claude/sharp-cori-29w5eg`) holds the progress/handoff commits and has not been merged to
  main.

## How a release goes (unchanged)

1. Merge to main (apps: merge commit with `expectedHeadSha`; Link: squash) only when every check on the PR head is green.
2. "Tag a release" (`tag.yml`, inputs `tag`, `sha`) → Release publishes a hidden prerelease and runs the full CI
   (Tier 2 included). A gates fix needs a new rc, because Gates runs the `gates.yml` inside the tag.
3. `gates.yml` dispatched on the rc tag ref with `previous`. Every job green; at most one re-run per job, and a flake
   is not a root cause.
4. `promote.yml` with `rc-tag`. Verify: list both releases' assets with their `digest`, download `manifest.json`,
   `arcade-release.json` and `SHA256SUMS.txt` with `gh api -H 'Accept: application/octet-stream'
   repos/qa-p1/<repo>/releases/assets/<id>` (`gh release download` uses GraphQL and fails in the cloud), and confirm
   the binaries and SHA256SUMS are identical, the JSON differs only in channel/tag/notes, and `manifest.json.sig`
   exists. Then repo `docs/v1/PROGRESS.md` and the catalog `PROGRESS.md`.

---

# Older handoff (2026-11-15 ~20:25 UTC) — superseded, kept for history

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

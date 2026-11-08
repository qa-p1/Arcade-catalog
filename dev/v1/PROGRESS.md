# Arcade 1.0.0 progress

Update this after every finished step (see `PLAN.md` §How the work runs). Newest entries go at the top of the log.
Detail lives in each repo's `docs/v1/PROGRESS.md`.

## Status

| # | Repo | Step (1 lock · 2 untangle · 3 fix · 4 dead code · 5 memory/perf · 6 CI · 7 Round 5 · 8 release) | Latest rc | Stable |
|---|---|---|---|---|
| 1 | Link | **v1.0.5 tagged** (601af05, through "Tag a release" after CI, Ecosystem e2e and the desktop harness passed on it): Tier 2 smoke polls `--status` ([PR #52](https://github.com/qa-p1/Arcade-Link/pull/52)), `perf_budget.py` counts wakeups per thread ([PR #53](https://github.com/qa-p1/Arcade-Link/pull/53)) · 1.0.4 (a076adb): desktop app outside the checkout, `perf_budget.py` | — | [v1.0.5](https://github.com/qa-p1/Arcade-Link/tree/v1.0.5) (tag) |
| 2 | Tools | 1–7 done ([PR #23](https://github.com/qa-p1/Arcade-tools/pull/23) merged as 7682ac9, green on every job: Linux, Windows, macOS, Tier 1 Hyprland, Tier 2 sway/KWin/Mutter/X11; on Link 1.0.5; memory bg 12 / closed 12 / open 258 PSS; perf cold 712 ms, show 630 ms, open 8.5 wakeups/s, disk 374 MB; design pass D13) · **8: `v1.0.0-rc.1` tagged**, but its Release failed in `prepare` (Python 3.10 has no `tomllib`; nothing published) → fix in [PR #39](https://github.com/qa-p1/Arcade-tools/pull/39); rc.2's macOS bundle failed (`wc -l` padding; nothing published) → fix with the Gates workflow in [PR #40](https://github.com/qa-p1/Arcade-tools/pull/40) (D14), merged · **[`v1.0.0-rc.3`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.3) published** (Linux bundle needed one re-run: an unexplained 25 s hang on the first window open, open item) · [Gates on rc.3](https://github.com/qa-p1/Arcade-tools/actions/runs/42500704532): every gate passed on the published files (budgets, upgrade from 0.4.6, N-1, Tier 1 + 2, Windows/macOS smoke, delta 14.1 of 94.5 MB) but the run is red on a `tee` path bug in the delta step → fix in [PR #41](https://github.com/qa-p1/Arcade-tools/pull/41) · [`v1.0.0-rc.4`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.4) published; [Gates on rc.4](https://github.com/qa-p1/Arcade-tools/actions/runs/42506931186) passed everything except the rc.3 → rc.4 self-update, which found that Tools could not install any rc (`--channel test` refused by every installer) and retried a failed update every minute (Tools D15) → fix in [PR #42](https://github.com/qa-p1/Arcade-tools/pull/42) · [`v1.0.0-rc.5`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.5) published; [Gates on rc.5](https://github.com/qa-p1/Arcade-tools/actions/runs/42514624358) red only on a race in the tray test (killed the resident before a second launch's unpacked copy handed over) → fix in [PR #43](https://github.com/qa-p1/Arcade-tools/pull/43) · next: rc.6 + Gates with `update-from: v1.0.0-rc.5` · stable blocked by B1 | rc.5 | — |
| 3 | Box | not started | — | — |
| 4 | Clipboard | not started | — | — |
| 5 | Look | not started | — | — |
| 6 | Find | not started | — | — |
| 7 | Lens | not started | — | — |
| 8 | Shelf | not started | — | — |
| 9 | Wheel | not started | — | — |
| 10 | Fleet finish | not started | — | — |

## Open blockers

- **B1 — `ARCADE_UPDATE_SIGNING_KEY` cannot be set from the cloud session.** `gh` has no valid token
  (`GH_TOKEN` rejected) and the session's GitHub tools cannot write Actions secrets. No keypair was generated (the
  private key may live nowhere but the secret). Owner action: run `arcade-link keygen --secret-to-gh` (see Link
  `docs/SIGNING.md` once merged) on a machine with `gh` logged in, then commit the printed public key to Tools.
  Until then every `promote.yml` fails by design, so **no stable promotion of Tools or any app is possible**; all
  other work continues. Link's `v1.0.0` is a tag with no signed manifest and is not blocked.
- **B2 — `qa-p1/Arcade-template` cannot be created** (the session may not create repositories). The template is
  kept and tested in Link `template/` (Link `docs/v1/DECISIONS.md` D2). Owner action: create the repo from it and
  mark it as a template.

## Log

- 2026-11-08 (session 2) — Tools rc.5 published from f903b6e (PR #42). Its Gates run failed only in the tray
  step's Link-off section: a race in the test, which killed the resident while a second launch's unpacked copy
  (U1) was still handing over, so that copy became the instance. Reproduced locally on the published rc.5
  AppImage (2 of 6 runs), fixed in PR #43 (0 of 10). rc.5's run stays red, so rc.6 carries the fix and the
  rc.5 → rc.6 self-update gate.
- 2026-11-08 (session 2) — Tools rc.4 published. Gates on it, with `update-from: v1.0.0-rc.3`, passed every gate
  but the self-update, which found two real bugs (reproduced locally on the published files): Tools asked installers
  for `--channel test`, which they all refuse, so no rc could be installed; and a failed self-update was retried
  every minute. The delta worked (79 KB of 94 MB). Fixed with regression tests in PR #42 (Tools D15).
- 2026-11-08 (session 2) — **Gates on Tools rc.3**, its first run: every gate passed on the published files; the
  run is red only because the delta step wrote its log into a `target/` that a fresh checkout lacks (the test had
  passed). rc.3 is not promotable; the fix is PR #41, leading to rc.4 and the rc.3 → rc.4 self-update gate.
- 2026-11-08 (session 2) — **Tools `v1.0.0-rc.3` published** (hidden prerelease, test channel) from f246c5b after PR #40
  passed every check. The Linux bundle's first attempt timed out opening the window right after a background start;
  it passed elsewhere every time and on one re-run, so the cause is still open and the next failure will show the
  hung launch's output and processes. Gates on rc.3 started.
- 2026-11-08 (session 2) — Tools rc.2's Release failed in the macOS bundle job after its smoke passed: the staging
  step compared macOS's space-padded `wc -l` as a string. Nothing published. PR #40 fixes it and adds `gates.yml`
  (Tools D14), which runs every exit gate against a published rc's files, including Tools' delta, signature and
  tampered-chunk checks on the published AppImages (0.4.6 → 1.0.0 fetched 15.3 of 92.7 MB) and an rc → rc
  self-update through GitHub. Writing it found that a login start counted as use, so Tools never auto-updated
  itself at the first check (fixed, with a test).
- 2026-11-08 (session 2) — Tools rc.1's Release failed in its first job (`check-versions.py` needs Python 3.11+, the
  job used ubuntu-22.04's 3.10); nothing was published. Release builds from the tag's workflow, so the fix
  (Tools PR #39) leads to rc.2; the rc.1 tag stays.
- 2026-11-08 (session 2) — **Tools step 8 started**: PR #23 merged (7682ac9) after every job passed at f3a609f
  (version 1.0.0); `v1.0.0-rc.1` tagged through "Tag a release", which started "Release" on the test channel.
- 2026-11-08 (session 2) — **Link v1.0.5 tagged** on 601af05 after CI, e2e and the harness passed on it: the Tier 2
  smoke polls `--status` (PR #52; Qt CI's broken-toolchain cleanup now on every OS), and `perf_budget.py` counts
  wakeups per thread (PR #53): its first Tools run read open-window wakeups as -2.3/s, which passes any budget; the
  real figure is about 11/s (budget 20). Tools moved to 1.0.5 (af2b20b) with D12 corrected.
- 2026-11-08 (session 2) — Tools **design pass** (D13, 10e29ae): a check in `scripts/check` holds the UI to the kit
  (colours, type, tokens, spacing scale, "Couldn't …" wording); 6 off-scale gaps and 8 messages fixed, and the
  error state now says what failed. Tier 2 sway smoke failed once on a fixed 8 s sleep (Tier 1 Hyprland and the other
  Tier 2 desktops green): Link PR #52 polls `--status` instead, for 1.0.5.
- 2026-11-08 (session 2) — **Link v1.0.4 tagged** (tag on a076adb, the merge of PR #51, after CI, Ecosystem e2e
  and the desktop harness passed on it). Tools moved to it (37ba008) with the performance-budget step in CI (D12).
- 2026-11-08 (session 2) — **Tools gates prepared** on PR #23 (e2b0104, 8dffc89): N-1 runs the tray test's peer
  checks with the mock peer on the v0.4.4 and v0.4.15 Link CLIs the published apps use (Tools D11; passes locally);
  `scripts/verify-upgrade.py` installs the published 0.4.6, runs it on a user's data, installs the new AppImage over
  it and checks everything is kept (passes locally from the verified 0.4.6 file; runs on the rc at step 8); the delta
  test now covers a tampered chunk (rejected, intact file installed) and a tampered file (never installed). Guide
  screenshots are generated and Features covers channels, signing and deltas. CI is still red only from GitHub's
  release-download 504s (NSIS, linuxdeploy, appimagetool, Nix): bundling now retries twice.
- 2026-11-08 (session 2) — **Link v1.0.3 tagged** at 4cf9eff after CI, Ecosystem e2e and the harness passed on that
  commit: page-out now covers the heap and every private mapping (Tools' closed PSS 36 → 12), and `budgets.json` sets
  Tools' window-open cap to 281 PSS from CI measurements (Tools D10). Tools moved to it (6e4ac67). Tools' Tier 1 test
  failed on its own harness use (a layer surface has no `at`/`size`); fixed, and found that the desktop workflows put
  the app inside the caller's checkout, where it counts as a dev build: fixed in Link PR #51 for the next tag.
- 2026-11-08 (session 2) — **Link v1.0.2 tagged** at 3e4aa6c ("Tag a release", after CI, Ecosystem e2e and the
  desktop harness passed on that commit). Tools moved to it (Cargo, lockfile, workflows, design kit, vendored
  trimmer; the local focus-ring override removed).

- 2026-11-08 (session 2) — Tools memory measured on the packaged AppImage against Link's new trim: background
  40 → 15–18 PSS (budget 30 met), after close 71 → 28–45 (30 met with swap, as on CI runners), window open
  350 → 261–334 (225 not reachable without a UX trade: WebKitWebProcess keeps ~123 MB of in-use malloc for
  llvmpipe compositing; Tools D10, `LOCAL.md` §4). CI's Linux package check then found that uninstall left
  `arcade.tools.lock`, `icon-theme.cache` and `mimeinfo.cache` in a fresh HOME; fixed in Link (PR #47) with
  tests that failed first, plus a flaky `ETXTBSY` runtime test.

- 2026-11-08 — Link v1.0.1 tagged through its workflow after the desktop harness passed on main. Tools moved to it:
  T3 is a normal test; `cargo deny` clean (zip 9); notices generated (`scripts/notices.py`) and shown in About;
  SECURITY.md, Keep a Changelog, Dependabot; all repository conformance rules pass. PR #23's red macOS/Windows/Linux
  checks were a Linux-only test built everywhere and a package smoke that predated U1's relaunch; both fixed.
- 2026-11-08 — Tools (PR #23): VENDORED moved to Link v1.0.0 (CI was red on it); the release-gate Test channel
  override was never wired and a stored Test channel would have trusted unsigned rc manifests (fixed, D5); dead code
  removed (an unused second backup implementation, ~1,300 lines); the memory items applied (D7); releases now rc →
  promote and nightlies through Link's reusable workflows (D8). Link 1.0.1 opened (PR #45), including fixes to
  `tools/fleet/fleet_budget.py` (it could never have started its D-Bus session, and would have read U1 apps as 0 MB).

- 2026-11-07 — **Link v1.0.0 tagged** at `d60772c` through "Tag a release", after every gate passed on that commit:
  CI (3 OSes), Ecosystem e2e, release-flow e2e (draft rc → promote → signature → byte-identical), Desktop harness
  (Tier 1 Hyprland incl. C0 reproduced on released Clipboard 0.3.2; Tier 2 sway/KWin/Mutter/X11) and Contract on
  the same code. Template `Cargo.lock` committed against the tag. Owner-only steps are in `LOCAL.md`.
- 2026-11-07 — Tools: spec and audit in `docs/v1`; behaviour lock (known bugs as `should_panic`/XFAIL, D3; TL-11's
  "120 s total timeout" disproved by test, resume is the real gap); `manager.rs` split by area (D4); fixes listed in
  the table, each with a regression test that failed first. T3 (legacy folders) fixed in Link for 1.0.1.

- 2026-11-07 — Link: release primitives, protocol/peer check, shared runtime, QML dialog fix, ARCADE_APP.md and
  conformance checker, reusable release workflows and the Hyprland harness are on Link PR #32. Conformance baseline
  of the 8 released apps: `AUDIT/conformance-baseline.md`. Detail: Link `docs/v1/PROGRESS.md`.
- 2026-11-07 — Session 1 started. `setup-env.sh` run. Link step 0 done: brief copied to Link `docs/v1/`
  (branch `claude/tender-feynman-3vt7dg`). Blockers B1, B2 recorded.

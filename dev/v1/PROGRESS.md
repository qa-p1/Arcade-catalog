# Arcade 1.0.0 progress

Update this after every finished step (see `PLAN.md` §How the work runs). Newest entries go at the top of the log.
Detail lives in each repo's `docs/v1/PROGRESS.md`.

## Status

| # | Repo | Step (1 lock · 2 untangle · 3 fix · 4 dead code · 5 memory/perf · 6 CI · 7 Round 5 · 8 release) | Latest rc | Stable |
|---|---|---|---|---|
| 1 | Link | **v1.0.4 tagged** (a076adb, through "Tag a release" after CI, Ecosystem e2e and the desktop harness passed on main; [PR #51](https://github.com/qa-p1/Arcade-Link/pull/51)): desktop workflows run the app outside the checkout, `perf_budget.py`, template PNG icon | — | [v1.0.4](https://github.com/qa-p1/Arcade-Link/tree/v1.0.4) (tag) |
| 2 | Tools | 1–6 done · 7 Round 5 in progress ([PR #23](https://github.com/qa-p1/Arcade-tools/pull/23)): on Link 1.0.4 (37ba008); memory: background 12.6 and closed 12.4 PSS vs 30 (met), window open 263–268 PSS within the 281 cap set from CI (D10, owner option in `LOCAL.md` §4); Tier 2 desktop green on sway, KWin, Mutter and X11; Tier 1 Hyprland test fixed (layer geometry, install outside the checkout) · N-1, upgrade and tampered-chunk checks added · perf budgets in CI (D12) · design pass done (D13: `verify-design.py` in CI, 4 states × 2 themes captured; 10e29ae) · next: Tier 2 sway smoke race → Link 1.0.5 ([PR #52](https://github.com/qa-p1/Arcade-Link/pull/52)), CI green, then 8 rc | — | — |
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

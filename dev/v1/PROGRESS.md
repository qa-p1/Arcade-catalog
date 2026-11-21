# Arcade 1.0.0 progress

Update this after every finished step (see `PLAN.md` §How the work runs). Newest entries go at the top of the log.
Detail lives in each repo's `docs/v1/PROGRESS.md`.

## Status

**Current state (2026-11-15 ~20:25 UTC) is in `HANDOFF.md`; the rows below predate it.**

| # | Repo | Step (1 lock · 2 untangle · 3 fix · 4 dead code · 5 memory/perf · 6 CI · 7 Round 5 · 8 release) | Latest rc | Stable |
|---|---|---|---|---|
| 1 | Link | **v1.0.9 tagged** (65cb57e, after CI, Desktop harness and real-fleet e2e passed) · **[#70](https://github.com/qa-p1/Arcade-Link/pull/70) squash-merged (68b4967) and [#71](https://github.com/qa-p1/Arcade-Link/pull/71) release 1.0.10 squash-merged (2748ebf)**: tag v1.0.10 after CI, Desktop harness and real-fleet e2e pass on it · older: [#70](https://github.com/qa-p1/Arcade-Link/pull/70) open: `qt/arcade_unpacked.h` (C twin of `relaunch_unpacked` for Shelf, Wheel, Clipboard; 14-case `tst_Unpacked`), uninstall removes the app's own unpacked copies (Rust and Qt) · **[#68](https://github.com/qa-p1/Arcade-Link/pull/68) squash-merged 2026-11-15 (65cb57e): release 1.0.9** (app-gates.yml, `tools/gates/n1_app.py`, Dart kit app marks, LEGACY_PENDING empty, harness starts real AppImages with `ARCADE_UNPACKED=1`; [#67](https://github.com/qa-p1/Arcade-Link/pull/67) merged as 1073e2b) · v1.0.9: tag after CI, Desktop harness and the dispatched real-fleet e2e pass on 65cb57e · older: **v1.0.8 tagged** (34f8030, 2026-11-15, through "Tag a release" after CI, Desktop harness and the dispatched real-fleet e2e all passed on it; [#66](https://github.com/qa-p1/Arcade-Link/pull/66) squash-merged): compact key chips, eliding HintBar, caches saved only on main, `windows-installer` (Inno) in the reusable publish/nightly/promote, real-fleet login-item checks fixed · #63 merged (f867e7f, caches saved only on main) · **1.0.8 bump in [PR #64](https://github.com/qa-p1/Arcade-Link/pull/64)**: tag after CI, harness and real-fleet e2e pass on its merge (079f954 itself is still 1.0.7 in Cargo.toml, so it could not be tagged) · older: **v1.0.6 tagged** (cd380d6, tag a1c60d9, through "Tag a release" after CI, Ecosystem e2e and the desktop harness passed on it): `runtime::cap_malloc_arenas`, lazy crash folder, portal stand-in serves the host registry, reports `trigger_description` and registers bound shortcuts with Hyprland (`gshortcuts`), seatd race and Nix download fixes ([PR #54](https://github.com/qa-p1/Arcade-Link/pull/54), [#55](https://github.com/qa-p1/Arcade-Link/pull/55), [#56](https://github.com/qa-p1/Arcade-Link/pull/56)) · 1.0.5 (601af05, through "Tag a release" after CI, Ecosystem e2e and the desktop harness passed on it): Tier 2 smoke polls `--status` ([PR #52](https://github.com/qa-p1/Arcade-Link/pull/52)), `perf_budget.py` counts wakeups per thread ([PR #53](https://github.com/qa-p1/Arcade-Link/pull/53)) · 1.0.4 (a076adb): desktop app outside the checkout, `perf_budget.py` | **v1.0.10 tagged** (2748ebf) · **[#72](https://github.com/qa-p1/Arcade-Link/pull/72) squash-merged (f685140): 1.0.11**, `ARCADE_UNPACKED` names the copy's folder so an inherited marker (Restart successor, app started from a copy) no longer keeps a process on its FUSE mount; `is_unpacked_copy()` / `arcade_is_unpacked_copy()` · [#73](https://github.com/qa-p1/Arcade-Link/pull/73) open: `app-publish.yml` publishes files under names GitHub keeps (Box rc.1 found it), part of 1.0.11; tag v1.0.11 after CI, harness and real-fleet e2e on its merge · — | [v1.0.9](https://github.com/qa-p1/Arcade-Link/tree/v1.0.9) (tag) |
| 2 | Tools | [#50](https://github.com/qa-p1/Arcade-tools/pull/50) merged 2026-11-15 (fdbbc3e): the delta gate runs for any app (`ARCADE_TOOLS_GATE_APP`), for the apps' gates · **8 done: [1.0.0 stable](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0)** promoted from `v1.0.0-rc.11` (f4b86bd) on 2026-11-15 by [Promote](https://github.com/qa-p1/Arcade-tools/actions/runs/43659111568): AppImage, dmg, setup.exe and SHA256SUMS byte-identical to rc.11 (same SHA-256 digests); `manifest.json` signed, verified against the built-in key `RWSUOvlVbQYN…` (trusted comment `app=arcade.tools version=1.0.0 tag=v1.0.0 channel=stable`). Gates: [11/11](https://github.com/qa-p1/Arcade-tools/actions/runs/43604006265) (update from rc.10) and the one-launcher gate in Link's [real fleet](https://github.com/qa-p1/Arcade-Link/actions/runs/43617572879) (`arcade_tools_update_retires_old_desktop_ids` on f4b86bd: 4 old entries retired, one launcher, one login item) · earlier: 1–7 done ([PR #23](https://github.com/qa-p1/Arcade-tools/pull/23) merged as 7682ac9, green on every job: Linux, Windows, macOS, Tier 1 Hyprland, Tier 2 sway/KWin/Mutter/X11; on Link 1.0.5; memory bg 12 / closed 12 / open 258 PSS; perf cold 712 ms, show 630 ms, open 8.5 wakeups/s, disk 374 MB; design pass D13) · **8: `v1.0.0-rc.1` tagged**, but its Release failed in `prepare` (Python 3.10 has no `tomllib`; nothing published) → fix in [PR #39](https://github.com/qa-p1/Arcade-tools/pull/39); rc.2's macOS bundle failed (`wc -l` padding; nothing published) → fix with the Gates workflow in [PR #40](https://github.com/qa-p1/Arcade-tools/pull/40) (D14), merged · **[`v1.0.0-rc.3`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.3) published** (Linux bundle needed one re-run: an unexplained 25 s hang on the first window open, open item) · [Gates on rc.3](https://github.com/qa-p1/Arcade-tools/actions/runs/42500704532): every gate passed on the published files (budgets, upgrade from 0.4.6, N-1, Tier 1 + 2, Windows/macOS smoke, delta 14.1 of 94.5 MB) but the run is red on a `tee` path bug in the delta step → fix in [PR #41](https://github.com/qa-p1/Arcade-tools/pull/41) · [`v1.0.0-rc.4`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.4) published; [Gates on rc.4](https://github.com/qa-p1/Arcade-tools/actions/runs/42506931186) passed everything except the rc.3 → rc.4 self-update, which found that Tools could not install any rc (`--channel test` refused by every installer) and retried a failed update every minute (Tools D15) → fix in [PR #42](https://github.com/qa-p1/Arcade-tools/pull/42) · [`v1.0.0-rc.5`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.5) published; [Gates on rc.5](https://github.com/qa-p1/Arcade-tools/actions/runs/42514624358) red only on a race in the tray test (killed the resident before a second launch's unpacked copy handed over) → fix in [PR #43](https://github.com/qa-p1/Arcade-tools/pull/43), merged (d7ad568) · [`v1.0.0-rc.6`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.6) published (Release green first time); [Gates on rc.6](https://github.com/qa-p1/Arcade-tools/actions/runs/42520824716): tray fixed, all else passed except the self-update (a self-installed Tools has no package hash, so an rc never sees the next rc of the same version; Tools D16) and a one-off open-window memory reading (301 vs 281 PSS; 34 other runs 256–262; open item) → fix in [PR #44](https://github.com/qa-p1/Arcade-tools/pull/44), merged · [`v1.0.0-rc.7`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.7) published; [Gates on rc.7](https://github.com/qa-p1/Arcade-tools/actions/runs/42526166767) (no `update-from`: rc.6 lacks D16) **all green** (open PSS 255.8, cold 350 ms, show 331 ms, disk 371.5 MB); no re-offer of itself checked on the published file · [PR #45](https://github.com/qa-p1/Arcade-tools/pull/45) merged; `v1.0.0-rc.8` tagged but its [Release](https://github.com/qa-p1/Arcade-tools/actions/runs/42528082923) failed (nothing published): `--quit` right after `--restart` missed Link's 150 ms hello while Tools was starting, a real CLI bug (Tools D17), fixed in [PR #46](https://github.com/qa-p1/Arcade-tools/pull/46) (its CI also found a tray-test false alarm on the same 150 ms probe, fixed there) · [`v1.0.0-rc.9`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.9) published (b6ac23f) · [Gates on rc.9](https://github.com/qa-p1/Arcade-tools/actions/runs/42535663129): **every gate passed incl. the self-update** (rc.7 → rc.9, delta 8.5 of 94.5 MB) **except open-window memory** (297.5 vs cap 281; 2 of 5 Gates runs high, all else 256–262); not re-run to green (Tools D18); the [memory probe](https://github.com/qa-p1/Arcade-tools/actions/runs/42536860332) found it: glibc thread arenas in WebKit, created or not by timing (default 3 of 8 runners at 298–308, `MALLOC_ARENA_MAX=2` 8 of 8 at 252–254); Tools now caps arenas at two (D18, [PR #47](https://github.com/qa-p1/Arcade-tools/pull/47) merged as 873eab1; its CI 253.3) · **[`v1.0.0-rc.10`](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0-rc.10): [Gates](https://github.com/qa-p1/Arcade-tools/actions/runs/42544104046) all green on the published files (11/11)**: self-update rc.9 → rc.10 with a delta (8.9 of 94.5 MB), upgrade from 0.4.6, N-1, Tier 1 + 2, 3-OS smoke, delta/signature/tamper, budgets (open PSS 252.0, cold 388 ms, show 342 ms, disk 371.5 MB) · **not done: rc.10 lacks the crash reports TOOLS.md §Crash reports requires** (Tools writes none for itself and has no "<App> crashed" view with Copy report / Open GitHub issue; found 2026-11-09 while moving Box onto Link's runtime) → crash reports in Tools, then rc.11 and its gates; promotion also needs B1 | rc.11 | **[1.0.0](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0)** |
| 3 | Box | **[#44](https://github.com/qa-p1/Arcade-box/pull/44) merged (30b9267) and [#45](https://github.com/qa-p1/Arcade-box/pull/45) release 1.0.0 merged (bed8a19)** · **8: `v1.0.0-rc.1` tagged on bed8a19**, Release running; then Gates on the published rc, Promote · earlier: [#44](https://github.com/qa-p1/Arcade-box/pull/44) open (step 7 part 2): `gates.yml` on Link `app-gates.yml@v1.0.9` (D20) with `scripts/verify-upgrade.py` (published 0.4.3 with a user's data → candidate, by hand; passed locally against the real 0.4.3), accessibility pass (D21: axe-core WCAG 2.1 A/AA, focus, reduced motion in `scripts/check`; 34 findings on main fixed), SECURITY.md downloader rows, README screenshots retaken (`npm run screenshots`) · next: merge, 1.0.0 bump, rc.1, Gates · **[#43](https://github.com/qa-p1/Arcade-box/pull/43) merged 2026-11-15 (f9d21f5), step 7 part 1:** Link 1.0.8 (D16), unused release script removed (D17), Keep a Changelog (D18), **BR-17** (shortcut without the portal Registry) and **BR-18** (strict CSP for the Island and dashboard, tested under the layout and key tests) fixed with tests that fail first, pinned-image Copy fixed (its CSP blocked it), notices and licence inventory on 1.0.8 · Round 5 done in #43: schema versions and downgrade safety (clipboard history, Link peers, installed plugins; v0.4.3 fixture), notices and licence in About and the bundle, uninstall removes Box's unpacked copies (checked by the AppImage inventory) · Round 5 left: N-1, downloader rows in SECURITY.md, a11y, README screenshots; then gates.yml on Link `app-gates.yml@v1.0.9` and step 8 · **[#40](https://github.com/qa-p1/Arcade-box/pull/40) merged 2026-11-15 (c64b521): memory U1/W0/W1/W3b/OPEN1/BX1 (step 5, D14) and rc-only release machinery (step 6, D15)** · **#36 (Link 1.0.7) and #38 (CI, D13) merged 2026-11-14; #37 (untangle) re-merged with main for CI** · 0 brief done · **1 behaviour lock** in [PR #19](https://github.com/qa-p1/Arcade-box/pull/19) (Island keys BR-0/5/6/11/12, core BR-4/B-7/B-8/B-9/B-10/B-25/U-1/BR-7/BR-15/BR-16, CLI-2, BR-8, Tier 1 Hyprland BR-0/1/2 as known bugs; merged as b958041) · app standard [PR #20](https://github.com/qa-p1/Arcade-box/pull/20) merged (effb510) | **rc.1 published, [Gates](https://github.com/qa-p1/Arcade-box/actions/runs/43726431384) red at "Published files"**: GitHub stored `Arcade Box_…` as `Arcade.Box_…` while SHA256SUMS/manifest name the original (lost rename when moving to Link's app-publish) → Link [#73](https://github.com/qa-p1/Arcade-Link/pull/73); rc.2 on Link 1.0.11 (also moves Box's crate from 1.0.8) · — | — |
| 4 | Clipboard | **[#21](https://github.com/qa-p1/Arcade-clipboard/pull/21) merged: step 4 (D7)** · step 5 (U1 in the Rust launcher, W0/CB1a trim in the runner, CB2, image cache cap) in progress on Link 1.0.10 · earlier: [#21](https://github.com/qa-p1/Arcade-clipboard/pull/21) open: step 4 dead code (D7) · U1 waits for Link [#70](https://github.com/qa-p1/Arcade-Link/pull/70) (C twin) · **[#20](https://github.com/qa-p1/Arcade-clipboard/pull/20) merged 2026-11-15 (00b3d9b): step 2 untangle (D3–D6)** · **[#19](https://github.com/qa-p1/Arcade-clipboard/pull/19) merged 2026-11-15 (63f9adb): Link 1.0.8, rc-only releases (step 6), CB-5, D1-D2** · 2 untangle on [#20](https://github.com/qa-p1/Arcade-clipboard/pull/20): core split by concern (D3), Hyprland library (D4), Wayland clipboard library (D5), clip building as a function with tests (D6) · 3 fix done · next: rest of step 2, 4, 5, 7, 8 | step 5 done locally (`local/clipboard-step5`: U1, W0/CB1a, CB2, CB4, packaged U1 check), push on Link 1.0.11 · Round 5 security/notices pass running · — | — |
| 5 | Look | [#24](https://github.com/qa-p1/Arcade-look/pull/24) open: step 7 gates (D13), `gates.yml` and `scripts/verify-upgrade.py` (Look had no upgrade test; 0.4.1 → 0.4.3 passed locally on the published AppImages) · **[#22](https://github.com/qa-p1/Arcade-look/pull/22) merged: step 4 (D11)** · **[#23](https://github.com/qa-p1/Arcade-look/pull/23) merged (40231bb)**: step 5 (D12: U1, W0, W1, W3b, OPEN1 with `libarcade-trim.so`); first CI run red on the packaged check reading the resident's exec-time environ, fixed to check WebKit's helpers (adc3dfd) · earlier: [#22](https://github.com/qa-p1/Arcade-look/pull/22) open: step 4 dead code (D11) · step 5 (U1, W0, W1, W3b, OPEN1) in progress · **[#21](https://github.com/qa-p1/Arcade-look/pull/21) merged 2026-11-15 (0b3a1e1): rc-only releases (step 6), `--remove-data` fix, one identity module (step 2)** · next: rest of step 2, 4, 5, 7, 8 | **[#24](https://github.com/qa-p1/Arcade-look/pull/24) merged (a1d867a): gates (D13)** · Round 5 security/notices pass running (SECURITY.md, deny.toml, THIRD_PARTY_NOTICES generator) · next: `is_unpacked_copy()` on Link 1.0.11, rc.1 · **8 done: rc.3 → [1.0.0](https://github.com/qa-p1/Arcade-look/releases/tag/v1.0.0) (2026-11-17)** · rc.3 | **[1.0.0](https://github.com/qa-p1/Arcade-look/releases/tag/v1.0.0)** |
| 6 | Find | [#22](https://github.com/qa-p1/Arcade-Find/pull/22) open: step 7 gates (D17), `gates.yml`, upgrade from 0.4.3 and 0.5.4 (both passed locally on the published AppImages), Tier 1 `find_desktop.py` in CI for the first time · **[#21](https://github.com/qa-p1/Arcade-Find/pull/21) merged (642921b): step 5 U1 (D16)** · next: 7, 8 · earlier: [#21](https://github.com/qa-p1/Arcade-Find/pull/21) open: step 5 U1 (D16; W0 and FD1 were already in) · **[#20](https://github.com/qa-p1/Arcade-Find/pull/20) merged 2026-11-15 (7995744): step 4 dead code (D15)** · **[#19](https://github.com/qa-p1/Arcade-Find/pull/19) merged 2026-11-15 (eabe53d): rc-only releases (step 6), caches on main only, untangle (step 2)** · 1 lock and 3 fix done · next: 5, 7, 8 | **[#22](https://github.com/qa-p1/Arcade-Find/pull/22) merged (08a90ca): gates, Round 5, Link 1.0.13, 1.0.0 (D17–D19)** · **8 done: rc.1 → [1.0.0](https://github.com/qa-p1/Arcade-Find/releases/tag/v1.0.0) (2026-11-17)** · rc.1 | **[1.0.0](https://github.com/qa-p1/Arcade-Find/releases/tag/v1.0.0)** |
| 7 | Lens | [#23](https://github.com/qa-p1/Arcade-lens/pull/23) open: step 7 gates (D9), `gates.yml` and `scripts/verify-upgrade.py` (Lens had no upgrade test; 0.4.1 → 0.4.2 passed locally on the published AppImages) · **[#22](https://github.com/qa-p1/Arcade-lens/pull/22) merged (541a35f): step 5 W0 + U1 (D8)** · next: 7, 8 · earlier: [#22](https://github.com/qa-p1/Arcade-lens/pull/22) open: step 5 W0 + U1 (D8) · **[#21](https://github.com/qa-p1/Arcade-lens/pull/21) merged 2026-11-15 (b6e09c5): step 4 dead code (D7)**; first push broke the macOS/Windows build (`Rect::is_empty` and an import only they use), fixed in cc4be6a and checked with clippy for `x86_64-pc-windows-gnu` · **[#20](https://github.com/qa-p1/Arcade-lens/pull/20) merged 2026-11-15 (86bbedd): rc-only releases (step 6), one PATH lookup (step 2)** · open: LN-10, RD-LENS-4 (need the harness) · next: 5, 7, 8 | **[#23](https://github.com/qa-p1/Arcade-lens/pull/23) merged (24cf776): gates (D9)** · **[#37](https://github.com/qa-p1/Arcade-lens/pull/37) merged (3dad560): CLI-2** · **8 done: rc.4 → [1.0.0](https://github.com/qa-p1/Arcade-lens/releases/tag/v1.0.0) (2026-11-17)** · rc.4 | **[1.0.0](https://github.com/qa-p1/Arcade-lens/releases/tag/v1.0.0)** |
| 8 | Shelf | step 5 (Link 1.0.10, U1, W0, SH1) in progress · **[#15](https://github.com/qa-p1/Arcade-Shelf/pull/15) merged 2026-11-15:** `Store::add` split (step 2, D4) and step 4 dead code (D5), 17/17 ctest · **[#14](https://github.com/qa-p1/Arcade-Shelf/pull/14) merged 2026-11-15 (b9b9459): Link 1.0.8 (D3), rc-only releases (step 6), `Desktop.cpp` split by concern (step 2)** · 3 fix done · next: 5, 7, 8 | — | — |
| 9 | Wheel | step 5 (Link 1.0.10, U1; W0 already in) in progress · **[#21](https://github.com/qa-p1/Arcade-wheel/pull/21) merged 2026-11-15 (1834b38)** · **[#23](https://github.com/qa-p1/Arcade-wheel/pull/23) merged 2026-11-15 (3b16a05): step 4 dead code; the first push missed the macOS initializer of the removed `launchTarget` (DMG builds failed), fixed in 9f9f894** · next: 5, 7, 8 | — | — |
| 10 | Fleet finish | not started | — | — |

## Open blockers

None. B1 and B2 were done from the owner's PC on 2026-11-11:
- **B1 done:** `ARCADE_UPDATE_SIGNING_KEY` is set on all 8 app repos (Tools, Box, Clipboard, Look, Find, Lens, Shelf,
  Wheel) by `arcade-link keygen --secret-to-gh`; the private key exists nowhere else. Public key (key id
  `960D066D55F93A94`) `RWSUOvlVbQYNllRw2PgYmp2vg3GsQv3DJy868cCpzxQMnSL1ygcN/EXt` is committed to Tools
  `resources/update-keys.pub` (Tools 6bfba35 on PR #49). Stable promotion is unblocked once a Tools build with
  this key is released. Secrets can't be read back, so a new app repo can't get this key copied: give it a
  key through a rotation (Link `docs/SIGNING.md` §Rotation) covering every app repo.
- **B2 done:** [qa-p1/Arcade-template](https://github.com/qa-p1/Arcade-template) is created from Link `template/`
  (origin/main) and marked as a GitHub template. Link `template/` stays the tested source; resync the repo when it
  changes.

## Log

- 2026-11-21 (cloud session, end) — **Handoff to the local session** (`HANDOFF.md` top section, `LOCAL-PROMPT.md`).
  Box is left out of the local session (owner's call). Clipboard is the only app still in flight.
- 2026-11-21 (cloud session) — **Clipboard 1.0.0 stable; real-user run; Tools 1.0.1 in flight.** Box left out.
  - **Clipboard:** rc.3 (#35: CLI-2/CLI-4 answered by the launcher) passed all 13 Gates jobs, including the upgrade
    from 0.3.2 with history and keyring and both desktop suites; promoted; files byte for byte rc.3's; docs #36.
  - **Tools 1.0.1:** #55 (the owner's bug: a self-installed Tools never offered its own update; the delta gate
    follows Tools' rule; quit during start-up) merged; rc.1 published and superseded by #56, the real-user run's
    fixes (D27–D33). Next: #56 green → merge → rc.2 → Gates (update-from rc.1) → Promote.
  - **Real-user run on Linux:** see `dev/v1/REAL-USER-RUN.md`.
- 2026-11-18 (cloud session, night) — **Shelf and Wheel 1.0.0 stable; Clipboard rc.2 failed Gates; Link 1.0.14.**
  - **Shelf [1.0.0](https://github.com/qa-p1/Arcade-Shelf/releases/tag/v1.0.0)** promoted from `v1.0.0-rc.4`
    (e8b4a26, Link 1.0.13) after [Gates](https://github.com/qa-p1/Arcade-Shelf/actions/runs/44222853395) 13/13, the
    upgrade from 0.4.0 and both desktop suites included; AppImage, dmg, setup.exe and SHA256SUMS byte for byte as rc.4,
    metadata differs only in channel, tag and notes link. Earlier rcs: rc.1 gates runner missing `libEGL.so.1`
    ([#22](https://github.com/qa-p1/Arcade-Shelf/pull/22)), rc.2 an unknown option exited 1, not 2
    ([#23](https://github.com/qa-p1/Arcade-Shelf/pull/23)), rc.3 the upgrade job lacked libOpenGL and Tier 2 timed out
    on a slow mirror ([#24](https://github.com/qa-p1/Arcade-Shelf/pull/24)). Docs
    [#25](https://github.com/qa-p1/Arcade-Shelf/pull/25) merged.
  - **Wheel [1.0.0](https://github.com/qa-p1/Arcade-wheel/releases/tag/v1.0.0)** promoted from `v1.0.0-rc.4`
    (5481c63, Link 1.0.13) after [Gates](https://github.com/qa-p1/Arcade-wheel/actions/runs/44226061986) 12/12;
    AppImage, both dmgs, setup.exe, zip and SHA256SUMS byte for byte as rc.4. Earlier rcs: rc.1 gates runner missing
    `libEGL.so.1` ([#25](https://github.com/qa-p1/Arcade-wheel/pull/25)), rc.2 Release failed on a tray test that
    assumed Tools answers within the 300 ms cap ([#26](https://github.com/qa-p1/Arcade-wheel/pull/26)), rc.3 Release
    Tier 2 timed out on a slow mirror ([#27](https://github.com/qa-p1/Arcade-wheel/pull/27)). Docs in
    [#28](https://github.com/qa-p1/Arcade-wheel/pull/28).
  - **Link v1.0.14** tagged (a5a3783): Tier 2 caches its ~90 MB of desktop packages per runner image, prefetches them
    16 at a time with a mirror fallback, unlocks a gnome-keyring for apps that need the Secret Service, and waits up to
    60 s for the compositor. Shelf, Wheel and Clipboard use it for Tier 2.
  - **Clipboard**: [#22](https://github.com/qa-p1/Arcade-clipboard/pull/22) merged (e5ec844): gates and
    `verify-upgrade.py` (0.3.2 → 1.0.0 with the user's history and keyring). rc.1
    [Gates](https://github.com/qa-p1/Arcade-clipboard/actions/runs/44226756864) failed Linux conformance: `release.yml`
    built the AppImage on ubuntu-24.04 (CI and the changelog say 22.04), so it needed a newer glibc than 22.04 has.
    Fixed in [#34](https://github.com/qa-p1/Arcade-clipboard/pull/34) (163f958). rc.2 (built on 22.04)
    [Gates](https://github.com/qa-p1/Arcade-clipboard/actions/runs/44232113005) failed: CLI-2 (an unknown flag exits 0)
    and CLI-4 (`--arcade-manifest` exits 1 with no output, likely because conformance runs without a display), and
    Tools' delta gate (the delta from 0.3.2 fetched 50.2% of the file; the gate demands under half, which conflicts
    with the Tools #54 decision). Upgrade and both desktop suites were skipped. Next steps in `HANDOFF.md`.
  - Wheel docs [#28](https://github.com/qa-p1/Arcade-wheel/pull/28) merged (debd7f6).
  - Box: parked by the owner. Tools 1.0.1 (later): a quit right after start can leave a stale endpoint (Link replaces
    it, so low impact).

- 2026-11-17 (cloud session, afternoon) — **Lens and Find 1.0.0 stable; Box rc.7 on its way.**
  - **Lens [1.0.0](https://github.com/qa-p1/Arcade-lens/releases/tag/v1.0.0)** promoted from `v1.0.0-rc.4` (3dad560,
    Link 1.0.13) after [Gates](https://github.com/qa-p1/Arcade-lens/actions/runs/44075745595) 12/12; installers and
    SHA256SUMS byte for byte as rc.4. Lens docs [#38](https://github.com/qa-p1/Arcade-lens/pull/38) merged.
  - **Find [1.0.0](https://github.com/qa-p1/Arcade-Find/releases/tag/v1.0.0)** promoted from `v1.0.0-rc.1` (08a90ca,
    Link 1.0.13) after [Gates](https://github.com/qa-p1/Arcade-Find/actions/runs/44100470122) 12/12 (Tier 1 Hyprland
    7/7, Tier 2 sway/KWin/Mutter/X11); installers and SHA256SUMS byte for byte as rc.1, metadata differs only in channel,
    tag and notes link. On the way, Find [#22](https://github.com/qa-p1/Arcade-Find/pull/22) fixed two things CI found:
    `notices.py` read `cargo metadata` with the Windows code page (garbled "Döring", `--check` failed on Windows), and
    on Hyprland a result dragged out of the panel never reached the drop window (the layer's exclusive keyboard hold kept
    the pointer in it; the drag now switches to on-demand focus). Find docs in
    [#31](https://github.com/qa-p1/Arcade-Find/pull/31).
  - Box: rc.5 failed its own Release (UI check read the scroller before the stylesheet applied; fixed in
    [#51](https://github.com/qa-p1/Arcade-box/pull/51)). rc.6 Gates passed everything except native notices: ten
    `gir1.2-*` typelib packages the AppImage bundles were not installed on the gates runner (hidden in rc.4 by the pango
    failure); fixed in [#52](https://github.com/qa-p1/Arcade-box/pull/52). rc.7 (e40ddcd) is building.
- 2026-11-17 (cloud session, later) — **Look 1.0.0 stable; chrono advisories; Box rc.5 and Lens rc.4 on their way.**
  - **Look [1.0.0](https://github.com/qa-p1/Arcade-look/releases/tag/v1.0.0)** promoted from `v1.0.0-rc.3` (b25664e,
    Link 1.0.13) after [Gates](https://github.com/qa-p1/Arcade-look/actions/runs/44048439660) 12/12. AppImage, dmg,
    setup.exe and SHA256SUMS byte-identical to rc.3; `manifest.json`/`arcade-release.json` differ only in channel
    (test → stable) and tag; `manifest.json.sig` present. Look docs in [#41](https://github.com/qa-p1/Arcade-look/pull/41).
  - Delta gate: Lens's AppImage (one ~15 MB Rust binary) changes throughout on a rebuild, so Tools' own rule (a delta
    only when it saves ≥ 20%) downloads the whole file and the gate failed. Owner's decision: the gate accepts the
    whole file when Tools declines a delta, still checking digest, tampered file and signature (Tools
    [#54](https://github.com/qa-p1/Arcade-tools/pull/54)). Box rc.4 failed the same way.
  - New advisories RUSTSEC-2026-0543 (chrono) and -0555 (chrono-tz), "unmaintained", fail `cargo deny` everywhere they
    reach. Tools: its one user (the shortcut index's Lua sandbox) moved to jiff (in #54). Box and Lens: accepted with
    reasons (calamine's dates and Box's date tools; rxing in Lens), moving to jiff after 1.0. Find (`trash`) will need
    the same.
  - Lens [#37](https://github.com/qa-p1/Arcade-lens/pull/37): unknown option exits 2 with a stderr hint (rc.3 failed
    CLI-2), checked on the built AppImage; then rc.4 → Gates.
  - Box [#50](https://github.com/qa-p1/Arcade-box/pull/50): rc.4 Gates was the first to reach `native-notices --check`
    on the published AppImage; the Gates runner lacked `gstreamer1.0-pipewire` and `libpango1.0-dev`, which the build
    host bundles from. Then rc.5 → Gates.

- 2026-11-17 (cloud session) — **Link 1.0.13 merged; Box #48 and Lens #28 merged; Look's Restart hang found.**
  - Look rc.2 [Gates](https://github.com/qa-p1/Arcade-look/actions/runs/43960628849): every job passed except the
    Linux checks: `verify-resident.py` "explicit Restart replaces the process" timed out (it passed in the release
    build). A diagnostic branch on the Gates setup (Look `claude/sharp-cori-29w5eg-wip-restart`, 12 runs) failed once:
    the successor's unpacked copy hung in its `AppRun` on `gsettings`, crashed in `systemd-coredump`. Cause: Link's
    `relaunch_unpacked` gave the copy the launcher's environment (`GSETTINGS_SCHEMA_DIR`, `GIO_EXTRA_MODULES` in the
    FUSE mount the launcher releases at once); linuxdeploy's GTK hook runs `gsettings` when the portal does not
    answer. Every app on U1 has it, Tools 1.0.0 included.
  - Link [#75](https://github.com/qa-p1/Arcade-Link/pull/75) squash-merged (a24146f): the copy gets no reference to the
    mount (Rust and `qt/arcade_unpacked.h`, with tests); release 1.0.13. Tag after main CI and the real-fleet e2e.
    The CI speed-up moves to 1.0.14.
  - Box [#48](https://github.com/qa-p1/Arcade-box/pull/48) merged (4b354ac): AppImage built on ubuntu-22.04 (D24),
    libvips tests on a 24.04 checks-only entry, native notices from 22.04, `XInitThreads()` first in `main` (the
    Island aborted on 22.04's libX11 1.7 with "[xcb] Too much data requested from _XRead"); all six checks green.
  - Lens [#28](https://github.com/qa-p1/Arcade-lens/pull/28) merged (fea7951): conformance (icons, dependabot, step
    timeouts, LINK-2 wording; D17). rc.2's Release built everything but its publish failed: the `"*-*"` artifact
    pattern also took Tier 1's `desktop-lens` logs and GitHub refused the empty `keyring.log`; nothing was left
    published. Fixed by naming the installer artifacts (Lens D18).
  - Next: tag Link v1.0.13; Box, Look and Lens move to it (staged locally), then Box rc.4, Look rc.3, Lens rc.3 →
    Gates → Promote.

- 2026-11-16 (cloud session) — **Link 1.0.12 tagged; Look's v1 PR merged; Box rc.3 on its way.**
  - Box rc.2 [Gates](https://github.com/qa-p1/Arcade-box/actions/runs/43921442645): published files, budgets, delta, N-1, Windows and macOS smoke passed; Linux conformance failed with "GLIBC_2.39 not found" (Link's CLI cache keyed by `runner.os` only, so a ubuntu-24.04 CLI was restored on ubuntu-22.04); the Linux checks and both desktop suites did not run.
  - Link [#74](https://github.com/qa-p1/Arcade-Link/pull/74) (88915ce): CLI cache keyed by runner image; the desktop harness accepts a one-pixel cursor difference. **v1.0.12 tagged** after CI, the Desktop harness and the real-fleet e2e passed on 88915ce.
  - Box [#47](https://github.com/qa-p1/Arcade-box/pull/47): workflows on Link 1.0.12 (D23), app unchanged; then rc.3 → Gates → Promote.
  - Look [#25](https://github.com/qa-p1/Arcade-look/pull/25) merged (4248b77): Link 1.0.11, Tier 1 on Hyprland (12/12 in CI), Round 5 security (D16, cargo deny green on the live database), native notices from the built AppImage. Accessibility pass (D17) in progress.
  - Lens [#24](https://github.com/qa-p1/Arcade-lens/pull/24): the Wayland analyze fix passed Tier 1's overlay checks in CI; security pass merged in (D12); macOS test job got no runner (re-run).

- 2026-11-15 (cloud session, evening) — **Box rc.2 releasing; Lens Tier 1 found a Wayland bug; work handed to the local session.**
  - Link v1.0.11 tagged (b00a1ca). Box [#46](https://github.com/qa-p1/Arcade-box/pull/46) merged (513cb3f), `v1.0.0-rc.2` tagged, Release run 43754158123 in progress.
  - Lens [#24](https://github.com/qa-p1/Arcade-lens/pull/24): Link 1.0.11, CHANGELOG, Tier 1 desktop test. Its first run found that `--window analyze` ("Analyze with Lens") never opened on Wayland; fixed in 34b1dbb.
  - Look branch pushed (Link 1.0.11, `is_unpacked_copy()`, Tier 1), no PR yet. Security passes for Lens and Look on `-wip-security` branches, unreviewed.
  - Owner approved a CI speed-up (Link 1.0.12, Release reuses main's build) after Box is promoted. Details and next steps in `HANDOFF.md`.

- 2026-11-15 (cloud session, late afternoon) — **Link 1.0.10 tagged, 1.0.11 merged; Lens and Look gates merged; Box rc.1 gates found a publish bug.**
  - Link 1.0.11 ([#72](https://github.com/qa-p1/Arcade-Link/pull/72)): `ARCADE_UNPACKED` was inherited by a Restart's successor and by apps started from
    a copy, which then stayed on their FUSE mount (found by Clipboard's and Wheel's step 5 packaged checks). Rust and C fixed with
    tests that fail without the fix.
  - Box rc.1 Gates failed at "Published files": asset names with spaces were changed by GitHub. Fixed for every app in Link
    [#73](https://github.com/qa-p1/Arcade-Link/pull/73); Box rc.2 follows on Link 1.0.11.
  - Round 5 security pass (SECURITY.md, cargo deny in CI, generated notices with `--check`) running for Find, Lens, Look and
    Clipboard; Shelf (notices still name Link v0.3.0) and Wheel next.

- 2026-11-15 (cloud session, afternoon) — **Step 5 merged for Find and Lens, Box 1.0.0-rc.1 tagged, Link 1.0.9 tagged and 1.0.10 merged.**
  - Merged on all-green heads: Find [#21](https://github.com/qa-p1/Arcade-Find/pull/21), Lens [#22](https://github.com/qa-p1/Arcade-lens/pull/22),
    Box [#44](https://github.com/qa-p1/Arcade-box/pull/44) and [#45](https://github.com/qa-p1/Arcade-box/pull/45) (1.0.0), Clipboard
    [#21](https://github.com/qa-p1/Arcade-clipboard/pull/21), Look [#22](https://github.com/qa-p1/Arcade-look/pull/22), Link
    [#70](https://github.com/qa-p1/Arcade-Link/pull/70) and [#71](https://github.com/qa-p1/Arcade-Link/pull/71) (1.0.10).
  - Tagged: Link v1.0.9 (65cb57e), Box `v1.0.0-rc.1` (bed8a19, Release running). Link v1.0.10 after its post-merge runs.
  - Merged: Look [#23](https://github.com/qa-p1/Arcade-look/pull/23) (step 5; its first run was red on a packaged check that read the
    resident's exec-time environ, fixed to check WebKit's helpers). Shelf, Wheel and Clipboard step 5 in progress on Link 1.0.10.
  - Opened, step 7 gates: Find [#22](https://github.com/qa-p1/Arcade-Find/pull/22), Lens [#23](https://github.com/qa-p1/Arcade-lens/pull/23),
    Look [#24](https://github.com/qa-p1/Arcade-look/pull/24). Lens and Look had no upgrade test; both now do. Missing for
    Round 5: SECURITY.md in Find, Lens, Look, Shelf and Clipboard; THIRD_PARTY_NOTICES in Look and Clipboard.
- 2026-11-15 (cloud session, morning, cont.) — **Find step 4 merged; step 4 PRs for Clipboard and Look; step 5 for
  Find and Lens; Box step 7 part 2; Link C twin of the unpacked runtime.**
  - Merged: Find [#20](https://github.com/qa-p1/Arcade-Find/pull/20) (7995744) on 9/9 green.
  - Opened: Clipboard [#21](https://github.com/qa-p1/Arcade-clipboard/pull/21), Look [#22](https://github.com/qa-p1/Arcade-look/pull/22)
    (step 4); Find [#21](https://github.com/qa-p1/Arcade-Find/pull/21), Lens [#22](https://github.com/qa-p1/Arcade-lens/pull/22)
    (step 5); Box [#44](https://github.com/qa-p1/Arcade-box/pull/44) (gates, upgrade gate, a11y, security rows, screenshots);
    Link [#70](https://github.com/qa-p1/Arcade-Link/pull/70) (RT-7 for C/C++ apps, uninstall removes own copies).
  - Link 1.0.9 on 65cb57e: CI and Desktop harness green; real-fleet e2e running; tag after it passes.
- 2026-11-15 (cloud session, morning) — **Step 4 for Lens, Wheel and Shelf, Box step 7 part 1 and Link 1.0.9 merged.**
  - Merged on all-green heads: Lens [#21](https://github.com/qa-p1/Arcade-lens/pull/21) (b6e09c5), Wheel
    [#23](https://github.com/qa-p1/Arcade-wheel/pull/23) (3b16a05), Shelf [#15](https://github.com/qa-p1/Arcade-Shelf/pull/15),
    Box [#43](https://github.com/qa-p1/Arcade-box/pull/43) (f9d21f5), Link [#68](https://github.com/qa-p1/Arcade-Link/pull/68)
    (release 1.0.9, squash 65cb57e).
  - Link 1.0.9: CI, Desktop harness and real-fleet e2e (`real_apps=true`) running on 65cb57e; tag after all three pass.
  - Find [#20](https://github.com/qa-p1/Arcade-Find/pull/20) (step 4) in CI; Look and Clipboard step 4 in progress.
- 2026-11-15 (cloud session, after the limit reset) — **Clipboard step 2 and Tools' per-app delta gate merged; CI fixes.**
  - Merged on all-green heads: Clipboard [#20](https://github.com/qa-p1/Arcade-clipboard/pull/20) (00b3d9b), Tools
    [#50](https://github.com/qa-p1/Arcade-tools/pull/50) (fdbbc3e).
  - Overnight failures, root-caused and fixed: Lens #21 (macOS/Windows-only uses of removed items), Wheel #23 (macOS
    initializer), Box #43 (licence inventory and notices still named Link 1.0.7), Link #67's real-fleet run (Box's
    launcher now hands over to an unpacked copy and exits 0, so the harness lost the process: the harness now starts
    AppImages with `ARCADE_UNPACKED=1`, 810a667; a real-fleet run is dispatched on it). Find's "own tray with Link
    disabled" check also failed in that run; it is re-checked on the new run before any change.
  - Box BR-17/BR-18 fixed (they were still open on main), Shelf step 4 finished (PR #15).
- 2026-11-15 (cloud session) — **Five app PRs merged; Box Round 5 audited.**
  - Every check green on the PR heads; merged with merge commits: Clipboard [#19](https://github.com/qa-p1/Arcade-clipboard/pull/19),
    Find [#19](https://github.com/qa-p1/Arcade-Find/pull/19), Shelf [#14](https://github.com/qa-p1/Arcade-Shelf/pull/14),
    Lens [#20](https://github.com/qa-p1/Arcade-lens/pull/20), Look [#21](https://github.com/qa-p1/Arcade-look/pull/21).
    Clipboard's and Shelf's main builds on Link 1.0.8 are what LEGACY_PENDING in Link's real-fleet e2e waits on.
  - Clipboard step 2 continues on [#20](https://github.com/qa-p1/Arcade-clipboard/pull/20) (D3-D6; 47 Flutter tests).
  - Box Round 5 audit: schema/0.x fixtures, downgrade safety, N-1, `gates.yml` and the conformance, budgets, tier 2,
    upgrade and delta gates are missing; licence, docs, a11y, uninstall are partial. Box step 7 started with Link
    1.0.8, the unused manifest script and the changelog.
- 2026-11-15 (cloud session) — **Link v1.0.8 tagged; Tools 1.0.0 stable; Clipboard and Shelf on Link 1.0.8.**
  - [Link #66](https://github.com/qa-p1/Arcade-Link/pull/66) green on 9316e43 (CI, every real-fleet group: install
    22 passed + 2 XFAIL, trayhost 27, tools-hub 42, shortcuts 20; 0 skipped): squash-merged as 34f8030. On 34f8030:
    [CI](https://github.com/qa-p1/Arcade-Link/actions/runs/43617558914), [Desktop harness](https://github.com/qa-p1/Arcade-Link/actions/runs/43617569981)
    and the dispatched [real-fleet e2e](https://github.com/qa-p1/Arcade-Link/actions/runs/43617572879) all green
    (fleet: Box 42a3d3b, Lens ba1d3f0, Look 09041ad, Wheel 870bbb8, Shelf 46f1d0c, Find 3456d57, Clipboard d1c5ecb,
    Tools f4b86bd) → **`v1.0.8` tagged** through "Tag a release" ([43659058956](https://github.com/qa-p1/Arcade-Link/actions/runs/43659058956)).
  - **Tools 1.0.0 promoted.** The one-launcher gate passed on f4b86bd (the rc.11 commit) in that run, the last gate
    left after Gates 11/11. [Promote](https://github.com/qa-p1/Arcade-tools/actions/runs/43659111568) republished
    rc.11 as [v1.0.0](https://github.com/qa-p1/Arcade-tools/releases/tag/v1.0.0) (latest, not a prerelease). Checked
    after: every package and SHA256SUMS has the rc's SHA-256 digest; `arcade-release.json` says `stable`; the
    signed `manifest.json` verifies (minisign, prehashed) against Tools' built-in key with trusted comment
    `app=arcade.tools version=1.0.0 tag=v1.0.0 channel=stable`. Not checked here: an installed rc.11 on the stable
    channel being offered 1.0.0 (Gates' self-update covers the same path, rc.10 → rc.11).
  - Box [#40](https://github.com/qa-p1/Arcade-box/pull/40) (5/5 green) merged with a merge commit (c64b521).
  - **Clipboard → Link 1.0.8** (f0095f5; was v0.4.4): pin, lockfile, `sync-design.py` at the tag (additive kit
    changes only: key chips, emoji fallback), VENDORED names the tag; clippy 1.98.1 clean, `cargo test --workspace`,
    `check-docs.py`. Untangle started with `docs/v1/DECISIONS.md`: D2 removes the vendored `arcade-release.py`,
    which nothing ran since step 6 (8442444). **Shelf → Link 1.0.8** (372690a; was v0.3.0): `vendor-link.py
    --revision v1.0.8`, `check-vendor.py` 136 files, `check.py` with Qt 6.8.3 green (17/17). Its format check caught
    the Desktop split's continuation indent in `DesktopPlacement.cpp` (fixed, 2bb7778). Both drop out of
    `LEGACY_PENDING` once their main builds are green on 1.0.8. Next: the app PRs (Clipboard, Shelf, Find, Lens, Look,
    Wheel), now that v1.0.8 exists.
- 2026-11-14 (cloud session, from 13:36 UTC) — **Handoff picked up; Tools rc.11 tagged; Link 1.0.8 bump.**
  - Re-checked every PR first. Tools #49 head ad45884 was 20/20 green (macOS dmg passed at 10:24): merged (merge
    commit f4b86bd), `v1.0.0-rc.11` tagged through "Tag a release", which started Release.
  - Link: CI, Desktop harness and real-fleet e2e ([43580856047](https://github.com/qa-p1/Arcade-Link/actions/runs/43580856047),
    all four real-fleet groups) were green on 079f954, but 079f954 still says 1.0.7 in `Cargo.toml`, so "Tag a
    release" would refuse v1.0.8. #63 (green) squash-merged as f867e7f; the bump is [#64](https://github.com/qa-p1/Arcade-Link/pull/64)
    (fmt and clippy clean on 1.88). The gates re-run on its merge commit before the tag.
  - Step 3 merges (every check green on the reviewed head; merge commits): Box #36 (Link 1.0.7, 9480801) and #38
    (CI D13, bbc247a), Lens #19 (ba1d3f0), Clipboard #18 (d1c5ecb). Reviewed against their specs, then merged: Find
    #18 (3456d57), Look #20 (09041ad), Wheel #17 (870bbb8; vendored `src/link` byte-identical to Link v1.0.7).
    Review notes: Wheel's `--status` exit 3 matches ARCADE_APP CLI-1; Look's and Wheel's new unknown-option checks
    accept every flag Link, the installers and the desktop entries pass; Find's uncapped `--search` limit is CLI-only
    (Link peers stay at 1000). Left for Find step 2: two inserted functions took over the doc comments of
    `index_state` (service.rs) and `needs_compaction` (index.rs).
  - Box #37 (untangle) conflicted with #38 only in `docs/v1/DECISIONS.md` (both appended): resolved on
    `claude/sharp-cori-29w5eg` (D12 then D13), clippy on 1.88 before the push.
  - **Runner contention (step 6 finding):** the merge wave made Dependabot rebase every open Dependabot PR, and each
    started a full CI build: 24 queued runs (Box 6, Tools 12 incl. memory probes, Link 2, Wheel 3, plus a superseded
    Box main run) sat ahead of the rc.11 publish job (queued for an hour after every build passed at 13:55), Link #64
    and the main builds the v1.0.8 gate needs. Cancelled those 25 runs (re-runnable; Dependabot rebuilds its PRs
    on the next rebase). Fix to make per repo in step 6: `rebase-strategy: disabled` (or a weekly schedule with
    grouped updates) in `.github/dependabot.yml`, so a merge to main doesn't queue one build per Dependabot PR.
  - **Box, found while preparing step 6:** `release.yml` ran on every pushed `v*` tag and published it as the
    latest stable release, so the first `v1.0.0-rc.1` would have reached users untested. Fixed locally with Tools'
    shape (rc-only `tag.yml`, test-channel `release.yml` via Link `app-publish`, `promote.yml`, `nightly.yml`;
    Box D15), together with step 5 (memory, D14). Pushed once #39 merges (the branch is #39's head).
  - `LEGACY_PENDING` plan: one Link PR drops every app whose 1.0.7 main build is green (Tools, Lens, Box, Find,
    Look, Wheel), then CI + harness + real-fleet e2e on that commit, then tag v1.0.8 there (the strict XFAIL fails
    a run if a listed app passes, so the list must match the fleet when the e2e runs).
  - This session pushes to `claude/sharp-cori-29w5eg` in every repo (this file included), which continues
    `claude/tender-feynman-3vt7dg`.
  - 14:16 UTC: Tools rc.11 Release ([43600684898](https://github.com/qa-p1/Arcade-tools/actions/runs/43600684898))
    green, 14/14 jobs (published to the test channel); Gates dispatched on `v1.0.0-rc.11` with `update-from`
    v1.0.0-rc.10, `previous` v0.4.6 ([43604006265](https://github.com/qa-p1/Arcade-tools/actions/runs/43604006265)).
    Link #64 green on every check, squash-merged (e1a543b, `Cargo.toml` 1.0.8).
  - `LEGACY_PENDING` PR: [Link #65](https://github.com/qa-p1/Arcade-Link/pull/65) keeps only Clipboard (main
    still pins Link v0.4.4, not 1.0.7) and Shelf. It merges once the six 1.0.7 main builds are green (Tools
    f4b86bd, Box bbc247a, Find 3456d57, Lens ba1d3f0, Look 09041ad, Wheel 870bbb8; none finished yet), since the
    picker takes each app's newest green main run.
  - Tools rc.11 Gates green, 11/11 ([43604006265](https://github.com/qa-p1/Arcade-tools/actions/runs/43604006265)):
    published files, macOS dmg, budgets, delta + signature + tampered chunk, Windows installer, Linux (conformance,
    package, upgrade from v0.4.6 and rc.10, tray, N-1, self-update), Hyprland, sway, mutter, kwin, x11. **Promote is
    held for one gate gates.yml doesn't cover:** "exactly one launcher and at most one login item" after an upgrade
    (PLAN exit gates). Link's real-fleet e2e checks it (`arcade.tools_update_retires_old_desktop_ids`) on Tools
    main f4b86bd, the rc.11 commit, once #65 is merged; promote rc.11 when that passes.
  - Main builds at the 1.0.7 commits green: Tools, Look, Find, Wheel; Box and Lens running. Cancelled one more
    Dependabot run (Link #40), queued ahead of release work.
  - Box [#39](https://github.com/qa-p1/Arcade-box/pull/39) green 5/5 (incl. Hyprland), merged (merge commit
    42a3d3b; #37's untangle lands with it). Steps 5 + 6b + Dependabot replayed on it: [Box #40](https://github.com/qa-p1/Arcade-box/pull/40)
    (clippy 1.88 clean, 38 desktop tests). It merges after the Link v1.0.8 e2e, so the e2e's Box build stays the
    one #65 expects.
  - Prepared and pushed without PRs (no CI until opened): Find doc-comment fix (step 2), Tools and Wheel Dependabot
    config, and Clipboard's Link 1.0.8 groundwork (install strings "Just run it", CI's isolated runner at the pinned
    tag; it compiles and 101 tests pass against Link 1.0.8). **Clipboard `release.yml` has Box's rule-zero hazard**
    (a pushed `v*` tag publishes stable): fix in its step 6. Shelf re-vendor dry run at 1.0.8: 18 files plus
    `arcade_trim.h`; its legacy ids are already declared.
  - All six 1.0.7 main builds green (Box bbc247a last, after its macOS DMG build). Link #65 green, squash-merged
    (ce9a71c). On ce9a71c: CI (push), Desktop harness and real-fleet e2e (`real_apps=true`) dispatched; v1.0.8 is
    tagged there through "Tag a release" when all three pass.
  - **Real-fleet e2e on ce9a71c red** ([43608443967](https://github.com/qa-p1/Arcade-Link/actions/runs/43608443967)):
    install group `*_update_retires_old_desktop_ids` failed for all six 1.0.7 apps. Each left the old *login item*,
    never the old launcher. Cause, a test bug: every e2e session sets `ARCADE_HOME`, Link's `Environment::discover`
    then roots config at `ARCADE_HOME/.config` and ignores `XDG_CONFIG_HOME`, and the check planted the old login
    items under `XDG_CONFIG_HOME`. Link's own `legacy_id_entries_running_the_installed_file_are_retired` covers the
    behaviour in that layout. Also `Development build (arcade.look)` lacked `libdav1d-dev`. Both fixed in
    [Link #66](https://github.com/qa-p1/Arcade-Link/pull/66), labelled `e2e-real-fleet` so the matrix runs on the PR.
    No v1.0.8 tag and no Tools promotion until the re-run on its merge commit is green; this check is Tools'
    one-launcher exit gate. Box #40 waits too.
  - Box #40 Ubuntu check failed `native-notices.py`: the new `usr/lib/libarcade-trim.so` (OPEN1) maps to no system
    package. Listed as Box's own, as in Tools (b2a0d1f); re-running.
  - **Step 6 (rule zero) across the fleet.** All six remaining apps built stable directly: Clipboard on any pushed
    `v*` tag, Find, Lens, Look, Shelf and Wheel on a manual `stable` dispatch. None promoted a tested rc. Each now has
    Tools' and Box's shape on its `claude/sharp-cori-29w5eg` branch: `tag.yml` makes only `vX.Y.Z-rc.N` and starts
    `release.yml`, which publishes on the hidden `test` channel through Link `app-publish@v1.0.8`; `promote.yml`
    (`app-promote`) and `nightly.yml` (`app-nightly`). Clipboard 4322ea0, Find 6e2fc47, Lens 343a0cc, Look da206ed,
    Wheel ba1b238, Shelf 5287f11. Find, Look and Wheel keep their own installer verification in a stage job. Look's
    installers lose the spaces in their names before upload (GitHub turns them into dots, so metadata would name
    files that don't exist). The signing secret is in all eight repos (LOCAL.md item 1).
  - Two Link gaps found doing it, fixed in a local Link commit (df91c7c) for 1.0.8, pushed after #66's real fleet
    is green: the reusable publish described every Windows `.exe` as NSIS (Clipboard, Find, Lens and Wheel ship
    Inno, which ignores `/S`); it now takes `windows-installer`, and promotion reads the kind from the rc's
    `arcade-release.json`. `app-nightly` failed on per-platform artifacts that each carry metadata (Wheel): it now
    leaves the metadata out. PRs for the six apps open once v1.0.8 is tagged, since they pin it.
  - **Link #66 real fleet on 4fa246d** ([43610599997](https://github.com/qa-p1/Arcade-Link/actions/runs/43610599997)):
    trayhost and shortcuts green; install 20 passed, 2 XFAIL (Clipboard, Shelf), 2 failed. The ARCADE_HOME fix
    worked: Box, Lens, Look, Wheel and Find now retire their old entries. The two failures: (1) Tools "left"
    `autostart/arcade-tools.desktop`, which is Tools' *current* login item (`autostart_id: "arcade-tools"`, also its
    old launcher name); the check planted an "old" entry over it and expected it gone. Tools behaves correctly (one
    launcher `dev.arcade.Tools`, one login item; Box and Clipboard also keep a separate login-item name), so this is
    a second test bug: the check now skips the login item the first install recorded. (2) Look's development build
    now compiles but the install job lacked `libdav1d.so.7` at run time: the job installs `libdav1d7`. Both in
    c6c0654 on #66 together with df91c7c (Inno support); the real fleet and the draft release-flow e2e run on it.
  - Box #40 green 5/5 (incl. Hyprland); merged after #66's real fleet passes, so the e2e's picked fleet stays put.
  - While CI ran: **Clipboard CB-5 second half** (ba3d050): `--status` answers from the Rust core before GTK and the
    engine (C ABI `arcade_clipboard_status_line`, loaded by the runner's `main()`; engine path as fallback). Tests:
    a core test through the C ABI; `verify-appimage.py` runs the installed `--status` with no display and wants one
    JSON line and an empty stderr. Checked locally by compiling `main.cc` against the built core. **Shelf step 2**
    (234c53a): `Desktop.cpp` (1,852 lines) split by concern into `DesktopPlacement`, `DesktopFiles`,
    `DesktopShortcut`, `DesktopLogin` and the private `DesktopPrivate.h`, moved from line ranges (a line-multiset
    diff shows only the intended edits); `scripts/check.py` green locally with Qt 6.8.3 (17/17 ctest incl. `tst_Ui`
    under Xvfb), and the files also compile without DBus/X11. Windows/macOS compile only in CI (PR after v1.0.8).
  - #66 on c6c0654: Look's development build now passes (libdav1d7); release-flow e2e (drafts) green with the Inno
    assertion (the promoted Windows asset keeps `kind: inno`). Tools still failed: a silent `--no-launch` install
    records no login item, so the planting skip didn't apply. Link's installer takes an existing entry at the app's
    own autostart id as its login item (start at login carries over) and records it, which is what Tools did. The
    check now excludes the login item the receipt records *after* the update (9316e43); an entry the receipt doesn't
    own still fails, and "exactly one login item" is still asserted. Real fleet re-running.
  - More step work on the branches (no PRs until v1.0.8): **Lens** step 2, the parked one-PATH-lookup commit merged in
    (14a7493; clippy + tests on 1.88.0). **Find** CI saves Rust caches only on main (f7d2b38; the only repo left
    without `save-if`), and step 2 by the untangle skill from a scripted module graph: one `identity` module
    (`dev.arcade.Find` was defined twice; installer and tray imported Settings for the tagline), one `session` module
    (three Wayland checks, two Hyprland detections, two `hyprctl -j` runners), and a real bug found on the way: the
    event log and Link's captured stderr shared `arcade-find.log` with two rotation policies, so an event rotation
    moved the live stderr log aside and later deleted it (events now in `events.log`, with a test that fails on the
    old code). Find D11-D14. **Wheel** step 2 (D4): configuration included the platform interface for one value type.
    Step 4 fleet-wide: `cargo machete` finds no unused dependency (Look's `kamadak-exif` is a false positive).

- 2026-11-14 (local session) — **Link v1.0.7 tagged; fleet moving onto it; Box untangle and CI started.**
  - Link real-fleet e2e on 40ec027: tools-hub 42/42, trayhost 27/27, install 16/16 (+8 XFAIL), shortcuts 20/20,
    after Lens main's red CI (11 Nov DNS outage) was rerun so the fleet got Lens 0.4.2. **v1.0.7 tagged** (40ec027,
    "Tag a release"). Link #62 merged (1.0.8, unreleased: key chips, HintBar); its main checks are running.
  - Merged: Box #35 (P2 fixes, dead code, GStreamer notices), Lens #17 (all P0/P1 + five P2), Shelf #13, Clipboard
    #17. Tools #49 moved to Link 1.0.7 and `ammonia` 4.2.5 (RUSTSEC-2026-0533, published 12 Nov). Box #36 and
    Lens #18 move them to 1.0.7 (Lens from 0.4.14, no code changes).
  - Box step 2 (untangle, PR #37, D12): desktop `lib.rs` 2,542 -> 470 lines (`island`, `tray`, `instance`,
    `commands/<feature>`); one `safe_stem` (byte cap: long CJK names could exceed the file name limit), one
    `rgb_to_hsl`, one file-name character rule (six copies), one `fileList(tool)` (four copies).
  - Step 6 finding across the fleet: GitHub's 10 GB cache cap was full or over in Box, Lens, Clipboard, Link and
    Tools. Box's Linux Rust cache was always evicted (40-minute PRs); Lens, Clipboard and Link saved caches from
    pull requests. Fixes: Box #38 (one Linux package per PR, trimmed Windows/macOS caches, D13), Lens #19,
    Clipboard #18, Link #63 (save only on main).

- 2026-11-13 (local session) — **Link 1.0.7 merged; every app's P0/P1 fixed except Look/Wheel (partner agent).**
  - Link [#61](https://github.com/qa-p1/Arcade-Link/pull/61) merged (40ec027) with BP-4 (old desktop-id icons
    retired, Rust + Qt, tested). CI and the desktop harness green on main; the real-fleet e2e failed tools-hub 39/42
    on the same three Lens/Box release checks as before. Cause: Lens main CI had been red since the 11 Nov Azure DNS
    outage, so the picker used the last green Lens build, a `-dev` prerelease. Lens main rerun green; the e2e re-runs
    before the v1.0.7 tag. Link [#62](https://github.com/qa-p1/Arcade-Link/pull/62) (1.0.8): key chips no longer
    stretch (Clipboard RD-CLIPBOARD-2), HintBar elides (Shelf SH-3).
  - Box [#35](https://github.com/qa-p1/Arcade-box/pull/35): all B-xx P2s, BR-13, BP-2/3, one clipboard history,
    step 4 dead code (D11), apt retries; the native-notices artifact path fixed so the GStreamer notices can be
    committed. Backlog with reasons: BP-1, BP-5, non-ASCII watermark.
  - The handoff patches were reviewed and landed: Shelf SH-5 (bug fixed: a re-added item vanished), Find and Lens
    step 1 (one wrong Find lock rewritten), Clipboard (Forever retention made captures fail at random; fixed),
    Look's patch superseded by the 1.0.7 pin.
  - Lens, Shelf and Clipboard fixes as in the Status table, each with a test that failed before.

- 2026-11-11 (local session, owner's PC) — **Duplicate launchers fixed at the root; B1 and B2 done; Lens #16 and
  Box #34 merged.**
  - The owner saw two menu entries for Box, Look, Shelf, Clipboard and Wheel, and Look started twice at login. Cause:
    Link ≤ 1.0.6 kept an entry under an old desktop id (`dev.arcadebox.app`, `arcade-look`, `arcade.shelf`,
    `dev.arcade.clipboard`, `com.arcadewheel.ArcadeWheel`) whenever it ran the same AppImage as the new one; every
    app already listed those ids. Fixed in the Rust and Qt installers on Link #61 (3dbaab9, CHANGELOG 1.0.7) with
    tests that failed before; new real-fleet e2e check per app. New fleet rule and checklist item "One launcher per
    app" in `PLAN.md`. The owner's own desktop was cleaned by hand.
  - B1: signing key set on all 8 app repos, public key on Tools PR #49 (6bfba35). B2: `qa-p1/Arcade-template`.
  - [Lens #16](https://github.com/qa-p1/Arcade-lens/pull/16) merged (e889670) and
    [Box #34](https://github.com/qa-p1/Arcade-box/pull/34) merged (67d0359) after re-checking green; Box's Tier 1
    job showed BR-0/BR-1 passing and BR-2 XFAIL.

- 2026-11-11 (session 3, 09:40 UTC) — **Tools "close under load" was a harness bug; Box step 3 core + Island fixes;
  e2e down to two causes.**
  - **Close under load (Tools open item) is Link's `wmclose`, not Tools.** Locally under CPU load the first close
    was lost about half the time (7 of 13). Tools was idle in `poll` and a second close worked. `XEventsQueued`
    showed nothing queued, and an X protocol trace (xtrace) showed the server never delivered the first
    ClientMessage, neither to Tools nor to an independent `xev` listener. `wmclose` only flushed and exited, and an
    X server that polls a client after it has gone drops it unread. With `XSync` + `XCloseDisplay` it was 0 of 10.
    The fix is on Link [PR #61](https://github.com/qa-p1/Arcade-Link/pull/61) (46400dd) and ships in Link 1.0.7.
  - **Real-fleet e2e (run 42988304697, head e6442e2):** shortcuts 20/20, trayhost 27/27, tools-hub 39/42,
    install 15/16 (from 21 failing before the picker/adapter/signing fixes). The three tools-hub failures are one
    cause: Lens labels main builds `0.4.2-dev.<sha>`, a prerelease that Tools' stable channel rightly refuses.
    Fixed in Lens [PR #16](https://github.com/qa-p1/Arcade-lens/pull/16) (Lens D6: main builds carry the Cargo
    version, like every other app). The install failure (Tools does not quit on `app.quit` after its install
    relaunch) is being reproduced.
  - **Box step 3 (fixes), pushed to `claude/tender-feynman-3vt7dg`, PR to follow:**
    - Core: B-7 calculator, B-8 units, B-9 date spans and time-zone inputs/abbreviations, B-10 diff, B-25
      processes, U-1 numeric options, BR-15/16 downloads, BR-4 search. Typed expressions now route to their
      converter, and whole words rank first.
    - Island: BR-0 (P0, Escape goes back one step; a running job stays reachable), BR-5/6 hints, BR-11 highlight,
      BR-12 fresh re-show, BR-1 lost shortcut release.
    - Each finding's lock test was flipped with its fix; `cargo test -p arcade-core`, clippy, svelte-check, the
      key lock and the layout check all pass locally. Decisions D7 (ambiguous converter input).
    - Left in step 3: BR-2 (input region, needs the Hyprland harness on CI), BR-3 (GStreamer packaging), BR-7,
      BR-8, BR-9.

- 2026-11-11 (session 3, 09:00 UTC) — **Link: gate change merged; the real-fleet e2e had been blind since Nov 8.**
  The owner stopped the code-writing subagents; the lead works the plan in order again. Long waits (CI runs,
  releases, probes) now go to a read-only Sonnet watcher that reports back while the lead keeps working; local
  long jobs run as background commands (brief: session scratchpad `watcher-brief.md`).
  - Link [PR #60](https://github.com/qa-p1/Arcade-Link/pull/60) (the memory gate measures the open window once the
    app is idle) merged as 39a86c7 after Tools probe
    [run 42903942776](https://github.com/qa-p1/Arcade-tools/actions/runs/42903942776) on 8 runners: default and
    arenas-2 passes open 217.5–221.2 MB PSS with no note; busy pass 207.5–221.9, measured after 8 s on 6 runners, no
    "still busy" failure. Main CI and e2e contracts green.
  - **Found:** every nightly real-fleet e2e since Nov 9 failed to compile (Tools removed `portable_backup`, which
    Link's adapter imported), so no real-app check ran for three days. On Link's branch: the adapter uses the backup
    Tools ships (bc86cd0); the artifact picker skips Dependabot jobs that hid Box's packaging run (811251d, test
    fails without the fix); loopback fixture releases are signed with Tools' debug-only test key through Link's own
    `release-manifest --sign` and served as a release list, as Tools now requires (e6442e2). First run with the
    adapter fix ([42984806891](https://github.com/qa-p1/Arcade-Link/actions/runs/42984806891)): all six available
    apps' backup round trips pass. A second run with all three fixes is being watched.
  - **Found (Tools, real bug, blocks the next Tools rc):** with every CPU busy, a window close (WM_DELETE_WINDOW)
    sent a few seconds after the window opens is ignored while Tools stays responsive; a second close works.
    Reproduced locally (2 of 4 runs) and in the probe's busy pass (4/8 and 7/8 runners on two runs, before and after
    the gate change). Being traced in GTK's delete path.
  - Open from run 42984806891, under investigation: Tools did not quit within 15 s of `app.quit` in the install
    check (not reproduced locally with Tools main's or PR #49's build: both quit in 3 s), and Find with Link
    disabled did not report its own tray icon.

- 2026-11-10 (session 3, 21:30 UTC) — **Resumed after a usage-limit stop.** The account's 5-hour limit ended every
  agent at about 06:10 UTC, ten minutes into the code-writing pass; nothing was lost (work was on disk). Committed
  work is pushed and all seven Sonnet agents were resumed where they stopped, now told to commit and push after every
  unit of work. On their branches at the stop: Wheel 8 commits (to b2160fd), Clipboard 4 (to ab746fa: retention with
  a storage budget), Look 3 (to 4fe14c6: Escape steps back one level), Find and Shelf 1 each (the brief), Box and Lens
  uncommitted edits only. Their own `docs/v1/PROGRESS.md` files list each commit; a summary per repo follows here
  when each agent reports.
  **Tools memory, judged by the rule fixed in D21** (probe [run 42764576055](https://github.com/qa-p1/Arcade-tools/actions/runs/42764576055),
  7 runners): normal passes 217–220 MB; under load two runners read 293–294 at 6 s, all of it WebKit code
  (file-backed 95–101 MB, other memory within 4.3 MB), settled by 10 s. So the gate may wait for the app to be idle
  (Tools D22): Link [PR #60](https://github.com/qa-p1/Arcade-Link/pull/60), and a probe run with that gate is
  measuring before v1.0.7 is tagged. New finding, within budget: Tools' first update check 60 s after start lifts an
  open window to 252–266 MB until the next trim (Tools D21, open item).
- 2026-11-10 (session 3) — **Owner rule (chat): parallel code-writing pass with Sonnet agents.** "Write most of the
  code part of all the steps … use sonnet agents … at least complete the writing code part; checking and releasing
  after." This replaces "one agent, no subagents" for writing code. Seven agents started ~06:00 UTC, one per app repo
  (Box, Clipboard, Look, Find, Lens, Shelf, Wheel), with a common brief: steps 0–7 in priority order (brief, behaviour
  lock, P0/P1 fixes, app standard on Link v1.0.6, CI workflows, dead code, untangle, memory/Round 5), committing to
  `claude/tender-feynman-3vt7dg` in their own repo only, documenting every commit as tested locally or not run in the
  repo's `docs/v1/PROGRESS.md`. They open no PRs, merge nothing, tag and release nothing; Link changes they need are
  listed, not made. Tools and Link stay with the lead. Checking (CI, gates) and releases follow, by the PLAN's rules.
- 2026-11-10 (session 3) — **Box PR #20 merged** (effb510): Link 1.0.6 runtime (crash reports, arena cap), CLI-2,
  Linux identity, notices, SECURITY.md, Wasmtime 36 LTS, cargo deny over the workspace (RUSTSEC-2026-0459 accepted,
  D6); green on 3 OSes and Hyprland. CI-speed note for Box step 6: the Windows check took 41 min, macOS 40, Linux 35
  (target < 8 warm).
- 2026-11-10 (session 3) — **Correction: the memory fix is not complete; Link v1.0.7 not tagged.** Link main
  51d8ad8 (1.0.7, [PR #59](https://github.com/qa-p1/Arcade-Link/pull/59)) passed CI, Ecosystem e2e and the
  Desktop harness (dispatched; an earlier harness run on f199e6a lost sway/KWin to an Azure apt mirror outage, also
  seen in Tools probes). The 8-runner probe on Tools PR #49's build ([run 42758214825](https://github.com/qa-p1/Arcade-tools/actions/runs/42758214825))
  read ~220 MB open PSS in every normal pass (WebKit file-backed 20.8 MB, was 56/104), but its pass with every CPU
  busy through the 6 s sample read **289.7** on one runner (budget 281). The tag waits; the slow-open case goes back
  to the Fable advisor with the probe data. Box [PR #20](https://github.com/qa-p1/Arcade-box/pull/20): cargo deny
  found RUSTSEC-2026-0459 (bundled SQLite); accepted for Box's own database with reason (Box D6, SECURITY.md), fix
  with the fleet's Rust 1.89.
- 2026-11-10 (session 3) — **Tools PR #49's memory gate: cause found and fixed** (diagnosed with Fable 5.2's
  advice). Not the PR: the probe on unchanged rc.10 ([run 42750339792](https://github.com/qa-p1/Arcade-tools/actions/runs/42750339792))
  read 247.6–251.5 on 7 runners and 289.5 in the gate's own command on a slow one, with 48 MB more WebKit code
  resident: the trimmer ran at 2 s and then every 20 s, and a page still loading at 2 s kept its code until 22 s, past
  the gate's 6 s sample. Link [PR #58](https://github.com/qa-p1/Arcade-Link/pull/58) (merged, a4c1ff6): the trimmer
  trims again while a helper settles (Link D14), and `relaunch_unpacked` no longer leaks the arena cap into apps
  Tools starts (also in rc.10; test fails without the fix). Tools eb89d96 (D21) vendors it and uses Link's cap:
  **its CI gate read 219.7 MB open PSS** (was 309; cap 281), all other jobs green; the 8-runner probe on that
  build is running. Link 1.0.7 release PR [#59](https://github.com/qa-p1/Arcade-Link/pull/59). The background
  1.4 MB reading is real (resident paged out to swap; PSS excludes swap), unchanged since rc.3. Box
  [PR #20](https://github.com/qa-p1/Arcade-box/pull/20) opened from the handoff patches (local `scripts/check` green).
- 2026-11-10 (session 3) — **Box PR #19 (behaviour lock) merged** (b958041) after [run 42751978552](https://github.com/qa-p1/Arcade-box/actions/runs/42751978552)
  passed on 3 OSes and Hyprland, 11 of 11 Island checks as expected (BR-2, BR-1, BR-0 XFAIL; BR-0 now behind two
  passing locks: Escape clears typed text, Return keeps the Island open). **Link [PR #57](https://github.com/qa-p1/Arcade-Link/pull/57)
  merged** (f199e6a): the portal stand-in forgets a client that left the bus, as the real portal does (self-test
  proves it; every Link check green); not tagged yet, it goes into v1.0.7. The `box-standard` patches applied on
  Box main; local checks running before the PR.
- 2026-11-10 (session 3) — **Box PR #19's Island test is green on Hyprland** ([run 42750460847](https://github.com/qa-p1/Arcade-box/actions/runs/42750460847),
  43640ba): first show in 4.7 s, BR-2, BR-1, BR-0 XFAIL, 9 of 9 as expected. Cause (diagnosed with Fable 5.2's
  advice, owner rule): a race in the test, not Box. After the restart the test waited for "shortcut bound", which the
  portal stand-in already reported from the first Box's session (a Box that quits never closes it), so the press went
  only to that dead session before the new Box listened. The test now waits for the new Box's own
  `state=registered`; Box logs every step from `Activated` to the Island's WebView, and a miss prints box.log and
  portal.log. BR-0 now first proves typed keys and Return reach the Island (78f41f2), so its XFAIL cannot come from
  lost input. Link follow-up (next patch): the stand-in should drop a session whose owner left the bus.
- 2026-11-10 — **Handoff state.** Box PR #19 run 42578967289 attempt 2 (c5d1e98, harness Link cd380d6): Linux,
  Windows, macOS green; `desktop / hyprland` fails at "The shortcut opens the Island" after 30.3 s. Box binds the
  shortcut both times (portal stand-in log), but after the press there is **no WebKit process at all** (only
  `arcade-desktop --background` and its AppImage), so the Island's WebView was never created: either Box did not get
  or act on `Activated`, or `with_island`/`island_window` failed silently. Next: log the activation path in Box (or
  check the stand-in's Press return and `portal.log`) before touching timeouts again.
  Box's unpushed `box-standard` commits (Link runtime, crash reports, CLI-2, Linux identity, notices, SECURITY.md,
  Wasmtime 36 LTS, zip 9, cargo deny, Link v1.0.6 tag) are saved as patches in `dev/v1/handoff/box-standard/`
  (base 262565b, on PR #19's branch): after PR #19 merges, restart the Box branch from main and `git am` them.
- 2026-11-10 — **Owner rule (chat):** when something has failed after repeated attempts, ask a Fable model
  (medium effort) for advice or let it fix it, instead of retrying again; an exception to "use no subagents".
  First use: Tools PR #49's open-window memory gate (PSS 309 vs 281; rc.10 measured 252). CI on the 9th
  (07:30–07:46 UTC) failed in Box and Tools AppImage bundling during a GitHub release-download outage (504s,
  linuxdeploy); the re-runs bundled fine. Box PR #19 now builds on all three OSes; its Island test is running.
- 2026-11-09 (session 2) — **Link v1.0.6 tagged** (cd380d6) after PR #56 (stand-in registers shortcuts with
  Hyprland) and main's CI, Ecosystem e2e and Desktop harness passed; the self-test proves `hyprctl globalshortcuts`
  lists a bound shortcut and `hl.dsp.global` reaches the client. Box PR #19's Island test now binds on the harness
  and reaches the first show (test fixes: database under `ARCADE_HOME`, 30 s for the first WebView show). Tools
  now pins `tag = "v1.0.6"`; its full check is running before the crash-reports PR.
- 2026-11-09 (session 2) — **State for resuming.** Link main 8059160 (PR #55: seatd race, Nix download,
  portal `trigger_description`, lazy crash folder) green on CI, Ecosystem e2e and Desktop harness, but not tagged:
  Box's Island test then failed with "hyprland_binding_unavailable" because Box checks that Hyprland lists its
  portal shortcut, which only xdg-desktop-portal-hyprland made happen. The stand-in now registers bound shortcuts
  with Hyprland itself (Link branch 94dc587, `gshortcuts` helper; self-test covers it); Box PR #19 runs on it
  (fede6ae). Next: merge that into Link, tag **v1.0.6**, then Tools: pin Link `tag = "v1.0.6"` (now a rev),
  notices, PR (crash reports 50e5349 + cargo-deny over the workspace 85e46a0, Tools D19/D20), rc.11, Gates
  (`update-from: v1.0.0-rc.10`). Box: local branch `box-standard` (Link runtime, crash reports, CLI-2, Linux
  identity, notices incl. 142 native packages, SECURITY.md, Wasmtime 36 LTS, zip 9, cargo deny; Box D4/D5; all
  workspace tests pass) waits for PR #19 to merge, then moves to tag v1.0.6.
  Correction to Tools D20's context: Tools' cargo-deny job was green only because a root package checks just
  itself; with `--workspace` it found 10 advisories, now each accepted with a reason or fixed.
- 2026-11-09 (session 2) — **Correction: Tools is not ready to promote.** Wiring Box to Link's runtime showed
  Tools never calls `runtime::install_crash_reports` and has no crash-report view, though TOOLS.md requires
  "<App> crashed" with "Copy report" and "Open GitHub issue" (owner checklist: local crash reports). No exit gate
  checked it, so rc.10's green Gates did not cover it. Nothing was promoted (B1). Next: build it in Tools (with a
  gate), cut rc.11, run Gates, then continue Box; Box PR #19 and Link PR #54 (1.0.6) run meanwhile.
- 2026-11-09 (session 2) — Tools PR #48 (rc.10 docs) merged. **Box started:** spec and audit copied (Box D2); the
  behaviour lock pins every P0/P1 the tests can reach as a known bug that fails for the audit's own reason (Box D3):
  Island keys in Playwright, core findings through `Arcade` (downloader against a local HTTP server), the CLI, and a
  new Tier 1 job running the Island on headless Hyprland from the CI-built AppImage. Next: move Box onto Link 1.0.5
  and the app standard, then untangle and fix.
- 2026-11-09 (session 2) — **Tools `v1.0.0-rc.10`: every exit gate passed on the published files** (Gates run
  42544104046, 11 of 11 jobs), the self-update from rc.9 included (delta 8.9 of 94.5 MB, back in the background in
  65 s). Open-window PSS 252.0 against 281; cold start 388 ms, so D18's possible slowdown did not hold on CI. Tools'
  steps are done except promotion, which needs the owner's signing key (B1). Moving on to Box.
- 2026-11-09 (session 2) — The memory probe (PR #47) explained rc.6's and rc.9's open-window readings: on eight
  runners the gate's own command measured 3 of 8 at 298–308 MB and 5 at 257–261, and with `MALLOC_ARENA_MAX=2` all 8
  at 252.2–253.5. glibc gives a thread its own arena when the main one is contended, so how many WebKit made while the
  window opened depended on timing. Tools now caps arenas at two for itself and its WebKit processes (apps it starts
  do not inherit it; test fails without that). Perf compared before applying: show unchanged, first start faster,
  fewer wakeups, cold start possibly ~66 ms slower (overlapping samples; recorded in Tools D18 as a possible trade for
  the owner if it holds). Merged as 873eab1; `v1.0.0-rc.10` tagged.
- 2026-11-08 (session 2) — **Gates on Tools rc.9: every gate passed, the self-update included** (rc.7 updated
  itself to rc.9 with a delta of 8.5 of 94.5 MB, 9 %, and came back in the background after 67 s), **except the
  open-window memory**: 297.5 MB PSS against Tools' own cap of 281 (D10). With rc.6's 301.4 that is two of five Gates
  runs; 30 CI runs and three Gates runs measured 256–262. Not re-run to green (Tools D18): the memory probe (PR #47)
  measures the published file on eight runners, with and without `MALLOC_ARENA_MAX=2`, to find the cause.
- 2026-11-08 (session 2) — PR #46 merged (b6ac23f; its first CI run read a missed 150 ms hello in the tray test as
  a restart, which the PR also fixed). **Tools `v1.0.0-rc.9` published**, Release green. Gates started on rc.9 with
  `update-from: v1.0.0-rc.7`: the first run in which both sides of the self-update have D16.
- 2026-11-08 (session 2) — Tools rc.8's Release failed in the Linux bundle's resident check, so nothing was
  published. The diagnostics added after PR #42's one-off failure showed the cause: `--quit` sent 0.85 s after
  `--restart` reached a Tools still starting GTK/WebKit and gave up after Link's 150 ms hello window. The same applies
  to a person's `--quit`/`--restart`/`--status` after a (re)start; Tools D17 gives commands 2 s, with a CLI test
  (fake Tools answering hello after 600 ms) that fails at 150 ms. rc.9 next.
- 2026-11-08 (session 2) — **Tools `v1.0.0-rc.7` published** (f5b5ecc, PR #44). **Gates on rc.7: every job green**
  on the published files (budgets back at 255.8 MB open PSS), run without `update-from` since the installed rc.6
  decides without D16. On the published file rc.7 finds its own release and offers nothing, now by package hash.
  rc.8 comes from PR #45 (the self-update gate prints the update decision when it fails); Gates on rc.8 with
  `update-from: v1.0.0-rc.7` is the first run in which every gate can pass.
- 2026-11-08 (session 2) — Gates on Tools rc.6: the tray race is fixed and every gate passed except two. The
  self-update found a real bug: rc.5 saw rc.6 and offered nothing, because a self-installed Tools has no package
  hash and every rc is version `1.0.0`. Fixed in PR #44 with a regression test (Tools D16); since the old Tools
  decides, the gate needs rc.7 and rc.8. Open-window memory read 301 MB PSS once (budget 281; 34 other runs today
  256–262; rc.5 and rc.6 identical locally): unexplained, kept as an open item, budget unchanged.
- 2026-11-08 (session 2) — PR #43 merged (d7ad568); **Tools `v1.0.0-rc.6` published** from it, every Release job
  green on the first attempt (including the Linux bundle's resident check). Gates started on rc.6 with
  `previous: v0.4.6` and `update-from: v1.0.0-rc.5`, the first run that includes the self-update gate on a build
  with the D15 fixes.
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

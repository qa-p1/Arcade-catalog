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

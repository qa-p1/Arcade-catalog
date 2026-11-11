# Local handoff (2026-11-11, from the cloud session)

The owner continues this work in a local session. Everything below is pushed: every repo is on branch
`claude/tender-feynman-3vt7dg` with nothing unpushed. The plan, rules and log are unchanged: `PLAN.md`, `README.md`
(owner decisions win), `PROGRESS.md` (newest first, update after every finished step), `LOCAL.md` (owner-only items),
and each repo's `docs/v1/PROGRESS.md` and `DECISIONS.md`.

## Open PRs (all opened by the lead; merge only through the repo's workflows after every gate passes)

| PR | Head | State at hand-off | Next |
|---|---|---|---|
| [Link #61](https://github.com/qa-p1/Arcade-Link/pull/61) | 46400dd | CI and the push/PR e2e runs reported green (09:19 UTC). The real-fleet e2e runs only on `workflow_dispatch`; last dispatched run 42988304697 (head e6442e2) was RED with two causes, both outside Link (below). | Merge once the Lens fix is on Lens main, then dispatch Ecosystem e2e on Link main and the Desktop harness, then tag **v1.0.7** with "Tag a release" (Cargo version is already 1.0.7). |
| [Lens #16](https://github.com/qa-p1/Arcade-lens/pull/16) | a17197e | Check suites reported green (09:26 UTC). | Merge, so that Lens main builds report `0.4.2`, not `0.4.2-dev.<sha>` (Lens D6). |
| [Box #34](https://github.com/qa-p1/Arcade-box/pull/34) | 2dc7c5d | Check suites reported green (09:56 UTC). Confirm the Tier 1 Hyprland job shows BR-0 and BR-1 passing and BR-2 still XFAIL. | Merge, then continue Box step 3 (below). |

"Reported green" comes from GitHub check-suite events, not a fresh read; re-check each PR before merging.

## What was found and done today

1. **Tools "close under load" was a Link harness bug, not Tools.** `tools/fleet/wmclose.c` called `XFlush` and
   exited. Under CPU load the X server saw the request and the hang-up together and dropped the client unread, so
   the close was never delivered. An X protocol trace (xtrace) and an independent `xev` listener both confirmed it.
   Losses: 7 of 13 local runs before, 0 of 10 with `XSync` + `XCloseDisplay`. The fix is in Link #61 (CHANGELOG
   1.0.7). Tools PR #49 therefore needs no close fix; record that in Tools `docs/v1/DECISIONS.md` when you touch
   it.
2. **Real-fleet e2e (run 42988304697):** shortcuts 20/20, trayhost 27/27, tools-hub 39/42, install 15/16.
   - The three tools-hub failures are all Lens: its main builds were prereleases (`-dev.<sha>`), which Tools'
     stable channel correctly refuses. Fixed by Lens #16.
   - The install failure (`arcade.tools did not quit` after its install relaunch, endpoint pid still alive after
     `app.quit`) is **not yet explained**. My local probe (`peerquit`) was inconclusive: it looked for
     `*tools*.json` but the endpoint file is `arcade/run/arcade.tools.endpoint`, so the quit was never sent.
     Reproduce it locally first. The e2e sends `app.quit` over a raw Link connection whose hello claims client id
     `arcade.tools` (`tools/real_apps.py` `Peer`), after
     `--install --silent` with `APPIMAGE_EXTRACT_AND_RUN=1`.
3. **Box step 3** (all in #34, each with its lock test flipped, tested locally):
   - Core: B-7, B-8, B-9 (spans plus time zones), B-10, B-25, U-1, BR-15, BR-16, BR-4 (P0, search).
   - Island: BR-0 (P0), BR-5, BR-6, BR-11, BR-12.
   - Shortcut: BR-1.
   - Decisions D7 (converter readings) and D8 (fresh re-show; footer regex).

## Next steps, in plan order

1. Merge Lens #16, then Link #61, then e2e and harness on Link main, then tag Link v1.0.7.
2. **Tools PR #49:**
   - Move the Link pins from v1.0.6 to v1.0.7:
     - ci.yml lines 60, 292, 298, 303, 307
     - gates.yml lines 39, 96, 180, 223, 282, 288, 291, 295
     - memory-probe.yml line 51
     - nightly.yml lines 22, 26
     - promote.yml lines 15, 18
     - release.yml lines 150, 156
     - Cargo.toml line 24
     - crates/arcade-tools-overlay/Cargo.toml lines 12, 16
     - VENDORED Tag and Commit (both)
   - Regenerate Cargo.lock and the notices.
   - Explain the install-relaunch quit failure above.
   - Crash reports (TOOLS.md §Crash reports, still missing in rc.10).
   - Then CI green, merge, tag `v1.0.0-rc.11`, Release (test channel), and Gates with `update-from` rc.10.
3. **Box (after #34):**
   - BR-2: the Island's transparent area takes clicks on Hyprland. Box already calls GTK
     `input_shape_combine_region`, and `gtkwindow.c` 3.24.41 does not reset it. Find out under the Hyprland
     harness whether Hyprland honours the input region for focus and clicks; if not, resize the window to the card.
   - BR-3: GStreamer plugins (P0, packaging).
   - BR-7 (text/Markdown to PDF), BR-8 (engines list), BR-9 (Window Pin), CLI-2.
   - Then the remaining steps.
4. **Clipboard, Look, Find, Lens, Shelf, Wheel:** the stopped code-writing agents left uncommitted work. It is
   saved, unreviewed, as patches in `dev/v1/handoff/<repo>-uncommitted.patch`. Each applies to the repo's
   `claude/tender-feynman-3vt7dg` at the commit named below, with `git apply`. Review every change against the spec
   before committing; none of it has been tested.
   - Find @7653ec1: UI model, content search, a CLI search test, `tests/desktop/`.
   - Shelf @27cf9ec: Link `Service`.
   - Clipboard @ab746fa: overlay, history, controller, the Rust core and link store, the Linux lifecycle bridge.
   - Lens @a17197e: keys (D2), installer, overlay and annotate.
   - Look @4fe14c6: Cargo pin only.
5. Lens `release.yml` labels nightlies `-dev.<sha>`, but fleet nightly tags are `-nightly.<date>.<n>`. Check this
   against Tools' nightly channel in Lens step 4 (Lens PROGRESS).
6. Last: tick PLAN's owner-requests checklist with evidence links and write the final summary at the top of
   PROGRESS.md.

## Owner-only (unchanged; LOCAL.md)

- **B1:** set `ARCADE_UPDATE_SIGNING_KEY` (`arcade-link keygen --secret-to-gh`) and commit the public key to Tools.
  Until then no stable promotion is possible.
- **B2:** create `qa-p1/Arcade-template` from Link `template/`.

## Working rules carried over

- Test only with drafts and hidden `X.Y.Z-rc.N` prereleases. Promote byte for byte, only after every gate in PLAN.md
  passes on the published rc files.
- Never delete releases or tags, and never force-push main.
- A missing decision: choose what fits README.md, record it in that repo's DECISIONS.md, and continue.
- A Link change an app needs goes Link PR, then merge, then a Link patch tag through "Tag a release".

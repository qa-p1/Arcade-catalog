# Arcade 1.0.0 — master plan

On GitHub this folder is `qa-p1/Arcade-catalog` › `dev/v1/`. Paths below are relative to it.

**Outcome:** every Arcade app and Arcade Link ships a stable `1.0.0` (Link: `v1.0.0`). Each one has nothing known
broken, is untangled and free of dead code, has fast CI, stays within its memory and performance budgets, follows
`ARCADE_APP.md`, and was verified end to end from its published files before release.

Read in this order:
1. This file, all of it.
2. `README.md`, which records every owner decision. It wins over any spec if they disagree.
3. `PROGRESS.md`, which says where to continue.
4. The current app's spec in `specs/`, and the audit evidence it cites in `AUDIT/`.
5. The overhaul standard `../overhaul/STANDARD.md`, which still applies unless `README.md` or a spec says otherwise.

## Zero broken releases (the most important rule)

- **Nothing broken reaches users.** A stable release, whether `1.0.0`, a later patch or a nightly, is published only
  after every exit gate below has passed against the exact published test files. No exception, no "fix it in
  1.0.1", however long it takes.
- **Testing happens only on things users can't receive.** That means GitHub draft releases, and `X.Y.Z-rc.N`
  prereleases on the hidden `test` channel. Today's Tools ignores prereleases (it only follows `releases/latest`
  and the `nightly` tag), and Tools 1.0 never shows `test`. Make as many drafts and rc's as needed.
- **Stable is a byte-for-byte promotion of a verified rc.** It is never a rebuild.
- **When in doubt, don't ship.** If a gate is flaky, fix the flakiness, then re-run it on a fresh rc. A gate that
  "passed on retry" doesn't count until the cause is understood.
- **Don't break what users have now.** Every 1.0 release keeps publishing the `arcade-release.json` and asset names
  that the installed Tools 0.4.6 understands, so existing installs keep updating until they're on Tools 1.0.

## How the work runs

- **One session, one agent, no subagents.** Do everything yourself, one repo at a time, in this order:

  | # | Spec | Repo | Release |
  |---|---|---|---|
  | 1 | `specs/LINK.md` | `qa-p1/Arcade-Link` | `v1.0.0` tag + the app standard |
  | 2 | `specs/TOOLS.md` | `qa-p1/Arcade-tools` | Tools 1.0.0 (updater, nightly, signed manifests, chunk store) |
  | 3 | `specs/BOX.md` | `qa-p1/Arcade-box` | Box 1.0.0 |
  | 4 | `specs/CLIPBOARD.md` | `qa-p1/Arcade-clipboard` | Clipboard 1.0.0 desktop + Android APK + unsigned iOS IPA |
  | 5 | `specs/LOOK.md` | `qa-p1/Arcade-look` | Look 1.0.0 |
  | 6 | `specs/FIND.md` | `qa-p1/Arcade-Find` | Find 1.0.0 |
  | 7 | `specs/LENS.md` | `qa-p1/Arcade-lens` | Lens 1.0.0 |
  | 8 | `specs/SHELF.md` | `qa-p1/Arcade-Shelf` | Shelf 1.0.0 |
  | 9 | `specs/WHEEL.md` | `qa-p1/Arcade-wheel` | Wheel 1.0.0 |
  | 10 | `specs/FLEET.md` | all | fleet-wide final pass (all 1.0 apps together) |

  Finish and release one before starting the next. If a later app needs a Link change, open a Link PR, merge it,
  tag a Link patch release, then continue.
- **Full autonomy.** You merge your own PRs, cut rc releases, open cross-repo PRs and promote stable. Nobody reviews
  before release, so every check below is automated, and nothing is promoted until all of them pass.
- **Record progress after every step.** Update `PROGRESS.md` (in this folder; commit it straight to catalog main)
  after each finished step, and the repo's own `docs/v1/PROGRESS.md` for detail. After a context compaction, a usage
  pause or a new session, re-read this file and `PROGRESS.md`, then continue from the last recorded step. Never redo
  finished steps.
- **First step in each repo:** copy its spec to `docs/v1/SPEC.md` and the relevant audit files to `docs/v1/audit/`
  (text only, no images), so the repo carries its own brief.
- **Environment:** run `scripts/setup-env.sh` once per session. It is idempotent, and skips what's installed.

## The loop for each repo

Do these in order. Each one is a PR or a few, merged when green.

1. **Behaviour lock.** Write the tests that pin today's intended behaviour before changing anything: CLI, `--status`,
   Link messages, data formats, every audit finding as a failing regression test, and the fleet rules (Escape,
   popups, single instance). Tests for a known bug are marked expected-to-fail until step 3 fixes them.
2. **Untangle**, following the untangle-codebase skill (a copy is in `skills/untangle-codebase/SKILL.md`; the
   original is at github.com/caldoai/skills). The owner has already answered its step 1: do both extras. Do steps
   2–5 yourself, ignoring its "summarize with subagents" tip, because this plan uses no subagents (use the skeleton
   and dependency-graph scripts instead). The extras:
   - remove comments that only restate the code;
   - do the tests extra last: remove tests that would never catch a real bug, and fix tests that fail without one.

   Log every decision in `docs/v1/DECISIONS.md`. Move shared code to Link where `specs/LINK.md` says so.
3. **Fix** every finding in the spec, P0 first. Each fix comes with its regression test.
4. **Dead code.** Remove it with the language's own tools (`cargo machete`/`udeps`, `knip`/`ts-prune`,
   `flutter analyze` + `dart_code_metrics`, `clazy`/`-Wunused`). Keep only what is provably used, including by CI,
   packaging, Link entry points and other apps.
5. **Memory and performance.** Apply the spec's items from `AUDIT/memory.md` and meet the budgets in `README.md` and
   the spec.
6. **CI.** Meet the targets: PR under 8 minutes warm, release under 15, nightly or promotion under 5. Use the
   `ci.yml`, `release.yml`, `nightly.yml` and `promote.yml` shape from `specs/LINK.md` §CI. Every network step gets a
   timeout and a retry.
7. **Round 5 items** (`README.md`): data schema versions and migrations, security, LICENSE and notices,
   accessibility, the design pass, docs, clean uninstall, N-1 compatibility.
8. **Release** (below).

Commit in small, reviewable PRs, with conventional commit titles. Never force-push main.

## Exit gates: 1.0.0 ships only when all pass

- [ ] Every P0 and P1 finding is closed with a regression test that failed before the fix. P2 items are fixed or
      moved to `BACKLOG.md` with a reason, time-boxed to one day per app.
- [ ] `arcade-link conformance` passes: ARCADE_APP.md rules, Escape and popup rules, `--status` JSON, paths, logs,
      LICENSE and notices, and the desktop entry/identity.
- [ ] Budgets met in CI: background-idle memory (PSS), the app's share of the fleet budget, idle CPU ≈ 0% with
      bounded wakeups, cold start, show latency and disk use.
- [ ] The desktop end-to-end suite is green: Tier 1 headless Hyprland, plus Tier 2 smoke tests (sway, KWin, Mutter,
      X11) with no crash and no data loss. No coredumps during any test.
- [ ] Upgrade test: install the real previous release from its published files, populate data, update to the rc,
      and everything is kept. The Nightly → Stable downgrade path also works. Afterwards there is exactly one
      launcher and at most one login item for the app (fleet rule "One launcher per app").
- [ ] (Apps and Tools; not Link) A delta update from the previous release works through Tools, the signed manifest verifies, and a tampered
      chunk is rejected.
- [ ] N-1 test: the rc talks to the previous released versions of its peers over Link.
- [ ] `cargo deny`/`audit` (or the equivalent) is clean, `SECURITY.md` and `THIRD_PARTY_NOTICES` are present, and
      the licence check is green.
- [ ] Docs updated: README with current screenshots, in-app guide, and `CHANGELOG.md` (Keep a Changelog).
- [ ] Windows and macOS beta builds build and pass their CI smoke tests.

## Release

1. Bump to `1.0.0-rc.N`. Tag through the repo's "Tag a release" workflow, then run "Release" with
   `channel=test`. rc releases are GitHub prereleases on the hidden `test` channel, which Tools never offers.
2. Run every exit gate against the published rc files, never against a local build.
3. If anything fails, fix it, cut `rc.N+1`, and repeat. There's no limit on the number of rc's.
4. **Promote:** run "Promote" with the rc tag. It republishes the same bytes as `1.0.0` on the stable channel and
   signs the manifest, with no rebuild. Then verify the promoted assets match the rc's hashes, and that Tools offers
   the update.
5. Update `PROGRESS.md`, the catalog (`catalog.json` version and notes), and the repo's `docs/STATUS.md`.

Hotfix after 1.0.0: the same path, `1.0.1-rc.1` → promote, target under one hour. A bad release gets the catalog
`bad` flag, so Tools stops offering it and offers rollback.

## Fleet rules (every app, enforced by the conformance checker)

- Popups and overlays never close on pointer leave or a focus change. Only Escape, choosing an item, the shortcut
  again, or an explicit outside click close them.
- Escape goes back one step: a sub-view returns to its parent, a search with text clears it, a destructive dialog is
  cancelled, and only the top empty view closes. Footer hints say exactly what the keys do.
- `--status` prints one-line JSON and never opens UI. Unknown CLI arguments print usage and exit 2.
- Restart re-executes `$APPIMAGE` (or the installed launcher), never the inner binary of a mount (CB-4, TL-1).
- Data, config, cache and logs live only under `arcade/<app>` XDG paths. Legacy folders are migrated once and
  retired.
- **One launcher per app (owner request, 2026-11-11).** After any install, update or repair there is exactly one
  menu entry (`dev.arcade.<App>.desktop`) and at most one login item per app. Every older desktop id the app ever
  used is listed in its `legacy_desktop_ids` / `legacyDesktopIds`, and Link (≥ 1.0.7) retires entries under those
  ids, even when they run the installed file, carrying Start at login over. Root cause of the duplicates on the
  owner's desktop: Link ≤ 1.0.6 kept old-id entries that pointed at the same AppImage, so Box, Look, Shelf,
  Clipboard and Wheel each showed twice. Each app moves to Link ≥ 1.0.7 (Shelf and Wheel re-vendor `qt/`) and, in
  the same change, is removed from `LEGACY_PENDING` in Link `tools/e2e_checks/real_hub.py`, so its
  `*_update_retires_old_desktop_ids` e2e check must pass. Tools' rename from `app.arcadetools` to its OS id must
  pass the same check. A new rename adds the old id to the app's list and to `LEGACY_DESKTOP_IDS` there.
- Logs have levels, rotate, contain no secrets or clip contents, and drop known-harmless toolkit noise.
- Crash reports stay local. Tools offers "Copy report" and "Open GitHub issue" after the user reviews it.
- Child processes are always reaped (Lens LN-3).
- Nothing polls in the background without a reason. A timer only runs while its view is visible (Tools TL-8).

## Safety for the release machinery

- The chunked updater always falls back to a full download on any verification failure. Tools ships it first and
  must update itself with it twice (rc.N → rc.N+1 → 1.0.0) before any app depends on it.
- The signing private key exists only in GitHub Actions secrets (`ARCADE_UPDATE_SIGNING_KEY`). If the secret is
  missing, the promote job fails; it never publishes unsigned stable releases.
- Never delete published releases or tags. Superseded rc's stay as prereleases.
- Any destructive migration keeps a backup until the next successful start.

## When blocked

- If an external service or runner is down, retry with backoff, then continue with the next independent step and
  note it in `PROGRESS.md`.
- If the headless Hyprland harness can't be made to work within one day (`specs/LINK.md` §1), use the sway headless
  fallback for the compositor tests. Record which Hyprland-specific checks are not automated in `PROGRESS.md` and in
  that app's release notes. This is the only allowed reduction in the gates.
- If a decision is genuinely missing, choose the option most consistent with `README.md`, record it in
  `docs/v1/DECISIONS.md`, and carry on. Don't stop to ask.

## Owner requests checklist (verify each before the final summary)

The final summary in `PROGRESS.md` ticks each item with a link to its evidence (PR, CI run, release):
- [ ] Every repo is untangled with both extras, `DECISIONS.md` is committed, and dead code is removed.
- [ ] CI meets its targets (PR < 8 min, release < 15, nightly/promote < 5), built once and promoted.
- [ ] Every P0/P1 audit finding is fixed with a test; every P2 is fixed or in `BACKLOG.md`.
- [ ] Every Box tool runs once with a real input in CI.
- [ ] Clipboard's picker never closes on pointer leave or focus change (C0), and the fleet popup rule holds
      everywhere.
- [ ] Box: Escape in a tool returns to search (BR-0), and the Escape rule holds everywhere.
- [ ] The Nightly per-app switch in Tools works, with a badge, and switching back to Stable is safe.
- [ ] Delta updates through the shared chunk store work on every platform, with signed manifests and a full-download
      fallback.
- [ ] rc test releases were used for every app, and stable was promoted byte-for-byte.
- [ ] `ARCADE_APP.md`, the template repo, `arcade-link conformance` and the `/new-arcade-app` skill exist, and every
      app passes conformance.
- [ ] All apps together stay under 500 MB in the background (fleet CI job), and every per-app budget is met.
- [ ] Local crash reports, with "Copy report / Open GitHub issue" in Tools.
- [ ] Clipboard ships an Android APK (release-signed) and an unsigned iOS IPA, and desktop ↔ Android sync is tested.
- [ ] Linux Tier 1 (Hyprland) is fully verified, Tier 2 has passing smoke tests, and Windows and macOS beta builds
      ship.
- [ ] Round 5:
  - [ ] the done bar;
  - [ ] migrations and the safe downgrade;
  - [ ] signed updates;
  - [ ] the security pass, `SECURITY.md` and dependency audits;
  - [ ] LICENSE and notices;
  - [ ] DnD, hold, tray and multi-monitor tests;
  - [ ] performance budgets;
  - [ ] the design and accessibility pass;
  - [ ] N-1 compatibility;
  - [ ] hotfix flow and the `bad` flag;
  - [ ] docs;
  - [ ] clean uninstall.
- [ ] Shelf's hover panel never auto-closes. Clipboard retention plus storage budget works, and Private mode is always
      visible.
- [ ] One launcher per app: after upgrading the real 0.x fleet to 1.0, the app menu shows each app once and each
      starts once at login (fleet rule; Link `*_update_retires_old_desktop_ids` passes for all 8, `LEGACY_PENDING`
      empty).
- [ ] No feature was added beyond the plan; ideas went to `BACKLOG.md`.

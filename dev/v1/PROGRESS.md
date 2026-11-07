# Arcade 1.0.0 progress

Update this after every finished step (see `PLAN.md` §How the work runs). Newest entries go at the top of the log.
Detail lives in each repo's `docs/v1/PROGRESS.md`.

## Status

| # | Repo | Step (1 lock · 2 untangle · 3 fix · 4 dead code · 5 memory/perf · 6 CI · 7 Round 5 · 8 release) | Latest rc | Stable |
|---|---|---|---|---|
| 1 | Link | PR [#32](https://github.com/qa-p1/Arcade-Link/pull/32): release primitives, peer check, runtime, ARCADE_APP.md + conformance, reusable workflows, harness (CI pending) | — | — |
| 2 | Tools | not started | — | — |
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

- 2026-11-07 — Link: release primitives, protocol/peer check, shared runtime, QML dialog fix, ARCADE_APP.md and
  conformance checker, reusable release workflows and the Hyprland harness are on Link PR #32. Conformance baseline
  of the 8 released apps: `AUDIT/conformance-baseline.md`. Detail: Link `docs/v1/PROGRESS.md`.
- 2026-11-07 — Session 1 started. `setup-env.sh` run. Link step 0 done: brief copied to Link `docs/v1/`
  (branch `claude/tender-feynman-3vt7dg`). Blockers B1, B2 recorded.

# Prompt for the local session (2026-11-21)

Owner: open Claude Code on your PC with all Arcade repos cloned side by side (Arcade-catalog, Arcade-Link,
Arcade-tools, Arcade-clipboard, Arcade-Shelf, Arcade-wheel, Arcade-Find, Arcade-lens, Arcade-look). Pull each repo's
`main`, and in Arcade-catalog check out branch `claude/sharp-cori-29w5eg` (the handoff lives there). Then paste the
text below.

---

You are continuing the Arcade 1.0.0 plan from a cloud session. Everything from that session is on GitHub.

Read, in order, in Arcade-catalog on branch `claude/sharp-cori-29w5eg`: `dev/v1/README.md` (the owner's decisions;
they win), `dev/v1/PLAN.md`, then the top section of `dev/v1/HANDOFF.md` (the current state; it supersedes the
Status table in `PROGRESS.md`), then the newest entries of `dev/v1/PROGRESS.md`, then the `docs/v1/PROGRESS.md` and
`docs/v1/DECISIONS.md` of the repo you're working in.

**Leave Box out entirely.** The owner has their own plans for Arcade-box: don't read, change, tag, release or
comment on it, and don't count it as missing from the fleet.

Where things stand: Link v1.0.14; Tools, Find, Lens, Look, Shelf and Wheel are 1.0.0 stable and verified. Clipboard
is the one app left: `v1.0.0-rc.2` failed Gates on two things, both described in HANDOFF.md:
1. Clipboard's own CLI contract: an unknown flag must exit 2 with the usage on stderr, and `--arcade-manifest` must
   print the manifest and exit 0 when no display is available. Reproduce it on the published rc.2 AppImage before
   you change anything.
2. Tools' delta gate demands the delta fetch less than half the file; Clipboard's fetched 50.2%. Align the gate with
   Tools' own rule (owner's decision in Tools #54) in Tools 1.0.1, and record it in Tools' DECISIONS.md.

Then cut Clipboard rc.3, run Gates on the published rc (previous v0.3.2), and promote only when every job is green.
That includes the upgrade test and both desktop suites, which have not yet run against a published Clipboard rc.
Verify 1.0.0 byte for byte against the rc and update the docs. HANDOFF.md has the exact steps. After Clipboard, do
Tools 1.0.1's second item (the quit race) if there is time.

Rules (the owner's):
- Rule zero: never release anything broken. rc → Gates on the published rc → Promote byte for byte → verify.
- Merge only when every check on the PR head is green. Apps: merge commit with the expected head SHA. Link: squash.
- At most one re-run per job. A flake is not a root cause. Never skip, disable or loosen a test just to get green.
- Never force-push, except `--force-with-lease` to restart a branch whose history is already merged. Never delete
  releases or tags.
- Commit as `git -c user.name=Claude -c user.email=noreply@anthropic.com commit`. No trailers anywhere: no
  Co-Authored-By, no session links, no "Generated with" lines in commits, PRs or comments.
- Clippy with the repo's pinned toolchain and `-D warnings` before every Rust push (Clipboard: 1.98.1).
- At most 3 apps in flight at once. Use subagents only for concrete, well-specified jobs, and check their output.
- When a decision is missing, choose what fits README.md best, write it in the repo's `docs/v1/DECISIONS.md`, and
  continue. Explain things to the owner plainly and simply.
- Update the repo's `docs/v1/PROGRESS.md` and the catalog `dev/v1/PROGRESS.md` after each finished step.

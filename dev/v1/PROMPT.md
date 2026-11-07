# The one prompt for the cloud session

Owner: start one Claude Code cloud session on Opus 5.5 at high effort, with these repos attached:
- Arcade-catalog
- Arcade-Link
- Arcade-tools
- Arcade-box
- Arcade-clipboard
- Arcade-look
- Arcade-Find
- Arcade-lens
- Arcade-Shelf
- Arcade-wheel

Then paste the text below.

---

You are carrying out the Arcade 1.0.0 plan, start to finish, on your own.

The plan is in the Arcade-catalog repo at `dev/v1/`. Read `dev/v1/PLAN.md` first, then `dev/v1/README.md` (the
owner's decisions; they win over everything else), then `dev/v1/PROGRESS.md`. Continue from the last step recorded
there. If nothing is recorded yet, begin with `specs/LINK.md`. Run `dev/v1/scripts/setup-env.sh` once at the start of
this session.

Rule zero: never release anything broken. Test only with GitHub draft releases and hidden `X.Y.Z-rc.N`
prereleases (as many as needed). Promote to stable byte-for-byte only after every exit gate in PLAN.md passes
against the published rc files, however long that takes.

Rules:
- Do all the work yourself, one repo at a time, in the order in PLAN.md. Use no subagents.
- You may merge your own PRs, publish rc test releases, open PRs on other repos and promote stable releases, but only
  through each repo's workflows and only after every exit gate in PLAN.md passes against the published files.
  Nothing ships unverified, however long it takes.
- Update `dev/v1/PROGRESS.md` after every finished step, so the work can resume after a pause, a compaction or a new
  session.
- Don't stop to ask questions. When a decision is missing, choose what fits README.md best, record it in the repo's
  `docs/v1/DECISIONS.md`, and continue.
- Never delete releases or tags, and never force-push main.
- When all nine are released as 1.0.0 and `specs/FLEET.md` passes, tick PLAN.md's "Owner requests checklist" with evidence links and write a final summary at the top of `dev/v1/PROGRESS.md`: versions, links,
  and anything moved to BACKLOG.md.

# Spec 10: Fleet finish (all 1.0 apps together)

**Outcome:** the nine 1.0 releases are proven together as one product. Fix anything found with a patch release
through the same rc → promote path.

1. **Fleet memory and performance job** (`specs/LINK.md` §1.5 and §2b), run on the published 1.0 files:
   - all 8 in the background: under 500 MB RSS and PSS in total, with every per-app budget met;
   - one window open: within the budgets in `README.md`;
   - idle CPU ≈ 0% for every app.
2. **Fleet end to end:**
   - Install everything from scratch through Tools on a fresh HOME, then use one real cross-app flow per Link
     action: Box → Lens capture, Look → actions to Box, Clipboard and Shelf, Find → Look preview, Wheel actions.
   - Upgrade from the full 0.x fleet (the real released files) to the 1.0 fleet, and keep all data.
   - Uninstall everything, and nothing is left behind.
3. **Design pass:**
   - Capture the same states (empty, list, settings, error, light and dark) for all 8 apps under the harness and
     put them side by side in `dev/v1/fleet-screens/`.
   - Fix drift in fonts, icons, spacing, colours or error wording against the Link design kit (patch releases).
4. **Accessibility pass:** keyboard-only use of each app's main flow, visible focus, contrast check, 150% scaling.
5. **Docs:**
   - The catalog page lists 1.0 for every app.
   - `dev/v1/README.md` gets a "Shipped" note.
   - `BACKLOG.md` collects every deferred idea.
6. **Owner requests checklist:** tick every item in `PLAN.md` with evidence links, and write the final summary in
   `PROGRESS.md`.

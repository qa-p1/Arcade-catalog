# Arcade 1.0.0

Every Arcade app ships 1.0.0: untangled, without dead code, with fast CI, with nothing known broken, and polished.
This folder holds the plan. Each spec is self-contained, so the single Claude Code cloud session can run it cold after any compaction or restart.

Starting point (2026-11-06): Tools 0.4.6, Box 0.4.3, Look 0.4.3, Find 0.5.4, Lens 0.4.2, Clipboard 0.3.2,
Shelf 0.4.0, Wheel 0.5.0, all released, verified and installed. Link is on 0.4.15.
The previous plan, `../ARCADE_OVERHAUL/` (README decisions and STANDARD.md), still applies unless this plan says otherwise.

## Decisions (owner, 2026-11-06)

- **Untangle every repo** with the untangle-codebase skill
  (github.com/caldoai/skills/blob/main/skills/untangle-codebase/SKILL.md), including both extras:
  - **Comments:** remove comments that only restate the code.
  - **Tests:** remove tests that wouldn't catch a real bug, and fix the ones that fail without one. This is done last.
- **Shared code moves into Arcade Link.** Install and desktop integration, child-process launch and restart (environment
  sanitizing), single instance, and tray hosting are written once in Link. The Rust apps and Clipboard's Rust core use them.
  Shelf and Wheel (C++) keep their own implementations but must pass the same contract tests.
- **Each app ships 1.0.0 when ready.** It needs every exit gate green, including the automated real-desktop checks (headless Hyprland). The owner doesn't have to be present.
  Order: Link, Tools, then the apps.
- **The broken list comes from a local real-use audit** of all eight installed apps, done before the specs are written.
  Evidence goes in `AUDIT/`.

- **Nightly is a per-app switch in Tools.** Setting an app to Nightly replaces its stable install and shows a
  "Nightly" badge. Nightly builds from main on a schedule, is skipped when nothing changed, and promotes main CI's
  already-tested files. Switching back to Stable installs the newest stable even when its version is lower.
- **Updates download only the changed pieces, on every platform, from one shared piece store.** Tools downloads only
  missing content-defined chunks (with HTTP Range requests against GitHub release assets) for every app and for itself.
  Linux AppImages work as they are. macOS and Windows ship an uncompressed app archive next to the installer so
  chunking works there too. One chunk store is shared across apps. Any verification failure falls back to a full
  download. Measured savings are in `RESEARCH.md`.
- **CI targets:** PR checks under 8 minutes with warm caches, a full stable release under 15 minutes, and nightly or
  rc-to-stable promotion under 5 minutes (nothing is rebuilt). The approach follows T3 Code: build once and promote the
  same bytes, cache compiled dependencies, shard tests, skip the scheduled nightly when nothing changed, and put a
  timeout on every network step.
- **Test releases before 1.0.0.** The implementing agent may publish any number of `X.Y.Z-rc.N` prereleases on a hidden
  `test` channel that Tools never offers. An rc is verified by installing from the published files, a delta update from
  the previous release, smoke tests on every platform, and the owner's real-desktop check. Stable `1.0.0` is then
  promoted from that exact rc's files, byte for byte, with no rebuild. Nothing ships until it is verified, however long
  that takes.
- **The Arcade app standard has four parts and lives in Arcade Link:**
  - `ARCADE_APP.md`: short, normative must-haves.
  - A GitHub template repo that already builds, tests, releases and passes conformance.
  - An automatic conformance checker in the Link CLI that every app's CI runs.
  - A `/new-arcade-app` Claude Code skill that goes from a vague idea to a released app with the template and checker.

  The existing apps move onto the same structure during v1, so they become the reference examples. This replaces
  `NEW_APP_SPEC.md`, keeping its content.
- **Popups never close on their own.** A popup or overlay closes only on Escape, choosing an item, its shortcut again,
  or an explicit outside click. Never because the pointer left it. This is fleet-wide and is a conformance check.
  Clipboard's picker (C0) currently breaks it.

- **Platforms:** Linux is first-class and fully verified for 1.0.0. Windows and macOS builds keep shipping, labelled
  beta, unsigned and tested in CI only. Signing and notarization come later.
- **Size:** installs stay self-contained AppImages. The shared chunk store removes duplicate downloads, and Box gets
  packaged like the other Tauri apps (today it shares almost nothing with them).
- **Crashes and errors:** every app writes crash and error reports locally, with nothing sent anywhere. Tools shows
  "<App> crashed", plus "Copy report" and "Open GitHub issue", which pre-fills an issue only after the owner reviews it.
  Logs have levels and drop known-harmless toolkit noise.
- **Scope:** polish, plus fixing everything wrong that the audit or the implementing agents find, plus the Clipboard
  picker fix (C0). No new features. Feature ideas go to `BACKLOG.md` for after 1.0.0.

- **Mobile is in.** Clipboard Android and iOS get the same audit, untangle and polish. The Android APK ships with 1.0.0
  as normal. iOS ships an unsigned IPA in the release, which the owner sideloads with 3uTools after v1 is out.
  Desktop to mobile sync must work end to end.
- **One cloud session, one agent, no subagents.** The owner starts a single Claude Code cloud session on Opus 5.5 at
  high effort, with every Arcade repo attached and one prompt. That one agent does all the work itself, in order:
  Link, then Tools, then each app one at a time (Box, Clipboard, Look, Find, Lens, Shelf, Wheel). It finishes and
  releases one before starting the next. No subagents.
- **Full autonomy.** Cloud sessions merge their own PRs, publish rc test releases, open PRs on other repos when they
  find a contract bug, and promote stable 1.0.0 themselves. Nobody checks on the owner's desktop before release, so
  every real-desktop check has to be automated in CI. That includes a headless Hyprland session for compositor-specific
  behaviour (Box Island as a floating layer, tray, global shortcuts, popups not closing on pointer leave), alongside
  Xvfb and private D-Bus.
- **Where the plan lives:** a master `PLAN.md` and one `PROGRESS.md` live in Arcade-catalog `dev/v1/`, together with
  this README, RESEARCH and the audit. Each repo also carries its own self-contained `docs/v1/SPEC.md`, so the agent can
  focus on one app at a time. The single session updates `PROGRESS.md` after every step, so after a context
  compaction, a usage-limit pause or a new session it continues from the last recorded step.

- **Escape goes back one step; it never closes everything at once** (owner, 2026-11-06). Inside a tool or sub-view,
  Escape returns to the previous view (in Box: from a tool back to the Island's search). In a search with text it
  clears the text. Only on the top-level empty view does it close. A running job keeps going and stays reachable.
  Footer hints always match what the key really does. This applies fleet-wide and is a conformance check (Box BR-0).

- **Memory: the whole fleet stays under 500 MB** (owner, 2026-11-06). All Arcade apps running together, every process
  tree summed (including WebKit and helper children), use under 500 MB in normal use. Today it's about 800 MB or more.
  UX must not get worse: open latency stays the same and no feature is lost. Every app gets a background-idle budget,
  and CI measures fleet-total PSS with all apps running. The details come from `AUDIT/memory.md`.

## Round 5 decisions (owner, 2026-11-06): open-source v1 standard, doable without destabilizing the ecosystem

- **Each app has a measurable "done" bar.** 1.0.0 ships only when every gate passes:
  - every P0/P1 audit finding is closed with a regression test that fails before the fix;
  - the Link conformance checker is green;
  - memory, idle CPU and wakeups, cold start, show latency and disk use are within budget;
  - the automated desktop tests show zero crashes and zero coredumps;
  - an upgrade from the real released 0.x install (installed from published files) keeps all data and settings;
  - the delta update from the previous release works;
  - docs and the changelog are updated.

  P2 polish is time-boxed per app. Anything left over goes to `BACKLOG.md`, and that never blocks the release.
- **Data safety and migrations.**
  - Every settings and data file carries a schema version, with forward migrations tested from each released 0.x.
  - A downgrade never silently breaks data. Switching Nightly → Stable (a lower version) takes a backup first. Stable
    either reads the newer data (unknown fields are kept) or restores the backup taken at the switch, and tells the user.
  - The single-copy rule from the overhaul still applies.
- **Signed updates.** Every release publishes a manifest of file hashes and chunk lists, signed with ed25519
  (minisign-compatible).
  - The public key is built into Tools, and Tools refuses any file or chunk that the signed manifest doesn't cover.
  - The private key lives only in GitHub Actions secrets. Tools accepts a current and a next key, so the key can be
    rotated.
  - The GitHub release SHA-256 alone is no longer trusted.
- **Desktop support tiers (Linux):**
  - **Tier 1, fully verified and release-blocking:** Hyprland (headless Hyprland in CI, plus the owner's machine).
  - **Tier 2, works with documented limits:** KDE Plasma, GNOME and Sway on Wayland, plus X11 sessions.
    - CI smoke tests on each start every app, show its window, and check tray/fallback and the CLI:
      sway headless, `kwin_wayland --virtual`, `mutter --headless`, and Xvfb.
    - Where a desktop lacks a feature, the app explains the limitation in Settings and keeps working. Example: GNOME
      has no layer-shell or global-shortcuts portal everywhere.
    - A Tier 2 failure blocks the release only when it's a crash or data loss.
  - Windows and macOS stay beta, as decided earlier.
- **Security pass on every risky surface,** with findings fixed or listed in `SECURITY.md`:
  - Clipboard pairing, sync crypto and relay;
  - Box plugins and the downloader (URL and argument handling);
  - Lens secrets (LN-8);
  - Link IPC: sockets stay 0600 in a 0700 directory, and a peer-UID check is added;
  - update and chunk verification.
  - Every repo gets `SECURITY.md`, `cargo-deny` or `cargo audit` (with flutter/pub and Qt equivalents) in CI, and
    Dependabot or Renovate for dependencies and GitHub Actions.
- **Licences and notices.** Every repo has a LICENSE (Tools and the C++ repos currently lack one).
  - Every app ships a generated `THIRD_PARTY_NOTICES` covering bundled WebKitGTK, GStreamer, Qt (LGPL, with
    relinking info), ffmpeg, tesseract, fonts and crates/pub packages. It's shown in About.
  - CI fails when a dependency has an unknown or incompatible licence.
- **Automated coverage for what the audit couldn't drive:** drag and drop in and out (Shelf, Find, Box), Wheel's
  physical hold and release, tray Quit/Restart/Quit-all, and multi-monitor placement. This runs in the headless
  desktop harness, with synthetic input at the protocol level.
- **Performance budgets in CI** next to memory:
  - idle CPU ≈ 0% and wakeups per second bounded, in the background and with a window open on its default page;
  - cold start and show latency;
  - disk use: the installer cache is bounded (TL-7).
- **One design pass across the fleet.** The same states (empty, list, settings, error, light and dark) are captured
  for all 8 apps and compared side by side: fonts, icons, spacing, colours and error wording come from the Link
  design kit. It looks and behaves like one product.
- **Accessibility basics.** Everything is reachable by keyboard, focus is visible, text and controls meet WCAG AA
  contrast, layouts work at 125–150% scaling, and reduced motion is respected. Accessibility-bus warnings are fixed
  rather than silenced where the toolkit allows.
- **Mixed versions keep working.** The Link protocol carries a version. Every release is tested against the previous
  released version of its peers (N-1 ↔ N), because apps ship one at a time.
- **After the release:**
  - GitHub issue and PR templates, plus labels;
  - `CONTRIBUTING.md`;
  - a 1.0.x hotfix flow through the same rc → promote path, under one hour;
  - a "bad release" flag in the catalog, so Tools stops offering a release and offers rollback.
- **Docs current at 1.0.** In-app guides (TL-12), each repo's README with screenshots, the catalog page and the
  CHANGELOG (Keep a Changelog format) all describe 1.0.0.
- **Clean uninstall.** Uninstalling an app through Tools removes its files, autostart entry, launcher entry, caches
  and Link registration. "Remove data too" is a separate, explicit choice. A fresh-HOME test proves nothing is left.
- **Final gate is automatic.** The agent promotes stable once every gate passes; the owner doesn't have to be present.
  The hotfix flow covers anything found afterwards.
- **Shelf:** a docked panel opened by hover never collapses by itself. It closes only on Escape, the shortcut, the
  tab or an explicit outside click (SH-8 and RD-SHELF-1 follow the fleet popup rule with no exception).
- **Clipboard history retention is the user's choice.**
  - Keep history for a chosen time (including Forever) and within a storage budget the user sets.
  - When stored history exceeds the budget, the oldest unpinned clips are removed automatically. Settings shows the
    space used.
  - Pinned clips are never removed automatically.
  - The default is Forever within a 256 MB budget.
- **Clipboard Private mode is always visible.** While it's on, the tray icon, the History header and the picker show
  it, so it can never be on without the user knowing. The owner's real install was found with Private mode on and
  nothing captured since 19:13, cause unknown. The spec checks every path that can turn it on.

- **Memory result** (`AUDIT/memory.md`, verified 2026-11-07):
  - **Today:** 1196 MB RSS / 767 MB PSS for the real fleet, AppImage helpers included.
  - **All 8 apps in the background:** with the UX-neutral items (U1 unpacked runtime, W0 and W1 trims, WH1 Wheel
    software renderer, CB1a, W3b), about **427 RSS / 313 PSS**: under 500 on both measures, with no UX loss.
  - **With one window open:** a non-WebKit window gives about 440/325. With a WebKit window open (Tools, Box or
    Look) and OPEN1, PSS is about 465–502 and RSS about 650. That RSS can't reach 500 without a visible trade-off:
    compositing off, or Clipboard opening cold. Under the "UX must not get worse" rule the plan uses the UX-neutral
    set, and the open-window CI budget is PSS ≤ 500 / RSS ≤ 680.
  - **Optional, owner's call:** CB1b, moving Clipboard's engine out of the always-running process. That's −90/−74,
    and the first open after idle takes 0.1–0.15 s longer unless kept warm.

## Every spec contains

1. Verified broken features: the audit findings for that app, with how to reproduce each one.
2. Untangle: the skill's steps 2 to 5, with the decision log committed as `docs/v1/DECISIONS.md` in the repo.
3. Dead code: removal using the language's own tools, keeping only what is provably used, including CI, packaging and Link entry points.
4. CI: speed targets and the known bottlenecks.
5. Polish: the owner's list.
6. Behaviour lock: tests written before refactoring, so the intended behaviour is unchanged at the end.
7. Release 1.0.0: version bump, changelog, tag, and stable release through the repo's own workflows.
8. Done bar: the exit gates above, with the app's budgets (memory, CPU, start and show latency, disk).
9. Data: schema versions, migrations from every released 0.x, and the downgrade rule.
10. Security, licences and notices, dependency audit.
11. Desktop tiers: Tier 1 verification, and Tier 2 smoke tests with documented limits.
12. Design and accessibility pass, docs, clean uninstall, N-1 compatibility.

## Order

Link → Tools → Box → Clipboard → Look → Find → Lens → Shelf → Wheel → Fleet finish (`specs/FLEET.md`)

# Arcade everywhere: takeover prompt (stage 5 onward, on the owner's computer)

Paste everything in the block below into Claude Code on your own computer, in an empty folder. It stands alone.

```text
You are taking over the "Arcade everywhere" plan for the Arcade apps (GitHub owner: qa-p1) on the owner's own
computer. A cloud session did stages 1-4 and 6, most of 7, and stopped at stage 5 because it needs this computer
(GitHub chores with the owner's login, the Mozilla signing key, and the Zen browser). You continue from here to the
end. Work in plain, simple words with the owner. Never ask the owner to paste a secret into the chat.

== Where things are ==
Repos (github.com/qa-p1/...): Arcade-Link (the shared library: protocol, offers, helper, design kit, test runner),
Arcade-tools (the hub app; ships the Arcade helper), Arcade-box, Arcade-lens, Arcade-look, Arcade-Find, Arcade-Shelf,
Arcade-wheel, Arcade-clipboard (apps), Arcade-catalog (catalog.json, plans, reports). New at stage 5: Arcade-browser.
The plan: Arcade-catalog/dev/everywhere/PLAN.md (read sections 4.7, 5 and 6 first). The four small prompts this one
includes are in Arcade-catalog/dev/everywhere/LOCAL-PROMPTS.md (A, B, C, D); they are summarised below, follow the
file's exact text when you run them. Clone what you need with `gh repo clone qa-p1/<repo>`.

== Rules (the owner's, all of them hold) ==
1. Commits: `git -c user.name=Claude -c user.email=noreply@anthropic.com commit`. No Co-Authored-By, no session
   links, no "Generated with" lines or footers in commits, PR bodies or comments.
2. Work on a branch and open a PR; never push to main. Never force-push (except --force-with-lease when the remote
   holds only already-merged history).
3. Merge only when every check on the PR's head is green. App repos: merge commit with the head SHA pinned
   (`gh pr merge N --merge --match-head-commit $(git rev-parse HEAD)`; always take the SHA from git rev-parse, never
   type it). Arcade-Link and Arcade-catalog: squash.
4. A failing job gets at most one re-run, and only when the log shows it never ran or the infrastructure failed
   (e.g. a macOS job with 0 steps, no runner name and the annotation "The job was not acquired by Runner of type
   hosted even after multiple attempts" with "Due to capacity constraints, jobs targeting macOS arm64 runners may
   experience longer queue times": GitHub had too few Apple Silicon Macs on 2026-11-23; read the job's annotations
   with `gh api repos/qa-p1/<repo>/check-runs/<job id>/annotations`). If the re-run is starved too, wait and push the
   next real change; never an empty commit. "Flake" is not a root cause: find the cause. Never skip,
   quarantine or loosen a test to get green.
5. At most 3 app repos in flight at once. Don't spawn sub-agents.
6. Every app release: tag `vX.Y.Z-rc.N` via the repo's tag.yml workflow (inputs tag, sha; run on main;
   `git push` of tags is refused) → the Release run on that tag → gates.yml on the rc tag (input `previous` = the
   previous stable tag; Tools also takes `update-from` = an earlier rc on the test channel) → promote.yml on main
   (input `rc-tag`) → check the stable release is byte-for-byte the rc: AppImage, dmg, setup.exe and SHA256SUMS.txt
   identical; arcade-release.json and manifest.json differ only in channel, tag and notes link; manifest.json.sig
   only in stable → a docs PR (CHANGELOG section dated, docs/v1/PROGRESS.md entry with the run links).
7. Secrets only through `gh secret set NAME --repo ...` typed by the owner in the terminal prompt. The owner's email
   is private: never put it in commits, URLs or requests.
8. Keep disk use sane: don't repeatedly fill and clean the disk; delete a build folder once when it's no longer needed.

== State when the cloud session stopped (2026-11-23) ==
Stable releases: Link v1.1.1 (tag), Tools 1.1.1, Box 1.0.0, Lens 1.1.0, Look 1.1.0, Wheel 1.1.0, Shelf 1.1.0,
Find 1.1.0, Clipboard 1.1.0, all promoted from their rc and checked byte for byte (Find 1.1.0 without its macOS
gate: see "Still open"). Confirm with `gh release view --repo qa-p1/<repo>` before you start.
What works today: every app's actions are on its Link 1.1 card (surfaces, ranks, one-click, limits); every app's own
"other apps" list comes from Link's shared offers (catalog rules + the user's pins/hides/defaults); Tools 1.1 ships
the Arcade helper: file manager menus on Linux (Open With + Files, Caja, Dolphin, Nemo, Thunar), Windows (Explorer,
"Show more options" on 11) and macOS (Finder Quick Actions + Services, Tools 1.1.1), and an Everywhere page (pins,
output folder, a default per job). Not yet: the browser extension (stage 5).
STATUS.md files are current in every repo; each app README has a "Use it from anywhere" section that says the
browser extension "comes in a later update" or "will offer ... when it ships": update those sentences when it ships.

== Step 1: GitHub chores and the Zen check (LOCAL-PROMPTS.md prompts A and B) ==
A: (1) delete the 12 merged `claude/sharp-cori-29w5eg-wip-*` branches listed in prompt A after checking each is
fully in main; nothing else. (2) Add the "Update to Arcade Lens 1.0.0 or later" note at the top of Arcade-lens
releases v0.4.1 and v0.4.2. (3) Create the empty repo qa-p1/Arcade-browser (same visibility as Arcade-Link,
Dependabot alerts on). (4) The owner creates Mozilla AMO API credentials on the website, then types them into
`gh secret set AMO_JWT_ISSUER --repo qa-p1/Arcade-browser` and `gh secret set AMO_JWT_SECRET --repo qa-p1/Arcade-browser`.
B: find by testing (a probe native-messaging host and a temporary add-on) exactly which folder or registry key the
owner's Zen reads native messaging host manifests from; clean up everything. Report both before going on.

== Step 2: stage 5, the browser extension 1.0.0 (PLAN.md 4.7, stage 5) ==
1. Arcade-browser (PLAN.md 4.7 is the spec; this is the full list, build all of it):
   Base: one TypeScript codebase, no framework, two builds: Chromium-family MV3 (Chrome, Edge, Brave, Vivaldi, Opera;
   service worker; a fixed `key` so the extension ID is the same wherever it is unpacked) and Firefox-family MV3
   (Firefox, Zen and other forks; background script). The design kit's tokens from Arcade-Link, light and dark.
   The extension knows NO app's actions: every item it shows is an offer the Arcade helper returns over native
   messaging (`dev.arcade.helper`) for what the user is pointing at, using the user's pins/hides/defaults and the
   catalog rules. A new app or action appears without an extension update.
   Surfaces:
   a. Right-click menus on: an image, a link, a video or audio element, selected text, the page itself, and a PDF.
      Grouped as the offers say ("Arcade ▸ Convert ▸ ..."), pinned/default actions first, "More..." opens the popup.
   b. On-page buttons:
      - Under every YouTube video: a Download button with the full form from Box's downloader card (video/audio,
        quality, format, subtitles), remembering the last choice; plus Transcript, Thumbnail and Audio only as
        offers. The same button on the other sites Box's downloader supports, where the page has a video element.
      - On images: a small hover button (a setting, on by default) with the image offers.
      - Where buttons go on each site (CSS selectors) is data in catalog.json `browser.sites`, never code, so a
        site layout change is fixed in the catalog without an extension release (MV3 forbids remote code; selector
        data is allowed).
   c. Toolbar popup = the Island in the browser: search every action of every installed app, including actions
      with no input (calculator, units, currency, time zones, dates, colour, password, UUID, QR for this page's URL,
      IP, WHOIS for this site, site check, ...); each action's options form is drawn from its card's data; recent
      jobs with live progress, cancel, and open/reveal the result.
   d. Live results on selected text: when the selection looks like an amount, quantity, time or date, the menu
      title shows the answer from Box's converters ("12 USD ≈ ₹1,002", "5 mi = 8.05 km") within 150 ms, otherwise
      a plain entry.
   e. Finished downloads: a notification "Downloaded report.pdf · Compress · OCR · Open in Look" from the offers
      for that file (a setting, on by default).
   f. Send to my devices: on links, images, selections and the page URL, listing the user's devices from Clipboard
      (`clipboard.devices`), greyed out with the reason past Clipboard's limits (16 MB, 32 files).
   g. Not connected: "Install Arcade Tools to connect" with a link; an app that isn't installed shows
      "Install Arcade X" (Tools' request_install).
   h. Settings page: hover button on/off, download notifications on/off, connection status and a "Test connection".
   What the user must find there, per app (PLAN.md 4.8; it comes from the cards, check every line in the e2e):
   - Box: media download (video, audio, formats, subtitles), transcript, thumbnail, all images on the page, direct
     file download, page to PDF or screenshot, page to text/Markdown, site check, WHOIS, QR for the page; every image
     tool on any web image (fetched to a handoff file first: convert, resize, compress, crop, remove background,
     upscale, palette, ...); text tools on selections (clean, case, statistics, diff, JSON format, JWT, regex, hash,
     encode/decode, URL inspect, text to speech, QR); the live converters; the no-input tools and saved pipelines
     in the popup; screen tools listed as "Open in Box".
   - Lens: Read text, Scan QR/barcode, Pick colours, Find links/emails/phone numbers/dates/addresses and its other
     recognizers and chains on web images; Pin on screen.
   - Look: Preview a link or a downloaded file; Inspect.
   - Find: "Search my files for this" on selected text.
   - Shelf: "Keep on Shelf" for links, images, text and the page.
   - Clipboard: "Copy to Arcade Clipboard" and "Send to my devices ▸ <device>".
   - Wheel: "Add to Wheel" on any offer.
   - Tools: "Install Arcade X", engine hints ("Install FFmpeg").
   Tests (PLAN.md section 5.6), all in CI on every PR, each written to fail first:
   - Chromium: Playwright with the unpacked extension (headed under Xvfb), the real helper and real app packages;
     menus through the extension's own handlers (Playwright can't click browser menus); the YouTube button against a
     local YouTube-like page (CI gets "confirm you're not a bot" from real YouTube); downloads from a local server;
     the 150 ms live-result budget measured.
   - Firefox: Selenium + geckodriver with the add-on installed as temporary, the same scenarios.
   - Native messaging end to end through the real host files the helper writes, for both families.
   Distribution: the release workflow attaches Arcade-browser-chromium-<v>.zip and Arcade-browser-firefox-<v>.xpi,
   signed (unlisted) with `web-ext sign` using the AMO_JWT_ISSUER / AMO_JWT_SECRET secrets from step 1; rc → test
   → stable like the apps. Tools' Everywhere page shows the install steps, opens the right page in the right
   browser, and shows "Connected" once the extension pings the helper.
2. Arcade-catalog: `browser.sites` for YouTube and the downloader's other sites (squash PR, schema + validate.py).
3. Arcade-Link: add Zen's folder from step 1 B to the helper's host-file writer (Link patch release v1.1.2 after its
   CI and real-fleet e2e), then Tools picks it up (Tools 1.1.2 through the release flow).
4. Release the extension 1.0.0 after its CI, the e2e with the released helper and Box, and a check that the .xpi is
   signed.

== Step 3: the rest of stage 7 ==
- Tools' docs/user/everywhere.md: the browser section (install steps for Chrome/Edge/Brave and Firefox/Zen, with
  pictures) and "Connected" check; user pages for the extension in Arcade-browser.
- Each app README: change "the browser extension will offer ... when it ships" to say where it is now.
- catalog.json: the extension entry if the catalog lists it, `pairs` sentences where an app has none (Box,
  Clipboard, Look, Shelf, Wheel fall back to Link's compiled sentences today), and `rules` (hide/rename/boost/jobs)
  for anything the real-user run shows is noisy.
- Arcade-catalog draft PR #9 (the owner's October report): ask the owner whether to merge or close it.

== Step 4: stage 8, real-user runs and fixes ==
Linux first (a real desktop with Chromium, Firefox and Zen, Nautilus and Dolphin): install Tools from its release,
every app through Tools, set up the extension, then use every surface of PLAN.md 4.5 and 4.7 on real files and real
sites and every app's offers. For each problem: a test that fails first, the fix, re-release the affected app.
Then LOCAL-PROMPTS.md prompt C (Windows) and prompt D (macOS) on the owner's PCs, with two additions to both:
- Arcade Lens pin menu (RD-LENS-4, fixed in Lens 1.1.0 but never seen on a real desktop): select a small screen
  area, pin it, right-click the pin: the whole menu must be visible, not cut off by the pin's window; after the menu
  closes the pin returns to its size. Screenshot both.
- macOS only: Finder → right-click files → Quick Actions shows "Arcade…" and each pinned action (Tools 1.1.1), they
  run, and they disappear after "Uninstall everything".
Write dev/everywhere/REAL-USER-RUN.md (Linux) and the C/D reports; supersede dev/v1/HANDOFF.md with
dev/everywhere/HANDOFF.md.

== Still open from the cloud session (do these too) ==
- Find 1.1.0 was released from v1.1.0-rc.3 WITHOUT three of its gates (the owner's decision on 2026-11-23): the
  macOS dmg smoke never got a GitHub Mac (twice), and the Tier 1/Tier 2 Linux desktop gates, which wait on it, were
  skipped. When macOS runners are available again, run Find's gates.yml on the v1.1.0-rc.3 tag (input previous:
  v1.0.1) once and record the result in Arcade-Find docs/v1/PROGRESS.md; anything that fails gets a test, a fix
  and a 1.1.1. If Find's docs PR for 1.1.0 (CHANGELOG dated, PROGRESS, STATUS) isn't merged, merge it.
- Arcade-Link CI: jurplel/install-qt-action has no timeout in ci.yml and e2e.yml (3 places); cap it at 10 minutes
  with one retry step, as Arcade-Shelf's ci.yml does (a hung Qt download held a job for 1h46m).
- Look: the Tauri 2.12 upgrade with the plugin updates Dependabot proposed (adds second copies of cssparser,
  html5ever, dom_query: check binary size), notify-rust 4.19 and zip 9.8 when the toolchain moves to Rust 1.89.
  Playwright stays on 1.64.1 until the Chromium abort "Check failed: has_site_" in the sandboxed HTML preview check
  is gone; check Look's HTML preview on Windows (WebView2 is Chromium) when WebView2 reaches that Chromium.
- Clipboard: hotkey_manager 0.4 and window_manager 0.7 with the move to Flutter 3.50 (Dart 3.14).
- Clipboard CI: the Android job has no Gradle cache, so every run fetches the Kotlin/Gradle plugins from Maven
  Central; the v1.1.0-rc.2 Release run failed once on "Received status code 429 ... Too Many Requests". Add a Gradle
  cache that is saved only on main (Link spec section 4), e.g. gradle/actions/setup-gradle with
  `cache-read-only: ${{ github.ref != 'refs/heads/main' }}`.
- Find: accesskit_unix 0.24, smithay-client-toolkit 0.20 and x11rb 0.14 only together with an egui/winit update.
- Find start-up stall (open, cause unknown): the v1.1.0-rc.1 and rc.2 Release runs each failed one end-to-end check
  with a Find resident that never answered --status and printed nothing (rc.1 tests/real-peers.py, where Look and
  Box didn't register either; rc.2 tests/wayland-lifecycle.py). Every PR/main run passed, including 20 repeats.
  Since #35 real-peers leaves target/e2e/real-peers/failure-diagnostics.json and logs/; since #36 the resident writes
  start-up milestones to events.log (starting, lock taken, service started, answering commands), which both tests
  keep. If it happens again, read those in the e2e-screenshots artifact and fix the step where it stopped. The earlier one-off "0.4.3 did not load the configured pins and
  history" (check-upgrade.py, 0 of 20 repeats) may be the same stall: check-upgrade now prints the app's state too.
- Box: gates back to `--dashboard` once Link's runner supports it there; a real-fleet e2e of the helper with Box.
- Lens: LN-10 (the colour-pick loupe label shows the dimmed overlay colour).
- Stage 9 (only when the owner has certificates): signed Windows sparse package with IExplorerCommand, signed
  installers; macOS Developer ID signing, notarization and a Finder extension.

Start with step 1. Before each step, tell the owner in two or three plain sentences what you are about to do.
```

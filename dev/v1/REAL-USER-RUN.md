# Real-user run, 2026-11-21 and 22 (Linux)

A desktop session as an ordinary user (`tester`, not root): Xvfb, openbox, an xfce4 panel with a StatusNotifier
tray, D-Bus and gnome-keyring. Everything was done the way a person would do it: downloads into `~/Downloads`,
double-clicks, the apps' own install dialogs, clicks in Tools' window and tray menu. Every installed file was
checked against the SHA-256 GitHub publishes for that release. Box was left out (the owner's call).

## Starting point

Tools 1.0.0 from its first-run dialog; onboarding installed Find and Look. Old releases installed from their own
downloads, outside Tools: Lens 0.4.2, Shelf 0.4.0, Wheel 0.5.0, Clipboard 0.3.1.

## What worked

| Flow | Result |
| --- | --- |
| Take over an app ("Let Tools manage it"), then update it from Updates | Lens 0.4.2 → 1.0.0 and Shelf 0.4.0 → 1.0.0; files = published 1.0.0; Shelf's item kept |
| Repair a deleted AppImage (Find) | Reinstalled, file = published 1.0.0 |
| Remove an app keeping data, then Check & install again (Look) | Launcher, autostart, registry entry removed; settings kept byte for byte; reinstalled file = published |
| Tools 1.0.0 → 1.0.1 by hand (the owner's path) | "Update or open installed Arcade Tools?" → Install: installed file = the release asset, download removed, one Tools running |
| Start at login off and on | Autostart entry removed, then restored with `--background` |
| Check for updates offline | Says it couldn't connect |
| Roll back offline (Shelf 1.0.0 → 0.4.0) | Works from the kept copy; item kept; file = published 0.4.0 |
| Tools killed (SIGKILL) right after Update | Shelf correctly on 1.0.0; Tools restarts cleanly from its launcher |
| Tools killed during an install (Look, 158 MB) | Nothing half-installed; the downloaded file is deleted on the next start |
| Lens 1.0.0 starts | Yes (0.4.1 and 0.4.2 crash on start: a font panic, fixed in 1.0.0) |

## What broke, and the fixes (Tools 1.0.1, PR qa-p1/Arcade-tools#56)

Each fix has a test that fails without it.

- **D27, the owner's bug again:** apps installed outside Tools were counted in the tray ("Updates (3)") while the
  Updates page said "You're up to date". The page, Home and the sidebar badge now count what the tray counts; on
  Linux one click updates the app and lets Tools manage it.
- **D28:** one app's old release without a manifest (Clipboard 0.3.2) made the whole page say the check failed and
  "check your connection". Now only that app says it couldn't be checked.
- **D29:** an app card didn't show the update the last check found.
- **D30:** a deleted app file showed as three issues in jargon; the first button, "Remove entry", would have made
  Tools forget the app. Now one issue: "Its app file is missing. Repair installs it again".
- A card of an app that isn't installed said "Update 1.0.0".
- **D31:** Recent activity showed the oldest 20 entries, oldest first; repairs read "1.0.0 → 1.0.0"; errors started
  with internal codes ("network:").
- **D32:** a Tools killed right after an update lost that update from Recent activity.
- **D33:** after that kill, the page offered "Roll back to v1.0.0" while 1.0.0 was installed.

## Second pass: rc.2 and rc.3 (Tools 1.0.1 PRs qa-p1/Arcade-tools#57 and #58)

| Flow | Result |
| --- | --- |
| Tools rc.1 → rc.2 from inside Tools (Updates page, test channel) | Installed file = the rc.2 asset; history recorded |
| Tools rc.2 → rc.3 by hand (download, "Update or open installed Arcade Tools?" → Install) | Installed file = the rc.3 asset, download removed, one Tools, from its unpacked copy |
| Updates page and tray agree | "Updates (2)" in the tray, badge 2 on the page (Wheel 0.5.0 and Clipboard 0.3.1, "installed outside Tools") |
| Update Clipboard 0.3.1, installed from its own download (rc.3) | One step: file = published 1.0.0, Tools manages it, both clips kept, delta download 7.9 of 15.8 MB |
| Update Wheel 0.5.0 the same way | File = published 1.0.0, settings identical, delta download 3.8 of 48 MB |
| Every app off its AppImage mount | After restarts from Tools: Tools and all six apps run from their unpacked copies, no FUSE mount left |
| Home: "Lens needs Tesseract" → Open Engines | Clear: the apt command to copy, and Download with Arcade |

Fixed in 1.0.1 (each with a test that fails without the fix):

- **D34:** programs Tools started inherited its "already unpacked" marker, so Lens, Look, Shelf and the new Tools
  after a self-update stayed on their AppImage mounts with a FUSE helper each.
- **D35:** Update on an app installed from its own download refused with "Choose Let Tools manage it", although the
  page offered it (the one-step path required no record; Tools builds one from the app's receipt). Recent activity
  showed the internal code "unmanaged:".
- **D36:** that one-step update's history line had no target version ("from 0.3.1" only); and an rc that Tools had
  installed under the test override was never offered the next rc of the same version.
- **D37:** Download with Arcade for Tesseract failed: "curl: symbol lookup error" (the system curl loaded Tools'
  bundled libnghttp2). Broken on current distributions since 1.0.0. Tools now runs the download with the user's
  environment; the same fix is merged in Link (qa-p1/Arcade-Link#79, not yet tagged).

## Third pass: rc.4 and the released 1.0.1

| Flow | Result |
| --- | --- |
| Tools rc.3 → rc.4 by hand | File = the rc.4 asset, download removed, one Tools from its unpacked copy |
| Engines → Download with Arcade (Tesseract) | "Tesseract is ready"; 5.5.3 runs with eight languages; Home's "Lens needs Tesseract" cleared |
| Released 1.0.1 updates itself from inside Tools | File and record = the published 1.0.1, Tools reopened from its unpacked copy, no mount left, then "up to date" |
| Home at the end | 6 installed, 6 running, nothing needs attention, no updates |

Tools 1.0.1 was promoted from rc.4 after both Gates runs passed 11 of 11 (one with update-from rc.3, one from
0.4.6); its files are byte for byte rc.4's.

Also released: Clipboard 1.0.0 (rc.3 passed all 13 gates; files byte for byte the rc's).

## Noted in the third pass, and what happened to each

The owner asked for all of them to be fixed where it made sense (2026-11-22). Outcomes, verified in the fourth pass
below unless it says "test only":

| Noted | Outcome |
| --- | --- |
| White tray mark hard to see on a light panel | Tools 1.0.2: the mark has a thin dark edge. Test only (`the_white_mark_has_a_dark_edge_and_keeps_its_white`): this pass's panel (tint2) shows no StatusNotifier icons |
| No transparency without a compositor | Shelf 1.0.1 detects that nothing composites and draws a square surface (seen). Find needed no change: without a compositor its bar showed no box |
| Lens dark vs Tools light on openbox | Link 1.0.15 reads the desktop's GTK/GNOME setting when there is no portal; Find and Lens 1.0.1 use it. Both light under System (seen) |
| Lens's install dialog much taller than its content | Lens 1.0.1: as tall as its content (seen) |
| An app restarted by itself keeps its start environment | **Not changed.** Link's harnesses start real AppImages with `ARCADE_UNPACKED=1` on purpose, so treating an inherited marker differently would change the tests of eight repos. Tools 1.0.1 already stops passing the marker on (D34), so only apps first started by Tools 1.0.0 are affected, until their next start |
| One-step update keeps no rollback copy | Tools 1.0.2 keeps the replaced version, and a rollback leaves the app managed by Tools. Rollback seen on Find; the one-step path is test only (no app here was in that state any more) |
| Tesseract dialog says "On Windows…" on Linux | Tools 1.0.2: "Arcade verifies the download and sets it up for you. Nothing else to install." (seen) |
| "1.0.1 → 1.0.1" after a hand-installed rc | Tools 1.0.2: at equal versions the installed file's hash decides. Test only (rc channel) |
| "v1.0.1 reinstalled" between two rcs | Tools 1.0.2 names the rc builds. Test only (rc channel) |

Also fixed from the third pass's notes: error messages fade after 12 seconds (seen: gone between 10 and 16 s), and Home
no longer says an engine is missing when its version check is slow at login (Tools 1.0.2). Lens 0.4.1 and 0.4.2 still
crash on start; their release notes need a line pointing to 1.0.0 (owner, text in `HANDOFF.md`).

## Fourth pass: Link 1.0.15, Tools 1.0.2, Find, Lens and Shelf 1.0.1 (2026-11-22)

Each app went rc → Gates on the published files → Promote, and each stable release was checked against its rc: same
commit, same digests for every package and SHA256SUMS, `arcade-release.json` and `manifest.json` differing only in
channel, tag and notes, the manifest signed, the release marked latest.

| Release | Promoted from | Gates on the rc |
| --- | --- | --- |
| Link v1.0.15 | tag on 09d52ee after CI, desktop harness and real-fleet e2e ([#81](https://github.com/qa-p1/Arcade-Link/pull/81)) | — |
| Tools 1.0.2 | rc.2 (e098fc8) | 11/11 (run 45017370828) |
| Find 1.0.1 | rc.2 (961f0ad) | 12/12 (run 45013880691) |
| Lens 1.0.1 | rc.1 (f59d0d4) | 12/12 (run 45016208047) |
| Shelf 1.0.1 | rc.1 (28d2033) | 13/13 (run 45008430296) |

Not promoted, and why:

- **Tools rc.1** passed Gates 11/11, but RUSTSEC-2026-0592 (`url` before 2.5.9: stack overflow in `Url::origin` on
  nested `blob:` URLs) came out while it was in flight. rc.2 has `url` 2.5.9; so do Find rc.2 and Lens rc.1. Shelf
  has no Rust build.
- **Find rc.1** failed Gates in the upgrade test. Since Link's relaunch, the process `--quit` talks to is the launcher;
  the app runs as an unpacked copy that saves the user's data as it exits, and the test compared the data before that
  copy had finished. The test now waits until no Find from its own folder is running
  ([#33](https://github.com/qa-p1/Arcade-Find/pull/33)), which is stricter, not looser. rc.2 passed.
- **Link 1.0.15** also fixed its real-fleet e2e: two sessions shared `/tmp`, where AppImages run with
  `APPIMAGE_EXTRACT_AND_RUN` rewrite one unpack folder per AppImage on every start, so one session's start broke the
  other's (Find exited 127). Each session now has its own `TMPDIR`.

Unexplained, recorded: Find's main CI failed once with "0.4.3 did not load pins/history". It passed 5 of 5 times
locally and on its one re-run.

Real-user check on the released files (openbox with tint2, no compositor):

| Flow | Result |
| --- | --- |
| Tools 1.0.1 updates itself to 1.0.2 from inside Tools | File = published (4c77050a…); 1.0.1 kept; runs from its unpacked copy; no mount left |
| Find, Lens, Shelf 1.0.0 → 1.0.1 from Updates | Files = published (722283af…, 8fd93d58…, 86d4a205…); each keeps 1.0.0 |
| Recent activity and Previous versions | Every update listed; a kept copy for Tools, Find, Lens and Shelf |
| Roll back Find to 1.0.0 | Record 1.0.0, previous 1.0.1, still managed by Tools, 1.0.0 running; Updates offers 1.0.1 again |
| Update Find to 1.0.1 again | File = published 1.0.1, kept copy = published 1.0.0 (26fbb8ca…), managed by Tools, runs from its unpacked copy |
| Shelf with no compositor | Square surface, no black box |
| Find and Lens under Appearance "System" | Light, like Tools |
| Lens install dialog | As tall as its content |
| Tesseract removed, then Engines → Download with Arcade | Linux wording in the dialog; "Tesseract is ready" in about 3 s; 5.5.3 with eight languages. While it was missing, Home's "1 thing needs attention" was right |
| Every app started at once, as at login | No false "engine missing" on Home. Look showed "Not running" for a few seconds while it started, then Running |

A mistake in my test setup, not in the apps: the first login restart used `su` without a clean environment, so the
apps inherited the container's `CURL_CA_BUNDLE`, a file the test user can't read, and the first download failed with
"curl: (77) error setting certificate file". That is what Link 1.0.15 is meant to do: curl runs with the user's own
environment, and it fails the way the user's own curl would. After a clean restart every process was checked free of
those variables, and the download worked.

Noted, not changed: Look's card says "Not running", with a Start button, for a few seconds after login while Look is
still starting (its process was already running). What Start does in that moment was not tested.

## Not covered

Windows and macOS had no real-user run (the release gates smoke-test their installers on the published files).

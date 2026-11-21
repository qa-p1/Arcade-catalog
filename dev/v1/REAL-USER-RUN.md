# Real-user run, 2026-11-21 (Linux)

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

Fixed (each with a test that fails without the fix):

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

Also released today: Clipboard 1.0.0 (rc.3 passed all 13 gates; files byte for byte the rc's).

## Noted, not changed

- The tray mark is white on Linux by design (GNOME, Plasma and Hyprland panels are dark). On a light panel (XFCE's
  default) it is hard to see. Suggestion: a thin dark outline so it reads on both.
- Without a compositor, Find's bar and Shelf's capsule sit in a grey or black box (no transparency). Every desktop
  that matters has a compositor; noted for X11 setups without one.
- Lens follows "System" to dark while Tools shows light on the same desktop (no portal colour scheme on openbox).
- Lens 1.0.0's install dialog window is much taller than its content.
- An app restarted by itself keeps the environment it was started with: Shelf, first started by rc.2 (D34), stayed on
  its mount after its own Restart until it was quit and started again. Users updating from Tools 1.0.0 get clean
  starts at the next login or app start.
- The one-step update keeps no rollback copy of the app's own 0.x install (the two-step "Let Tools manage it", then
  Update, does). Owner's call (Tools DECISIONS D36).
- On Linux the Tesseract download dialog still says "On Windows, finish the installer that opens".
- rc builds all say "1.0.1", so with the test override Recent activity shows "v1.0.1 reinstalled" and Previous
  versions "Roll back to v1.0.1" between two rcs (test channel only).

## Not covered

Windows and macOS had no real-user run (the release gates smoke-test their installers on the published files).

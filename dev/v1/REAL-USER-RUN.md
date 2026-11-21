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

Also released today: Clipboard 1.0.0 (rc.3 passed all 13 gates; files byte for byte the rc's).

## Noted, not changed

- The tray mark is white on Linux by design (GNOME, Plasma and Hyprland panels are dark). On a light panel (XFCE's
  default) it is hard to see. Suggestion: a thin dark outline so it reads on both.
- Without a compositor, Find's bar and Shelf's capsule sit in a grey or black box (no transparency). Every desktop
  that matters has a compositor; noted for X11 setups without one.
- Lens follows "System" to dark while Tools shows light on the same desktop (no portal colour scheme on openbox).
- Lens 1.0.0's install dialog window is much taller than its content.

## Not covered

Windows and macOS had no real-user run (the release gates smoke-test their installers on the published files).

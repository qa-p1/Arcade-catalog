# Real-desktop test log (owner's machine, CachyOS + Hyprland)

Started 2026-10-15. Authorized by the owner for the plan §17.3 checks and §18 performance numbers.

## Baseline before the test
- No `~/Applications/Arcade`, no `~/.config/arcade`, no Arcade launchers in `~/.local/share/applications`,
  nothing in `~/.local/bin`, no autostart entries. `~/.local/share/arcade/apps` existed and was empty.
- `~/.config/hypr` has no Arcade references. It is never edited by this test.

## Changes to the live profile (every one is listed)
- 22:52 Installed 7 released apps with `--install --silent --no-launch` from `~/Downloads/arcade-test/` (all checksums OK;
  70–210 ms each): Find 0.3.0, Lens 0.2.0, Look 0.2.0, Box 0.2.0, Shelf 0.2.0, Wheel 0.3.0+build.48, Clipboard 0.1.0.
  Created: `~/Applications/Arcade/*.AppImage` (7), `~/.local/share/applications/` launchers (7), `~/.local/bin/`
  CLI links (7), `~/.local/share/arcade/installs/*.json` receipts (7), autostart entries for Find, Lens, Look
  (each app's default). `arcade-find --version` works from fish.
- 22:55 Started all 7 detached in their login modes (`--background`, Look `--service`), without Tools.
  `arcade-link ls`: all 7 running and registered; 7 SNI tray icons on the bar (8 items with the existing one);
  no errors in any app log. A cross-app call without Tools, Link CLI → Box `box:arcade.image.ocr` on a test
  PNG, returned "Arcade Link works" in 224 ms (tesseract 5.5.3).
- 22:58 Idle memory on the real session (Hyprland, AMD GPU), background modes, no windows open. App process tree
  only; each AppImage runtime parent adds about 17–22 MiB:
  | App | RSS / PSS / USS (MiB) |
  |---|---|
  | Find | 51.8 / 48.2 / 48.1 |
  | Lens | 13.6 / 11.4 / 11.3 |
  | Look | 60.7 RSS |
  | Box | 419 RSS (arcade-desktop 171 + WebKitWebProcess 184 + WebKitNetworkProcess 64) |
  | Shelf | 109.4 / 70.9 / 67.0 |
  | Wheel | 98.3 / 64.0 / 60.8 |
  | Clipboard | 143.7 / 86.6 / 79.3 |
  Finding: Box keeps a hidden webview alive at idle. Sent for a fix (lazy webview, Box 0.2.1).
- 23:05 Window open latency on the real GPU (app already running in the background, command → window mapped
  in Hyprland): Find overlay 38 ms (layer surface, median of 2), Lens settings 107 ms, Shelf 168 ms, Box settings
  247 ms, Look settings 662 ms, Wheel settings 822 ms. One sample each except Find.
  Repeat samples weren't possible: Hyprland 0.56 parses `hyprctl dispatch` as Lua, so `closewindow address:…` is
  a syntax error. I didn't guess the Lua form, because `hl.dsp.window.close()` without a window argument closes
  the focused window.
- 23:07 `arcade-link quit` for Clipboard, Look, Shelf, Wheel, Box and Lens: all quit cleanly and their tray
  icons left the bar (8 → 2). Restarted all six in background mode: all running, 8 tray items again.
- 23:10 More cross-app calls over Link, no Tools: `find.search "arcade"` 4.6 ms (results, truncated),
  `look.inspect` on a PNG 0.4 ms, `lens.recognize` on a PNG 178 ms (3 findings, Tesseract),
  `clipboard.devices` 0.6 ms (no paired devices). Server-side times as reported by the CLI.
- 23:48 Updated Box 0.2.0 → 0.2.1 from the GitHub release with the self-installer (`--install --silent
  --no-launch`, 224 ms; checksum OK; receipt now 0.2.1). Restarted with `--background`: `arcade-desktop` 81 MiB
  RSS and no WebKit processes (0.2.0: 419 MiB). Finding: Look (`--service`) keeps a 404 MiB WebKitWebProcess plus
  a 36 MiB NetworkProcess alive after its window closes. Sent for the same fix (Look 0.2.1).
- 23:37 Wheel Settings checked on screen (grim, owner-approved): most app icons render as an "A" placeholder,
  and the layout is clipped at a 1228×693 tile. Causes: no Qt SVG icon engine in the AppImage, and no icon theme
  (Papirus-Dark) without the host `qtengine` platform theme. Sent for a fix (Wheel 0.3.1).

## Cleanup (2026-10-16, owner's request before going remote)
- Quit all apps over Link, then ran each installed AppImage's `--uninstall --silent`: all 7 returned
  `"uninstalled": true`. Launchers, CLI links, autostart entries, receipts and icons were removed by the
  uninstallers.
- Then deleted the leftovers and every Arcade data folder the test created (all born 2026-10-15 22:52 or later):
  - `~/Applications/Arcade` (only an empty `.previous`);
  - `~/.config/{arcade-find,arcadelens,arcade-look,Arcade Wheel}`;
  - `~/.local/share/{app.arcadelook,arcade,arcade-find,arcadelens,dev.arcadebox.app,dev.arcade.clipboard}`;
  - `~/.cache/{arcade,Arcade Wheel}`;
  - `~/Downloads/arcade-test`.
- Also removed, at the owner's request "delete every arcade app and clean up everything":
  - the old dev install `~/.cargo/bin/arcade-lens` (2026-10-04);
  - the dev caches `~/.cache/arcade-dev`, `~/.cache/arcade-orchestrator` (3.6 GB agent build cache) and
    `~/.cache/test_WheelController`.
- `~/.local/share/arcade` existed before the test with an empty `apps/` folder; it is now removed entirely.
- Never touched: `~/.config/hypr`, shell profiles. No Arcade process is running. Source checkouts under
  `~/Work/Coding` were kept; every change in them is pushed to GitHub.

## Not done on the real desktop (needs the owner's machine)
- Tools 0.2.1 steps: install Tools, tray hosting (one icon, submenus, icons return on quit and `kill -9`),
  the `Super+/` overlay over several apps, rebinding Find's shortcut from Tools, update and rollback of one app
  through Tools, Tools window first paint and memory after the window closes.
- Re-check Wheel 0.3.1 (icons, layout) and Look 0.2.1 (idle memory) once released.

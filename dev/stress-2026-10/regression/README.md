# Stress-test regression checks (2026-10)

Failing checks for bugs in `../ARCADE_STRESS_REPORT.md`. Each exits 1 while its bug is present and 0 once fixed.
All but the Wheel check run only inside Arcade-Link's isolated runner (`python3 tools/e2e.py run -- …`), which
provides a private D-Bus, Xvfb, a throwaway keyring and a temporary HOME; `common.require_isolation()` refuses to run
anywhere else. Scripted installs (`--install --silent`) delete the AppImage they are given (report m2), so pass copies.
The tray checks need `python3-dbus` and `python3-gi` (here: `/usr/bin/python3.12`; the default Python 3.13 had no D-Bus bindings).

| Check | Finding | On the released apps |
|---|---|---|
| `tools_webview_alive.py TOOLS.AppImage [--control]` | F1 Tools window blank without DRI3 | FAIL ("WebKitWebProcess died within 8 s; window is blank (1 colours)"); `--control`: PASS (1917 colours) |
| `tools_start_all_child_env.py TOOLS.AppImage CLIPBOARD.AppImage [--control]` | F2 apps started by Tools inherit its AppImage environment; Clipboard never starts | FAIL ("Clipboard is not running 20 s after 'Start all Arcade apps'"); `--control`: PASS |
| `clipboard_tray_late_watcher.py CLIPBOARD.AppImage [--control]` | F4 no tray icon when the watcher appears after Clipboard | FAIL (`--control`: PASS) |
| `wheel_appimage_needs_libopengl.py WHEEL.AppImage` | F5 Wheel needs the host's libOpenGL.so.0 (no runner needed) | FAIL |
| `find_live_rebind.py FIND.AppImage [--link arcade-link]` | F7 rebind over the Link doesn't work until restart | FAIL (`applied: true, via: native`, chord ignored); built-in control after restart: PASS |
| `clipboard_answer_fd.py CLIPBOARD.AppImage` | m1 headless answers overwrite a redirected file / fail on a socket | FAIL |

`common.py` holds the isolation guard and helpers; `sni.py` is a minimal StatusNotifierWatcher plus DBusMenu helpers.
Tools' GUI backup (F3) has no command line or Link entry point, so it has no check here; its reproduction is in the report.

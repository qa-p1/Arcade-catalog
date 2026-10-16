# Stress-test regression checks (2026-10)

Failing checks for bugs found in `../ARCADE_STRESS_REPORT.md`. Each exits 1 while its bug is present and 0 once fixed.
They run only inside Arcade-Link's isolated runner (`python3 tools/e2e.py run -- …`), which provides a private D-Bus,
Xvfb, a throwaway keyring and a temporary HOME; `common.require_isolation()` refuses to run anywhere else.

| Check | Finding | Status on the released app |
|---|---|---|
| `clipboard_answer_fd.py <Clipboard AppImage>` | m1: headless answers overwrite redirected output / fail on a socket | FAIL |
| `clipboard_tray_late_watcher.py <copy of Clipboard AppImage> [--control]` | F4: no tray icon when the watcher appears after Clipboard starts | FAIL (`--control`: PASS) |

`clipboard_tray_late_watcher.py` performs a scripted `--install --silent`, which deletes the AppImage it is given
(report m2), so pass a copy. It needs `python3-dbus` and `python3-gi`.

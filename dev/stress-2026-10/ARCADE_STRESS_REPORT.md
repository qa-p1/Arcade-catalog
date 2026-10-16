# Arcade real-user stress test — October 2026

Brief: `dev/CLOUD_STRESS_TEST_PROMPT.md`. Run date: 2026-10-16 (UTC). Tester: a cloud coding agent working in a
Linux container, as a user would, with the released files only.

**This is a partial run.** Journeys 1, 2, 3 (most of it) and 7 (most of it) were run on Linux. Journey 9 was run in
part. Journeys 4, 5, 6, 8 and 8b were not run, or barely. Every row says *not run* where I did not exercise it; nothing
below is marked passed without having been run. Section 6 lists what is missing and why.

Releases under test (all downloaded from GitHub Releases; every `SHA256SUMS` and release manifest verified):

| App | Release tested | Older releases used (update / migration) |
|---|---|---|
| Arcade Find | v0.3.1 | v0.3.0, v0.2.1 (pre-self-installer) |
| Arcade Lens | v0.2.0 | v0.1.1 (downloaded, not exercised) |
| Arcade Look | v0.2.1 | v0.2.0, v0.1.2 (downloaded, not exercised) |
| Arcade Box | v0.2.1 | v0.2.0, v0.1.2 (downloaded, not exercised) |
| Arcade Shelf | v0.2.0 | v0.1.1 (downloaded, not exercised) |
| Arcade Wheel | v0.3.1+build.56 | v0.3.0+build.48, v0.2.0+build.33 (downloaded, not exercised) |
| Arcade Clipboard | v0.1.0 | — |
| Arcade Tools | v0.2.1 | v0.2.0, v0.1.0 (downloaded, not exercised) |
| Arcade Link (CLI + e2e harness) | built from tag v0.3.0 | — |

**Test desktop.** Ubuntu 24.04 container; Xvfb 1920×1080 (no GPU, no DRI3); Openbox; xfce4-panel with its
systray plugin as the StatusNotifierWatcher/host; a real gnome-keyring; D-Bus session bus; FUSE (`/dev/fuse` set
to the usual 0666). Each persona is a normal non-root user with its own X display and session bus: *maya* (main),
*zoe* (`HOME="/home/Zoë Ångström %"`), *zoe2* (`HOME="/home/Zoë Ångström"`), *tiny* (64 MiB tmpfs HOME, for
disk-full), *old* (pre-self-installer Find). Files were run the way a file manager runs them: copied into
`~/Downloads`, `chmod +x`, executed detached.

Evidence: screenshots in [`screenshots/`](screenshots/), logs in [`logs/`](logs/), failing regression checks in
[`regression/`](regression/). Screenshot names start with the journey (`j1-…`, `j3-…`).

---

## 1. Verdict

**Partly.** On Linux, without Tools, a real user can download each app, install it from the app's own prompt, use
it, and the apps find each other and work together (Find → Shelf, Find → Look, Lens → Clipboard, drag and drop with
Shelf, Wheel launching apps). They survive a reboot, a second double-click and a deleted download. The weak spot
is Arcade Tools. On a display without DRI3 (VNC, xrdp, VMs without 3D, Xvfb) its window is blank and its install
prompt is invisible. Apps that Tools starts inherit Tools' AppImage environment, so Clipboard cannot start from
Tools at all and adopting it silently turns history off. Its "Back up settings" still leaves out Lens and Shelf,
although release notes call that fixed. Its install/repair/update path depends on GitHub's anonymous 60-calls-an-hour
API limit. Removing Tools wasn't tested, but killing it (`kill -9`) hands every tray icon back within about 0.1 s
(one timed run per app), and 50 start/quit cycles were clean. Two
non-Tools problems would also stop real users: Wheel's AppImage does nothing on a stock Ubuntu 24.04 without
`libopengl0`, and Clipboard autostarted before the panel gets no tray icon for the whole session (and quits when its
window is closed). Windows and macOS were **not run** (section 6).

---

## 2. Matrix

Legend: ✅ works · ❌ broken · ⚠️ works with a real problem (see the finding) · **nr** = not run · n/a = not applicable.
Linux = the Xvfb desktop above. "Install via Tools" and "update/rollback via Tools" were blocked first by the blank
window (worked around) and then by the GitHub API limit.

### Linux (real-ish)

| App | Standalone install | Install via Tools | Adoption | Update | Rollback | Uninstall | Works with others, no Tools | Tray hand-off |
|---|---|---|---|---|---|---|---|---|
| Clipboard 0.1.0 | ✅ j1-clip-01..04 | nr | ❌ stops Clipboard (F2) | nr | nr | nr | ✅ Lens→history, Wheel launch | ⚠️ hand-off ✅, login race ❌ (F4) |
| Find 0.3.1 | ✅ (prompt partly off-screen, UX) | ⚠️ attempted: 403 from GitHub API (F9) | ✅ | ⚠️ double-click 0.3.0→0.3.1 replaces file, old instance keeps running (m5) | nr | ✅ own uninstaller; ⚠️ Tools keeps a stale record (F6) | ✅ → Shelf, → Look | ✅ |
| Lens 0.2.0 | ✅ | nr | ✅ (opens its window, UX) | nr | nr | nr | ✅ capture → Clipboard | ✅ |
| Look 0.2.1 | ✅ | nr | ✅ (opens its window, UX) | nr | nr | nr | ✅ preview from Find | ✅ |
| Box 0.2.1 | ✅ | nr | ✅ | nr | nr | ⚠️ documented `arcade-box --uninstall` = command not found (m3) | ✅ tray menu | ✅ |
| Shelf 0.2.0 | ✅ | nr | ✅ | nr | nr | nr | ✅ drop on / drag out, auto-launched by Find | ✅ (XEmbed fallback without SNI watcher) |
| Wheel 0.3.1 | ⚠️ needs host `libopengl0`, silent failure (F5) | nr | ✅ (opens Settings, UX) | nr | nr | nr | ✅ launches apps (list stale until restart, m4) | ✅ (own icon lingers ~3 s on collapse) |
| Tools 0.2.1 | ❌ blank window without DRI3 (F1); ✅ with workaround env | n/a | n/a | nr (self-update) | nr | nr | n/a | ✅ collapse 7→1, hand-back ≤102 ms |

### Windows CI, macOS arm64 CI, macOS Intel CI

| App | All eight columns |
|---|---|
| All 8 apps | **nr** — no real machine; CI logs and artifacts are not reachable from this sandbox (section 6). |

---

## 3. Findings, worst first

Every Tools GUI step after F1 was run with `WEBKIT_DISABLE_COMPOSITING_MODE=1`, because otherwise Tools draws
nothing on this display. Without that, none of the Tools journeys can be done on Xvfb at all.

### F1 — blocker — Tools 0.2.1 window is blank on X servers without DRI3

- **Steps:** maya (no Tools yet, 7 apps running with own icons) downloads `Arcade-Tools-0.2.1-x86_64.AppImage`,
  double-clicks it. `firstrun maya …/Arcade-Tools-0.2.1-x86_64.AppImage j3-02-tools-prompt`.
- **Expected:** "Install Arcade Tools?" prompt, then the Tools window.
- **Actual:** an empty white window that stays empty (checked at 5, 15 and 25 s). The tray has *already* collapsed
  from 7 icons to Tools' one, so the user has lost all their tray icons and sees nothing to click.
  `strace -f` shows `WebKitWebProcess` dying with `SIGSEGV {si_code=SEGV_MAPERR, si_addr=0x40}` about 0.9 s after
  start; the window is never repainted.
- **Narrowing:** Look 0.2.1 ships the *same* `libwebkit2gtk-4.1.so.0` (sha256 `bad3b5ee…`) and renders fine on the
  same display. `WEBKIT_DISABLE_COMPOSITING_MODE=1` or `WEBKIT_DISABLE_DMABUF_RENDERER=1` makes Tools render;
  `LIBGL_ALWAYS_SOFTWARE=1` does not.
- **Evidence:** `screenshots/j3-02-tools-prompt.png`, `j3-03-tools-window-25s.png` (blank),
  `j3-06-tools-with-workaround.png`, `j3-tray-before-after.png`.
- **Suspected cause:** `Arcade-tools src-tauri/src/desktop.rs:115-121` sets
  `HardwareAccelerationPolicy::Never` on the webview's settings *after* the webview is built. That is the only
  difference from Look I could find. The renderer has already chosen its compositing path by then. Setting it
  before the first load, or setting `WEBKIT_DISABLE_COMPOSITING_MODE` when no DRI3 is available, is the likely fix.
- **Who hits it:** Xvfb/CI, VNC and xrdp sessions, VMs without 3D acceleration, and likely the NVIDIA proprietary
  X11 driver.

### F2 — major — apps started by Tools inherit Tools' AppImage environment (Clipboard never starts)

- **Steps:** with Tools running (workaround env), Apps → *Start all*; or adopt Clipboard; or tray → Clipboard →
  *Open* while Clipboard is stopped.
- **Expected:** each app starts with the user's environment.
- **Actual:** children get `LD_LIBRARY_PATH` pointing into Tools' `/tmp/.mount_*`, `GTK_THEME=Adwaita:light`,
  `PYTHONHOME`, `GIO_MODULE_DIR`, `GTK_PATH`, and an `XDG_DATA_DIRS` that still names the deleted Downloads mount.
  Read from `/proc/<pid>/environ` of the started apps: `logs/env-of-app-started-by-tools.txt`.
  - Clipboard: `clipboard: symbol lookup error: … undefined symbol: g_once_init_enter_pointer`, exit 127.
    (`logs/clipboard-started-by-tools.log`). *Start all* ends with 6 of 7 running. **After adopting Clipboard, Clipboard is no longer running**, so clipboard
    history silently stops (`arcade-link ls`: installed, no process; Tools card flips Running → Installed).
  - Wheel started by Tools cannot launch LibreOffice from the wheel; the same Wheel started from the menu can
    (`screenshots/j3-39-wheel-clean-launches-lo.png`).
  - Tools' Engines tab says LibreOffice is unavailable although 24.2 is installed: its own `soffice --version` probe
    fails with `symbol lookup error … libcurl-gnutls … nghttp2_option_set_no_rfc9113` (exit 127)
    (`screenshots/j3-21-engines.png`).
  - Dark-theme users get forced to the light theme in every app Tools starts.
- **Evidence:** `screenshots/j3-37-after-start-all.png`, `j3-28-after-adopt-all.png`.
- **Suspected cause:** `Arcade-tools src/manager.rs` (adopt/start/restart path) spawns with the inherited
  environment; it needs to drop or restore the AppImage runtime variables (`APPDIR`, `APPIMAGE`, `LD_LIBRARY_PATH`,
  `GTK_*`, `GIO_*`, `PYTHON*`, `XDG_DATA_DIRS` entries under the mount). The same applies to `src/engines.rs`
  probes.

### F3 — major (and a test gap) — Tools "Back up settings" leaves out Lens and Shelf

- **Steps:** Tools → Settings → *Back up settings*, then *Restore* from that file.
- **Expected:** all 7 apps backed up (release notes for Tools 0.2.0/0.2.1 list the Lens and Shelf backup bugs as
  fixed).
- **Actual:** the backup reports Lens "App returned an invalid settings handoff." and Shelf "expected value at
  line 1 column 1"; neither is in the file. Restore restores 5 apps; its confirmation still lists Lens and Shelf as
  "will be replaced", using raw IDs (`arcade.lens`) rather than names.
- **Evidence:** `screenshots/j3-54-backup-confirm.png`, `j3-55-restore-plan.png`, `j3-56-restore-result.png`,
  `j3-57-restore-result.png`.
- **Suspected cause:** the GUI goes through `Arcade-tools src/hub.rs:356 export_backup` → `src/backup.rs`, which
  requires `output.kind == "file/any"` (`src/backup.rs:98`; Lens 0.2.0 exports `file/code`) and parses every export
  with `serde_json::from_slice` (`src/backup.rs:374-378`; Shelf's export is binary). The Link e2e checks cover
  `src/portable_backup.rs` instead, so CI is green while the button users press is broken.

### F4 — major — Clipboard autostarted before the tray host never gets a tray icon (and then quits on close)

- **Steps:** login autostart starts `clipboard --background` a few seconds before the panel's
  StatusNotifierWatcher appears (normal login race). Then close the Clipboard window.
- **Expected:** Clipboard waits for the watcher and registers its icon when it appears; it keeps running in the
  background.
- **Actual:** its window is shown, no tray icon appears for the whole session, and closing the window **quits**
  Clipboard although *Keep running in the background* is on. History capture stops without telling the user. Wheel
  and Shelf don't hit this: they fall back to XEmbed icons (X11 only).
- **Regression check:** `regression/clipboard_tray_late_watcher.py`: control (watcher first) PASS; real order
  (watcher 4 s later) **FAIL** "no StatusNotifierItem registered within 10 s after the watcher appeared".
- **Evidence:** `screenshots/j1-all-reboot-20s-tray.png`, `j1-all-reboot.png`.
- **Suspected cause:** `Arcade-clipboard platform/desktop/arcade_desktop_bridge/linux/lifecycle_bridge.cc` around
  lines 520-534: `setBackgroundEnabled` checks `TrayHostAvailable()` once and refuses background mode; the
  name-owner watch for the watcher is only installed inside `OpenTray`, which is never reached.

### F5 — major (and a test gap) — Wheel AppImage silently does nothing without `libopengl0`

- **Steps:** on Ubuntu 24.04 without the `libopengl0` package, double-click `ArcadeWheel-0.3.1-Linux-x86_64.AppImage`.
- **Expected:** install prompt, or at least an error dialog.
- **Actual:** nothing visible. From a terminal: `AppRun.wrapped: error while loading shared libraries:
  libOpenGL.so.0: cannot open shared object file`.
- **Suspected cause:** the bundled `usr/lib/libLayerShellQtInterface.so.6` has `NEEDED libOpenGL.so.0`, which
  linuxdeploy's exclude list leaves to the host. GitHub's Ubuntu runner image has the library preinstalled, so CI
  never sees this. Bundle it, or check for it in `AppRun` and show a message.

### F6 — major — Tools keeps a stale record after an app uninstalls itself

- **Steps:** Find is Tools-managed; the user uninstalls it from the menu entry's *Uninstall* action (Find's own
  uninstaller). Open Tools → Apps; press *Refresh*.
- **Expected:** Find is shown as not installed and offered under *Available*.
- **Actual:** Apps shows "Needs repair · Installed executable is missing"; *Available* says "Every app in the
  catalog is installed"; *Refresh* changes nothing. The record stays at `~/.local/share/arcade-tools/arcade.find.json`.
  *Repair* then needs the GitHub API (F9) and did nothing visible.
- **Evidence:** `screenshots/j3-30-apps-after-find-uninstall.png`, `j3-32-after-refresh.png`, `j3-34-find-repair-confirm.png`,
  `j3-35-repair-progress-*.png`, `j3-36-after-repair.png`, `j4-find-uninstall-dialog.png`.

### F7 — major — Rebinding Find's shortcut in Tools leaves no working shortcut on X11 until Find restarts

- **Steps:** Tools → Shortcuts → Find: change Ctrl+Alt+F to Ctrl+Alt+G, apply. Press each chord (`xdotool key`).
- **Expected:** Ctrl+Alt+G opens Find right away; Ctrl+Alt+F no longer does.
- **Actual:** Tools shows "Applied · native" and Find's manifest is updated, but **neither** chord opens Find.
  After Find restarts, Ctrl+Alt+G works. (The 0.3.1 fix — restoring the *same* chord after a settings restore —
  does pass: `screenshots/j3-58-find-after-restore.png`.)
- **Evidence:** `screenshots/j3-40-shortcuts.png`, `j3-41-change-shortcut.png`, `j3-44-after-apply.png`.

### F8 — major (vs the 0.2.1 release claim) — Look and Box keep a WebKit network process after their window closes

- **Steps:** open, then close Look's window (Box: open, then close the Island). Sample processes for several minutes.
- **Expected (release notes):** the web processes are released when the window closes.
- **Actual:** `WebKitWebProcess` is released, but `WebKitNetworkProcess` (≈50 MiB RSS) stays alive: more than
  3.5 min for Look, more than 60 s (same PID for 2.5 min) for Box. Look's main process stays at 189 MiB RSS; Box
  goes from 82 MiB before the first Island open to 174 MiB after.

### F9 — major — Tools' install, repair and update depend on GitHub's anonymous API limit

- **Steps:** Tools → Find → *Install* / *Repair*; *Check for updates*.
- **Actual:** `HTTP status client error (403 Forbidden) for url (https://api.github.com/repos/qa-p1/Arcade-Find/releases/latest)`.
  The cause was the unauthenticated limit (60 requests/hour per IP; `remaining: 0`). In this sandbox the IP is
  shared, but NAT, CGNAT, office and university networks share IPs too. The error banner is raw, appears away from
  the button that caused it and stays when changing tabs; *Repair* reports nothing.
- **Not measured:** how many API calls one Tools start uses (planned; not done).
- **Suggestion:** read the catalog/`latest` from a static file (release asset or GitHub Pages) or `releases/latest/download/…`
  redirects, cache ETags, and show a human message with a retry time.

### Minor

- **m1 Clipboard headless answers overwrite or fail.** `--version`, `--arcade-manifest` and `--integration-status`
  reopen stdout via `/proc/self/fd/$ARCADE_ANSWER_FD`. A redirected file loses its earlier content (the offset
  resets), and a socket stdout fails (`PathNotFoundException '/proc/self/fd/5'`, exit 1).
  `regression/clipboard_answer_fd.py` **FAILS** today: the file contains only `b'Arcade Clipboard 0.1.0\n'`.
  Code: `apps/flutter_app/lib/main.dart:54-60 _answerSink`, `linux/runner/my_application.cc:144`.
- **m2 `--install --silent` deletes its source file wherever it is**, not only in `~/Downloads` (verified for
  Clipboard and Find from a folder outside HOME). This isn't documented, and there is no `--keep` option.
- **m3 Box's command is `arcade-desktop`.** `docs/uninstalling.md:11` and Box's README say `arcade-box`;
  `arcade-box --uninstall` → command not found.
- **m4 Wheel doesn't see apps installed after it started.** It needs *Refresh*, and even then their icons stay
  generic until Wheel restarts (`screenshots/j2-wheel-08a-actions-stale.png`, `j2-wheel-09-crop.png`,
  `j2-wheel-10-crop.png`).
- **m5 A double-click update leaves the old process running.** Find 0.3.0 → 0.3.1 replaces the file, but
  `arcade-link ls` still reports 0.3.0 running; there's no restart prompt.
- **m6 Migrating from pre-self-installer Find 0.2.1.** Double-clicking 0.3.1 shows a plain "Install Arcade Find?"
  that doesn't mention the old copy. 0.2.1 keeps running through the single-instance handoff, and its file stays in
  `~/Applications` (`screenshots/j7-old-find021.png`, `j7-old-then-031-crop.png`).
- **m7 A `%` in HOME makes every menu entry unlaunchable.** Exec lines escape it as `%%` (spec-correct), but GLib
  refuses the entries ("Unable to load application information"). The same HOME without `%` works.
- **m8 Adoption makes useless rollback copies.** It copies every adopted app byte-for-byte into
  `~/Applications/Arcade/.previous` (383 MiB), so "rollback" would restore the same bytes.
- **m9 Read-only `~/Applications/Arcade`** gives a raw "Permission denied (os error 13)" without naming the folder.
  Good: no partial install is left (`screenshots/j7-ro-lens-result-crop.png`, `j7-ro-clip-result-crop.png`).
- **m10 Two install prompts open at once.** Install in the second prompt fails with "--install requires a real
  AppImage, not an ordinary or development binary." It should say the app is already installed. The end state is
  correct: one install, one receipt (`screenshots/j7-double-click-second-dialog.png`).
- **m11 The downloaded AppImage's FUSE mount lingers.** After installing with "Remove the downloaded file", the
  mount and runtime stay alive until the app quits (Clipboard, Find).
- **m12 Tools tray label is wrong with Link off.** It says "Arcade Clipboard (not running)" while Clipboard runs with
  Link turned off (`screenshots/j7-link-off-toolsmenu.png`).
- **m13 Clipboard's "Open Settings" desktop action** opens the clip list, not Settings.
- **m14 Link real-fleet `install` group fails on Tools' AppImage.**
  `arcade_tools_appimage_install_update_repair_uninstall_reexec: arcade.tools exited (0)` against the released
  0.2.1 AppImage, run locally (section 5). Not investigated; it may share F1's cause.

---

## 4. UX notes (nothing "failed", but a normal person would stumble)

**Install prompts**
- They differ across apps. Install is the last button in GTK prompts and the first in Qt/egui ones. "Start at login"
  is ticked for Find and Lens and unticked for Clipboard, Wheel and Shelf.
- Find's prompt and window open in varying places: bottom-left with 19 px off-screen, partly off-screen, sometimes
  centred (`screenshots/j2-find-01-prompt-crop.png`).
- Find's update prompt shows the arrow as a box: "Update Arcade Find 0.3.0 □ 0.3.1?"
  (`screenshots/j7-update-dblclick-crop.png`).
- Closing Lens's install prompt with the window's X runs Lens instead of cancelling.
- A double-click downgrade is refused safely, but the message doesn't say the file is older
  (`screenshots/j7-downgrade-find030-crop.png`).
- The disk-full dialog has a light-bulb icon; the message itself is clear (`screenshots/j7-diskfull-look-crop.png`).

**Clipboard**
- Plain history needs *Create mesh* first (`screenshots/j1-clip-04-mesh.png`).
- The app is called both "Mesh Clipboard" and "Arcade Clipboard"; Settings also says just "Arcade".
- The tray's "Private mode on/off" doesn't show the current state.
- Relative times ("2 min ago") don't refresh while the window is idle.

**Lens**
- No OCR action, and no hint why (Tesseract isn't installed).
- The "C" keycap hint types a "c" into the filter.

**Box**
- First run shows the hotkey as "control+alt+KeyB".
- Esc doesn't close the first-run card.

**Wheel**
- On X11/XFCE its global hotkey is unavailable. That's documented (it needs Wayland plus the GlobalShortcuts
  portal), but the in-app hint "Install xdg-desktop-portal…" points the user the wrong way
  (`screenshots/j1-wheel-03-shortcut-attention.png`).

**Tools: adoption**
- The card says "Choose *Let Arcade Tools manage this*", but the button is "Let Tools manage it", at the bottom of a
  long Details page under an unstyled list of about 70 items. It stays after adopting
  (`screenshots/j3-14-crop.png`, `j3-16-crop.png`).
- Adopting Lens, Look and Wheel opens their windows; Wheel's Settings window took a click meant for Tools.

**Tools: layout and states**
- Onboarding's bundle cards overlap their text (`screenshots/j3-22-onboarding-overlap.png`).
- The window jumps to Onboarding by itself.
- States contradict each other: "Loading…", "0 installed" and "every app is installed" can all appear for the same
  data (`screenshots/j3-11-tools-apps-5s.png` / `-15s` / `-30s`).
- Health messages end in "..".
- After *Install*, the Tools window disappears.

**Tools: shortcuts**
- The editor says "none bindings", records chords oddly and its layout breaks
  (`screenshots/j3-46-conflict-editor-layout.png`).
- A conflict is only reported after you confirm (`j3-42-crop.png`).
- The overlay shortcut can be edited, although the docs say it is fixed.

**Tools: other**
- Diagnostics leaves out the Lens, Wheel and Shelf logs. Redaction is good: home → `~`, no secrets
  (`screenshots/j3-49-diagnostics.png`).
- `arcade-tools --help` launches the GUI instead of printing help.
- Wheel's own tray icon stays about 3.1 s after Tools takes over (others under 60 ms; `logs/sni-tools-restart.log`).

**Docs**
- The release-status sections of each repo's `STATUS.md` name older versions.

---

## 5. Performance (Journeys 8, 8b) and developer suites (Journey 9)

### 8 / 8b budgets — Linux (Xvfb, no GPU). Windows/macOS: not run.

| Measure | Budget | Measured | Pass? | Method, sample |
|---|---|---|---|---|
| Startup added by tray-host watcher + `detect()` | ≤ 5 ms | — | **not measured** | Planned with/without Tools; not done. |
| Tray hand-back after `kill -9` Tools | ≤ 1 s (target ≤ 200 ms) | 43–102 ms per app (6 apps, Clipboard not running then) | ✅ on that run, but **sample too small** | `handback.py`: SIGKILL, poll the watcher every 10 ms. **1 run per app, not the required 20.** |
| Tools start/quit stability | (no budget) | 50/50 cycles: Tools hosted 1 item, all 7 own items back after quit, 0 orphans/zombies; fds/threads flat | ✅ | `logs/tools50.log`, `logs/fd-before.txt` vs `fd-after.txt`. Cycle 22 left one Tools process because I launched `arcade-tools --help` (it opens the GUI). |
| Tools idle RSS / CPU / wakeups | ≤ 40 MiB, 0 ticks / 30 s | — | **not measured** | |
| Tools window first paint (warm) | ≤ 400 ms | — | **not measured** | Also confounded by F1 (needs the workaround env). |
| Overlay `Super+/` → first frame | p95 ≤ 80 ms | — | **not measured** | |
| Shortcut index rebuild | ≤ 150 ms | — | **not measured** | |
| Per-app idle RSS / cold start / Link round-trip | ≤ 5 % vs STATUS.md | Look main 189 MiB + NetworkProcess ≈ 50 MiB after window close; Box 82 → 174 MiB after one Island open | ⚠️ (F8); baseline comparison not done | Single samples from `/proc/<pid>/status`. |
| 60-min soak | no growth | — | **not run** | |

### Journey 9 — developer suites

| Suite | Result | Notes |
|---|---|---|
| Arcade-Link unit tests (v0.3.0) | ✅ 35 OK, 2 skipped | |
| Link deterministic e2e (presence, install, trayhost, tools-hub) | ✅ 4/4 | The first run failed only because `install-harness` wasn't built; after `cargo build -p arcade-link --example install-harness --features install`, `install` passed. |
| Link real-fleet, local, against the released AppImages | install 7 pass / **1 fail** / 8 skip; trayhost 20 pass / 0 fail / 7 skip; tools-hub and shortcuts **did not finish** (the runner stopped with no result) | `logs/link-realfleet-local-summary.txt`. The skips are the development-build checks and Clipboard, whose release AppImage doesn't match the harness's "fresh build" component check. The fail is m14. |
| Link real-fleet in CI | green (runs 38868969998, 38865372945) | Read from the run conclusion only. Logs aren't reachable (section 6). |
| `cargo test` / `ctest` / `flutter test` / `npm run typecheck` on each repo's `main` | **not run** | |

**Test gaps** (a suite passes while the user journey fails):
- F3: the e2e tests `portable_backup.rs`; the GUI uses `backup.rs`.
- F5: CI runners have `libopengl0` preinstalled.
- F1: CI's Tools checks don't paint the webview under Xvfb, or they'd hit the crash.
- F2: no check starts a real app *from* Tools and looks at its environment or whether it's still running. The
  real-fleet trayhost checks also skip Clipboard entirely.

---

## 6. What I could not test, and why

- **Windows and macOS (Journeys 5, 6): not run.** There's no real machine. Running the CI workflows would mean
  pushing to main (not allowed), and the sandbox's network policy blocks `productionresultssa*.blob.core.windows.net`,
  where GitHub Actions keeps logs and artifacts, so no CI artifact could be downloaded or inspected. The CI
  conclusions above are context only.
- **Journey 3, partly:** updating and rolling back through Tools (including from pre-self-installer releases and
  while an app is busy), Tools self-update, and uninstalling Tools. Blocked first by F1, then by F9 (anonymous API
  limit). The Windows rollback notice doesn't apply on Linux.
- **Journey 4 (Leo, Tools first, fresh HOME): not run**, beyond the Find uninstall in F6.
- **Journey 7, partly:**
  - Run: double-click twice, deleted download, reboot, disk full, read-only folder, unicode/space/`%` HOME, PATH
    without `~/.local/bin`, missing keyring collection, downgrade, migration from 0.2.1, Link off, moved AppImage.
  - Not run: killing the installer at 50 %, killing an app mid-update, dropping the network mid-download, an offline
    catalog, a corrupted download, the clock moved forward a week. A corrupted download can't be served to a
    *release* Tools anyway: its loopback test source is debug-only (`src/source.rs`); Link's e2e covers it.
- **Journeys 8 and 8b:** mostly not measured (table above).
- **Real Wayland compositor and portals:** the desktop is X11 (Xvfb + Openbox), so Wheel's portal-only hotkey,
  layer-shell and Wayland tray behaviour weren't exercised.
- **Real GPU:** none. F1 is the visible consequence.

---

## Regression checks in `regression/`

Both run inside Arcade-Link's isolated runner (private D-Bus, Xvfb, keyring, temporary HOME). They refuse to run
anywhere else and exit 1 while their bug is present.

```sh
cd Arcade-Link
python3 tools/e2e.py run -- python3 ../Arcade-catalog/dev/stress-2026-10/regression/clipboard_answer_fd.py /path/Arcade-Clipboard-0.1.0-x86_64.AppImage
cp /path/Arcade-Clipboard-0.1.0-x86_64.AppImage /tmp/copy/   # the scripted install consumes its source (m2)
python3 tools/e2e.py run -- python3 ../Arcade-catalog/dev/stress-2026-10/regression/clipboard_tray_late_watcher.py /tmp/copy/Arcade-Clipboard-0.1.0-x86_64.AppImage
python3 tools/e2e.py run -- python3 ../Arcade-catalog/dev/stress-2026-10/regression/clipboard_tray_late_watcher.py /tmp/copy2/Arcade-Clipboard-0.1.0-x86_64.AppImage --control
```

| Check | Today |
|---|---|
| `clipboard_answer_fd.py` (m1) | **FAIL** (file overwritten; socket exit 1) |
| `clipboard_tray_late_watcher.py` (F4) | **FAIL**; `--control` PASS |

Planned but not written: the Tools webview staying alive under Xvfb (F1), the environment of apps Tools starts plus
*Start all* → Clipboard running (F2), the GUI backup including Lens and Shelf (F3), the Wheel AppImage's library
dependencies (F5), and Find's live rebind on X11 (F7).

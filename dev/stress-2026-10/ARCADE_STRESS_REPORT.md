# Arcade real-user stress test, October 2026

> **Status: draft.**
> - **Done and reported:** Journeys 1–4 and 7, plus most of Journey 8b.
> - **Pending:** soak analysis, 20-run hand-back, Link round trip, verification of three regression checks, the
>   per-repo test suites, and a source-level review for code and UX problems.
>
> This file is updated on the same branch as those finish.

Brief: `dev/CLOUD_STRESS_TEST_PROMPT.md`. Run on 2026-10-16 (UTC) by a cloud coding agent in a Linux container,
acting as a user would and using only the released files. Every row below was run. Anything not run says
**not run** and section 6 gives the reason.

**Releases tested** (all downloaded from GitHub Releases; every `SHA256SUMS` and release manifest verified):

| App | Release tested | Older releases used for update / rollback / migration |
|---|---|---|
| Arcade Find | v0.3.1 | v0.3.0 (self-installing), v0.2.1 (pre-self-installer) |
| Arcade Lens | v0.2.0 | v0.1.1 (pre-self-installer) |
| Arcade Look | v0.2.1 | v0.2.0 (self-installing); v0.1.2 downloaded, not exercised |
| Arcade Box | v0.2.1 | v0.2.0 (self-installing); v0.1.2 downloaded, not exercised |
| Arcade Shelf | v0.2.0 | v0.1.1 (pre-self-installer) |
| Arcade Wheel | v0.3.1+build.56 | v0.3.0+build.48 (self-installing); v0.2.0+build.33 downloaded, not exercised |
| Arcade Clipboard | v0.1.0 | none (first stable) |
| Arcade Tools | v0.2.1 | v0.2.0 (self-update source and rollback target); v0.1.0 downloaded, not exercised |
| Arcade Link (CLI and e2e harness) | built from tag v0.3.0 | none |

**Test desktop.**
- **Base:** an Ubuntu 24.04 container (4 vCPU, 16 GB).
- **Display:** Xvfb at 1920×1080, with no GPU and no DRI3.
- **Desktop:** the Openbox window manager and an xfce4-panel whose systray plugin is the StatusNotifier watcher and host.
- **Services:** a real gnome-keyring and a D-Bus session bus. FUSE is available, with `/dev/fuse` set to the usual 0666.
- **Users:** each persona is a normal non-root user with its own X display and session:

| Persona | Used for |
|---|---|
| maya | Journeys 1–3, 7 and 8 |
| upd | Update and rollback, starting from older releases |
| leo | Journey 4: Tools first, on a fresh HOME |
| kim | Killing an app's own installer |
| zoe | HOME `/home/Zoë Ångström %` |
| zoe2 | HOME `/home/Zoë Ångström` |
| tiny | HOME on a 64 MiB tmpfs |
| old | Pre-self-installer Find |
| bench | Benchmarks |

A downloaded file is opened the way a file manager does: copied into `~/Downloads`, `chmod +x`, executed detached.

**Deviations from a real user's machine** (they apply to every Tools step after Journey 3 step 1):
1. **WebKit workaround.** Tools ran with `WEBKIT_DISABLE_COMPOSITING_MODE=1`. Without it its window is blank on this
   display (F1).
2. **Authenticated GitHub access.** The sandbox's shared IP had used up GitHub's anonymous limit of 60 API calls an
   hour (F9). For the update and rollback runs (upd), Leo's journey and the abuse tests, Tools' traffic therefore
   went through the sandbox's egress proxy, which authenticates GitHub API calls. For the network-drop and
   corrupted-download tests a local mitmproxy sat in front of that proxy.

Evidence:
- Screenshots in [`screenshots/`](screenshots/); names start with the journey or persona (`j3-…`, `upd-…`, `leo-…`).
- Logs and measurements in [`logs/`](logs/).
- Failing regression checks in [`regression/`](regression/).

---

## 1. Verdict

**Partly.** On Linux, a user who installs the apps **from their own downloads and never installs Tools** gets
what was promised:

- Each app installs from its own prompt.
- The apps find each other and work together: Find → Shelf, Find → Look, Lens → Clipboard, drag and drop with Shelf,
  Wheel launching apps.
- They survive a reboot, a second double-click and a deleted download.
- Removing Tools later hands every icon back within half a second.

**Arcade Tools is where real users get hurt:**

- **Blank window.** On X servers without DRI3 (VNC, xrdp, VMs without 3D, Xvfb) the window is blank, including its
  install prompt.
- **Clipboard can't run under Tools.** Every app Tools starts inherits Tools' AppImage environment. So Clipboard
  never starts from Tools, and that includes a Clipboard installed from Tools' own catalog. Adopting Clipboard
  silently turns clipboard history off.
- **Backup.** "Back up settings" still leaves out Lens and Shelf.
- **Migration.** Tools can't adopt or update the pre-self-installer releases, so it can't migrate those users.
- **Uninstall.** Its menu "Uninstall" removes Tools silently, while Tools keeps running.
- **Budgets.** Its idle memory is about five times the budget, and the shortcut overlay takes about twice its latency
  budget.

**What works in Tools:**

- Updating, rolling back and self-updating between self-installing releases, with all settings kept.
- It refuses to update a busy app and doesn't touch the running job.
- It rejects a corrupted download.
- It recovers cleanly from a killed download or a dropped network.

**Other problems:**

- Wheel's AppImage does nothing on a system without `libopengl0`.
- Clipboard autostarted before the panel gets no tray icon for the session, and quits when its window is closed.

**Windows and macOS were not run** (section 6).

---

## 2. Matrix

Legend: ✅ works · ❌ broken · ⚠️ works but with a real problem (see the finding) · **nr** = not run · n/a = not applicable.
"Update" and "rollback" mean through Tools unless the cell says otherwise.

### Linux (Xvfb + Openbox + xfce4-panel)

| App | Standalone install | Install via Tools | Adoption | Update | Rollback | Uninstall | Works with others, no Tools | Tray hand-off |
|---|---|---|---|---|---|---|---|---|
| Clipboard 0.1.0 | ✅ | ❌ installs but never starts (F2) | ❌ stops Clipboard (F2) | nr (no newer release) | nr (no older release) | nr | ✅ | ⚠️ hand-back ✅; ❌ login race (F4) |
| Find 0.3.1 | ✅ | ✅ | ✅ | ✅ 0.3.0→0.3.1, settings and shortcut kept | ✅ | ✅ own uninstaller; ⚠️ Tools keeps a stale record (F6) | ✅ | ✅ (⚠️ 190 ms own-icon flash during its own uninstall) |
| Lens 0.2.0 | ✅ | ✅ (also refuses a corrupted download) | ✅ 0.2.0; ❌ 0.1.1 can't be adopted (F10) | ❌ from 0.1.1 (F10); manual download leaves 0.1.1 in the menu and login (F11) | nr | ✅ via Tools, including data | ✅ | ✅ |
| Look 0.2.1 | ✅ | ✅ (recovers after Tools killed mid-install) | ✅ | ✅ 0.2.0→0.2.1 | ✅ | ✅ via Tools; ⚠️ WebKit data left (m15) | ✅ | ✅ |
| Box 0.2.1 | ✅ | ✅ (reinstall reuses kept data) | ✅ | ✅ 0.2.0→0.2.1; busy Box refused, job kept | ✅ | ✅ via Tools; ⚠️ documented `arcade-box` command missing (m3) | ✅ | ✅ |
| Shelf 0.2.0 | ✅ | ✅ (cancel mid-download is clean; retry works) | ✅ 0.2.0; ❌ 0.1.1 can't be adopted (F10) | ❌ from 0.1.1 via Tools (F10); ✅ manual download keeps held items | nr | ✅ own `arcade-shelf --uninstall`; ⚠️ stale Tools record (F6) | ✅ | ✅ |
| Wheel 0.3.1 | ⚠️ needs host `libopengl0` (F5) | ✅ | ✅ | ✅ 0.3.0→0.3.1 | ✅ | nr | ✅ (stale action list, m4) | ✅ (own icon lingers ~3 s on collapse) |
| Tools 0.2.1 | ❌ blank without DRI3 (F1); ✅ with the workaround | n/a | n/a | ✅ self-update 0.2.0→0.2.1 | ✅ self-rollback 0.2.1→0.2.0 | ⚠️ silent; no "Tools only" option (F12) | n/a | ✅ collapse 7→1; hand-back within 0.5 s |

### Windows CI, macOS arm64 CI, macOS Intel CI

| App | All eight columns |
|---|---|
| All 8 apps | **nr**: no real machine, and CI logs and artifacts are not reachable from this sandbox (section 6). |

---

## 3. Findings, worst first

Each finding gives:
- the severity;
- steps, expected and actual results;
- evidence;
- the suspected cause.

Commands ran as the persona inside its own desktop session.

### F1 · blocker · Tools 0.2.1 window is blank on X servers without DRI3
- **Steps:** maya, with seven apps already running and seven tray icons, double-clicks
  `Arcade-Tools_0.2.1_amd64.AppImage` in `~/Downloads`.
- **Expected:** the "Install Arcade Tools?" prompt, then the Tools window.
- **Actual:**
  - The window stays white; checked at 5, 15 and 25 s.
  - The tray has already collapsed to Tools' single icon, so the user loses every icon and has nothing to click.
  - `strace -f` shows `WebKitWebProcess` dying with `SIGSEGV {si_code=SEGV_MAPERR, si_addr=0x40}` about 0.9 s after start.
- **Narrowing:**
  - Look 0.2.1 ships the same `libwebkit2gtk-4.1.so.0` (sha256 `bad3b5ee…`) and renders fine on this display.
  - `WEBKIT_DISABLE_COMPOSITING_MODE=1` or `WEBKIT_DISABLE_DMABUF_RENDERER=1` fixes it; `LIBGL_ALWAYS_SOFTWARE=1` does not.
  - The same happens on fresh HOMEs (Leo, upd).
- **Evidence:** `screenshots/j3-02-tools-prompt.png`, `j3-03-tools-window-25s.png`, `j3-06-tools-with-workaround.png`,
  `j3-tray-before-after.png`. Regression check: `regression/tools_webview_alive.py`.
- **Suspected cause:** `Arcade-tools src-tauri/src/desktop.rs:115-121` sets `HardwareAccelerationPolicy::Never`
  after the webview is built. That's the only difference from Look.
- **Who is affected:** VNC and xrdp users, VMs without 3D, Xvfb and CI, and probably the NVIDIA proprietary X11 driver.

### F2 · major · Apps started by Tools inherit Tools' AppImage environment, so Clipboard never runs under Tools
- **Steps (any of these):**
  - Tools tray → *Start all Arcade apps*.
  - Adopt Clipboard.
  - Press *Open* on Clipboard's card.
  - Leo (fresh HOME, Tools first) installs Clipboard from Tools' catalog.
- **Expected:** Clipboard starts, and every app runs with the user's environment.
- **Actual:**
  - **The environment:** children get Tools' mount variables (`LD_LIBRARY_PATH=/tmp/.mount_Arcade…/usr/lib…`,
    `GTK_THEME=Adwaita:light`, `PYTHONHOME`, `GIO_MODULE_DIR`, `GTK_PATH`, and an `XDG_DATA_DIRS` that starts with
    Tools' mount). See `logs/env-of-app-started-by-tools.txt`.
  - **Clipboard:** it exits with `undefined symbol: g_once_init_enter_pointer` (exit 127;
    `logs/clipboard-started-by-tools.log`). *Start all* leaves 6 of 7 running. Adoption stops Clipboard's capture
    silently. For Leo, Clipboard installs but never appears in Link's registry, and *Open* does nothing, with no
    error (`screenshots/leo-14b.png`). Started from the menu, it runs.
  - **Wheel:** a Wheel started by Tools can't launch LibreOffice (`screenshots/j3-39-wheel-clean-launches-lo.png`).
    Leo's Wheel built its default deck from Tools' `XDG_DATA_DIRS`: "Arcade Tools" appears twice, and one entry is
    `Arcade Tools.desktop`, which exists only inside Tools' temporary mount (`screenshots/leo-15-wheel.png`).
  - **Engines:** Tools' Engines tab reports LibreOffice as missing, because its own `soffice --version` probe fails
    the same way (`screenshots/j3-21-engines.png`).
  - **Theme:** apps Tools starts are forced to the light theme.
- **Regression check:** `regression/tools_start_all_child_env.py` clicks *Start all* through Tools' DBusMenu.
- **Suspected cause:** `Arcade-tools src/manager.rs` (start, adopt and restart) and `src/engines.rs` spawn children
  with the inherited environment. The AppImage runtime variables need to be stripped or restored first.

### F3 · major (and a test gap) · Tools "Back up settings" still leaves out Lens and Shelf
- **Steps:** Tools → Settings → *Back up settings*, then *Restore*.
- **Expected:** all seven apps are backed up. The Tools 0.2.0 and 0.2.1 notes list the Lens and Shelf backup bugs
  as fixed.
- **Actual:**
  - Lens: "App returned an invalid settings handoff."
  - Shelf: "expected value at line 1 column 1".
  - The backup file contains 5 apps (`unzip -l` shows box, clipboard, find, look, wheel).
  - The restore plan still lists Lens and Shelf as "will be replaced", by raw ID.
- **Evidence:** `screenshots/j3-54-backup-confirm.png`, `j3-55-restore-plan.png`, `j3-56-restore-result.png`,
  `j3-57-restore-result.png`.
- **Suspected cause:**
  - The GUI calls `src/hub.rs:356 export_backup` → `src/backup.rs`.
  - `src/backup.rs:98` requires `kind == "file/any"`, but Lens exports `file/code`.
  - `src/backup.rs:374-378` runs `serde_json::from_slice` on every export, but Shelf's export is binary.
  - The e2e suite tests `src/portable_backup.rs`, a different module, so CI is green.
- **No regression check:** Tools has no command line or Link method for its backup, so a check would need the webview.

### F4 · major · Clipboard started before the tray host never gets a tray icon, then quits when its window closes
- **Steps:** at login, autostart runs `clipboard --background` a few seconds before the panel's watcher appears.
  Later the user closes the Clipboard window.
- **Expected:** the icon appears when the watcher does, and Clipboard keeps running in the background.
- **Actual:**
  - The window is shown and no icon appears for the whole session.
  - Closing the window quits Clipboard, although *Keep running in the background* is on, so history capture stops
    silently.
  - Wheel and Shelf fall back to XEmbed icons in the same situation.
- **Evidence:** `screenshots/j1-all-reboot-20s-tray.png`. Regression check:
  `regression/clipboard_tray_late_watcher.py` FAILS; its `--control` passes.
- **Suspected cause:** `Arcade-clipboard platform/desktop/arcade_desktop_bridge/linux/lifecycle_bridge.cc` (about
  lines 520-534). `setBackgroundEnabled` checks `TrayHostAvailable()` once, and the watcher's name-owner watch is
  installed only inside `OpenTray`.

### F5 · major (and a test gap) · The Wheel AppImage silently does nothing without `libopengl0`
- **Steps:** on a host without the `libopengl0` package (it was missing on this Ubuntu 24.04 image), double-click
  `ArcadeWheel-0.3.1-Linux-x86_64.AppImage`.
- **Expected:** the install prompt, or at least an error dialog.
- **Actual:** nothing visible. From a terminal:
  `AppRun.wrapped: error while loading shared libraries: libOpenGL.so.0`.
- **Cause:**
  - The bundled `usr/lib/libLayerShellQtInterface.so.6` has `NEEDED libOpenGL.so.0`, which linuxdeploy's exclude
    list leaves to the host.
  - `libopengl0` comes in with Qt6 GUI and development packages; whether a stock desktop install has it was not
    checked.
  - GitHub's runner images have it, so CI never sees this.
- **Regression check:** `regression/wheel_appimage_needs_libopengl.py` FAILS. It only reads ELF headers and runs anywhere.

### F6 · major · Tools keeps a stale record when an app uninstalls itself
- **Steps:**
  - maya: Find is managed by Tools, and the user picks *Uninstall* from Find's menu entry.
  - Leo: Find is uninstalled through its menu action, and Shelf through `arcade-shelf --uninstall`.
- **Expected:** Tools shows the app as not installed and offers it under *Available*.
- **Actual:**
  - Tools shows "Needs repair · Installed executable is missing" for both.
  - *Available* doesn't list them; maya even saw "Every app in the catalog is installed".
  - *Refresh* doesn't help.
  - The records stay in `~/.local/share/arcade-tools/arcade.<id>.json`.
- **Evidence:** `screenshots/j3-30-apps-after-find-uninstall.png`, `j3-32-after-refresh.png`, `leo-24b.png`.

### F7 · major · Rebinding Find's shortcut from Tools leaves no working shortcut on X11 until Find restarts
- **Steps:** Tools → Shortcuts → Find: change Ctrl+Alt+F to Ctrl+Alt+G, then press each chord.
- **Expected:** Ctrl+Alt+G opens Find straight away.
- **Actual:**
  - Tools shows "Applied · native" and the manifest is updated.
  - Neither chord opens Find until Find restarts.
  - Restoring the *same* chord, the case 0.3.1 fixed, works (`screenshots/j3-58-find-after-restore.png`).
- **Evidence:** `screenshots/j3-40-shortcuts.png`, `j3-41-change-shortcut.png`, `j3-44-after-apply.png`.
  Regression check: `regression/find_live_rebind.py`.

### F8 · major (the release notes say this was fixed) · Look and Box keep a WebKit network process after their window closes
- **Steps:** open, then close Look's window, or open and close Box's Island. Sample processes for several minutes.
- **Expected:** the web processes are released.
- **Actual:**
  - `WebKitWebProcess` goes, but `WebKitNetworkProcess` (about 50 MiB) stays: more than 3.5 min for Look, and more
    than 60 s with the same PID for 2.5 min for Box.
  - Box goes from 82 MiB before the first Island open to 174 MiB after it.
  - Tools has the same pattern: its 48 MiB network process outlives its window (F13).

### F9 · major · Tools' install, repair and update depend on GitHub's anonymous API limit
- **Steps:** Tools → *Install*, *Repair* or *Check for updates* from an IP that has used up its anonymous budget.
- **Actual:**
  - `HTTP status client error (403 Forbidden) for url (https://api.github.com/repos/qa-p1/Arcade-Find/releases/latest)`,
    shown as a raw red banner away from the button that caused it.
  - *Repair* reports nothing.
  - The limit is 60 requests an hour per IP. NAT, CGNAT, office and university networks share IPs.
- **Measured** (on the authenticated proxy, through mitmproxy's log and the `rate_limit` counter):
  - The first update check of 8 apps used 8 counted calls.
  - A Tools start plus opening Apps used 5.
  - A repeat check used 0, because ETags work.
  - Each check also requests `releases/tags/nightly` for every app (F14), so it makes twice the requests needed.

### F10 · major · Tools can't adopt or update pre-self-installer apps (Shelf 0.1.1, Lens 0.1.1)
- **Steps:** upd, with Shelf 0.1.1 in `~/Applications` and Lens 0.1.1 in `~/Downloads`, as their READMEs said.
  - Tools → Shelf → *Let Tools manage it* → *Adopt*.
  - Then *Update* → *Confirm* → *Update*.
- **Expected:** the brief calls this the real-world migration path. Tools should migrate the user to 0.2.0, or
  explain how to.
- **Actual:**
  - *Adopt* runs the old AppImage with installer flags. The result is a red raw
    "ArcadeShelf: Unknown options: install, silent, channel, no-launch", and the app restarts as a side effect.
    Lens fails the same way ("…install-XUonq8.AppImage failed (exit status: 1): arcade-lens: …").
  - *Update* asks twice. The second dialog says "Installed outside Arcade Tools. Choose Let Arcade Tools manage
    this", then refuses: "Let Arcade Tools manage this installation first."
  - The only way out is to download 0.2.0 by hand.
- **Evidence:** `screenshots/upd-14-shelf-adopt-crop.png`, `upd-16-shelf-adopt-top-crop.png`,
  `upd-17-shelf-update-click-crop.png`, `upd-18-shelf-update-3-crop.png`, `upd-21-shelf-update-top-crop.png`,
  `upd-23-lens-adopt-result-crop.png`.

### F11 · major · Lens 0.2.0 installed over Lens 0.1.1 leaves the menu and login on 0.1.1
- **Steps:** Lens 0.1.1 ran from `~/Downloads` and added itself to the menu and login. The user double-clicks Lens
  0.2.0 and chooses *Install*, then reboots.
- **Expected:** the menu entry, *Capture* action and login start 0.2.0.
- **Actual:**
  - The receipt lists the desktop entry, 6 icons and the autostart entry as "existing entry belongs to another
    installation".
  - `arcade-lens.desktop`, including its *Capture* and *Quit* actions, and `autostart/arcade-lens.desktop` still run
    `~/Downloads/ArcadeLens-0.1.1-linux-x86_64.AppImage`.
  - Only the `arcade-lens` command runs 0.2.0.
  - After a reboot, Link shows Lens **0.1.1** running.
  - Shelf 0.1.1 had no menu entry, so its manual migration is clean, apart from the old file and old process (m6).
- **Evidence:** the receipt's `integration.skipped` list, and `logs/` (upd autostart log).

### F12 · major · Tools' menu "Uninstall" removes Tools silently, and there is no "uninstall Tools only"
- **Steps:** upd, with Tools running, picks *Uninstall* from Tools' menu entry
  (`Arcade-Tools.AppImage --uninstall`).
- **Expected:** a confirmation, then Tools goes away and the apps keep working with their own icons.
- **Actual:**
  - **Silent removal:** there's no dialog or feedback. The Tools AppImage, receipt, menu entry, autostart, command
    and icon are removed.
  - **Tools keeps running:** the running Tools keeps its window and tray. Its About page then says "Installed
    executable is missing. Choose Repair" and offers "Install Arcade Tools for this user".
  - **No Tools-only option:** Settings only offers *Uninstall Arcade…*, which removes every managed app and then Tools.
  - **Apps still list Tools:** their receipts still say `managedBy: tools`.
  - **Leftovers:** `autostart/arcade-tools.desktop.arcade-tools.bak` and the `.previous/tools-arcade.*` folders.
  - **What works:** after the user quits that Tools, all seven apps had their own icons back within 0.5 s, and
    cross-app calls still work.
- **Evidence:** `screenshots/upd-53-uninstall.png`, `upd-54-tools-settings-crop.png`, `upd-55-cli-uninstall.png`,
  `upd-56-tray.png`.
- **Cause:** `Arcade-tools src-tauri/src/installation.rs:321-331` runs the uninstall straight away on `--uninstall`.
  The `.desktop` action calls that path.

### F13 · major (performance budget) · Tools idle is 202 MiB and wakes about once a second
- **Steps:** Leo, Tools hosting the tray, window closed for more than 15 s.
- **Budget:** ≤ 40 MiB RSS, 0 polling, 0 CPU ticks over 30 s.
- **Actual:**
  - **Memory:** tree RSS **202 MiB**: `arcade-tools` 155 MiB (PSS 82 MiB) plus a 48 MiB `WebKitNetworkProcess` that
    outlives the window.
  - **CPU:** 0 ticks in 30 s, within budget.
  - **Polling:** `strace -c -f` shows 4,644 `read` calls in 30 s. Thread `PressureMonitor` (WebKit's memory-pressure
    monitor) reads `/proc/meminfo` one byte at a time, plus cgroup memory files, about once a second.
- **Evidence:** `logs/tools-idle-strace.txt`, `logs/tools-idle-reads.txt`.
- **Suggestion:** drop the whole WebKit context, including the network process and pressure monitor, when the window
  closes, or move hosting into a separate small process.

### F14 · major (performance budget) · The shortcut overlay takes about 150 ms to appear
- **Steps:** Super+/ (Tools' overlay hotkey) pressed 25 times with `xdotool`, timed until the
  "Arcade Tools Shortcuts" window is mapped and painted.
- **Budget:** p95 ≤ 80 ms.
- **Actual:** n=24 warm presses: median **154 ms**, p95 **179 ms**, max 212 ms. The method adds up to about 20 ms.
- **Cause:** `Arcade-tools src-tauri/src/hotkey.rs:42-46`: every press `spawn_detached`es a new
  `arcade-tools-overlay --toggle` process, so each open pays a process start.
- **Test gap:** Link's `shortcuts` group passes `real_overlay_paints_its_first_frame_under_xvfb` without timing it.
- **Evidence:** `logs/overlay-latency.txt`.

### F15 · major · Wheel spends about 1 s of CPU on every clipboard copy, and reads every copied item
- **Steps:** with Wheel running in the background and its wheel never opened, copy any text with `xclip`.
- **Expected:** a resident launcher costs nothing while idle.
- **Actual:**
  - **CPU:** 99–121 CPU ticks (about 1 s) per copy, whatever the size: a 20-byte string costs as much as 2.7 MB.
    It's 0 when nothing is copied. Measured on maya during the soak (81.8 s of Wheel CPU in 60 min) and on a freshly
    started Wheel for Leo.
  - **Who pays:** anyone who copies often pays it on every copy; on a laptop that's battery drain.
- **Cause:** `Arcade-wheel src/providers/ArcadeLinkProvider.cpp:391` subscribes to `QClipboard::dataChanged`. In
  `:414-428` it then:
  - reads the text, HTML, URLs and any image of every new clipboard item on the GUI thread;
  - emits `changed()` twice per copy (once to clear, once when the worker has converted it), which rebuilds the
    action model.
- **Privacy:** every copied item, passwords from a password manager included, is pulled into Wheel's memory and
  converted the moment it's copied, even if the wheel is never opened.
- **Fix:** read the clipboard lazily when the wheel opens.

### F16 · major (budget) · Wheel's tray hand-back takes over half a second in about half the runs
- **Steps:** `kill -9` Tools 20 times while all seven apps run (maya).
- **Expected:** each app's own icon is back within 200 ms (limit 1 s).
- **Actual:**
  - Six apps came back in a median of 22–31 ms (p95 ≤ 45 ms).
  - Wheel was bimodal: 10 runs at 30–58 ms and 9 at 580–1107 ms, over 1 s once.
  - The ~3 s for Wheel's own icon to go away when Tools takes over is the same symptom in the other direction.
- **Evidence:** `logs/handback-maya.jsonl`.

### Minor

**Tools: update checks and leftovers**
- **m16 Nightly 404s fail every check.** Tools 0.2.0 and 0.2.1 query `releases/tags/nightly` for every installed
  app, managed or not. The 404s for Find, Shelf, Tools and Wheel set `lastSuccess: null` and show a raw red
  "Last check issue: … Arcade-wheel/releases/tags/nightly", although every stable lookup succeeded. Tools also works
  out meaningless nightly "updates", such as Clipboard `0.1.0-nightly.8 > 0.1.0`
  (`screenshots/upd-07-after-check-crop.png`).
- **m17 Transaction folders are never cleaned up.** Every Tools install, update or rollback leaves a
  `.previous/tools-<id>-XXXX/` folder holding a full extra AppImage, even after success. `.previous` reached 501 MB
  for 5 apps on upd. Adoption also copies byte-identical "previous" builds (m8).
- **m18 Killed or interrupted Tools jobs leave temporary files.**
  - `kill -9` of Tools during the install copy left 233 MB in `~/.cache/arcade-tools/downloads`.
  - It also left a `.previous/tools-arcade.look-*` folder. Neither is cleaned up on restart.
  - Nothing half-installed reached `~/Applications`, and the retry worked.
- **m19 The busy check comes after the download.** Tools downloads the whole update (118 MB for Box) and only then
  refuses because the app is busy. The confirmation doesn't mention that the app is busy. The refusal itself is
  correct, and the job finished.
- **m20 Old AppImage runtimes stay alive.** Each Tools self-update or rollback leaves the previous Tools AppImage
  runtime and its FUSE mount running: five after three cycles. Once, a runtime outlived
  `arcade-link quit tools` by more than 18 min.

**Install and uninstall leftovers**
- **m21 A killed self-installer leaves a `.stage` file.** `kill -9` of Look's own installer early in its copy left
  `~/Applications/Arcade/Arcade-Look.<sha256>.stage` (7.8 MB). The next install works, but the `.stage` file is never
  removed.
- **m15 Look's WebKit data survives removal.** *Remove settings and data* for Look removes only
  `~/.config/arcade-look`; `~/.local/share/app.arcadelook` (WebKit storage) stays. `docs/uninstalling.md` lists the
  same single folder.
- **m22 Find flashes its own icon while uninstalling.** Its `--uninstall` process registered its own tray item for
  about 190 ms while Tools hosted the tray. That was the only flash seen in Leo's whole journey
  (`logs/leo-sni.log`).

**Error messages**
- **m23 A network drop ends in a raw, hidden error.** The download ends after 20–30 s with only a raw red
  "Arcade Look: request or response body error" at the top of the page. The card just reverts to *Check & install*.
- **m24 Offline refresh claims success.** With no network, *Refresh catalog* says "Catalog refreshed (2026-10-11)."
  instead of saying it's offline and showing cached data. A restart while offline shows the cached catalog fine.

**Clipboard and Box**
- **m1 Clipboard's command-line answers overwrite or fail.** `--version`, `--arcade-manifest` and
  `--integration-status` reopen stdout through `/proc/self/fd/$ARCADE_ANSWER_FD`. A redirected file loses its earlier
  content, and a socket stdout fails with exit 1. `regression/clipboard_answer_fd.py` FAILS.
  Code: `apps/flutter_app/lib/main.dart:54-60` and `linux/runner/my_application.cc:144`.
- **m3 Box's command is misnamed in the docs.** Box links only `arcade-desktop` into `~/.local/bin`.
  `docs/uninstalling.md:11` and Box's README say `arcade-box`, which is bundled inside the AppImage but not installed.

**Updates, migration and placement**
- **m2 `--install --silent` deletes its source.** It deletes the source AppImage wherever it is, not only in
  `~/Downloads`. This isn't documented and there is no `--keep` option.
- **m4 Wheel's app list goes stale.** It doesn't pick up apps installed after it started (*Refresh* is needed), and
  their icons stay generic until a restart. Leo's deck lacked all five apps installed after Wheel.
- **m5 A double-click update leaves the old version running.** Find 0.3.0 → 0.3.1 replaces the file, but the running
  0.3.0 instance keeps running.
- **m6 Migration from a pre-self-installer release leaves the old version behind** (Find 0.2.1 and Shelf 0.1.1):
  - The prompt is a plain "Install Arcade X?" that doesn't mention the old copy.
  - The old process keeps running.
  - The old file stays in place.
  - Shelf's held items do carry over.
- **m7 A `%` in HOME breaks every menu entry.** The entries are spec-correct (`%%`), but GLib refuses them
  ("Unable to load application information").
- **m9 A read-only `~/Applications/Arcade` gives a raw error.** It shows "Permission denied (os error 13)" without
  naming the folder. Nothing partial is left.
- **m10 A second install prompt gives a misleading error.** With two prompts open, *Install* in the second says
  "--install requires a real AppImage…".
- **m11 The download's FUSE mount lingers.** The `~/Downloads` AppImage's mount and runtime stay alive until the app
  quits.
- **m12 Tools' tray label is wrong with Link off.** It says "Arcade Clipboard (not running)" while Clipboard runs with
  Link off.
- **m13 Clipboard's *Open Settings* action opens the clip list.**

**m14 Link real-fleet `install` group (local run against the release AppImages):**
`arcade_tools_appimage_install_update_repair_uninstall_reexec` fails with "arcade.tools exited (0)".
- **What the check expects:** Arcade-Link `tools/e2e_checks/real_hub.py:137-141` runs `--install --silent` without
  `--no-launch` and expects that process to re-exec into the installed package and serve the Link.
- **What Tools does:** it `spawn_detached`es a `--background` copy and exits 0
  (`Arcade-tools src-tauri/src/installation.rs:313-318`).
- **User-visible effect:** the Tools window disappears after *Install* (UX note). Either Tools or the contract needs
  to change.

---

## 4. UX notes (nothing "failed", but a normal person would stumble)

**Install prompts and first runs**
- **Inconsistent prompts.** Install is the last button in GTK prompts and the first in Qt and egui ones.
  "Start at login" is ticked for Find, Lens, Look and Tools, and unticked for Clipboard, Wheel and Shelf.
- **Prompts open in odd places.** Find's prompt and window open in varying places, sometimes partly off-screen.
  Lens 0.2.0's prompt opened at the bottom-right edge.
- **Missing glyph.** Find's update prompt shows "Update Arcade Find 0.3.0 □ 0.3.1?": the arrow glyph is missing.
- **Closing a prompt starts the app.** Closing Lens's install prompt with the window's X launches Lens.
- **Downgrade message.** A double-click downgrade is refused safely, but the message doesn't say the file is older.
- **Wrong icon.** The disk-full dialog has a light-bulb icon.

**Tools: install, updates and rollback**
- **Inconsistent confirmations.** Tools' self-update starts on *Review update* without a confirmation; app updates
  ask first.
- **"Same mode" isn't honoured.** Rollback says it will "reopen in the same mode", but background apps come back with
  their windows open (Find, Look, Wheel Settings). Adoption opens windows too (Lens, Look, Wheel).
- **Contradictory status.** The Updates page says "You are up to date" next to "Last check: Not checked yet".
- **Confusing labels and badges.** "Roll back" is shown for a *newer* saved version. Badges show raw values like
  `rolled_back`. A failed row shows "— → —". The *Update all* dialog runs app names together.
- **Raw IDs and silent cancel.** The progress toast uses raw IDs ("arcade.tools · Downloading"), and *Cancel* gives
  no "Cancelled" message.
- **Broken media and stuck notes.** Shelf's Details screenshot is a broken image, and "Preparing sanitized release
  notes…" never finishes.
- **Leftover autostart backup.** Running Tools from `~/Downloads` with "Start at login" ticked first writes an
  autostart entry pointing at the download. The installer then leaves `arcade-tools.desktop.arcade-tools.bak` behind
  on every fresh HOME.

**Tools: layout and pages**
- **Adoption is hard to find.** The card says "Choose Let Arcade Tools manage this". The button is called
  "Let Tools manage it" and sits at the bottom of a long Details page under an unstyled list of about 70 items.
  It stays after adopting.
- **Overlapping text.** Onboarding's bundle cards overlap their text.
- **Pages switch on their own.** The window jumps to Onboarding by itself.
- **Contradictory states.** "Loading…", "0 installed" and "every app installed" appear together.
- **Messages.** Health messages end in "..". Errors appear at the top of the page, out of view.
- **Shortcut editor.** It says "none bindings" and records chords oddly. A conflict is reported only after you
  confirm. The overlay shortcut can be edited although the docs say it is fixed.
- **Diagnostics.** The export leaves out the Lens, Wheel and Shelf logs, and `--help` launches the GUI.
- **Install hides the window.** After *Install*, the Tools window disappears because Tools relaunches in the
  background.

**Clipboard, Lens and Box**
- **Clipboard:**
  - Plain history needs *Create mesh* first.
  - It's called both "Mesh Clipboard" and "Arcade Clipboard".
  - The tray's "Private mode on/off" doesn't show its state.
  - Relative times don't refresh while idle.
- **Lens:**
  - There's no OCR and no hint why (Tesseract isn't installed; 0.1.1's settings offer *Download Tesseract*).
  - The "C" keycap hint types into the filter.
- **Box:** first run shows the hotkey as "control+alt+KeyB", and Esc doesn't close the first-run card.

**Wheel and docs**
- **Wheel:** its X11 hotkey is unavailable (documented). Its "Install xdg-desktop-portal…" hint is misleading on
  X11. Its own icon stays about 3.1 s when Tools takes over.
- **Docs:** the release-status sections of each repo's `STATUS.md` name older versions.

---

## 5. Journeys step by step

Each table gives what I did, what I expected, what happened and the evidence. Screenshots are under `screenshots/`.

### Journey 1: Maya, Linux, just wants clipboard history (no Tools)
| Step | Expected | Happened | Evidence |
|---|---|---|---|
| Double-click Clipboard 0.1.0 in `~/Downloads` | Install prompt | ✅ prompt | j1-clip-01-prompt-crop |
| Install | Menu entry, icon, command, receipt, autostart | ✅ entry with Settings, Quit and Uninstall actions; receipt 0600 | j1-clip-02-after-install |
| First run | History works | ⚠️ *Create mesh* is required first (UX) | j1-clip-04-mesh |
| Copy 30 items, including a 5 MB block, unicode, an image and a file list | All captured | ✅ 30 captured; the 5 MB paste matches byte for byte (sha256) | j1-clip-05-after-30-copies |
| Search, paste, pin, Pinned filter, Clear history | Work; pins survive Clear | ✅ | j1-clip-07…14 |
| Missing keyring collection | Clear message, no hang | ✅ clear message with Retry | j7-clip-no-keyring-collection |
| Reboot (login autostart) | Pins kept, capture on | ✅ pins kept; ❌ no tray icon when Clipboard starts before the panel (F4) | j1-clip-16-after-reboot, j1-all-reboot-20s-tray |
| Run the download again | "Already installed" | ✅ | j1-clip-17-second-run-crop |
| Delete the download | Installed copy keeps working | ✅ | (session log) |
| Wheel and Shelf, same steps | Same | ✅ prompts and integration; Wheel's X11 hotkey unavailable (documented) | j1-wheel-*, j1-shelf-* |

### Journey 2: Maya adds more apps, still no Tools
| Step | Expected | Happened | Evidence |
|---|---|---|---|
| Install Find, Lens, Look, Box | Prompts, integration | ✅ (prompt placement varies, UX) | j2-*-01-prompt-crop, j2-*-02-after-install |
| Apps discover each other | Each lists the others | ✅ all 7 | j2-wheel-07-connected-apps |
| Find → Shelf (action) | File lands on Shelf | ✅ | j2-find-05-actions-shelf, j2-find-06-after-add-to-shelf |
| Find → Look (Space) | Preview | ✅ in 0.68 s | j2-find-07-quicklook |
| Quit Shelf, Find → Shelf again | Shelf restarts | ✅ Find relaunches Shelf | j2-find-08-shelf-quit, j2-find-09-after-add-shelf-down |
| Lens capture → Clipboard | Appears in history | ✅ | j2-lens-06-in-clipboard-history |
| Drag onto Shelf, drag out | Works | ✅ | j2-shelf-04-dropped-on, j2-shelf-05-dragged-out |
| Wheel launches Clipboard; Box and Wheel tray menus | Work | ✅; ⚠️ Wheel's list is stale until Refresh and restart (m4) | j2-wheel-08a…10, j2-box-03-traymenu |

### Journey 3: Maya discovers Tools; update and rollback on upd
| Step | Expected | Happened | Evidence |
|---|---|---|---|
| Install Tools from its release | Prompt; finds 6 apps; tray goes 7 → 1 | ❌ blank window (F1); with the workaround ✅ 7 icons → exactly 1, submenu per app | j3-02, j3-03, j3-06, j3-tray-before-after, j3-09-tools-submenu-crop |
| Adopt the six apps | Managed; nothing breaks | ✅ receipts `managedBy: tools`; ❌ Clipboard stops (F2); windows open (UX); identical `.previous` copies (m8) | j3-17…28 |
| Install a removed app from the catalog, cancel, retry | Cancel is clean, retry works | Done on Leo (J4): ✅. On maya it hit the GitHub 403 (F9) | leo-05, leo-06, j3-35-* |
| upd: Tools 0.2.0 → self-update | Offers 0.2.1; updates itself | ✅ (no confirmation, UX); leftovers (m17, m20) | upd-05…09 |
| upd: adopt pre-self-installer Shelf and Lens 0.1.1 | Adopted, or a clear path | ❌ (F10) | upd-14…23 |
| upd: adopt Find 0.3.0, Look 0.2.0, Box 0.2.0, Wheel 0.3.0 | Managed | ✅ | upd-24…27 |
| upd: update Find 0.3.0 → 0.3.1, then roll back | Settings kept in both directions | ✅ shortcut Ctrl+Alt+J, rescan 12 h and show-hidden kept; the chord works after each | upd-29…33 |
| upd: update Box while it transcodes a 3-minute 1080p video | Tools waits or asks; the job survives | ✅ refused "Arcade Box is busy…"; the job finished (`big-compressed.mp4`); ⚠️ (m19) | upd-35, upd-36, upd-37b |
| upd: update Box, Look and Wheel; roll each back; *Update all* | Settings kept | ✅ dark theme, idle 17 min and radius 160 kept; *Update all* did 5 apps in about 40 s with Tools last | upd-38…47 |
| upd: Tools rolls itself back 0.2.1 → 0.2.0, then updates again | Works | ✅ | upd-43b, upd-44b |
| Shortcut center: list, conflict, rebind | Conflict flagged; new chord works | ✅ list and conflict; ✅ Box rebind; ❌ Find live rebind (F7) | j3-40…47 |
| Diagnostics ZIP | No secrets or home paths | ✅ home → `~`; ⚠️ Lens, Wheel and Shelf logs missing | j3-49-diagnostics |
| `kill -9` Tools | Icons back within about 1 s | ✅ 43–102 ms (1 run per app; 20-run figures in section 7) | j3-50-tray-after-kill9 |
| Start Tools again | Collapse, no duplicates | ✅ (Wheel's own icon lingers about 3 s) | j3-51-tray, logs/sni-tools-restart.log |
| Back up and restore settings | All 7 apps | ❌ Lens and Shelf missing (F3) | j3-54…57 |
| Uninstall Tools (upd) | Apps keep working with their own icons | ⚠️ silent uninstall while Tools keeps running (F12); after quitting it ✅ 7 own icons within 0.5 s; Link calls work; ✅ after reboot the apps autostart | upd-52…56 |

### Journey 4: Leo, Tools first (fresh HOME)
| Step | Expected | Happened | Evidence |
|---|---|---|---|
| Install only Tools (double-click) | Prompt and catalog | ✅ (with the workaround); ⚠️ leftover autostart `.bak` | leo-01, leo-02-apps |
| Shelf: *Check & install*, then cancel mid-download | Nothing half-installed | ✅ no file, no receipt; ⚠️ no "Cancelled" message | leo-05, leo-06 |
| Retry, then Wheel, Clipboard, Lens, Find, Box, Look (random order) | All installed and running | ✅ 6 running (3–18 s each); ❌ Clipboard never starts (F2) | leo-07…12b, leo-14b |
| No own-icon flash while Tools runs | None | ✅ 20 ms sampler: Tools' 1 icon throughout all installs | logs/leo-sni.log |
| Journey 2 checks again | Same as standalone | ✅ Shelf add and Look preview over Link; ❌ apps carry Tools' environment, so Wheel's deck is wrong (F2) | leo-15-wheel |
| Remove Box, Lens (with data) and Look via Tools | All integration gone; data per choice | ✅ entry, command, autostart, receipt, registry, Tools record, AppImage and icons gone; Lens data gone; ⚠️ Look's WebKit data stays (m15) | leo-17, leo-19, leo-20, logs/leo-leftovers-*.txt |
| Find via its `.desktop` *Uninstall*; Shelf via `arcade-shelf --uninstall` | Gone; Tools notices | ✅ integration gone; ❌ Tools shows "Needs repair" (F6); ⚠️ Find's icon flashed for 190 ms (m22) | leo-21b, leo-23b, leo-24b |
| Reinstall Box from Tools | Works, reuses kept data | ✅ | (receipt and data folder) |
| Leftover scan | Nothing but chosen data | Tools records for Find and Shelf; `app.arcadelook`; the autostart `.bak`; Find and Shelf data (kept by choice) | logs/leo-final.txt |

### Journey 7: The messy user
| Step | Expected | Happened | Evidence |
|---|---|---|---|
| Double-click the installer twice quickly | One install | ✅ one receipt; ⚠️ misleading error in the second prompt (m10) | j7-double-click-second-dialog |
| Run two copies of an app | Single instance | ✅ | (session log) |
| Kill Tools at 50 % of an install | No half state; recovers | ✅ nothing in Applications, retry works; ⚠️ 233 MB of temp files (m18) | (Leo, logs) |
| Kill an app's own installer mid-copy (kim, Look) | Recovers | ✅ the second install works; ⚠️ orphan `.stage` (m21) | kim-01, kim-02b |
| Kill an app mid-update or repair (Wheel, Leo) | No half state | ✅ repair completed, receipt consistent | leo-36b, leo-37b |
| Drop the network mid-download (iptables DROP for leo's UID) | Clear error; retry later | ✅ no half state; ⚠️ raw hidden error (m23) | leo-28-netdrop-*, leo-29b |
| Offline catalog | Cached and offline state, no crash | ✅ no crash; ⚠️ says "refreshed" (m24) | leo-30, leo-31 |
| Corrupted download (mitmproxy flips 1 byte mid-stream) | Refused | ✅ "failed SHA-256 or size verification. Nothing was installed." | leo-34b |
| Move or rename an installed AppImage | Repair or clear message | ✅ clear message (Shelf) | j7-moved-shelf-crop |
| Delete the installed file, keep the receipt | Handled | ⚠️ Tools: "Needs repair" (F6) | j3-30 |
| HOME with spaces and unicode / with `%` | Works | ✅ / ❌ menu entries unlaunchable (m7) | j7-zoe-*, j7-zoe2-* |
| Read-only `~/Applications`; disk full (64 MiB tmpfs) | Clear error | ⚠️ raw "os error 13" (m9) / ✅ clear message, cleaned up | j7-ro-*, j7-diskfull-look-crop |
| Downgrade by double-click; update by double-click | Refused; "Update?" | ✅ refused / ⚠️ old process keeps running (m5) | j7-downgrade-find030-crop, j7-update-dblclick-crop |
| Pre-self-installer migration (Find 0.2.1) | Clean migration | ⚠️ (m6) | j7-old-find021, j7-old-then-031-crop |
| PATH without `~/.local/bin` | Hint, no profile edited | ✅ `--integration-status` gives a `pathHint`; no profile changed | (session log) |
| Link off in Clipboard while Tools runs | Own icon kept | ✅; ⚠️ Tools' menu label is wrong (m12) | j7-link-off-tray-crop, j7-link-off-toolsmenu |
| No Secret Service keyring | Clear message | ✅ Clipboard explains and offers Retry | j7-clip-no-keyring-collection |
| Tools start/quit 50 times with all apps running | No orphans, flat fds and threads, no duplicates | ✅ 50/50 cycles: 1 hosted item, 7 own items back after each quit, flat fd and thread counts | logs/tools50.log, logs/fd-before.txt, logs/fd-after.txt |
| Clock forward a week (faketime +7 d on Tools) | Update check stays sane | ✅ checks after 64 s and records 2026-10-23; back on the real clock it checks after 65 s and corrects | (Leo, logs) |

### Journey 8: A day of use
See section 7 (soak).

---

## 6. What I could not test, and why
- **Windows and macOS (Journeys 5 and 6): not run.** There is no real machine. Running the CI workflows would mean
  pushing to main, which isn't allowed. The sandbox's network policy also blocks
  `productionresultssa*.blob.core.windows.net`, where GitHub Actions keeps logs and artifacts, so no CI artifact could
  be downloaded or inspected. Link's real-fleet CI runs 38868969998 and 38865372945 are green, but that is the run
  conclusion only.
- **Real Wayland compositor and portals:** the desktop is X11 (Xvfb + Openbox), so Wheel's portal hotkey, layer-shell
  and Wayland tray behaviour were not exercised.
- **Real GPU:** none here; F1 is the consequence.
- **Clipboard update and rollback:** only one Clipboard release exists. A busy-Clipboard update ("mid-paste") could
  not be done; the busy path was tested with Box instead.
- **Tools' GUI backup as a regression check:** there is no command line or Link entry point (F3).
- **Shortcut index rebuild time:** Tools exposes `elapsed_ms` only to its webview. The Shortcuts tab shows just
  "Updated <time>" and has no Rebuild button.
- **Auto-update "last used" idle logic:** no app was opted in.
- **Older releases not exercised:** Look 0.1.2, Box 0.1.2, Wheel 0.2.0, Tools 0.1.0 and Lens/Shelf rollback.

---

## 7. Performance (Journeys 8 and 8b) and developer suites (Journey 9)

> **Draft:** rows marked *pending* are still being measured; this section is updated when they finish.

**Method.**
- **Tool:** Arcade-Link v0.3.0's own `benchmarks/bench.py`, using its definitions, readiness signals, isolated
  profiles and private D-Bus. It was pointed at the released AppImages, extracted
  (`logs/bench_release.py` wrapper), and run as a separate `bench` user.
- **With a tray host:** the "host" runs add Link's fake Tools tray host (`arcade-link tray host`) to the session.
- **Sample size:** 20 runs per app and mode.
- **Machine:** this container (4 vCPU, no GPU). The 60-minute soak ran at the same time as the 20-run benchmark.
- **Baseline:** Link's `benchmarks/final-2026-10-08.json`, measured on a different machine with dev builds, so it is
  not like-for-like.

### 8b budgets (Linux; Windows and macOS not run)

| Measure | Budget | Measured | Pass? | Method, sample |
|---|---|---|---|---|
| Startup added by the tray-host watcher + `detect()` | ≤ 5 ms | Median delta with a host: Find −4.2, Lens +0.2, Look −4.9, Shelf −1.6, Wheel −2.8, Clipboard −2.9, Box +6.3 ms | ✅ (Box +6.3 ms is within its run-to-run spread: p95 154 vs 162 ms) | bench.py startup (spawn → readiness), with vs without `arcade-link tray host`; n=20 each |
| Tray hand-back after `kill -9` Tools | ≤ 1 s (target 200 ms) | Box, Find, Lens, Look, Shelf, Clipboard: median 22–31 ms, p95 ≤ 45 ms. **Wheel: bimodal, 10 runs at 30–58 ms and 9 at 580–1107 ms (p95 1107 ms)** | ✅ six apps; ❌ Wheel (over the 1 s limit once, over the 200 ms target in about half the runs) | Watcher polled every 10 ms, 20 runs on maya (19 valid; one lost to a D-Bus timeout in the harness). `logs/handback-maya.jsonl` |
| Tools idle, window closed, hosting on | ≤ 40 MiB, 0 polling, 0 CPU ticks / 30 s | **202 MiB** tree (155 + 48 MiB WebKit network process); 0 ticks / 30 s; ~1 wakeup/s (`PressureMonitor`) | ❌ (F13) | `/proc` RSS + PSS, utime+stime over 30 s, `strace -c -f` over 30 s |
| Tools window open → first paint (warm) | ≤ 400 ms | Median **354 ms**, p95 448 ms, max 448 ms (n=11 warm) | ⚠️ median passes, 2 of 11 over | Tray `Activate` over D-Bus → window mapped and ≥ 20 colours, sampled every ~5 ms |
| Overlay key → first frame | p95 ≤ 80 ms | Median **154 ms**, p95 **179 ms**, max 212 ms (n=24) | ❌ (F14) | `xdotool key super+slash` → "Arcade Tools Shortcuts" mapped and painted |
| Shortcut index rebuild | ≤ 150 ms, off the UI thread | not measurable | not measured | `elapsed_ms` is only exposed to Tools' webview; no Rebuild button in the UI (section 6) |
| Link round trip (`arcade-link status <app>` ×100) | (no number in the plan) | Median 3.3–4.1 ms, p95 ≤ 5.0 ms, max ≤ 7.8 ms for all 8 (including Tools) | ✅ | Includes starting the CLI process; maya with all apps running. `logs/link-rtt.txt` |

### Per-app figures vs Link's baseline (flag > 5 %)

| App | Startup median / p95 (n=20) | Baseline startup | Idle RSS | Baseline RSS | Idle CPU (ms / 5 s, median) | Warm invoke | Baseline warm |
|---|---|---|---|---|---|---|---|
| Find 0.3.1 | 45.0 / 70.5 ms | — | 17.9 MiB (empty index) | STATUS: 52 MiB with an index | 0 | 11.2 ms | — |
| Lens 0.2.0 | 11.1 / 16.8 ms | 3.0 ms ⚠️ | 108.0 MiB ⚠️ | 81.4 MiB | 5 | 9.3 ms ⚠️ | 1.5 ms |
| Look 0.2.1 | 134.2 / 157.3 ms | 74.7 ms ⚠️ | 107.4 MiB ⚠️ | 74.5 MiB | 10 | 115.9 ms ⚠️ | 37.7 ms |
| Box 0.2.1 | 119.5 / 154.1 ms | 68.7 ms ⚠️ | 126.0 MiB ✅ | 426.8 MiB | 0 | 14.5 ms ⚠️ | 7.7 ms |
| Shelf 0.2.0 | 78.0 / 84.9 ms | — | 139.0 MiB ⚠️ | STATUS: 79 MiB | 0 | 29.2 ms | — |
| Wheel 0.3.1 | 351.1 / 362.7 ms | 136.6 ms ⚠️ | 126.2 MiB ⚠️ | 115.3 MiB | 0 | 53.4 ms ⚠️ | 35.2 ms |
| Clipboard 0.1.0 | 316.4 / 349.4 ms | 193.3 ms ⚠️ | 261.4 MiB ✅ | 264.9 MiB | 0 | n/a | n/a |

⚠️ marks more than 5 % worse than the baseline.
- **Caveat:** the baseline was dev builds on another machine, which Look's STATUS.md calls faster. So these are flags
  to re-measure on one machine, not proven regressions.
- **Clear signals:**
  - Wheel's startup is about 2.6× the baseline. Its AppImage launches through an `AppRun.wrapped` wrapper.
  - Look's warm invoke is about 3× the baseline.
  - Shelf's RSS is 76 % over its own STATUS.md figure.
  - Box's idle RSS fell from 427 to 126 MiB, which is good.

### Journey 8 soak (60 min, maya, all 7 apps + Tools)

**What it did:** `logs/soak.sh` ran once a minute: a clipboard copy, Find search, Shelf add, Look preview and close,
and a list of Link apps. Every 5 min it added a Box action and a Lens capture; every 10 min it opened and closed the
Wheel and Clipboard settings. Tools was quit at minutes 20 and 40 and restarted at 22 and 42. RSS and CPU of every
Arcade process were sampled each minute (`logs/soak-maya.csv`, `logs/soak-summary.txt`). No action failed.

| Process | RSS start → end (MiB) | CPU over 60 min | Reading |
|---|---|---|---|
| Wheel | 124 → 213 (max 218) | **81.8 s** (1.36 s/min) | ❌ about 1 s of CPU per clipboard copy (F15); +80 MiB after the first Settings open, then about +4 MiB per open/close |
| Look | 59 → 191 | 21.7 s | +131 MiB after the first preview, then +17 MiB over 59 previews (about 0.3 MiB per preview, never returned): ⚠️ slow growth |
| Lens | 108 → 159 | 12.7 s | +51 MiB kept after the first capture, then flat; about 6 ticks/min idle |
| Box | 68 → 90 | 4.0 s | +22 MiB after the first action, flat after |
| Shelf | 137 → 175 | 3.2 s | Grows with the 60 items added (expected) |
| Clipboard | 256 → 282 | 1.9 s | Grows with the 60 clips stored (expected) |
| Find | 21.8 → 21.8 | 3.5 s | Flat ✅ |
| Tools (3 instances across the restarts) | 55–60 + 19 (AppImage runtime) | 1.5–1.6 s each | Flat. With its window never opened, Tools is about 75 MiB, still over the 40 MiB budget (F13) |
| Look's WebKitNetworkProcess | 52 → 52 | 0.3 s | Stays for the whole hour (F8) |

### Journey 9: developer suites

| Suite | Result | Notes |
|---|---|---|
| Arcade-Link unit tests (v0.3.0) | ✅ 35 OK, 2 skipped | |
| Link deterministic e2e (presence, install, trayhost, tools-hub) | ✅ 4/4 | Passed after building `install-harness` |
| Link real-fleet, local, against the release AppImages | install 7 pass / **1 fail** (m14) / 8 skip; trayhost 20 pass / 0 fail / 7 skip; tools-hub and shortcuts *pending* | `logs/link-realfleet-local-summary.txt`. The skips are the dev-build checks and Clipboard, whose release AppImage doesn't match the harness's fresh-build check |
| Link real-fleet in CI | green (runs 38868969998, 38865372945) | Run conclusion only; logs aren't reachable |
| `cargo test` / `npm run typecheck` on each repo's `main` | *pending* | Flutter and Qt6 dev packages aren't installed, so Clipboard's Flutter tests and the Shelf and Wheel builds will be marked not run |

**Test gaps** (a suite passes while the user journey fails):

| Finding | Why CI passes |
|---|---|
| F3 | The e2e suite tests `portable_backup.rs`; the GUI uses `backup.rs`. |
| F5 | Runner images ship `libopengl0`. |
| F1 | CI doesn't paint Tools' webview without DRI3. |
| F2 | No check starts a real app *from* Tools; the real-fleet trayhost checks skip Clipboard. |
| F14 | `real_overlay_paints_its_first_frame_under_xvfb` passes without timing the frame. |
| Overlay shortcut | `tools_overlay_shortcut_is_explicitly_fixed` passes while the UI lets you edit it. |

---

## Regression checks in `regression/`

Every check runs inside Arcade-Link's isolated runner (private D-Bus, Xvfb, keyring, temporary HOME), except
the Wheel one, which only reads ELF headers. Each exits 1 while its bug is present. See
[`regression/README.md`](regression/README.md).

| Check | Finding | Status |
|---|---|---|
| `clipboard_answer_fd.py` | m1 | **FAIL** (verified) |
| `clipboard_tray_late_watcher.py` | F4 | **FAIL**; `--control` PASS (verified) |
| `wheel_appimage_needs_libopengl.py` | F5 | **FAIL** (verified: `libOpenGL.so.0` needed by `usr/lib/libLayerShellQtInterface.so.6`) |
| `tools_webview_alive.py` | F1 | **FAIL** ("WebKitWebProcess died within 8 s; window is blank (1 colours)"); `--control` (`WEBKIT_DISABLE_COMPOSITING_MODE=1`) PASS (verified) |
| `tools_start_all_child_env.py` | F2 | **FAIL** ("Clipboard is not running 20 s after 'Start all Arcade apps'", clicked through Tools' DBusMenu); `--control` PASS (verified) |
| `find_live_rebind.py` | F7 | **FAIL** (`app.shortcuts.set` → `applied: true, via: native`, but Ctrl+Alt+G doesn't open Find); its control, the same chord after a restart, PASS (verified) |

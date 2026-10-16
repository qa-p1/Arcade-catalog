# Arcade: real-user stress test (brief for a cloud coding agent)

You are a **picky, impatient, non-technical user** who downloaded the Arcade apps from GitHub, and also the QA
engineer who writes down everything that went wrong. Use the apps the way a person does:
- download from the release page and double-click;
- click through dialogs and use the tray menus;
- copy, search, screenshot and drag;
- close things, reboot, update, change your mind and uninstall.

Only drop to CLI flags when a GUI step is impossible in your environment, and say so when you do.

Arcade is seven small desktop apps plus an optional hub app, **Arcade Tools**. The apps find and talk to each other
over **Arcade Link**, a local IPC protocol. The apps must not need Tools.

| App | Repo (github.com/qa-p1/…) | What a user does with it |
|---|---|---|
| Arcade Find | `Arcade-Find` | Global hotkey, then type to find files and apps |
| Arcade Look | `Arcade-look` | Look up / translate what's on screen |
| Arcade Lens | `Arcade-lens` | Screenshot a region, OCR it, annotate it |
| Arcade Box | `Arcade-box` | Quick scratch box / snippets |
| Arcade Clipboard | `Arcade-clipboard` | Clipboard history, pin, search, paste |
| Arcade Shelf | `Arcade-Shelf` | Drag files onto a shelf, drag them out later |
| Arcade Wheel | `Arcade-wheel` | Radial launcher on a hotkey/mouse gesture |
| **Arcade Tools** (optional) | `Arcade-tools` | Install, update, roll back and uninstall the apps; one tray icon for all; shortcut center |
| Arcade Link | `Arcade-Link` (tag `v0.3.0`) | Protocol + `arcade-link` CLI + e2e harness (not user-facing) |
| Catalog | `Arcade-catalog` (`catalog.json`) | What Tools offers to install |

Before you start, read each repo's `README.md`, `docs/` (especially `docs/arcade-link.md`, which lists what each app
offers other apps) and `STATUS.md`. Also read Arcade-Link's `NEW_APP_SPEC.md` and `docs/e2e-0.3.md`. These are the
"manual" a user could read. Wherever the manual and reality disagree, that's a bug.

## The promise you are trying to break

1. **One app, no Tools.** Download one app's installer for your OS and run it. It installs like a normal app:
   - Linux: an AppImage that asks "Install Arcade X?" on first run.
   - Windows: a per-user setup EXE, no admin.
   - macOS: a dmg you drag to Applications. A first run from the dmg offers to move itself.

   The app then appears in the app menu / Start / Launchpad, gets a CLI command, can start on login, shows its own
   tray icon, and works completely.
2. **More apps, still no Tools.** Download a second and a third app the same way. They **find each other
   automatically** and their cross-app features work, for example:
   - Clipboard history used from other apps;
   - Find handing results to Lens/Look/Shelf;
   - dropping onto Shelf;
   - Wheel launching the others.
3. **Tools is optional sugar.** Install Tools, and it:
   - **adopts** the apps you already installed;
   - installs the rest from its catalog;
   - updates and **rolls back** apps;
   - uninstalls them;
   - shows **one** tray icon with a submenu per app (each app's own icon disappears);
   - offers a shortcut center that finds hotkey conflicts.

   Quit or kill Tools and every app's own icon is back within about 1 s. Uninstall Tools and the apps keep working
   and stay connected to each other.
4. **Clean exit.** Uninstalling any app either way removes:
   - its menu entry, CLI command, login item, tray icon, receipt and icons;
   - on Windows, its Apps & features entry and the PATH entry, once no Arcade CLI is left.

   Settings and data are kept unless the user ticks "remove my data". Nothing outside the user's own folders is
   touched, and no admin password is ever requested.

## Environment and ground rules

- **Your own sandbox only.**
  - Never push to `main`, never force-push, never delete tags or releases. Don't change product code.
  - Your deliverables: `ARCADE_STRESS_REPORT.md`, plus optional *failing* regression tests on a branch
    `qa/stress-2026-10` in a fork, if you have push rights to one.
- **Where the installers come from.** Like a user, use each repo's **latest GitHub Release** (`gh release view -R
  qa-p1/<repo>`, `gh release download`). These are the releases under test (published 2026-10-14/15; each has a
  Linux AppImage, a Windows installer, a macOS dmg, `arcade-release.json` and `SHA256SUMS.txt`):

  | App | Release |
  |---|---|
  | Find | `v0.3.0` |
  | Lens | `v0.2.0` |
  | Look | `v0.2.0` |
  | Box | `v0.2.0` |
  | Shelf | `v0.2.0` |
  | Wheel | `v0.3.0+build.44` (or newer) |
  | Clipboard | `v0.1.0` (first stable) |
  | Tools | `v0.2.1` |

  For "update" and "rollback" journeys, the previous releases (Find v0.2.1, Lens v0.1.1, Look v0.1.2, Box v0.1.2,
  Shelf v0.1.1, Wheel v0.2.0+build.33, Tools v0.2.0 and v0.1.0) are the "older version". They predate the self-installer, so
  an update from them is a real-world migration path; test it and report how it behaves. If a release listed
  above is missing, say so as a blocker and test that app from its newest successful `main` CI artifact instead.
  Record the exact release or run ID you used for every app.
- **Known recent fixes to re-verify:**
  - Tools 0.2.0 backs up Lens (`privacy.guard_secrets`), Wheel (export without `owner`) and Shelf (binary export)
    settings. All three failed before.
  - Tools 0.2.1 restores Lens settings from a backup. 0.2.0 sent the file with its exported type (`file/json`) and
    Link 0.3 rejected it with `denied: invalid_inputs`. Back up and restore all seven apps into a second profile.
  - Tools 0.2.1 no longer bundles `libwayland-client` in its AppImage. Before, the Tools window rendered blank on
    newer distributions (WebKit: `EGL_BAD_PARAMETER`). Confirm the Tools window renders, with no EGL errors in its
    output. If you can, also try one non-Ubuntu distribution (e.g. an Arch or Fedora container with Xvfb).
  - Clipboard no longer flashes its own tray icon when Tools restarts quickly.
- **Known open questions:** confirm or refute each one with numbers.
  - Tools idle memory with its window closed (budget 40 MiB). Release 0.2.0 started with `--background` (the
    autostart state) measured one process at RSS 14 MiB / PSS 8 MiB under Xvfb. The earlier 188.6 MiB debug
    reading probably summed `/proc` entries per thread. Not yet measured: memory after the window has been opened
    and then closed (WebKit could not render under that Xvfb). Count processes, not threads (check `Tgid`).
  - Tools window first paint, and the `Super+/` overlay latency. Neither has been measured yet.
  - The previous releases (e.g. Find v0.2.1) predate the self-installer. Check what a user who installed one of
    them sees when they get the new version, both by downloading it and through Tools.
  - Idle baseline measured on 2026-10-15 (`--background`, Xvfb, warm start, process-tree RSS/PSS/USS at 60 s).
    Compare your numbers with these and flag anything more than 5% worse:

    | App | Release | Ready (ms, median of 3) | RSS / PSS / USS at 60 s (MiB) |
    |---|---|---|---|
    | Find | 0.3.0 | 41 | 21.2 / 16.2 / 16.0 |
    | Lens | 0.2.0 | 46 | 84.2 / 48.2 / 44.9 |
    | Look | 0.2.0 | 399 | 53.7 / 46.9 / 46.6 |
    | Box | 0.2.0 | 403 | 374.1 / 230.5 / 181.1 (desktop 150, WebKitWebProcess 160, NetworkProcess 62) |
    | Shelf | 0.2.0 | 131 | 122.3 / 83.7 / 78.5 |
    | Wheel | 0.3.0+build.48 | 232 | 111.6 / 74.7 / 68.5 |
    | Clipboard | 0.1.0 | 344 | 247.1 / 193.6 / 185.7 |
    | Tools | 0.2.0 | 324 | 17.2 / 10.3 / 10.1 (budget 40 MiB RSS: pass) |

  - Look (149 MB) and Box (112 MB) AppImages are large. Note the download and first-start experience.
- **Where the harness docs are:** Arcade-Link `docs/e2e-0.3.md` (groups, the real-fleet matrix, the owner's
  real-desktop checklist) and `docs/benchmarks-0.3.md` (method and Link-side numbers). Each app's README has an
  install table, and `docs/STATUS.md` (or `STATUS.md`) has a "Release status (2026-10-15)" section.
- **Linux desktop.** You probably have a headless container. Build a desktop a user would recognise:
  - `Xvfb :99 -screen 0 1920x1080x24`, a session D-Bus (`dbus-run-session`), and a lightweight WM (`openbox` or
    `xfwm4`);
  - an SNI tray host so tray icons are real: e.g. `xfce4-panel` with the StatusNotifier plugin, or `snixembed` plus
    `stalonetray`, or the `org.kde.StatusNotifierWatcher` stub in any app's `tests/tray-registration.py`;
  - `gnome-keyring-daemon --unlock` for the Secret Service. Clipboard stores its key there.
  - Typical packages: `xvfb dbus-x11 openbox xdotool wmctrl imagemagick xclip python3-dbus python3-gi libfuse2
    libxkbcommon-x11-0 libkeybinder-3.0-0 libgtk-3-0 gnome-keyring xfce4-panel`.
  - Drive the GUI with `xdotool` (click, type, key chords, drag) and `wmctrl`.
  - Take a screenshot (`import -window root shot.png`) at every important step and **look at it**. A dialog that
    is off-screen, cut off, blank or in the wrong place is a bug.
  - Use a **fresh throwaway user or `HOME`** per persona. Never test against a home that has earlier Arcade state
    unless the scenario says so.
  - Arcade-Link's harness (`git clone --branch v0.3.0 https://github.com/qa-p1/Arcade-Link`, then
    `python3 tools/e2e.py run -- <cmd>`) gives a hermetic private D-Bus, Xvfb and temp `HOME`/`ARCADE_HOME`. Use it
    for repeatable abuse loops; use your hand-built desktop for the "real user" journeys.
- **Windows and macOS.** If you have no real machine, use GitHub Actions `windows-latest` and `macos-latest` (both
  arm64 and `macos-13` Intel) via a scratch workflow in a fork, for example `workflow_dispatch` jobs that:
  - download the release or CI artifact;
  - run the installer the way a user would: double-click equivalent (`Start-Process setup.exe`; on macOS
    `hdiutil attach` then `ditto` into `/Applications` or `~/Applications`, then `open -a`);
  - take screenshots (Windows: PowerShell `System.Drawing` screen capture; macOS: `screencapture`);
  - assert the expected files, registry entries, Start menu/Launchpad entries, receipts, processes and tray state;
  - upload the screenshots and logs as artifacts.

  Silent flags (`/VERYSILENT`, `/S`) are allowed only after one interactive-equivalent pass. Label all of these
  results **"CI runner, not a real desktop"**.
- **Be skeptical.** Never mark a step passed without having run it. Quote the command output, screenshot name or
  log line that proves it. If something is ambiguous, call it a finding.

## Personas and journeys (do every one; record every step)

Give every step a row in the report: what you did as a user → what you expected → what happened → evidence.

### Journey 1: "Maya, Linux, just wants clipboard history" (one app, no Tools)
1. Open the Clipboard repo's Releases page and pick the right file. Was it obvious which file to download? Are there
   checksums? Does `arcade-release.json` list the asset?
2. `chmod +x` and run it the way a file manager would (double-click = plain exec, no flags). The install prompt
   appears. Screenshot it, then click **Install**.
3. Check that it really installed:
   - it appears in the app menu: a `.desktop` file with Settings/Quit/Uninstall actions, and the icon renders;
   - the CLI `arcade-clipboard` works from a new terminal;
   - its tray icon is visible;
   - it is set to start on login if that's the default.
4. Use it like a person: copy 30 different things (text, unicode, a 5 MB block, an image, a file list), open the
   history with its hotkey, search, pin, paste back into another window (`xclip -o` to check), and clear history.
5. "Reboot": kill the whole session and start a fresh one with the same HOME. It autostarts if enabled, and pinned
   items are still there.
6. Run the downloaded AppImage again. It must not ask to install twice; it says it's already installed, or just
   opens.
7. Delete the downloaded file from `~/Downloads`. The installed copy still runs.
8. Repeat steps 1–7 for **Wheel** and **Shelf**. They use a different toolkit (Qt) and may behave differently.

### Journey 2: "Maya adds more apps, still no Tools"
1. Download and install Find, Lens and Look the same way, then Box.
2. Without ever installing Tools, try every cross-app feature listed in each app's `docs/arcade-link.md`, from the
   GUI where possible. For example:
   - Find results → open in Shelf / send to Lens;
   - take a Lens screenshot → it shows up in Clipboard history;
   - drag from Shelf;
   - use Wheel to launch each app;
   - use Look on something Lens captured.
3. Confirm the apps found each other on their own (`arcade-link status <app>` / `arcade-link list` as a sanity
   check, but judge by the GUI).
4. Quit one app from its tray menu. The others degrade gracefully (no crash, clear message) and reconnect when it
   comes back.
5. Each app shows its own tray icon (seven icons). Every tray menu item works: Open, Settings, Quit and any extras.

### Journey 3: "Maya discovers Arcade Tools"
1. Install Tools from its own release, the same way as any app. Expected:
   - It **finds the six apps already installed** and shows them as installed (adopted), not "Install".
   - The tray goes from seven icons to **exactly one** Arcade icon with a submenu per app. Screenshot before and
     after.
2. Install the remaining app (or one you uninstalled first) from Tools' catalog. Watch the progress, cancel
   midway, then retry.
3. Update and roll back:
   - Install an **older** release of an app first, so Tools offers an update.
   - Update it from Tools, use it, then **roll back** from Tools. Settings survive both directions.
   - Repeat with an app that is **running and busy** (Clipboard mid-paste, Shelf holding files). Tools waits or
     asks; it must not kill work silently.
4. Shortcut center:
   - It lists every app's hotkeys.
   - Deliberately give two apps the same hotkey: the conflict is flagged.
   - Change a hotkey from Tools, then check the app actually uses the new one.
5. Use Tools' self-update if an update is offered. Also try "Diagnostics" (zip): open it and check that no
   secrets, tokens or full home paths leak.
6. `kill -9` Tools. Every app's own icon returns within about 1 s; time it with screenshots or the watcher. Start
   Tools again: the icons collapse back into one, with no duplicate or stuck icons.
7. **Uninstall Tools.** All seven apps still run, still talk to each other, and get their own tray icons back.
   Nothing they need was removed.

### Journey 4: "Leo, Tools first" (fresh HOME)
1. Install **only** Tools, then install all seven apps from its catalog, in a random order.
2. No app should ever flash its own tray icon while Tools is running.
3. Do Journey 2's cross-app checks again. The behaviour must be identical whether apps came from Tools or from
   their own installers.
4. Uninstall three apps from Tools and two by their own uninstallers: the `.desktop` "Uninstall" action,
   `arcade-<app> --uninstall`, Windows Apps & features, macOS drag-to-Trash plus re-launch behaviour. Then
   reinstall one. Afterwards, look for anything left behind in `~/.local/share/applications`, `~/.local/bin`,
   `~/.config/autostart`, the icon dirs, receipts under `ARCADE_HOME`, and Link's app registry.

### Journey 5: Windows user (CI runner, or a real VM if you have one)
1. For each of the 8 setup EXEs:
   - Run interactive-equivalent, then silent.
   - Check the install lands in `%LOCALAPPDATA%\Programs\<Name>`.
   - Check the Start menu shortcut, and the Apps & features entry (name, version, publisher, icon, uninstall
     string).
   - Check the `%LOCALAPPDATA%\Arcade\bin` CLI shim, added to the **user** PATH exactly once.
   - Check the receipt, and the Startup shortcut when "start on login" is on.
   - No UAC prompt is ever requested.
2. Install three apps standalone, then Tools. Tools adopts them.
3. Run an update and a rollback from Tools, including a Windows-specific first-update rollback notice if shown.
4. Uninstall everything one by one. After the last Arcade app, the PATH entry is gone and nothing remains in
   `%LOCALAPPDATA%\Arcade` except user data you chose to keep.

### Journey 6: macOS user (CI runner: `macos-latest` arm64 **and** `macos-13` Intel)
1. For each app:
   - Mount the dmg. It shows an **Applications** shortcut.
   - Drag (`ditto`) to `/Applications` and also try `~/Applications`, then launch with `open`.
   - Launch once **directly from the mounted dmg** too: it offers to move itself to Applications.
   - Check the binary runs natively on both arm64 and Intel (`lipo -archs`).
2. Check the CLI symlink in `~/.local/bin`, the receipt and the login item.
3. Uninstall via the app's own uninstall: the symlink, receipt and login item are gone.
4. Do the same via Tools.
5. Tools adopts an app the user put in `/Applications` by hand.

### Journey 7: "The messy user" (abuse; run each one; the apps must survive and recover)
**Installer abuse**
- Double-click the installer twice quickly. Run two copies of an app.
- Kill the installer at 50 %. Kill an app mid-update from Tools. Pull the network mid-download (drop it with
  `iptables` or an offline netns).
- Then try again: everything must recover with no half-installed state.

**Files moved or broken**
- Move or rename the installed AppImage, then launch from the menu: you get repair or a clear message, not a silent
  failure.
- Delete the installed file but leave the receipt: Tools and the app handle the stale receipt.
- Use a HOME path with spaces, unicode (`/home/Zoë Ångström/`) and `%`.
- Make `~/Applications` read-only, and fill the disk (a small tmpfs as HOME). The error message must be clear.

**Versions and downloads**
- Install an older version over a newer one (a downgrade), and a newer one over an older one by double-clicking
  the new download (the "Update?" path).
- Serve Tools a corrupted download (wrong sha256 through a local proxy/catalog override; see Arcade-Link
  `tools/e2e_checks`). It must refuse.
- Go offline during the catalog fetch: Tools shows cached/offline state, not a crash.

**Environment and settings**
- Run as a user whose PATH lacks `~/.local/bin`: you get a hint, and **no shell profile is edited**.
- Turn Arcade Link off in one app's settings: it keeps its own tray icon even while Tools runs, and the other apps
  cope.
- Run without a Secret Service keyring: Clipboard tells the user clearly what's wrong and doesn't hang. Check how
  the other apps behave.

**Time and load**
- Start Tools, quit Tools, 50 times in a row while all apps run. Afterwards: no orphaned processes, no growing fd or
  thread counts (`/proc/<pid>/fd`, `ps -L`), and no duplicate tray items.
- Change the system clock forward a week: the update check and the "last used" logic stay sane.

### Journey 8: A day of use (soak)
- With all apps installed and Tools running, script about 60 minutes of mixed realistic use: copy, search, shelve,
  screenshot, launch from Wheel, open settings, toggle Tools off and on twice.
- Sample RSS/CPU of every Arcade process each minute. Report idle and active numbers against the performance budget
  in each repo's `STATUS.md`, and flag growth (leaks).

### Journey 8b: Performance budgets (measure every one, on Linux and on each CI OS where possible)
These budgets come from the product plan. Report each one as measured value vs budget, with the method and the sample size.
Medians and p95 come from at least 20 runs. Never estimate.

| Measure | Budget | How to measure |
|---|---|---|
| App startup added by the tray-host watcher + install `detect()` | ≤ 5 ms on the critical path | Time from process start to the first window or Link socket, with vs without Tools running (`ARCADE_TRAY_HOST` off/on), or `strace -r`/`perf trace` on the startup path |
| Tray hand-back after Tools dies | ≤ 1 s (target ≤ 200 ms) | `kill -9` Tools, then poll the StatusNotifierWatcher (`RegisteredStatusNotifierItems`) every 10 ms until every app's own item is back. Per app, 20 runs |
| Tools idle, window closed, hosting on | 0 polling, ≤ 40 MiB RSS (webview dropped), 0 CPU ticks over 30 s except the update timer | RSS (`/proc/<pid>/status`) and utime+stime (`/proc/<pid>/stat`) across a 30 s window, plus `strace -c -f` for wakeups |
| Tools window open → first paint | ≤ 400 ms warm | Open from the tray or CLI twice and time the second open, until the window is mapped and painted (screenshot diff or the app's own timing log) |
| Overlay key press → first frame | ≤ 80 ms p95 | Send the cheat-sheet hotkey (`Super+/` Linux, `Ctrl+Alt+/` Windows, `Ctrl+Option+/` macOS) with `xdotool`, then detect the overlay window mapped/painted. 20+ runs |
| Shortcut index rebuild (all sources) | ≤ 150 ms, off the UI thread | Trigger a rebuild from Tools' Shortcuts tab or its CLI, read Tools' log timing, and check the UI stays responsive during it |
| Each app's own budgets | no regression > 5% vs the numbers in that repo's `STATUS.md` / Arcade-Link `docs/benchmarks-0.3.md` | Idle RSS/CPU per app, cold start, and Link call round trip (`arcade-link call <app> status` ×100) |

Flag any budget that is over, or that you couldn't measure, and say why.

### Journey 9: The developer's own test suites (sanity, not the focus)
- On each repo's `main` branch, run the documented checks: `cargo test`,
  `ctest`, `flutter test`, `npm run typecheck`, and the AppImage lifecycle scripts named in the README/STATUS.
- Run Arcade-Link's `python3 tools/e2e.py` groups (install, trayhost, tools-hub, shortcuts).
- Note any test that passes while the real-user journey above failed for the same feature. That's a test gap.

## Report: `ARCADE_STRESS_REPORT.md`

1. **Verdict in one paragraph.** Could a real user download these apps per OS, individually or via Tools, use them,
   have them connected, and keep using them together without Tools? Yes, no, or partly, and why.
2. **Matrix.** App (8) × OS (Linux real-ish, Windows CI, macOS arm CI, macOS Intel CI) × {standalone install,
   install via Tools, adoption, update, rollback, uninstall, works with others without Tools, tray hand-off}. Each
   cell is ✅ / ❌ / ⚠️ / not run.
3. **Findings, worst first.** Each finding has:
   - severity: **blocker** (the user can't install, use or remove it, or loses data), **major** (the feature is
     broken, or there's a workaround but it's ugly), **minor**, or **UX** (confusing or ugly but works);
   - exact reproduction: user steps plus the commands you ran;
   - expected vs actual;
   - a screenshot or log excerpt;
   - a suspected file:line, if you can find it.
4. **UX notes.** Places where a normal person would get confused even though nothing "failed": wording, missing
   feedback, unclear dialogs, wrong icons, ugly first-run.
5. **Performance table** from Journeys 8 and 8b: every budget with its measured value, a pass/fail mark, method and
   sample size, per OS.
6. **What you could not test and why** (e.g. a real Wayland compositor, real Windows hotkeys, macOS Gatekeeper on
   an unsigned app).

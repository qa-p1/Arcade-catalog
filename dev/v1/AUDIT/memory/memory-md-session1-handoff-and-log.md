# Arcade memory audit — fleet under 500 MB (research agent, 2026-11-06)  [WRITTEN AS I GO — see "Status" at bottom]

> # HANDOFF — read this first (written 2026-11-06 end of session 1; resume from here)
> Task (unchanged): research only, NO code changes. Find what must change in each Arcade app so ALL apps together stay < 500 MB (PSS **and** RSS, FUSE stubs included) with no UX loss
> (owner rule: UX must not get worse). Deliverable = this file: measured table, ranked work items (app, cause, evidence file:line, MB now→after, fix, UX risk), per-app budgets for
> (A) all 8 in background and (B) all 8 + one window open, a plain reachability statement, CI conformance check. Final message = compact ranked list + projected fleet totals.
>
> **PSS vs RSS:** RSS = RAM pages a process has mapped, shared libraries counted in full in every process (what htop/btop and Tools' dashboard show; sums double-count).
> PSS = shared pages split among the processes sharing them (sum ≈ RAM really used). The owner's "800 MB+" is RSS-like: Tools Home sums sysinfo RSS of ONE pid per app (`src/dashboard.rs:47-82`), no children, no stubs.
>
> ## Status
> **Measured & logged (do not redo):** §2 findings F1–F18 below, raw data `memory/lab-*.jsonl`, `memory/fleet-*.jsonl`, `memory/real-cycle-*.jsonl`, `memory/logs/*.log`, screenshots `memory/shot-*.png`,
> Haiku source refs `memory/refs/refs-{tauri-qt,clipboard,launch}.md` (302 of 305 quoted lines re-verified against source), Flutter probe `memory/probe/`, harness `memory/tools/` (scripts still point at the old scratchpad path `S=`; change it).
> Additional results NOT yet written into F-log (all measured):
> - **Unpacked Tools, aged cycle (Xvfb, `exp_rel.py tools trim+dontneed --ext`):** bg 17/10 → open 540/320 (window mapped 0.45 s) → closed+35 s **203/104** (UI 133/54 + net proc 69/50) → kill net proc + trim + dontneed **60/38** → reopen **0.30 s**, open again 466/294. (RSS/PSS MB)
> - **Fleet, all 8 together on Xvfb, unpacked** (`fleet-ext.log`): bg 755/564; **after one trim+dontneed 448/372** (Clipboard alone 220/193 because llvmpipe; other 7 apps total 228/179). Tools window open adds ~+515/+305 (532/320).
>   Per app unpacked bg → trimmed (RSS/PSS): Tools 34/27→17/13, Box 85/78→48/44, Look 60/53→37/33, Find 31/26→17/14 (small lab index; real index adds ~25 MB), Lens 12/10→6/5, Shelf 75/63→43/36, Wheel(GL) 132/58→62/34, Clipboard 326/249→220/193.
> - **Fleet AppImage (stub attribution BUG, stubs read 0):** apps only 753/586 bg; Tools window open 1215/844; closed+45 s 912/656. Re-run needed for stubs (see TODO 3). Lab stubs when active: Tools 22, Box 21, Look 22, Find 19, Lens 17, Clipboard 19, Shelf 23, Wheel 22 MB (real: 112 total, partly swapped).
> - **Cold start from nothing, Xvfb, median s (AppImage → unpacked):** Tools 0.68→0.31, Box 0.92→0.46, Look 0.67→0.32, Clipboard 0.29→0.22. Real-GPU stock Flutter exec→first frame 0.22 s (5 runs). In-place reopen after release: Tools 0.40/0.30(unpacked), Box 0.38–0.46, Look 0.32–0.34.
> - **Compositing off, Xvfb, open idle:** Tools 529/312→420/238, Box 531/315→432/251, Look 507/291→401/221. **Open + trim + compositing off (Tools, Xvfb):** 415/233 → 259/168 (→297/201 after exercising tabs) → with anon page-out 174/86 (68 MB swap).
> - **Wheel `--preview` first draw on Xvfb:** GL 142/83 → 227/160 (+85 MB, never released); software backend 70/59 → 81/65. Wheel unpacked+software+startup-trim 42/26.
> - **Xvfb inflates Flutter** (llvmpipe): Clipboard 321/256 bg vs 181/109 on the real GPU; `GALLIUM_DRIVER=softpipe` worse (443/382), `LP_NUM_THREADS=1` 321/239; Flutter has no software-render switch (probe ignored `enable-software-rendering`). CI needs a separate Clipboard allowance until its engine leaves the resident process.
> - Fonts/icons: ≤1.4 MB PSS fonts per process, icon-theme caches ≤0.2 MB (negligible). Fleet swap on the real desktop 128–140 MB.
>
> **NOT done (the interruptions killed the queued lab scripts; run only these):**
> 1. `exp_rel.py box trim+dontneed --ext` and `... look ...` (aged unpacked release numbers for Box/Look; Tools done above). Optional: `scenario.py tools|box --cycles 3 --env MALLOC_ARENA_MAX=1 --env TOKIO_WORKER_THREADS=2` (arena/tokio effect with window open; bg effect already ≤3 MB, safe to skip).
> 2. `hot_reshow.py look` / `box` (re-show latency while webview still alive vs after release) and `twowin.py ext` / `twowin.py hl` (Tools+Look windows both open: separate unpacked copies vs Look's identical libs hardlinked to Tools' inodes; Tools & Look ship byte-identical libwebkit/JSC/GTK/ICU, 221 MB; Box has a different WebKit build).
> 3. `fleet_lab.py image2 --open tools` (AppImage fleet with fixed stub attribution; script already fixed).
> 4. Write-up steps: consolidate §3/§4 (below, from this handoff), **run the CI script once** (`memory/tools/fleet_budget.py --apps ~/Applications/Arcade --open tools --json out.json`; stub attribution fixed, never executed yet; expect budget failures with a budgets file), cleanup, desktop check, final ranked list.
> Resume: `lab.py` starts Xvfb :95 and private dbus by itself; unpacked payloads must still exist in `/var/tmp/arcade-audit-ext/<App>/squashfs-root` (needed for items 1–2). Scratchpad is on tmpfs `/tmp` (lost on reboot): if gone, re-extract with `Arcade-X.AppImage --appimage-extract` into /var/tmp (NOT /tmp: tmpfs pages get swapped and give invalid numbers).
>
> ## Draft ranked work items (fill numbers from F-log; verify file:line in source; orchestrator verifies too)
> | id | app | fix | now → after (RSS/PSS MB, measured unless "est") | UX risk / keep UX equal |
> |---|---|---|---|---|
> | U1 | all 8 (Link + packaging) | **Unpacked runtime**: AppImage keeps single-file distribution but its runtime extracts once to `$XDG_DATA_HOME/arcade/runtime/<app>-<ver>-<hash>/` then `execv`s AppRun with `APPIMAGE`+`APPDIR` set (no FUSE daemon, no stub). Touch points: `Link manifest.rs:486-504` (`current_executable` needs exe under `$APPDIR`), `install.rs:263,323` (Exec=), `client.rs:372-393` (spawn), Tools `installation.rs:121-139`/`platform.rs:370-400`/`paths.rs:118-135`, Clipboard `main.cc:49-90` (release_mount_handles), `childenv.rs:21-36`. | stubs 112/112 → 0 (lab 166); Tools fresh bg 73/65 → 17/10; cold start −0.37/−0.46/−0.35 s | disk +1.5 GB uncompressed (btrfs zstd ≈ 0.6 GB; ext4 full), first launch extracts (once per version), GC old dirs. Same entry path/env contract, starts faster. |
> | W1 | Tools, Box, Look | After last window is destroyed: SIGTERM child `WebKitNetworkProcess` (kept alive by tauri-runtime-wry `lib.rs:2575-2590`, tauri#14626), `malloc_trim`, `madvise(DONTNEED)` on read-only executable mappings. Tools `desktop.rs:253-262`+`resident/memory.rs:4-15` (today PAGEOUT only, skipped for pages shared with the net process), Box `lib.rs:1469,1506-1517` (malloc_trim only), Look `app.rs:340,725-760` (nothing). Put one shared fn in Link. | Tools 232/137 → 75/55 (AppImage), **60/38 unpacked**; Box 256/160 → 94/74; Look 245/150 → 79/59; real aged: Box 191/108, Look 195/112 | reopen unchanged (Tools 0.40/0.30 s, Look 0.32 s). Only data in network process is localStorage onboarding flag (Tools `Onboarding.svelte:56`): delay kill ≥3 s, use SIGTERM. |
> | W0 | Tools, Box, Look, Find, Lens, Shelf, Wheel, Clipboard | One `trim+dontneed` after init (and each hide) | Box 85/78→45/42, Look 54/47→34/30, Shelf 74/62→41/35, Wheel 76/40→42/26, Find 23/18→10/8, Lens 15/12→6/4, Tools 17/10→12/9 | none measured |
> | WH1 | Wheel | `QQuickWindow::setGraphicsApi(Software)` exactly like Shelf `main.cpp:287-292` (no ShaderEffect/MultiEffect in Wheel/Shelf QML; kit `Shadow.qml` is software-safe). Wheel `main.cpp:416` creates the overlay at start; software also removes GL first-draw (+85 MB). | Xvfb 142/83 → 70/59; real 114–143/57–86 → est 70/45 | visual diff screenshot of `--preview` still to be taken on real session; no effects used |
> | CB1 | Clipboard | Flutter engine cannot shed its view (probe: destroy view 230/166 = no change, unrealize worse; `FlutterEngineRemoveView` refuses implicit view). Bare engine on real GPU 156/73; Clipboard 181/109. Options: (a) in-process trim only: est 120/96 (probe 156/73→95/60); (b) move capture + store to a small resident daemon (capture already out of process: `arcade_clipboard_wl_capture` watcher started from Dart `desktop_adapter.dart:603-606`, Dart orchestration `app_controller.dart:363-367,1410-1510`, Rust core already a library) and spawn Flutter UI on demand: est 30/22 | (a) −60/−13; (b) −150/−87 | (b) first open after idle 0.11 s → ~0.25 s (cold start 0.22–0.29 s) — breaks "same latency" unless a keep-warm window (e.g. 60 s) is used; large engineering. Recommend (a) now, (b) optional for scenario-B headroom. |
> | CB2 | Clipboard | `--status/--version/--arcade-manifest/--restart` boot a full Flutter engine in a throw-away process (`my_application.cc:171-181`, `main.cc:84-92` only `--help` fast-paths) → answer from C++ or the Link socket | transient ~150–250 MB and ~0.5 s per CLI call → 0 | none |
> | CB3 | Clipboard | list rows carry `text` (≤32 KiB) + `preview` (500 chars) but UI renders only `preview` (`history.dart:330`, `quick_overlay.dart:321`): drop `text` from list payload; `Image.memory` without `cacheWidth` (`clipboard_widgets.dart:300`) and no `imageCache` limit (default 100 MiB): set 24 MiB; window the `_items` list (`app_controller.dart:61,606`, `_historyLimit` +250) | bounded, only matters with big clips/Forever | none |
> | CB4 | Clipboard | owner decision (Forever, 256 MB budget, prune oldest unpinned) does not exist yet: only `retention_hours` 24 and `max_items` 500 clamp 10 000 (`store.rs:16,1005-1046`, `core.rs:1558-1567`); search decrypts every row (`store.rs:456-560`) — streaming, not retained; keep it that way, keyset-paginate, prune by `SUM(length)` | RAM stays bounded if only previews cross FFI | none |
> | SH1 | Shelf | thumbnail `QCache` 64 MiB default, preference up to 1 GiB, never cleared on hide (`ThumbnailProvider.cpp:22,121-125`): default 16 MiB, hard cap 64 MiB, `clear()` on hide | up to −64 MB when thumbnails shown | re-decode on reopen (2 pool threads) |
> | FD1 | Find | index 25.3 MB heap (`indexBytes` 25266078 for 302 671 entries; `index.rs:170` counts capacity, no `shrink_to_fit`); optional mmap + page-out when idle | −2…−5 (shrink), −20 optional | optional: first search after idle faults pages |
> | TD1 | Tools | dashboard "847 MB" = RSS of main pids; show tree PSS (incl. children/stub) so the owner sees what the machine pays (`dashboard.rs:47-82`); Home polling 2 s (`Home.svelte:69-71`, 6 % CPU open) | metric only | none |
> | LK1 | Look | big text/markdown peak: 5 MB .txt/.md → 880/654 (prior notes `memory/look.jsonl`), returns to 180 after 30 s; virtualize/truncate; `mediaserver.rs:35-50` thread-per-connection never stopped (minor) | peak −300 est | none if truncated banner already exists |
> | BX1 | Box | 500-item clipboard history fully in RAM (`clipboard_history.rs:20,92`), job results kept (`link.rs:183-189` no cap), 24 tokio workers | few MB | none |
> | NEG | all | glibc arenas, tokio worker caps: measured ≤3 MB (threads 39→19) — do not prioritise | | |
>
> ## Draft projection (estimates marked; recompute from final data)
> * Baseline real aged fleet: RSS 1084 / PSS 655 + stubs 112/112 = **1196 / 767** (22:13 snapshot; at 23:00 with Tools fresh 907/585 + 121).
> * **Case A, all 8 background**, after U1+W1+W0+WH1+SH1 (+CB1a): per app RSS/PSS ≈ Tools 45/35, Box 70/55, Look 55/45, Clipboard 120/96, Wheel 45/27, Shelf 43/36, Find 40/38, Lens 6/4 = **≈ 424 / 336** (<500 both, no UX loss). With CB1b (Clipboard daemon): ≈ 334 / 262.
> * **Case B, + one window open** (PSS fits; RSS does not for WebKit): PSS ≈ 336 − bg + open(168–228) ≈ 470–490 (A) or ~410 (CB1b). RSS: UX-neutral set (W1 + open-time trim, Tools open 325/228) ≈ 424−45+325 ≈ **700**; + compositing off (259/168) ≈ **640**; + anon page-out to swap (174–233/86–141) ≈ **550–610**; + Clipboard daemon on top ≈ **460–520**. => **RSS < 500 with a WebKit window open is not reachable without a visible trade-off** (compositing off needs owner's eyes; swap-assisted page-out risks swap-in jank; CB1b adds 0.15 s). If the open window is Wheel/Shelf/Find/Lens/Clipboard(in-process) it IS reachable (+0…+12 MB).
>
> ## One-window-open options per WebKit app (analysis so far; owner asked for a concrete list, recommend the one with no visible UX cost)
> 1. *Release the other hidden WebKit apps' webviews while one is open* — already true after W1: hidden apps destroy their webview (Tools on close; Box immediately on window close but 15 s on Escape/shortcut hide, `lib.rs:1286,1459`; Look 30 s, `app.rs:37`). Shortening Box's 15 s / Look's 30 s only helps if two apps are used within that window and removes the hot re-show (0.05–0.1 s → 0.3–0.4 s): visible cost, gain 0 in steady state → do not shorten. (hot re-show numbers: TODO 2)
> 2. *Shared WebKitNetworkProcess* — WebKit runs one network process per UI process; sharing across apps would need one host process for all three apps (architecture rewrite). With W1 only one network process (33 PSS/60 RSS) exists when one window is open → gain 0. Reject.
> 3. *Smaller WebKit caches / memory-pressure settings* — `WebKitCacheModel`, `webkit_web_context_set_memory_pressure_settings` (WebKitGTK ≥2.34) to cap the WebProcess (anon ≈100 MB: JSC + bmalloc): needs a prototype in each app (apps load local assets, so cache shrink has ~no UX effect; GC pressure may cost jank). **Unmeasured** — the one candidate still needing a measurement (est −20…−40 RSS/PSS).
> 4. *Drop a hidden app's WebProcess right after hide* — same as 1 (already destroyed with the webview; leftover is the net process + library pages, covered by W1).
> 5. Measured levers for the open window itself: **open-time trim** (UI process self-trim + `LD_PRELOAD` trimmer for the WebKit helper processes; Tools 528/319 → 325/228, click→repaint unchanged 145→141 ms) = **no visible UX cost → recommended**; compositing off (−79/−55 on the real GPU, pixel-identical stills, motion/video unverified) = needs owner's eyes; anon page-out (−120/−120 but 70–95 MB to swap) = reject unless RSS target is strict.
>
> ## Cleanup still to do (nothing cleaned yet)
> `/var/tmp/arcade-audit-ext` (1.5 GB; keep until TODO 1–2 done), 50 run dirs `/tmp/arl-*`, scratchpad `lab/` (129 MB), `flt/probe` build, copies are already in `memory/tools`. Xvfb :95 and lab dbus daemons are NOT running (killed by the interruptions); Xvfb :93/:92 belong to earlier agents — leave them.
> **Real desktop now == baseline:** windows = Shelf edge tab + T3 Code; all 8 apps running in background; Clipboard Private mode untouched; clipboard content never changed. Tools was restarted once by me (accidental window via `--status`, closed with `--quit`, relaunched with the mandated systemd-run command, now pid 339405). Lens has a pre-existing defunct child.
>
> ## Gotchas learned (save time)
> Tools has NO `--status` (unknown flag opens the window, T4) — never call it. `pkill -f '<pattern>'` can match and kill your own shell. /tmp is tmpfs (unpacked tests must live in /var/tmp). Lab `XDG_RUNTIME_DIR` must be short (sockets <108 bytes; Wheel failed on a long path; `lab.py` now uses `/tmp/arl-<hash>`). AppImage FUSE stub is NOT a child of the app (find by exe `*.AppImage` + HOME env). Overlay windows of Wheel/Shelf/Find/Lens are not detectable on Xvfb. Real-desktop apps that touch Hyprland rules (Box `hyprland.rs:70`) must not be run against the real compositor. Do not run an isolated Clipboard on the real session (its watcher would copy the owner's clipboard).


Goal: ALL 8 Arcade apps running together < 500 MB total (PSS **and** RSS, AppImage FUSE stubs included) with no UX loss.
No code changed. Evidence: `AUDIT/memory/` (raw), harness in `AUDIT/memory/tools/`. Previous partial notes: `memory/old-memory-md-2026-11-06-2207.md`, `memory/prior-agent-notes.md`.

## 0. Baseline of the owner's desktop when I started (restored at the end)
All 8 apps running in background (`--background`/`--service`), no Arcade window open except Shelf's edge tab (30x92 at right edge); only other window T3 Code.
Clipboard Private mode ON (untouched). Real Tools had just been relaunched fresh by the earlier agent.

## 1. Measured: owner's real fleet (read-only /proc), 2026-11-06 ~23:00, all apps "background"
| app | procs | RSS MB | PSS MB | FUSE stub RSS/PSS | threads |
|---|---|---|---|---|---|
| Tools (fresh restart) | 1 | 63.4 | 55.9 | 23.0 / 22.9 | 44 |
| Box (used earlier, webview released) | 2 | 192.2 | 105.6 | 18.5 / 18.5 | 61 |
| Look (used earlier, webview released) | 2 | 199.9 | 117.8 | 17.5 / 17.5 | 63 |
| Clipboard | 1 | 181.7 | 110.7 | 18.3 / 18.3 | 76 |
| Wheel | 1 | 140.7 | 84.0 | 16.7 / 16.7 | 24 |
| Shelf | 1 | 62.3 | 51.5 | 7.6 / 7.6 | 8 |
| Find | 1 | 53.3 | 48.2 | 5.1 / 5.1 | 31 |
| Lens | 1 | 13.9 | 11.3 | 14.5 / 14.5 | 10 |
| **FLEET** | | **907** | **585** | **121 / 121** | 317 |
| **FLEET + stubs** | | **1028** | **706** | | |
Earlier (22:13, Tools had been opened+closed): fleet RSS 1084 / PSS 655 (+112 stubs) — Tools 253/146.

## 2. Findings log (measured by this agent; consolidated into §3/§4 at the end)
Method: isolated labs on Xvfb :95 (private HOME/XDG/dbus, installed AppImages), harness `memory/tools/{lab,scenario,exp_rel,appmaps}.py`, raw `memory/lab-*.jsonl`.
Real-desktop cross-check: Tools window open on the real Hyprland/AMD GPU = RSS 523 / PSS 302 (Xvfb llvmpipe: 532/324) → Xvfb numbers are representative (±7 %).

**F1. Closed webview apps stay ~3x bigger than fresh.** Tools fresh bg 50/43 (RSS/PSS MB) → open 532/324 → closed+60 s 232/137 (never returns).
 Remaining after "release in place": UI process 172/98 (libs touched by WebKit/GTK/GL stay mapped, heap 42 MB anon) + **WebKitNetworkProcess 60/39 that never exits**.
**F2. Why the NetworkProcess never exits:** tauri-runtime-wry 2.11.4 `lib.rs:2575-2590` deliberately keeps the `WebContext` alive on Linux (tauri#14626), so WebKit keeps its network process.
 Killing it (SIGTERM, from the app, after the webview is destroyed) is harmless: next open respawns it, reopen 0.40 s vs 0.70 s first-ever open (measured, Tools).
**F3. File-backed pages can be dropped with no latency cost.** `madvise(MADV_DONTNEED)` on read-only executable mappings (never COW'd; refault from page cache) + malloc_trim + killing the net process:
 Tools closed 232/137 → **75/55** (A: trim+dontneed) or **59/38** (B: +MADV_PAGEOUT of anon, 19 MB goes to swap). Reopen after release 0.40 / 0.42 s (A / B) = same as before (0.40).
 Tools 0.4.6 already has `release_unused_runtime_pages` (src-tauri/src/resident/memory.rs) but it only does PAGEOUT of `.so` mappings; PAGEOUT skips pages mapped by another process (the NetworkProcess maps the same libs) → ineffective (measured: after-pageout 227/132).

**F4. The FUSE-mounted AppImage costs far more than its stub.** Same Tools build, fresh `--background`, 20 s (btrfs-backed unpacked copy vs AppImage), RSS/PSS MB:
 AppImage 50/43 + FUSE stub 23/22 = **73/65**;  unpacked `AppRun` **17/10** + no stub. Mapped file pages are 4–7x more resident through FUSE
 (binary 11.9 MB vs 1.7; libwebkit 7.6 vs 0.6). All 8 stubs = 111 MB RSS/PSS (they hold squashfuse caches, 16–21 MB anon each; swapped out when idle).
 (An earlier "ext" run from a tmpfs path was invalid: tmpfs pages were swapped out. Re-done on btrfs `/var/tmp`.)
**F5. Negative results (measured, bg fresh):** `MALLOC_ARENA_MAX=2` saves 0–2 MB; `MALLOC_ARENA_MAX=1 TOKIO_WORKER_THREADS=2` saves 1–3 MB and drops threads 39→19 (Box), 35→15 (Look), 30→20 (Tools).
 So glibc arenas and duplicate tokio runtimes are NOT a memory lever (only a thread-count/cleanliness one).
**F6. Real-desktop cycles (owner's GPU), RSS/PSS MB** (`memory/real-cycle-*.jsonl`): Box before 209/126 → open 467/300 (window mapped 0.50 s) → hidden 191/108.
 Look before 194/111 → open 438/266 (0.37 s) → +40 s released 195/112 (WebKit stays: network proc + libs). Clipboard before 181/109 → open (Settings page) 193/121 → hidden 193/121 (never gives back).
 Wheel `--preview` shown: 114/57 → 114/57 (+0: QML overlay + engine already resident while invisible). Find `--show`: 51.7/46.7 → same. Shelf `--show`: 61/50 → 62/51.
 Tools open (real GPU) 523/302; I opened it by accident with `--status` (Tools has no such flag, unknown flag opens the window — T4); closed by `--quit` and relaunched `--background`.

**F7. Trimming while the window is OPEN (Tools, Xvfb; shim runs in UI + WebKitWebProcess + WebKitNetworkProcess):** idle open 528/319 →
 `trim+dontneed` (drop executable-text pages, kernel refaults the working set): 325/228 (→ 364/254 after exercising every tab) →
 + `PAGEOUT` of anon: 207/111 but 94 MB sits in swap (285/179, swap 67 after use). Click→repaint over 8 tab switches: 145 ms before, 141 ms after, 140 ms after anon-pageout
 (probe resolution ~40 ms) → **no measurable UX change**. Per process: UI 201/113 → 102/63; WebProcess 267/173 → 181/140; NetworkProcess 60/33 → 42/26.
 Only the UI process can be trimmed by the app itself; the WebKit helpers need an `LD_PRELOAD` trimmer inherited through the AppRun environment (no WebKit API for it).
**F8. Shelf already forces the Qt Quick software renderer** (`src/main.cpp:287-292`, so no Mesa/LLVM; Shelf bg PSS 50). Wheel does not (GL → libgallium+libLLVM in a hidden process, QSGRenderThread, 12 Mesa threads).
 Neither app uses ShaderEffect/MultiEffect/DropShadow/layer effects (grep), and the shared kit's `Shadow.qml` is written to "work on the software renderer too".
**F9. Shelf's in-RAM thumbnail cache** (`src/ThumbnailProvider.cpp:22,121`): `QCache` 64 MiB default, user preference `thumbnailQuotaBytes` up to **1 GiB**, never cleared when the panel is hidden, no disk thumbnail cache.
**F10. Clipboard:** capture is driven from Dart (`app_controller.dart:363-367`, `_captureFromDesktop` → `_core.invoke('capture')`) with the native Wayland watcher in the Flutter plugin (`platform/desktop/arcade_desktop_bridge/linux/clipboard_bridge.cc`),
 so the Flutter engine/isolate must stay alive for capture; the runner keeps a *realized but unmapped* GTK window + GL context for the whole background life (`my_application.cc:62-72`).
 History is not held in RAM beyond one page: `history` returns <= `_historyLimit` (250, +250 per "load more") items, each with `text` (<= 32 KiB) + `preview` (500 chars) — bounded, but the list payload carries the full text field (see item CB-3).
 `--status/--version/--arcade-manifest` start a complete Flutter engine in a throw-away process (observed: my `--status` printed a second `dev.arcade.Clipboard` GTK instance) — ~0.5 s and ~150–250 MB transient per CLI call (item CB-4).
 Flutter 3.47.2 SDK on this machine ships `fl_engine_new_headless()` and `fl_view_new_for_engine()` (`/opt/flutter/bin/cache/artifacts/engine/linux-x64/flutter_linux/`), but "the engine must not be headless" for a view.

**F11. Flutter engine cannot shed its view (probe: stock `flutter create` app, release build, Flutter 3.47.2, Xvfb/llvmpipe so absolute MB are high, deltas matter):**
 hidden-but-realized window (what Clipboard does now) 233/166; destroy the GtkWindow+FlView and keep the engine alive: **230/166** (no change; the engine logs
 `FlutterEngineRemoveView ... The implicit view cannot be removed`); `gtk_widget_unrealize`: **306/228** (worse). Running Dart keeps ticking in all modes.
 → destroying/unrealizing the view does not free anything; the only ways to lower Clipboard are a smaller engine footprint or taking the engine out of the always-resident process (item CB-1).
**F12. Cold start of a UI process from nothing, Xvfb, warm page cache, window mapped (s), median of 4:** Tools AppImage **0.68** vs unpacked **0.31**; Box AppImage **0.92**.
 In-place reopen of an already-resident Tools after release is 0.40 s (F3). So a UI process spawned on demand from an UNPACKED payload (0.31 s) is not slower than today's in-place reopen,
 while the same spawn through the FUSE AppImage (0.68 s) is slower. (remaining apps in `res/coldstart.log`, §4.)
**F13. Tools "memory" number the owner sees** (Home dashboard, "7 running, 847 MB"): `src/dashboard.rs:47-82` sums sysinfo `process.memory()` (RSS) of ONE pid per app (from its endpoint file), no children, no stub.
 So the 800+ MB figure is a sum of main-process RSS (which double-counts the Mesa/LLVM and GTK libs mapped by every app), not what the machine pays; fleet PSS was 585–655 MB.
**F14. Haiku-collected, grep-verified source references** are in `memory/refs-tauri-qt.md` and `memory/refs-clipboard.md` (copied at the end). Notable: Box also keeps a 500-item clipboard history fully in RAM
 (`apps/desktop/src-tauri/src/clipboard_history.rs:20,92`); Look's media HTTP server thread-per-connection is never stopped (`mediaserver.rs:35-50`); Clipboard's `_items` has no Dart-side cap
 (`app_controller.dart:61,606`) beyond the 250-per-page request; there is NO size-budget pruning in the Clipboard core today (only `retention_hours` 24 and `max_items` 500, clamp 10 000: `store.rs:16,1005-1046`).

**F15. Bare Flutter engine on the owner's GPU** (stock app, hidden realized window, Wayland): **156/73** (RSS/PSS, anon 47, 38 threads). Clipboard's own Dart/Rust/plugins add only +25/+36
 (Clipboard bg 181/109). So even a perfectly lean Clipboard stays >= 156/73 while the Flutter engine lives in the resident process.
 With the trim shim on that probe: `dontneed` 95/60; + anon page-out 68/33 (18 MB to swap).
**F16. Startup-only trim of unpacked Rust apps (one `trim+dontneed` after init; stays down 30 s idle):** Box 85/78 → **45/42**, Look 54/47 → **34/30**, Tools 17/10 → 12/9.
 (Unpacked `Box` is bigger than Tools at bg because its 64 MB executable keeps 31 MB of pages resident after start; the trim removes them.)
**F17. WebKit software compositing (`WEBKIT_DISABLE_COMPOSITING_MODE=1`) on the owner's real Wayland session** (isolated instance, window open idle, RSS/PSS):
 Look **487/280 → 409/228**, Tools **532/322 → 453/267** (threads 138 → 96); window mapped 0.66→0.57 s (Look), 0.77→0.72 s (Tools). Static frames are pixel-identical (`memory/shot-real-look-{comp,nocomp}.png`).
 Not verifiable by screenshot: scroll/animation smoothness and video playback (Look), so this lever needs the owner's eyes before it ships.
**F18. Wheel software renderer (Xvfb):** GL (current) 142/83, 34 threads → `QT_QUICK_BACKEND=software` **70/59, 9 threads** (RSS −72, PSS −24; on the owner's GPU the PSS gain is smaller because radeonsi is lighter than llvmpipe: real Wheel 114–143 / 57–86).
 Unpacked Wheel (GL): 148/65 (stub gone: −22 RSS/PSS from the stub only).

## 2b. Session 2 findings (2026-11-07), appended as measured
**Machine rebooted between sessions** (uptime 2 min at resume): scratchpad (tmpfs) wiped, harness rebuilt from `memory/tools`, `/var/tmp/arcade-audit-ext` survived. After the reboot only Tools, Find, Look, Shelf, Wheel had autostarted (Box, Lens, Clipboard were not running; I did not start them: that is the owner's post-reboot state).
**F19. Fresh-boot real fleet (5 apps, ~2 min after login):** RSS 351 / PSS 282 + FUSE stubs 106/106 (Find 43/40, Look 60/54, Shelf 72/62, Tools 63/57, Wheel 113/70; stubs 16–23 each). Freshly started apps are small; the aged state (used once, closed) is what reaches 1084/655.
**F20. All 8 apps together on Xvfb, installed AppImages, stub attribution fixed** (`fleet-image2.log`): bg+70 s apps 753/599 + stubs 170/168 = **922 / 767**; Tools window open **1386 / 1028**; Tools closed +45 s **1081 / 821** (Tools 218/122 stays, never returns).
 (The lab PSS total 767 equals the real desktop's aged 767, so the lab fleet is a faithful stand-in for the CI check; Xvfb makes Clipboard 249 PSS instead of ~110.)
**F21. Aged release, unpacked payload (Xvfb, `exp_rel.py APP trim+dontneed --ext`), RSS/PSS:**
 Tools bg 17/10 → open 540/320 (mapped 0.45 s) → closed+35 s 203/104 (UI 133/54 + net proc 69/50) → net-proc kill + trim + dontneed **60/38**; reopen **0.30 s**; open again 466/294.
 Box bg 76/69 → open 541/324 (0.47 s) → closed+35 s 258/153 → released **92/71** (anon 34, thr 69); reopen **0.24–0.26 s**, open 446/280. (AppImage Box was 94/74, reopen 0.38–0.46 s: unpacked is faster.)
**F22. Two WebKit windows at once (Tools + Look, unpacked, Xvfb):** separate copies **1035 / 535**; Look's byte-identical libs hardlinked to Tools' inodes (121 files, 251 MB, one page cache) **1027 / 488** → shared payload saves **47 MB PSS, 0 RSS** (PSS only, and only when two WebKit apps are open together).
**F23. CI check run #1 (current installed builds, Xvfb, `memory/ci-run-current.json`, log `memory/logs/ci-run.log`):** the script runs end to end (8 apps together, window open, close, settle) and exits 1 with 22 budget failures, as it should today:
 background fleet 922 RSS / 750 PSS (apps + stubs), Tools window open 1391 / 1014, 30 s after close 847 / 683 (target budgets 680/540 under Xvfb). It also exposed a bug in my close step: `xdotool windowclose` destroys the X window and the app exits (Tools row read 0),
 `windowquit` does nothing without a window manager; fixed by shipping `wmclose.c` (sends WM_DELETE_WINDOW, what a title-bar button sends) next to the script. Re-run after the fix: see §7.
**F24. WebKit window floor (probe: python + system WebKitGTK 2.54, 940x780, 300 rows of static text, Xvfb):** UI process 191/88 + WebKitWebProcess 200/109 + WebKitNetworkProcess 65/32 = **456 RSS / 229 PSS** for an EMPTY page (compositing off: 452/227).
 Tools open (528/319) is only +72/+90 above that floor, trimmed Tools (325/228) is at the floor. So the fixed cost of one WebKit window is ~450 RSS / ~230 PSS before the app adds anything; RSS < 500 with a WebKit window open cannot be reached by trimming the app, only by moving pages out of RSS (trim/page-out).
**F25. Look hot re-show (AppImage, Xvfb):** first show (cold webview) 0.65 s; hide → show within 30 s (webview alive) **0.15 s** (3 runs: 0.154/0.151/0.152); after the 30 s release **0.29 s**. The keep-warm window is worth 0.14 s on every quick re-open: do not shorten Look's 30 s / Box's 15 s.
**F26. Fleet, Tools as the open window, unpacked + shim, Xvfb (`fleet-neutral-tools.log`; Clipboard here is llvmpipe 220/193, substitute ~120/96 for the real GPU):** bg 734/570 → after trim+dontneed **471/403** → Tools window open **958/691** → open + trim of all processes **716/572** → closed+30 s 544/443 → released **482/401**.
**F27. Box's own motion probe (`ARCADE_MOTION_PROBE`, `lib.rs:1236`, `motion-probe.js`: requestAnimationFrame intervals for 700 ms after every Island show), compositing on vs off** (raw: `memory/logs/box-motion-*.txt`):
 *Xvfb:* on avg 16.1–17.3 ms, max 31–69, 1 frame >25 ms per show; off avg 15.9, max 17–19, 0 frames >25 ms (off is smoother there: software-timed).
 *Real Wayland session, owner's GPU:* **on** avg 14.5–16.2 ms, p95 15–17, max 45–46 (first 113), 1 frame >25 ms per show; **off** avg 15.0–15.4, p95 **19–22**, max 31–40, 1 frame >25 ms per show.
 → on the real GPU, software compositing makes the Island animation slightly less even (p95 +4–5 ms, average +0.5 ms) with the same count of slow frames. Not identical, so OPEN2 is **not** UX-neutral for Box; unverified for Tools (no animations measured) and Look (video/PDF).
**F28. JavaScript JIT off (`JSC_useJIT=false`) on an open Tools window (Xvfb):** 513/298 → 505/291 (−8/−7): not a lever (and it slows heavy JS).
**F29. WebKit app as the open window, fleet lab (unpacked + shim, all others at trimmed-fresh level, Clipboard = llvmpipe 220/193; `fleet-{neutral,nocomp}-{tools,box,look}.log`), app tree RSS/PSS:**
 open+trimmed (UX-neutral): Tools **292/210**, Box **295/207**, Look **285/193** (fleet 716/572, 695/549, 689/537); + compositing off: Tools **242/170**, Box **243/165**, Look **236/155** (fleet 663/532, 638/499, 645/505).
 closed + released in place: Tools 60/39, Box 93/72, Look 82/61 (fleet 481/401, 491/410, 487/408).


# Prior agent agent-a8a772a604df19868.jsonl: commands and key outputs

## Read v1 plan README and research
```
# Arcade 1.0.0

Every Arcade app ships 1.0.0: untangled, without dead code, with fast CI, with nothing known broken, and polished.
This folder holds the plan. Each spec is self-contained so a Claude Code cloud session can run it cold, one repo per session.

Starting point (2026-11-06): Tools 0.4.6, Box 0.4.3, Look 0.4.3, Find 0.5.4, Lens 0.4.2, Clipboard 0.3.2,
Shelf 0.4.0, Wheel 0.5.0, all released, verified and installed. Link is on 0.4.15.
The previous plan, `../ARCADE_OVERHAUL/` (README decisions and STANDARD.md), still applies unless this plan says otherwise.

## Decisions (owner, 2026-11-06)

- **Untangle every repo** with the untangle-codebase skill
  (github.com/caldoai/skills/blob/main/skills/untangle-codebase/SKILL.md), including both extras:
  - **Comments:** remove comments that only restate the code.
  - **Tests:** remove tests that wouldn't catch a real bug, and fix the ones that fail without one. This is done last.
- **Shared code moves into Arcade Link.** Install and desktop integration, child-process launch and restart (environment
  sanitizing), single instance, and tray hosting are written once in Link. The Rust apps and Clipboard's Rust core use them.
  Shelf and Wheel (C++) keep their own implementations but must pass the same contract tests.
- **Each app ships 1.0.0 when ready.** It needs green CI and a real-desktop check on the owner's machine.
  Order: Link, Tools, then the apps.
- **The broken list comes from a local real-use audit** of all eight installed apps, done before the specs are written.
  Evidence goes in `AUDIT/`.

- **Nightly is a per-app switch in Tools.** Setting an app to Nightly replaces its stable install and shows a
  "Nightly" badge. Nightly builds from main on a schedule, is skipped when nothing changed, and promotes main CI's
  already-tested files. Switching back to Stable installs the newest stable even when its version is lower.
- **Updates download only the changed pieces, on every platform, from one shared piece store.** Tools downloads only
  missing content-defined chunks (with HTTP Range requests against GitHub release assets) for every app and for itself.
  Linux AppImages work as they are. macOS and Windows ship an uncompressed app archive next to the installer so
  chunking works there too. One chunk store is shared across apps. Any verification failure falls back to a full
  download. Measured savings are in `RESEARCH.md`.
- **CI targets:** PR checks under 8 minutes with warm caches, a full stable r
```

## Grep memory notes in real desktop audit
```
33:- A shows live actions from Box, Clipboard, Shelf and Wheel, with app glyphs and number-key hints. First Escape closes only this menu.
68:- Index: 302k files, 51,053 watched folders, 0 unwatched; idle 0.1 % CPU, 32 threads, 62 MB.
100:### LN-3 confirmed on the real desktop (zombies)
138:- Idle: 0 CPU ticks in 10 s, 8 threads.
```

## Grep memory notes in per-app audits
```
clipboard.md:15:| Image png 9 kB / jpeg 3.8 MB | yes | wl-copy | pass, thumbnails |
clipboard.md:16:| 5 MB text, 270 kB base64 text | yes | wl-copy | stored, row truncated (ok) |
clipboard.md:17:| File URIs (file + dir, symlinks, unicode name, 20 MB, broken link) | yes | text/uri-list | see CB-2 |
clipboard.md:30:| Quick picker (--overlay): open, Esc, Down/Enter | yes | CLI + xdotool | opens, Esc closes, Enter copies full 5 MB clip to wl clipboard; focus-loss close now reproduced (CB-3) |
clipboard.md:32:| Idle CPU / threads / memory, files written | yes | /proc, 30 s | see Backend |
clipboard.md:46:- 20 MB file: no clip created, no message (limit is 16 MB, "Up to 16 MB per clip" only appears in Add clip).
clipboard.md:49:Source: apps/flutter_app/lib/services/app_controller.dart:1427-1437 (`File(path).exists()` is false for directories, `size > 16 MB` returns silently).
clipboard.md:59:Item (e): a normal `--quit` in isolation does NOT crash (5 runs: idle, after heavy use, quit during a 3.8 MB capture; no coredump). The two existing SIGBUS cores (17:48 and 18:39 today, coredumpctl, PID 88197: thread tokio-rt-worker, libarcade_
clipboard.md:82:- Idle 30 s with window shown after heavy use: 0.23 % CPU, 92 threads, RSS 525 MB (owner's real background instance: 70 threads, 116 MB). RSS is large after holding a 3.8 MB JPEG and 5 MB text.
clipboard.md:83:- Files written: cfg/arcade/clipboard/settings.json, data/arcade/clipboard/{history.sqlite(+wal/shm), logs/diagnostics.log, profile.lock}, data/arcade/apps/arcade.clipboard.json, cache/mesa_shader_cache (GL). Nothing outside arcade folders exce
tools.md:11:| Background idle | yes | 30 s /proc sample | 0.00% CPU, 33 threads, 50 fds; r-idle-background.json |
tools.md:46:Fresh background idle does **not** reproduce ~9% CPU: no thread accumulated any CPU tick during 30 seconds. Thread names include 12 tokio workers, 2 tools-tray, 2 tools-shortcut-* and 2 arcade-link connections; duplication still needs explanation. 
shelf.md:25:| Idle CPU / memory | yes | /proc 30 s | 0.00 % CPU, 7 threads, 89 MB |
shelf.md:43:- Storage: default quota shows "536 MB". Default is 512 MiB (536870912) divided by 1,000,000 (ui/SettingsWindow.qml:192) and labelled MB. Show 512 MiB or use a round decimal default. The spec says MiB.
shelf.md:60:- Idle 30 s: 0.00 % CPU, 7 threads, 89 MB RSS, 21 fds.
look.md:21:| 1.3 MB / 81 MB text | yes | CLI | pass (truncated banner correct) |
look.md:22:| Idle: 0.1 CPU tick/s, no growth over 90 s; hidden-a
```

## Grep memory notes in per-app audits
```
clipboard.md:15:| Image png 9 kB / jpeg 3.8 MB | yes | wl-copy | pass, thumbnails |
clipboard.md:16:| 5 MB text, 270 kB base64 text | yes | wl-copy | stored, row truncated (ok) |
clipboard.md:17:| File URIs (file + dir, symlinks, unicode name, 20 MB, broken link) | yes | text/uri-list | see CB-2 |
clipboard.md:30:| Quick picker (--overlay): open, Esc, Down/Enter | yes | CLI + xdotool | opens, Esc closes, Enter copies full 5 MB clip to wl clipboard; focus-loss close now reproduced (CB-3) |
clipboard.md:32:| Idle CPU / threads / memory, files written | yes | /proc, 30 s | see Backend |
clipboard.md:46:- 20 MB file: no clip created, no message (limit is 16 MB, "Up to 16 MB per clip" only appears in Add clip).
clipboard.md:49:Source: apps/flutter_app/lib/services/app_controller.dart:1427-1437 (`File(path).exists()` is false for directories, `size > 16 MB` returns silently).
clipboard.md:59:Item (e): a normal `--quit` in isolation does NOT crash (5 runs: idle, after heavy use, quit during a 3.8 MB capture; no coredump). The two existing SIGBUS cores (17:48 and 18:39 today, coredumpctl, PID 88197: thread tokio-rt-worker, libarcade_
clipboard.md:82:- Idle 30 s with window shown after heavy use: 0.23 % CPU, 92 threads, RSS 525 MB (owner's real background instance: 70 threads, 116 MB). RSS is large after holding a 3.8 MB JPEG and 5 MB text.
clipboard.md:83:- Files written: cfg/arcade/clipboard/settings.json, data/arcade/clipboard/{history.sqlite(+wal/shm), logs/diagnostics.log, profile.lock}, data/arcade/apps/arcade.clipboard.json, cache/mesa_shader_cache (GL). Nothing outside arcade folders exce
tools.md:11:| Background idle | yes | 30 s /proc sample | 0.00% CPU, 33 threads, 50 fds; r-idle-background.json |
tools.md:46:Fresh background idle does **not** reproduce ~9% CPU: no thread accumulated any CPU tick during 30 seconds. Thread names include 12 tokio workers, 2 tools-tray, 2 tools-shortcut-* and 2 arcade-link connections; duplication still needs explanation. 
shelf.md:25:| Idle CPU / memory | yes | /proc 30 s | 0.00 % CPU, 7 threads, 89 MB |
shelf.md:43:- Storage: default quota shows "536 MB". Default is 512 MiB (536870912) divided by 1,000,000 (ui/SettingsWindow.qml:192) and labelled MB. Show 512 MiB or use a round decimal default. The spec says MiB.
shelf.md:60:- Idle 30 s: 0.00 % CPU, 7 threads, 89 MB RSS, 21 fds.
look.md:21:| 1.3 MB / 81 MB text | yes | CLI | pass (truncated banner correct) |
look.md:22:| Idle: 0.1 CPU tick/s, no growth over 90 s; hidden-a
```

## Snapshot owner's real instances read-only
```
=== real wheel 1360
    pid name                  RSS      PSS     anon     file    shmem     swap  thr
   1360 AppRun.wrapped      135.8     76.5     36.6     99.2      0.0     16.3   24
  TOTAL 1                   135.8     76.5     36.6     99.2      0.0     16.3   24

by mapping class (all procs; MB):  rss  pss  anon  swap  nmaps
  qt-libs                    29.2     29.2      1.3      0.4    131
  heap(brk)                  19.3     19.3     19.3      9.6      1
  anon(mmap/arena)           13.9     13.9     13.9      2.3     89
  other-libs                 16.2      5.7      0.6      1.1    538
  file:other                  6.5      4.1      0.1      0.0     17
  mesa/llvm                  49.2      3.4      0.6      2.3      9
  memfd                       0.7      0.7      0.7      0.5     16
  caches                      0.6      0.0      0.0      0.0      6
=== real shelf 1359
    pid name                  RSS      PSS     anon     file    shmem     swap  thr
   1359 arcade-shelf         69.1     57.9     30.2     38.9      0.0      6.9    8
  TOTAL 1                    69.1     57.9     30.2     38.9      0.0      6.9    8

by mapping class (all procs; MB):  rss  pss  anon  swap  nmaps
  qt-libs                    22.1     22.1      1.0      0.6     98
  heap(brk)                  21.0     21.0     21.0      2.1      1
  anon(mmap/arena)            5.4      5.4      5.4      3.4     65
  file:other                  6.3      3.9      0.1      0.0     17
  other-libs                 11.5      3.1      0.3      0.8    349
  memfd                       2.3      2.2      2.2      0.0     33
  fonts                       0.3      0.0      0.0      0.0      1
=== real look 24722
    pid name                  RSS      PSS     anon     file    shmem     swap  thr
  24722 arcade-look         190.5    115.0     68.3    122.2      0.0     18.0   54
  27844 WebKitNetworkPr      16.4      6.7      1.4     15.0      0.0     10.8    9
  TOTAL 2                   206.9    121.7     69.7    137.2      0.0     28.8   63

by mapping class (all procs; MB):  rss  pss  anon  swap  nmaps
  heap(brk)                  36.5     36.5     36.5      2.3      2
  anon(mmap/arena)           31.0     31.0     31.0     12.0    361
  webkit-libs                25.5     20.6      0.6      6.5     28
  other-libs                 36.4     18.5      0.7      5.7   1531
  file:other                 13.0     10.2      0.2      0.2     42
  mesa/llvm                  49.2      3.4      
```

## Write homemem and env helper scripts
```
            print(f"  {k:<22} {mb(v['Rss'])} {mb(v['Pss'])} {mb(v['Anonymous'])} {mb(v['Swap'])} {v['n']:>6}")
if __name__ == "__main__":
    main()
X0
X0_
X1
X1_
X92
X93
harneet   126361  0.0  0.0   6680  2272 ?        S<s  19:10   0:00 timeout 14000s Xvfb :93 -screen 0 1920x1080x24 -nolisten tcp
harneet   126362  0.0  0.4 566924 69620 ?        S<   19:10   0:07 Xvfb :93 -screen 0 1920x1080x24 -nolisten tcp
harneet   200109  0.1  0.4 527548 64388 ?        S<   21:24   0:02 Xvfb :92 -screen 0 1920x1080x24 -nolisten tcp
harneet   235707  0.0  0.0   8564  4488 ?        S<s  21:49   0:00 /bin/bash -c source /home/harneet/.claude/shell-snapshots/snapshot-bash-17939803208
harneet   235715  0.0  0.0   8564  2424 ?        S<   21:49   0:00 /bin/bash -c source /home/harneet/.claude/shell-snapshots/snapshot-bash-17939803208
```

## Launch Tools in background tray mode and sample
```
launched 236280
    pid name                  RSS      PSS     anon     file    shmem     swap  thr
 236280 arcade-tools         50.2     43.2      5.4     44.8      0.0      5.4   31
  TOTAL 1                    50.2     43.2      5.4     44.8      0.0      5.4   31   (+AppImage runtime stub rss=23.0 pss=23.0)
```

## Sample Tools background idle over time with maps
```
    pid name                  RSS      PSS     anon     file    shmem     swap  thr
 236280 arcade-tools         50.2     43.2      5.4     44.8      0.0      5.4   29
  TOTAL 1                    50.2     43.2      5.4     44.8      0.0      5.4   29   (+AppImage runtime stub rss=23.0 pss=23.0)

by mapping class (MB): rss  pss  anon  swap  nmaps
  other-libs                 24.1     17.6      1.1      1.5    698
  file:other                 12.6     12.1      0.1      0.7      9
  webkit-libs                 9.5      9.5      0.4      3.1     14
  anon(mmap/arena)            3.1      3.1      3.1      0.0    133
  heap(brk)                   0.7      0.7      0.7      0.0      1
```

## Identify windows and sample Tools with window open
```
927:  Window 927   Position: 0,0 (screen: 0)   Geometry: 1920x1080 
4194320: Arcade Tools Window 4194320   Position: 0,0 (screen: 0)   Geometry: 940x780 
4194321:  Window 4194321   Position: -1,-1 (screen: 0)   Geometry: 1x1 
    pid name                  RSS      PSS     anon     file    shmem     swap  thr
 238005 WebKitWebProces     252.4    156.2     88.3    158.3      5.8      0.0   56
 236280 arcade-tools        193.3     89.8     39.7    145.2      8.4      4.4   74
 237957 WebKitNetworkPr      60.0     32.5     19.1     40.9      0.0      0.0   10
 238004 dbus-broker-lau       3.9      0.4      0.3      3.7      0.0      0.0    1
 238006 dbus-broker           2.5      0.2      0.2      2.4      0.0      0.0    1
  TOTAL 5                   512.2    279.1    147.6    350.4     14.2      4.4  142   (+AppImage runtime stub rss=22.6 pss=22.6)

by mapping class (MB): rss  pss  anon  swap  nmaps
  anon(mmap/arena)           83.4     83.4     83.4      0.0    685
  webkit-libs               123.9     78.4      7.8      2.8     47
  heap(brk)                  42.4     42.4     42.4      0.0      5
  other-libs                101.7     35.2      7.6      1.0   2375
  file:other                 22.0     16.6      0.3      0.5     54
  mesa/llvm                 119.9     14.6      5.8      0.0     18
  memfd                      11.2      5.6      0.0      0.0      9
  shm                         2.8      1.4      0.0      0.0      1
  fonts                       3.6      0.3      0.0      0.0      9
  caches                      1.0      0.2      0.0      0.0      9
```

## Navigate Tools pages and sample memory
```
Apps RSS 509 PSS 282 anon 150 {'arcade-tools': 195, 'WebKitNetwor': 60, 'WebKitWebPro': 254}
Updates RSS 510 PSS 283 anon 150 {'arcade-tools': 195, 'WebKitNetwor': 60, 'WebKitWebPro': 254}
Shortcuts RSS 513 PSS 286 anon 153 {'arcade-tools': 196, 'WebKitNetwor': 60, 'WebKitWebPro': 257}
Learn RSS 516 PSS 288 anon 155 {'arcade-tools': 196, 'WebKitNetwor': 60, 'WebKitWebPro': 259}
Connections RSS 515 PSS 288 anon 155 {'arcade-tools': 196, 'WebKitNetwor': 60, 'WebKitWebPro': 259}
Engines RSS 516 PSS 289 anon 155 {'arcade-tools': 196, 'WebKitNetwor': 60, 'WebKitWebPro': 260}
Settings RSS 529 PSS 301 anon 168 {'arcade-tools': 201, 'WebKitNetwor': 60, 'WebKitWebPro': 268}
Home RSS 530 PSS 303 anon 169 {'arcade-tools': 202, 'WebKitNetwor': 60, 'WebKitWebPro': 268}
Apps RSS 530 PSS 303 anon 169 {'arcade-tools': 202, 'WebKitNetwor': 60, 'WebKitWebPro': 268}
Learn RSS 530 PSS 303 anon 169 {'arcade-tools': 202, 'WebKitNetwor': 60, 'WebKitWebPro': 268}
```

## Close Tools window and watch memory return
```
2097153|xdg-desktop-portal-gtk|10x10
4194305|arcade-tools|10x10
8388609|WebKitWebProcess|10x10
4194320|Arcade Tools|940x780
+3s RSS 231 PSS 120 anon 41 {'arcade-tools': 171, 'WebKitNetwor': 60}
+10s RSS 231 PSS 120 anon 41 {'arcade-tools': 171, 'WebKitNetwor': 60}
+30s RSS 231 PSS 120 anon 41 {'arcade-tools': 171, 'WebKitNetwor': 60}
+60s RSS 231 PSS 120 anon 41 {'arcade-tools': 171, 'WebKitNetwor': 60}
2097153|xdg-desktop-portal-gtk|10x10
4194305|arcade-tools|10x10
```

## Check cycle progress
```
real
tools-cycles.txt
tools.jsonl
closed-+60s            RSS  231 PSS  120 anon   41 swap   8 thr  77 | arcade-too:171 WebKitNetw:60
```

## Debug stuck cycle
```
<persisted-output>
Output too large (2.5MB). Full output saved to: /home/harneet/.claude/projects/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/tool-results/b6301060c.txt

Preview (first 2KB):
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: bc: command not found
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: [: =: unary operator expected
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: bc: command not found
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: [: =: unary operator expected
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: bc: command not found
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: [: =: unary operator expected
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: bc: command not found
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: [: =: unary operator expected
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: bc: command not found
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: [: =: unary operator expected
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: bc: command not found
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: [: =: unary operator expected
/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/tools_cycle.sh: line 8: bc: command not found
...
</persisted-output>
```

## Build Python driver and test 2 Tools cycles
```
cycle 1: window_mapped=0.01s painted=20.03s px=None
cycle1-open              RSS  515 PSS  286 anon  149 swap   8 thr 132 | WebKitWebP:264 arcade-too:191 WebKitNetw:60
cycle1-closed            RSS  240 PSS  128 anon   47 swap   8 thr  82 | arcade-too:180 WebKitNetw:60
cycle 2: window_mapped=0.44s painted=20.47s px=None
cycle2-open              RSS  510 PSS  299 anon  147 swap   8 thr 132 | WebKitWebP:258 arcade-too:192 WebKitNetw:60
cycle2-closed            RSS  242 PSS  144 anon   49 swap   8 thr  83 | arcade-too:182 WebKitNetw:60
```

## Check Tools cycle progress
```
cycle 1: window_mapped=0.38s painted=0.44s px=161619
cycle1-open              RSS  525 PSS  314 anon  162 swap   8 thr 145 | WebKitWebP:267 arcade-too:198 WebKitNetw:60
cycle1-closed            RSS  249 PSS  151 anon   56 swap   8 thr  83 | arcade-too:189 WebKitNetw:60
cycle 2: window_mapped=0.38s painted=0.45s px=161619
```

## Survey Look source for webview lifecycle
```
artifacts
assets
CHANGELOG.md
dist
docs
examples
index.html
LICENSE
node_modules
package.json
package-lock.json
public
README.md
requirements-dev.txt
rust-toolchain.toml
scripts
spec
src
src-tauri
tests
tools
tsconfig.json
VENDORED.md
vite.config.ts
app.rs
archive.rs
cli.rs
commands.rs
config.rs
detect.rs
e2e.rs
font.rs
fsx.rs
imaging.rs
installer.rs
installer_ui.rs
integration
lib.rs
link_consumer.rs
link.rs
main.rs
markdown.rs
media.rs
mediaserver.rs
office.rs
plugins.rs
portable_settings.rs
protocol.rs
rtf.rs
slides.rs
table.rs
text.rs
tray.rs
util.rs
window_geometry.rs
xml.rs
src-tauri/src/mediaserver.rs:3://! WebKitGTK's GStreamer pipeline doesn't stream reliably from custom URI schemes, but it
src-tauri/src/main.rs:1:// Prevents an extra console window on Windows in release builds.
src-tauri/src/config.rs:11:    /// Minutes before a non-resident process exits (0 = never). Webviews release after 30 s.
src-tauri/src/installer.rs:609:    data_folders.extend(dirs::home_dir().map(|h| h.join("Library/WebKit").join(IDENTIFIER)));
src-tauri/src/e2e.rs:20:/// Shorten only the existing release delay inside the private native-test runner.
src-tauri/src/e2e.rs:22:pub fn idle_release_delay(default: Duration) -> Duration {
src-tauri/src/e2e.rs:25:            std::env::var("ALOOK_E2E_RELEASE_MILLIS")
src-tauri/src/lib.rs:103:    // previews are webviews, and WebKit needs the AppImage's own directory.
src-tauri/src/lib.rs:234:            // WebKitGTK streams media reliably only over HTTP (see mediaserver.rs).
src-tauri/src/link_consumer.rs:512:        Ok(Some(arcade_link::manifest::releases_url(app_id).into()))
src-tauri/src/link_consumer.rs:947:/// Get opens the installed manager; otherwise returns the canonical release
src-tauri/src/tray.rs:52:/// Successors wait for the old process to release the single-instance slot.
src-tauri/src/app.rs:13:use tauri::{AppHandle, Emitter, Manager, WebviewUrl, WebviewWindow, WebviewWindowBuilder};
src-tauri/src/app.rs:36:// WebKit/WebView2 processes after browsing stops (SPEC §17.5), even with idleMinutes = 0.
src-tauri/src/app.rs:37:const WEBVIEW_IDLE_RELEASE: Duration = Duration::from_secs(30);
src-tauri/src/app.rs:49:        // Cancel an old release before rendering starts, not just after it paints.
src-tauri/src/app.rs:223:fn release_webview_ipc_on_destroy(window: &WebviewWindow) -> tauri::Result<()> {
src-tauri/src/app.rs:226:    use webkit2gtk::WebViewExt;
src-tauri/src/app.rs:268:        WebviewWindowBuilder::new(app, SETT
```

## Cycle progress and Clipboard layout
```
cycle 1: window_mapped=0.38s painted=0.44s px=161619
cycle1-open              RSS  525 PSS  314 anon  162 swap   8 thr 145 | WebKitWebP:267 arcade-too:198 WebKitNetw:60
cycle1-closed            RSS  249 PSS  151 anon   56 swap   8 thr  83 | arcade-too:189 WebKitNetw:60
cycle 2: window_mapped=0.38s painted=0.45s px=161619
cycle2-open              RSS  525 PSS  314 anon  162 swap   8 thr 143 | WebKitWebP:267 arcade-too:198 WebKitNetw:60
cycle2-closed            RSS  249 PSS  152 anon   57 swap   8 thr  83 | arcade-too:189 WebKitNetw:60
cycle 3: window_mapped=0.44s painted=0.45s px=161619
cycle3-open              RSS  527 PSS  315 anon  164 swap   8 thr 144 | WebKitWebP:268 arcade-too:200 WebKitNetw:60
cycle3-closed            RSS  251 PSS  153 anon   58 swap   8 thr  83 | arcade-too:191 WebKitNetw:60
cycle 4: window_mapped=0.38s painted=0.44s px=161619
cycle4-open              RSS  527 PSS  315 anon  163 swap   8 thr 141 | WebKitWebP:267 arcade-too:200 WebKitNetw:60
cycle4-closed            RSS  251 PSS  153 anon   58 swap   8 thr  83 | arcade-too:191 WebKitNetw:60
apps
assets
Cargo.lock
Cargo.toml
CHANGELOG.md
core
deploy
docs
flutter_rust_bridge.yaml
LICENSE
packaging
platform
README.md
rust-toolchain.toml
scripts
services
spec
target
tests
tools
apps:
flutter_app

apps/flutter_app:
analysis_options.yaml
android
assets
build
integration_test
ios
lib
linux
macos
pubspec.lock
pubspec_overrides.yaml
pubspec.yaml
test
windows
```

## Look at prior headless sway harness
```
xwayland disable
floating_modifier Mod4
. /tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/audit-cswt/env.sh
A=/home/harneet/Applications/Arcade
E=/home/harneet/Work/Coding/ARCADE_V1/AUDIT
shot(){ timeout 15 import -window root "$1"; }
mine(){ ps -eo pid,etimes,pcpu,nlwp,rss,comm,args --no-headers | awk -v s="$S" '1' | grep -E "$1" | grep -v grep | cut -c1-200; }
# usage: idle PID SECS -> cpu% over interval, threads, rss MB, fds
idle(){ local p=$1 s=${2:-30}; local t0=$(awk '{print $14+$15}' /proc/$p/stat); sleep $s; local t1=$(awk '{print $14+$15}' /proc/$p/stat); echo "pid=$p cpu=$(awk -v a=$t0 -v b=$t1 -v s=$s -v h=$(getconf CLK_TCK) "BEGIN{printf \"%.2f\", (b-a)/h/s*100}")% threads=$(ls /proc/$p/task | wc -l) rss=$(awk '/VmRSS/{print int($2/1024)}' /proc/$p/status)MB fds=$(ls /proc/$p/fd | wc -l)"; }
export ARCADE_NO_INSTALL_PROMPT=1
wl(){ env -u DISPLAY -u GDK_BACKEND QT_QPA_PLATFORM=wayland WAYLAND_DISPLAY=wayland-1 GDK_BACKEND=wayland "$@"; }
cp_(){ env -u DISPLAY WAYLAND_DISPLAY=wayland-1 "$@"; }
export WAYLAND_DISPLAY=wayland-1
wlc(){ WAYLAND_DISPLAY=wayland-1 wl-copy "$@"; }
. /tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/audit-cswt/h.sh
record
sensible-browser
xdg-open
xowner
#!/usr/bin/python3
import sys,json,os
from pathlib import Path
p=Path("/tmp/cswt-c7347b9d/action-events.jsonl")
with p.open("a") as f:f.write(json.dumps({"args":sys.argv[1:],"cwd":os.getcwd()})+"\n")
#!/bin/sh
exec /tmp/cswt-c7347b9d/bin/record sensible-browser "$@"
#!/bin/sh
exec /tmp/cswt-c7347b9d/bin/record xdg-open "$@"
ELF          >    P      @       �9          @ 8  @         @       @       @       H      H                   �      �      �                                                         `
      `
                                        �      �                                           �      �                   �-      �=      �=      �      �                   �-      �=      �=      �      �                   �      �      �      $       $                    `!      `!      `!      @       @                    �!      �!      �!                             S�td   `!      `!      `!      @       @              P�td   (       (       (       $       $              T�td   �       �       �       �       �              Q�td                                                  R�td   �-      �=      �=      @
```

## Check Tools cycle results so far
```
cycle1-open              RSS  525 PSS  314 anon  162 swap   8 thr 145 | WebKitWebP:267 arcade-too:198 WebKitNetw:60
cycle1-closed            RSS  249 PSS  151 anon   56 swap   8 thr  83 | arcade-too:189 WebKitNetw:60
cycle2-open              RSS  525 PSS  314 anon  162 swap   8 thr 143 | WebKitWebP:267 arcade-too:198 WebKitNetw:60
cycle2-closed            RSS  249 PSS  152 anon   57 swap   8 thr  83 | arcade-too:189 WebKitNetw:60
cycle3-open              RSS  527 PSS  315 anon  164 swap   8 thr 144 | WebKitWebP:268 arcade-too:200 WebKitNetw:60
cycle3-closed            RSS  251 PSS  153 anon   58 swap   8 thr  83 | arcade-too:191 WebKitNetw:60
cycle4-open              RSS  527 PSS  315 anon  163 swap   8 thr 141 | WebKitWebP:267 arcade-too:200 WebKitNetw:60
cycle4-closed            RSS  251 PSS  153 anon   58 swap   8 thr  83 | arcade-too:191 WebKitNetw:60
cycle5-open              RSS  527 PSS  315 anon  164 swap   8 thr 145 | WebKitWebP:266 arcade-too:201 WebKitNetw:60
cycle5-closed            RSS  251 PSS  153 anon   58 swap   8 thr  83 | arcade-too:191 WebKitNetw:60
cycle6-open              RSS  525 PSS  313 anon  161 swap   8 thr 144 | WebKitWebP:266 arcade-too:199 WebKitNetw:60
cycle6-closed            RSS  250 PSS  152 anon   57 swap   8 thr  83 | arcade-too:190 WebKitNetw:60
cycle7-open              RSS  524 PSS  313 anon  161 swap   8 thr 144 | WebKitWebP:265 arcade-too:199 WebKitNetw:60
```

## Add top-mappings tool and wait for cycles
```
cycle9-closed            RSS  250 PSS  153 anon   57 swap   8 thr  91 | arcade-too:190 WebKitNetw:60
cycle 10: window_mapped=0.38s painted=0.44s px=161619
cycle10-open             RSS  531 PSS  320 anon  168 swap   8 thr 143 | WebKitWebP:268 arcade-too:204 WebKitNetw:60
cycle10-closed           RSS  253 PSS  156 anon   60 swap   8 thr  83 | arcade-too:193 WebKitNetw:60
```

## Top mappings for Tools closed state
```
    pid name                  RSS      PSS     anon     file    shmem     swap  thr
 236280 arcade-tools        188.7    113.2     37.1    146.0      5.6      8.3   71
 237957 WebKitNetworkPr      59.8     38.0     18.7     41.1      0.0      0.0    8
  TOTAL 2                   248.5    151.1     55.8    187.1      5.6      8.3   79   (+AppImage runtime stub rss=21.0 pss=21.0)

by mapping class (MB): rss  pss  anon  swap  nmaps
  anon(mmap/arena)           41.1     41.1     41.1      0.0    361
  webkit-libs                53.0     35.5      4.0      3.0     28
  other-libs                 59.2     27.5      3.8      1.8   1519
  mesa/llvm                  62.5     20.7      0.2      2.7      9
  file:other                 19.2     16.7      0.0      0.8     25
  heap(brk)                   6.5      6.5      6.5      0.0      2
  shm                         5.6      2.8      0.0      0.0      1
  fonts                       0.8      0.0      0.0      0.0      2
== 236280 arcade-tools
    RSS     PSS    anon   swap    n  path
   50.5    18.8     0.0    1.3    4  /usr/lib/libLLVM.so.23.1
   29.0    29.0    29.0    0.0  254  [anon]
   18.7    12.5     0.4    2.8    7  $MNT/usr/lib/libwebkit2gtk-4.1.so.0
   16.6    16.6     0.0    0.8    6  $MNT/usr/bin/arcade-tools
   11.9     1.9     0.2    1.4    5  /usr/lib/libgallium-26.2.5-arch3.1.so
   11.4     8.9     0.2    0.2    7  $MNT/usr/lib/libjavascriptcoregtk-4.1.so.0
    6.1     6.1     6.1    0.0    1  [heap]
    5.6     2.8     0.0    0.0    1  /SYSV00000000 (deleted)
    4.7     4.3     0.0    0.1    6  $MNT/usr/lib/libgtk-3.so.0
    1.9     0.0     0.0    0.0    5  /usr/lib/libc.so.6
    1.8     0.1     0.0    0.1    5  /usr/lib/libstdc++.so.6.0.36
    1.6     0.8     0.0    0.0    6  $MNT/usr/lib/libgio-2.0.so.0
== 237957 WebKitNetworkPr
    RSS     PSS    anon   swap    n  path
   17.4    11.1     3.2    0.0    7  $MNT/usr/lib/libwebkit2gtk-4.1.so.0
   12.1    12.1    12.1    0.0  107  [anon]
    5.5     3.0     0.4    0.0    7  $MNT/usr/lib/libjavascriptcoregtk-4.1.so.0
    1.9     0.1     0.1    0.0    5  /usr/lib/libstdc++.so.6.0.36
    1.8     0.0     0.0    0.0    5  /usr/lib/libc.so.6
    1.6     0.8     0.0    0.0    6  $MNT/usr/lib/libgio-2.0.so.0
    1.3     0.7     0.1    0.0    6  $MNT/usr/lib/libicui18n.so.70
    1.1     1.0     0.0    0.0    5  $MNT/usr/lib/libsqlite3.so.0
    0.9     0.4     0.0    0.0    7  $MNT/usr/lib/libglib-2.0.so.0
    0.8     0.5     0.1    0.0    6  $MNT/usr/lib/l
```

## Start Box in background and sample idle
```
bg-10s                   RSS   73 PSS   66 anon   20 swap   0 thr  40 | arcade-des:73
bg-40s                   RSS   73 PSS   66 anon   20 swap   0 thr  38 | arcade-des:73
Arcade Box shortcut status: state=identity_unavailable message=Could not register portal identity `dev.arcade.Box`. Ensure `dev.arcade.Box.desktop` is installed before launching: ZBus Error: org.freedesktop.portal.Error.Failed: Could not register app ID: App info not found for 'dev.arcade.Box'
```

## Show Box Island and sample
```
island window 10485761 after 0.37s
island-open-idle         RSS  537 PSS  320 anon  171 swap   0 thr 142 | WebKitWebP:256 arcade-des:219 WebKitNetw:62
[('2097153', 'xdg-desktop-portal-gtk'), ('4194305', 'arcade-tools'), ('8388609', 'xdg-desktop-portal-gtk'), ('10485761', 'Arcade Box'), ('10485777', 'Arcade Box')]
```

## Skip Box onboarding and screenshot
```
island-after-skip        RSS  533 PSS  316 anon  167 swap   0 thr 140 | WebKitWebP:257 arcade-des:214 WebKitNetw:63
```

## Drive many Box tools and sample memory
```
tool-0-6*7               RSS  563 PSS  345 anon  194 swap   0 thr 138 | WebKitWebP:282 arcade-des:219 WebKitNetw:63
tool-1-14 gb to mb       RSS  562 PSS  344 anon  193 swap   0 thr 138 | WebKitWebP:281 arcade-des:219 WebKitNetw:63
tool-2-calculator        RSS  559 PSS  342 anon  190 swap   0 thr 128 | WebKitWebP:278 arcade-des:219 WebKitNetw:63
tool-3-timer 3s          RSS  555 PSS  337 anon  186 swap   0 thr 127 | WebKitWebP:278 arcade-des:214 WebKitNetw:63
tool-4-json format       RSS  256 PSS  150 anon   55 swap   0 thr  79 | arcade-des:193 WebKitNetw:63
tool-5-base64            RSS  256 PSS  150 anon   55 swap   0 thr  79 | arcade-des:193 WebKitNetw:63
tool-6-password          RSS  256 PSS  150 anon   55 swap   0 thr  77 | arcade-des:193 WebKitNetw:63
tool-7-qr code           RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-8-uuid              RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-9-color picker      RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-10-hash             RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-11-lorem            RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-12-regex            RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-13-diff             RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-14-markdown         RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-15-csv              RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-16-image resize     RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-17-image compress   RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-18-pdf merge        RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
tool-19-screenshot       RSS  256 PSS  150 anon   55 swap   0 thr  76 | arcade-des:193 WebKitNetw:63
```

## Run Box tools in single sessions with sampling
```
shown after 0.40s
tool2-0-calculator       RSS  539 PSS  320 anon  166 swap   0 thr 132 | WebKitWebP:267 arcade-des:209 WebKitNetw:63 vis
  (re-shown)
tool2-1-timer            RSS  534 PSS  314 anon  160 swap   0 thr 130 | WebKitWebP:261 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-2-json             RSS  532 PSS  313 anon  158 swap   0 thr 128 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-3-base64           RSS  534 PSS  314 anon  160 swap   0 thr 129 | WebKitWebP:261 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-4-password         RSS  533 PSS  314 anon  159 swap   0 thr 129 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-5-qr               RSS  533 PSS  313 anon  159 swap   0 thr 121 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-6-uuid             RSS  533 PSS  313 anon  159 swap   0 thr 129 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-7-color            RSS  533 PSS  314 anon  159 swap   0 thr 129 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-8-hash             RSS  533 PSS  314 anon  159 swap   0 thr 128 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-9-lorem            RSS  533 PSS  314 anon  159 swap   0 thr 121 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-10-regex           RSS  533 PSS  314 anon  159 swap   0 thr 126 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-11-diff            RSS  535 PSS  316 anon  161 swap   0 thr 119 | WebKitWebP:262 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-12-markdown        RSS  532 PSS  313 anon  158 swap   0 thr 127 | WebKitWebP:259 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-13-csv             RSS  532 PSS  313 anon  158 swap   0 thr 120 | WebKitWebP:259 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-14-image resize    RSS  534 PSS  315 anon  160 swap   0 thr 128 | WebKitWebP:261 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-15-image compress  RSS  533 PSS  314 anon  159 swap   0 thr 120 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-16-pdf             RSS  533 PSS  313 anon  158 swap   0 thr 128 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-17-screenshot      RSS  533 PSS  313 anon  159 swap   0 thr 128 | WebKitWebP:260 arcade-des:210 WebKitNetw:63 vis
  (re-shown)
tool2-18-units           RSS  533 PSS  313 anon  159 swap   0 thr 127 | WebKitWebP:260 a
```

## Open Box dashboard and sample
```
pre-dashboard-resident   RSS  528 PSS  308 anon  153 swap   0 thr 124 | WebKitWebP:259 arcade-des:206 WebKitNetw:63
dashboard win 10489440 0.26s
dashboard-open-idle      RSS  540 PSS  317 anon  163 swap   0 thr 132 | WebKitWebP:267 arcade-des:211 WebKitNetw:63
dashboard-scrolled       RSS  539 PSS  317 anon  162 swap   0 thr 132 | WebKitWebP:266 arcade-des:211 WebKitNetw:63
```

## Navigate Box dashboard pages sampling memory
```
dash-nav-Favorites       RSS  534 PSS  311 anon  156 swap   0 thr 121 | WebKitWebP:265 arcade-des:206 WebKitNetw:63
dash-nav-Recent          RSS  534 PSS  311 anon  156 swap   0 thr 121 | WebKitWebP:265 arcade-des:206 WebKitNetw:63
dash-nav-Jobs            RSS  534 PSS  311 anon  156 swap   0 thr 121 | WebKitWebP:265 arcade-des:206 WebKitNetw:63
dash-nav-Pipelines       RSS  541 PSS  318 anon  163 swap   0 thr 121 | WebKitWebP:267 arcade-des:211 WebKitNetw:63
dash-nav-Plugins         RSS  541 PSS  318 anon  162 swap   0 thr 121 | WebKitWebP:267 arcade-des:211 WebKitNetw:63
dash-nav-Engines         RSS  541 PSS  318 anon  163 swap   0 thr 122 | WebKitWebP:267 arcade-des:211 WebKitNetw:63
dash-nav-Settings        RSS  551 PSS  327 anon  170 swap   0 thr 126 | WebKitWebP:276 arcade-des:212 WebKitNetw:63
dash-nav-Tools           RSS  557 PSS  333 anon  176 swap   0 thr 126 | WebKitWebP:283 arcade-des:212 WebKitNetw:63
dash-nav-PDF             RSS  556 PSS  332 anon  175 swap   0 thr 123 | WebKitWebP:281 arcade-des:212 WebKitNetw:63
dash-nav-Images          RSS  554 PSS  331 anon  174 swap   0 thr 123 | WebKitWebP:280 arcade-des:212 WebKitNetw:63
dash-nav-Video           RSS  555 PSS  331 anon  174 swap   0 thr 123 | WebKitWebP:280 arcade-des:212 WebKitNetw:63
dash-nav-Audio           RSS  555 PSS  332 anon  175 swap   0 thr 123 | WebKitWebP:281 arcade-des:212 WebKitNetw:63
dash-nav-TextData        RSS  550 PSS  326 anon  169 swap   0 thr 122 | WebKitWebP:280 arcade-des:207 WebKitNetw:63
```

## Close Box windows and watch memory over time
```
12:const RELEASE_AFTER_CLOSE: Duration = Duration::from_secs(15);
96:/// Destroys the hidden dashboard after `RELEASE_AFTER_CLOSE` unless it was
102:        std::thread::sleep(RELEASE_AFTER_CLOSE);
closed-all-+3s           RSS  554 PSS  331 anon  174 swap   0 thr 121 | WebKitWebP:280 arcade-des:212 WebKitNetw:63
closed-all-+10s          RSS  548 PSS  327 anon  173 swap   0 thr 121 | WebKitWebP:277 arcade-des:208 WebKitNetw:63
closed-all-+20s          RSS  263 PSS  156 anon   58 swap   0 thr  79 | arcade-des:200 WebKitNetw:62
closed-all-+40s          RSS  263 PSS  156 anon   58 swap   0 thr  76 | arcade-des:200 WebKitNetw:62
closed-all-+70s          RSS  263 PSS  156 anon   58 swap   0 thr  76 | arcade-des:200 WebKitNetw:62
```

## Quit Box and view Look help
```
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
  File "/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem/bin/drv.py", line 65, in fmt
    return '%-24s RSS %4.0f PSS %4.0f anon %4.0f swap %3.0f thr %3d | %s' % (o.get('label', ''), t['rss']/1024, t['pss']/1024, t['anon']/1024, t['swap']/1024, t['threads'],
                                                                                                 ~^^^^^^^
KeyError: 'rss'
unix:path=/tmp/dbus-sKeJ2WzDAg,guid=cfeeddab95f078168de37d086aee02c7
Arcade Look: Press Space, see anything.

USAGE:
    arcade-look [OPTIONS] [PATH]

ARGS:
    PATH                     File or folder to preview (a file:// URI works too)

OPTIONS:
    --background             Start in the background without a window
    --service                Compatibility alias for --background
    --status                 Print running, version and Link state as one-line JSON
    --show                   Show the preview
    --hide                   Hide the preview
    --toggle                 Preview the selection or close the preview
    --settings               Open Settings
    --restart                Restart the running instance
    --install [--silent] [--no-launch] [--keep-download] [--channel C]
                             Install this AppImage or move this macOS app bundle
    --install-integration    Alias for --install
    --uninstall [--silent] [--remove-data]
                             Remove this installation using its receipt
    --uninstall-integration  Alias for --uninstall
    --repair                 Repair integration recorded in the install receipt
    --integration-status     Print receipt and integration status as JSON
    --quit                   Quit the running instance
    --arcade-manifest        Print the Arcade Link manifest (no side effects)
    --arcade-invoke          Run one Arcade Link request from stdin, without any UI
    -h, --help               Show this help
    -V, --version            Show the version

KEYS (in the preview window):
    Space / Esc  close         ←/→  previous / next file     Enter  open with default app
    I  info panel   F  fullscreen   +/-/0  zoom   ?  all shortcuts   Ctrl+Q  quit
```

## Start Look service and sample idle
```
bg-10s                   RSS   50 PSS   43 anon    9 swap   0 thr  37 | arcade-loo:50
bg-40s                   RSS   50 PSS   43 anon    9 swap   0 thr  35 | arcade-loo:50
```

## Open a 5MB text file in Look and sample
```
window 12582928 after 0.64s [('12582928', 'big.txt — Arcade Look')]
open-big.txt             RSS  653 PSS  435 anon  302 swap   0 thr 134 | WebKitWebP:386 arcade-loo:207 WebKitNetw:60
```

## Navigate Look through files sampling memory
```
Window 12582928   Position: 440,180 (screen: 0)   Geometry: 1040x720
nav0-big.txt — Arcade Look RSS  590 PSS  371 anon  238 swap   0 thr 135 | WebKitWebP:329 arcade-loo:201 WebKitNetw:60
nav1-big.txt — Arcade Look RSS  590 PSS  371 anon  237 swap   0 thr 132 | WebKitWebP:328 arcade-loo:201 WebKitNetw:60
nav2-big.txt — Arcade Look RSS  589 PSS  370 anon  236 swap   0 thr 130 | WebKitWebP:327 arcade-loo:201 WebKitNetw:60
nav3-big.txt — Arcade Look RSS  589 PSS  370 anon  236 swap   0 thr 130 | WebKitWebP:327 arcade-loo:201 WebKitNetw:60
nav4-big.txt — Arcade Look RSS  588 PSS  370 anon  236 swap   0 thr 130 | WebKitWebP:327 arcade-loo:201 WebKitNetw:60
nav5-big.txt — Arcade Look RSS  588 PSS  370 anon  236 swap   0 thr 130 | WebKitWebP:327 arcade-loo:201 WebKitNetw:60
```

## Open each big file type in Look and sample
```
open-big.jpg-t4          RSS  636 PSS  417 anon  283 swap   0 thr 129 | WebKitWebP:358 arcade-loo:218 WebKitNetw:60 peakRSS 637
open-big.png-t4          RSS  601 PSS  382 anon  248 swap   0 thr 137 | WebKitWebP:324 arcade-loo:217 WebKitNetw:60 peakRSS 601
open-big.pdf-t4          RSS  713 PSS  493 anon  352 swap   0 thr 144 | WebKitWebP:435 arcade-loo:218 WebKitNetw:60 peakRSS 713
open-big.mp4-t4          RSS  775 PSS  551 anon  378 swap   0 thr 159 | WebKitWebP:492 arcade-loo:218 WebKitNetw:65 peakRSS 778
open-big.md-t4           RSS  880 PSS  654 anon  481 swap   0 thr 146 | WebKitWebP:585 arcade-loo:230 WebKitNetw:64 peakRSS 903
open-big.txt-t4          RSS  878 PSS  653 anon  479 swap   0 thr 141 | WebKitWebP:582 arcade-loo:232 WebKitNetw:64 peakRSS 878
```

## Hide Look and watch memory release
```
hidden-+2s               RSS  809 PSS  584 anon  410 swap   0 thr 132 | WebKitWebP:513 arcade-loo:232 WebKitNetw:64
hidden-+10s              RSS  804 PSS  581 anon  410 swap   0 thr 132 | WebKitWebP:510 arcade-loo:229 WebKitNetw:64
hidden-+25s              RSS  785 PSS  562 anon  392 swap   0 thr 132 | WebKitWebP:496 arcade-loo:225 WebKitNetw:64
hidden-+33s              RSS  286 PSS  180 anon   97 swap   0 thr  74 | arcade-loo:221 WebKitNetw:64
hidden-+40s              RSS  286 PSS  180 anon   97 swap   0 thr  74 | arcade-loo:221 WebKitNetw:64
hidden-+70s              RSS  286 PSS  180 anon   97 swap   0 thr  72 | arcade-loo:221 WebKitNetw:64
```

## Hide Look and watch memory release
```
hidden-+2s               RSS  809 PSS  584 anon  410 swap   0 thr 132 | WebKitWebP:513 arcade-loo:232 WebKitNetw:64
hidden-+10s              RSS  804 PSS  581 anon  410 swap   0 thr 132 | WebKitWebP:510 arcade-loo:229 WebKitNetw:64
hidden-+25s              RSS  785 PSS  562 anon  392 swap   0 thr 132 | WebKitWebP:496 arcade-loo:225 WebKitNetw:64
hidden-+33s              RSS  286 PSS  180 anon   97 swap   0 thr  74 | arcade-loo:221 WebKitNetw:64
hidden-+40s              RSS  286 PSS  180 anon   97 swap   0 thr  74 | arcade-loo:221 WebKitNetw:64
hidden-+70s              RSS  286 PSS  180 anon   97 swap   0 thr  72 | arcade-loo:221 WebKitNetw:64
```

## Measure owner's real fleet read-only
```
app       procs     RSS     PSS anon+shm    swap  thr  stubRSS  stubPSS  processes
box           2   208.5   119.7     68.4    41.8   61     18.4     18.4  WebKitNetworkP,arcade-desktop
clipboard     1   174.6   102.9     69.4     0.0   73     18.5     18.5  clipboard
find          1    51.0    45.9     36.7    10.9   31      0.7      0.7  arcade-find
lens          1     7.0     4.6      2.0     3.1   10     13.9     13.9  arcade-lens
look          2   194.3   109.7     55.9    42.7   63     16.8     16.6  WebKitNetworkP,arcade-look
shelf         1    60.0    48.9     21.1    16.0    8      5.5      5.5  arcade-shelf
tools         2   253.4   146.3     62.5     9.1   73     21.0     21.0  WebKitNetworkP,arcade-tools
wheel         1   135.4    76.7     36.7    16.3   24     16.9     16.9  AppRun.wrapped
FLEET            1084.1   654.6    352.8   139.9  343    111.8    111.5
```

## Inspect AppImage FUSE stub memory
```
== 24731 Arcade-Look.App pplications/Arcade/Arcade-Look.AppImage
VmRSS:	   17192 kB RssAnon:	   16784 kB RssFile:	     408 kB VmSwap:	    7492 kB Threads:	2 
    RSS     PSS    anon   swap    n  path
   16.4    16.4    16.4    7.3   20  [anon]
    0.4     0.2     0.0    0.0    4  /home/harneet/Applications/Arcade/Arcade-Look.AppImage
    0.0     0.0     0.0    0.0    1  [vdso]
    0.0     0.0     0.0    0.0    1  [stack]
    0.0     0.0     0.0    0.0    1  [vvar]
    0.0     0.0     0.0    0.0    1  [vvar_vclock]
== 228194 Arcade-Tools.Ap plications/Arcade/Arcade-Tools.AppImage
VmRSS:	   21548 kB RssAnon:	   20832 kB RssFile:	     716 kB VmSwap:	     164 kB Threads:	2 
    RSS     PSS    anon   swap    n  path
   20.3    20.3    20.3    0.1   14  [anon]
    0.7     0.7     0.0    0.0    4  /home/harneet/Applications/Arcade/Arcade-Tools.AppImage
    0.0     0.0     0.0    0.0    1  [stack]
    0.0     0.0     0.0    0.0    1  [vdso]
    0.0     0.0     0.0    0.0    1  [vvar]
    0.0     0.0     0.0    0.0    1  [vvar_vclock]
== 24753 Arcade-Find.App pplications/Arcade/Arcade-Find.AppImage
VmRSS:	     696 kB RssAnon:	     436 kB RssFile:	     260 kB VmSwap:	   14040 kB Threads:	2 
    RSS     PSS    anon   swap    n  path
    0.4     0.4     0.4   13.7   22  [anon]
    0.3     0.3     0.0    0.0    4  /home/harneet/Applications/Arcade/Arcade-Find.AppImage
    0.0     0.0     0.0    0.0    1  [stack]
    0.0     0.0     0.0    0.0    1  [vdso]
    0.0     0.0     0.0    0.0    1  [vvar]
    0.0     0.0     0.0    0.0    1  [vvar_vclock]
== 1425 Arcade-Shelf.Ap plications/Arcade/Arcade-Shelf.AppImage
VmRSS:	    5680 kB RssAnon:	    5280 kB RssFile:	     400 kB VmSwap:	   10812 kB Threads:	2 
    RSS     PSS    anon   swap    n  path
    5.1     5.1     5.1   10.5   30  [anon]
    0.4     0.4     0.0    0.0    4  /home/harneet/Applications/Arcade/Arcade-Shelf.AppImage
    0.0     0.0     0.0    0.0    1  [stack]
    0.0     0.0     0.0    0.0    1  [vdso]
    0.0     0.0     0.0    0.0    1  [vvar]
    0.0     0.0     0.0    0.0    1  [vvar_vclock]
total 0
dr-x------ 2 harneet harneet  6 Nov  6 17:57 .
dr-xr-xr-x 9 harneet harneet  0 Nov  6 17:52 ..
lrwx------ 1 harneet harneet 64 Nov  6 17:57 0 -> /dev/null
lrwx------ 1 harneet harneet 64 Nov  6 17:57 1 -> /dev/null
lrwx------ 1 harneet harneet 64 Nov  6 17:57 2 -> /dev/null
lr-x------ 1 harneet harneet 64 Nov  6 17:57 3 -> /home/harneet/Applications/Arcade/Arcade-Look.AppImage
l-wx------ 1 harneet harneet 6
```


# Prior agent agent-a616b3ca03a1fb638.jsonl: commands and key outputs

## Read prior memory.md
```
# Arcade memory audit (2026-11-06) — IN PROGRESS, appended as measured

Goal: every Arcade app under 500 MB in all normal use, without UX loss. This file is written as the audit runs.
Evidence (raw JSONL samples, smaps breakdowns, screenshots): `AUDIT/memory/`. Harness: scratchpad `mem/bin/{treemem,homemem,topfiles,drv}.py`
(copied into `AUDIT/memory/tools/` at the end).

## 0. How numbers were taken

- **Process tree** = the app process plus all children (WebKitWebProcess, WebKitNetworkProcess, helpers). The AppImage FUSE runtime stub
  (`Arcade-X.AppImage`, ~15–25 MB RSS, mostly a squashfuse mount) is listed separately and NOT included in totals.
- **RSS** = what htop/btop show; sums double-count shared libraries (every WebKit process maps the same 95 MB `libwebkit2gtk`, every Mesa client
  maps `libLLVM` 50 MB). **PSS** splits shared pages across the processes that map them, so tree PSS is the real physical cost of the app.
  Both are reported everywhere. `anon` = RssAnon (private heap/JS/GPU-in-RAM, i.e. the part that is really "the app's data").
- Isolated runs: Xvfb :94 (llvmpipe software GL), private D-Bus, fresh HOME/XDG, real installed AppImages from `~/Applications/Arcade/`,
  no window manager (close = WM_DELETE_WINDOW sent with a tiny Xlib helper, same as a WM close button).
  Host GPU on the owner's machine is an AMD Cezanne (radeonsi); llvmpipe numbers are therefore an upper bound for anything that renders in-process.
- Owner's real instances were read from `/proc` only (no signals, no interaction).
```

## Read real-fleet and tools memory evidence
```
app       procs     RSS     PSS anon+shm    swap  thr  stubRSS  stubPSS  processes
box           2   208.5   119.7     68.4    41.8   61     18.4     18.4  WebKitNetworkP,arcade-desktop
clipboard     1   174.6   102.9     69.4     0.0   73     18.5     18.5  clipboard
find          1    51.0    45.9     36.7    10.9   31      0.7      0.7  arcade-find
lens          1     7.0     4.6      2.0     3.1   10     13.9     13.9  arcade-lens
look          2   194.3   109.7     55.9    42.7   63     16.8     16.6  WebKitNetworkP,arcade-look
shelf         1    60.0    48.9     21.1    16.0    8      5.5      5.5  arcade-shelf
tools         2   253.4   146.3     62.5     9.1   73     21.0     21.0  WebKitNetworkP,arcade-tools
wheel         1   135.4    76.7     36.7    16.3   24     16.9     16.9  AppRun.wrapped
FLEET            1084.1   654.6    352.8   139.9  343    111.8    111.5
----
    pid name                  RSS      PSS     anon     file    shmem     swap  thr
 236280 arcade-tools        188.7    113.2     37.1    146.0      5.6      8.3   71
 237957 WebKitNetworkPr      59.8     38.0     18.7     41.1      0.0      0.0    8
  TOTAL 2                   248.5    151.1     55.8    187.1      5.6      8.3   79   (+AppImage runtime stub rss=21.0 pss=21.0)

by mapping class (MB): rss  pss  anon  swap  nmaps
  anon(mmap/arena)           41.1     41.1     41.1      0.0    361
  webkit-libs                53.0     35.5      4.0      3.0     28
  other-libs                 59.2     27.5      3.8      1.8   1519
  mesa/llvm                  62.5     20.7      0.2      2.7      9
  file:other                 19.2     16.7      0.0      0.8     25
  heap(brk)                   6.5      6.5      6.5      0.0      2
  shm                         5.6      2.8      0.0      0.0      1
  fonts                       0.8      0.0      0.0      0.0      2
----
== 236280 arcade-tools
    RSS     PSS    anon   swap    n  path
   50.5    18.8     0.0    1.3    4  /usr/lib/libLLVM.so.23.1
   29.0    29.0    29.0    0.0  254  [anon]
   18.7    12.5     0.4    2.8    7  $MNT/usr/lib/libwebkit2gtk-4.1.so.0
   16.6    16.6     0.0    0.8    6  $MNT/usr/bin/arcade-tools
   11.9     1.9     0.2    1.4    5  /usr/lib/libgallium-26.2.5-arch3.1.so
   11.4     8.9     0.2    0.2    7  $MNT/usr/lib/libjavascriptcoregtk-4.1.so.0
    6.1     6.1     6.1    0.0    1  [heap]
    5.6     2.8     0.0    0.0    1  /SYSV00000000 (deleted)
    4.7     4.3     0.0    0.1    6  $MNT/usr/lib/libgtk-3.s
```

## Read findings overview
```
# v1 audit findings

Real-use audit of the installed fleet on the owner's machine (CachyOS, Hyprland), started 2026-11-06.
Installed versions: Tools 0.4.6, Box 0.4.3, Look 0.4.3, Find 0.5.4, Lens 0.4.2, Clipboard 0.3.2, Shelf 0.4.0, Wheel 0.5.0.
Each finding names the app, what happens, how it was observed, and what has been confirmed so far.

## Per-app reports

- Box: `box.md` (isolated, 27 findings) and `box-real.md` (real desktop). Owner requirement **BR-0**: Escape inside a
  tool returns to the Island's search and never closes the Island.
- Look, Find, Lens: `look.md`, `find.md`, `lens.md`. Clipboard, Shelf, Wheel, Tools: `clipboard.md`, `shelf.md`,
  `wheel.md`, `tools.md`. Real-desktop follow-ups: `real-desktop.md`.

## Tools

- **T1 — Idle CPU and thread growth.** *Real-desktop recheck: background 0.02% (old process), 0.0% fresh. With the window open on Home it costs 6.1%, because `src-ui/tabs/Home.svelte:71` polls all apps every 2 s. Fix: poll only while visible, every 10 s or event-driven.* Original note: Background Tools (pid 1355, up 1h25m, no window) measured 8.9% CPU over 20 s
  while idle; the Nov 3 baseline was 0.22%. Its threads grew from 68 to 75 within minutes. Breakdown:
  29 `tokio-rt-worker` threads (five of them each busy about 17% of the sample), 6 `tools-tray`, 6 `arcade-link-con`,
  4 inotify watchers, 32 sockets, 16 eventfds, 12 epoll instances, and 6 open `/proc/<pid>/stat` handles.
  Suspect: more than one tokio runtime, leaked tray or Link connection threads, and a tight poll of other apps' `/proc` stats.
  Load before it was seen: five app installs between 16:42 and 17:19, then app restarts. Still to do: reproduce from a
  fresh start, and check whether CPU climbs with each install or Link registry change.
- **T2 — Installer cache never pruned.** `~/.cache/arcade/tools/installers` holds 1.1 GB, unchanged since Oct 25.
  Keep only what an in-progress or rollback operation needs.
- **T3 — Legacy data folders kept forever.** `~/.local/share/arcade-tools` (22 MB) and `~/.local/share/app.arcadetools`
  are never retired. Every start logs "Left … in place: … already exists with different contents" for
  `update-history.jsonl` and `webview/mediakeys/v1/salt`. Migration should finish once, merging or archiving the old
  folders, and stop logging on every start.
- **T4 — No `--status`.** `Arcade-Tools.AppImage --status` prints nothing. Every other Rust app prints one-line JSON.

## Look

- **L1 — Duplicate login and launcher entries.
```

## Read real-fleet and tools memory evidence
```
app       procs     RSS     PSS anon+shm    swap  thr  stubRSS  stubPSS  processes
box           2   208.5   119.7     68.4    41.8   61     18.4     18.4  WebKitNetworkP,arcade-desktop
clipboard     1   174.6   102.9     69.4     0.0   73     18.5     18.5  clipboard
find          1    51.0    45.9     36.7    10.9   31      0.7      0.7  arcade-find
lens          1     7.0     4.6      2.0     3.1   10     13.9     13.9  arcade-lens
look          2   194.3   109.7     55.9    42.7   63     16.8     16.6  WebKitNetworkP,arcade-look
shelf         1    60.0    48.9     21.1    16.0    8      5.5      5.5  arcade-shelf
tools         2   253.4   146.3     62.5     9.1   73     21.0     21.0  WebKitNetworkP,arcade-tools
wheel         1   135.4    76.7     36.7    16.3   24     16.9     16.9  AppRun.wrapped
FLEET            1084.1   654.6    352.8   139.9  343    111.8    111.5
----
    pid name                  RSS      PSS     anon     file    shmem     swap  thr
 236280 arcade-tools        188.7    113.2     37.1    146.0      5.6      8.3   71
 237957 WebKitNetworkPr      59.8     38.0     18.7     41.1      0.0      0.0    8
  TOTAL 2                   248.5    151.1     55.8    187.1      5.6      8.3   79   (+AppImage runtime stub rss=21.0 pss=21.0)

by mapping class (MB): rss  pss  anon  swap  nmaps
  anon(mmap/arena)           41.1     41.1     41.1      0.0    361
  webkit-libs                53.0     35.5      4.0      3.0     28
  other-libs                 59.2     27.5      3.8      1.8   1519
  mesa/llvm                  62.5     20.7      0.2      2.7      9
  file:other                 19.2     16.7      0.0      0.8     25
  heap(brk)                   6.5      6.5      6.5      0.0      2
  shm                         5.6      2.8      0.0      0.0      1
  fonts                       0.8      0.0      0.0      0.0      2
----
== 236280 arcade-tools
    RSS     PSS    anon   swap    n  path
   50.5    18.8     0.0    1.3    4  /usr/lib/libLLVM.so.23.1
   29.0    29.0    29.0    0.0  254  [anon]
   18.7    12.5     0.4    2.8    7  $MNT/usr/lib/libwebkit2gtk-4.1.so.0
   16.6    16.6     0.0    0.8    6  $MNT/usr/bin/arcade-tools
   11.9     1.9     0.2    1.4    5  /usr/lib/libgallium-26.2.5-arch3.1.so
   11.4     8.9     0.2    0.2    7  $MNT/usr/lib/libjavascriptcoregtk-4.1.so.0
    6.1     6.1     6.1    0.0    1  [heap]
    5.6     2.8     0.0    0.0    1  /SYSV00000000 (deleted)
    4.7     4.3     0.0    0.1    6  $MNT/usr/lib/libgtk-3.s
```

## Read findings overview
```
# v1 audit findings

Real-use audit of the installed fleet on the owner's machine (CachyOS, Hyprland), started 2026-11-06.
Installed versions: Tools 0.4.6, Box 0.4.3, Look 0.4.3, Find 0.5.4, Lens 0.4.2, Clipboard 0.3.2, Shelf 0.4.0, Wheel 0.5.0.
Each finding names the app, what happens, how it was observed, and what has been confirmed so far.

## Per-app reports

- Box: `box.md` (isolated, 27 findings) and `box-real.md` (real desktop). Owner requirement **BR-0**: Escape inside a
  tool returns to the Island's search and never closes the Island.
- Look, Find, Lens: `look.md`, `find.md`, `lens.md`. Clipboard, Shelf, Wheel, Tools: `clipboard.md`, `shelf.md`,
  `wheel.md`, `tools.md`. Real-desktop follow-ups: `real-desktop.md`.

## Tools

- **T1 — Idle CPU and thread growth.** *Real-desktop recheck: background 0.02% (old process), 0.0% fresh. With the window open on Home it costs 6.1%, because `src-ui/tabs/Home.svelte:71` polls all apps every 2 s. Fix: poll only while visible, every 10 s or event-driven.* Original note: Background Tools (pid 1355, up 1h25m, no window) measured 8.9% CPU over 20 s
  while idle; the Nov 3 baseline was 0.22%. Its threads grew from 68 to 75 within minutes. Breakdown:
  29 `tokio-rt-worker` threads (five of them each busy about 17% of the sample), 6 `tools-tray`, 6 `arcade-link-con`,
  4 inotify watchers, 32 sockets, 16 eventfds, 12 epoll instances, and 6 open `/proc/<pid>/stat` handles.
  Suspect: more than one tokio runtime, leaked tray or Link connection threads, and a tight poll of other apps' `/proc` stats.
  Load before it was seen: five app installs between 16:42 and 17:19, then app restarts. Still to do: reproduce from a
  fresh start, and check whether CPU climbs with each install or Link registry change.
- **T2 — Installer cache never pruned.** `~/.cache/arcade/tools/installers` holds 1.1 GB, unchanged since Oct 25.
  Keep only what an in-progress or rollback operation needs.
- **T3 — Legacy data folders kept forever.** `~/.local/share/arcade-tools` (22 MB) and `~/.local/share/app.arcadetools`
  are never retired. Every start logs "Left … in place: … already exists with different contents" for
  `update-history.jsonl` and `webview/mediakeys/v1/salt`. Migration should finish once, merging or archiving the old
  folders, and stop logging on every start.
- **T4 — No `--status`.** `Arcade-Tools.AppImage --status` prints nothing. Every other Rust app prints one-line JSON.

## Look

- **L1 — Duplicate login and launcher entries.
```

## Read plan README, JSONL samples, scratchpad
```
# Arcade 1.0.0

Every Arcade app ships 1.0.0: untangled, without dead code, with fast CI, with nothing known broken, and polished.
This folder holds the plan. Each spec is self-contained so a Claude Code cloud session can run it cold, one repo per session.

Starting point (2026-11-06): Tools 0.4.6, Box 0.4.3, Look 0.4.3, Find 0.5.4, Lens 0.4.2, Clipboard 0.3.2,
Shelf 0.4.0, Wheel 0.5.0, all released, verified and installed. Link is on 0.4.15.
The previous plan, `../ARCADE_OVERHAUL/` (README decisions and STANDARD.md), still applies unless this plan says otherwise.

## Decisions (owner, 2026-11-06)

- **Untangle every repo** with the untangle-codebase skill
  (github.com/caldoai/skills/blob/main/skills/untangle-codebase/SKILL.md), including both extras:
  - **Comments:** remove comments that only restate the code.
  - **Tests:** remove tests that wouldn't catch a real bug, and fix the ones that fail without one. This is done last.
- **Shared code moves into Arcade Link.** Install and desktop integration, child-process launch and restart (environment
  sanitizing), single instance, and tray hosting are written once in Link. The Rust apps and Clipboard's Rust core use them.
  Shelf and Wheel (C++) keep their own implementations but must pass the same contract tests.
- **Each app ships 1.0.0 when ready.** It needs green CI and a real-desktop check on the owner's machine.
  Order: Link, Tools, then the apps.
- **The broken list comes from a local real-use audit** of all eight installed apps, done before the specs are written.
  Evidence goes in `AUDIT/`.

- **Nightly is a per-app switch in Tools.** Setting an app to Nightly replaces its stable install and shows a
  "Nightly" badge. Nightly builds from main on a schedule, is skipped when nothing changed, and promotes main CI's
  already-tested files. Switching back to Stable installs the newest stable even when its version is lower.
- **Updates download only the changed pieces, on every platform, from one shared piece store.** Tools downloads only
  missing content-defined chunks (with HTTP Range requests against GitHub release assets) for every app and for itself.
  Linux AppImages work as they are. macOS and Windows ship an uncompressed app archive next to the installer so
  chunking works there too. One chunk store is shared across apps. Any verification failure falls back to a full
  download. Measured savings are in `RESEARCH.md`.
- **CI targets:** PR checks under 8 minutes with warm caches, a full stable r
```

## Read measurement helpers
```
#!/usr/bin/env python3
"""treemem.py PID [--json] [--maps] : memory of a process tree (PID + all descendants)
Reads only /proc/<pid>/{status,smaps_rollup,smaps,task,stat}. Read-only."""
import os, sys, re, json, collections

def kids_of(root):
    ppid = {}
    for d in os.listdir('/proc'):
        if d.isdigit():
            try:
                with open(f'/proc/{d}/stat') as f:
                    s = f.read()
                rp = s.rindex(')')
                parts = s[rp+2:].split()
                ppid[int(d)] = int(parts[1])
            except Exception:
                pass
    out = [root]; i = 0
    while i < len(out):
        for p, pp in ppid.items():
            if pp == out[i] and p not in out:
                out.append(p)
        i += 1
    return out

def kv(path):
    d = {}
    try:
        with open(path) as f:
            for line in f:
                m = re.match(r'(\w+):\s+(\d+)', line)
                if m: d[m.group(1)] = int(m.group(2))
    except Exception:
        pass
    return d

def name(p):
    try:
        with open(f'/proc/{p}/comm') as f: return f.read().strip()
    except Exception: return '?'

def status(p):
    s = kv(f'/proc/{p}/status')
    s['Threads'] = s.get('Threads', 0)
    return s

def rollup(p):
    return kv(f'/proc/{p}/smaps_rollup')

CLASSES = [
 (r'^\[heap\]$', 'heap(brk)'),
 (r'^\[stack', 'stack(main)'),
 (r'^\[anon:.*(v8|JIT|jit)', 'anon-jit'),
 (r'^/memfd:', 'memfd'),
 (r'^/dev/dri|/dev/nvidia|/dev/kgsl', 'gpu-dri'),
 (r'^/dev/shm|^/SYSV|shmem', 'shm'),
 (r'\.sqlite|\.db(-wal|-shm)?$|-wal$|-shm$', 'sqlite-mmap'),
 (r'\.(ttf|otf|ttc|pfb)$', 'fonts'),
 (r'icon-theme\.cache|\.cache$|mesa_shader_cache', 'caches'),
 (r'/libwebkit|/libjavascriptcoregtk', 'webkit-libs'),
 (r'/libflutter|libapp\.so|libarcade_core|flutter_assets', 'flutter'),
 (r'/libQt6|/qt6|\.qml|/libQt', 'qt-libs'),
 (r'/libLLVM|llvmpipe|swrast|libgallium|libvulkan_lvp|dri\.so|/mesa', 'mesa/llvm'),
 (r'\.so(\.|$)', 'other-libs'),
 (r'^$', 'anon(mmap/arena)'),
]
def classify(path):
    if path.startswith('[heap]'): return 'heap(brk)'
    if path.startswith('[stack'): return 'stack(main)'
    for pat, c in CLASSES:
        if re.search(pat, path): return c
    if path.startswith('['): return path.split(' ')[0]
    if path.startswith('/'): return 'file:other'
    return 'anon(mmap/arena)'

def smaps(p):
    """group smaps by class; returns dict class -> {rss,pss,anon,swap,n}"""
    res = collections.defaultdict(lambda: collections.Counter())

```

## Snapshot fleet now, check filesystem/THP
```
app       procs     RSS     PSS anon+shm    swap  thr  stubRSS  stubPSS  processes
box           2   208.5   121.2     68.4    41.8   61     18.4     18.4  WebKitNetworkP,arcade-desktop
clipboard     1   175.3   106.0     70.1     0.0   73     18.5     18.5  clipboard
find          1    51.0    46.0     36.7    10.8   31      0.7      0.7  arcade-find
lens          1     7.0     4.6      2.0     3.1   10     13.9     13.9  arcade-lens
look          2   194.3   111.2     55.9    42.7   64     16.8     16.8  WebKitNetworkP,arcade-look
shelf         1    60.0    49.1     21.1    16.0    8      5.5      5.5  arcade-shelf
tools         2   253.4   148.0     62.5     9.1   73     21.0     21.0  WebKitNetworkP,arcade-tools
wheel         1   143.0    85.7     44.3    16.3   24     16.9     16.9  AppRun.wrapped
FLEET            1092.4   671.8    361.1   139.8  344    111.8    111.7
Filesystem     Type   Size  Used Avail Use% Mounted on
/dev/nvme0n1p2 btrfs  462G  129G  328G  29% /
tmpfs          tmpfs  7.5G  3.8G  3.8G  50% /tmp
/dev/nvme0n1p2 btrfs  462G  129G  328G  29% /home
[always] madvise never
/dev/nvme0n1p2 on / type btrfs (rw,noatime,compress=zstd:1,ssd,discard=async,space_cache=v2,subvolid=256,subvol=/@)
tmpfs on /tmp type tmpfs (rw,noatime,inode64,huge=advise)
7.3.0-4-cachyos
MemTotal:       15715204 kB
Cached:          5373028 kB
SwapCached:          344 kB
Zswap:                 0 kB
Zswapped:              0 kB
Mapped:           697280 kB
Shmem:            843256 kB
ShmemPmdMapped:        0 kB
FilePmdMapped:         0 kB
```

## Inspect libLLVM mappings in running Box
```
7f40eea00000-7f40f3087000 r--p 00000000 00:23 992197                     /usr/lib/libLLVM.so.23.1 rss=8144 pss=669 pd=0 anon=0 swap=0
7f40f3087000-7f40f7b3e000 r-xp 04686000 00:23 992197                     /usr/lib/libLLVM.so.23.1 rss=27164 pss=2405 pd=0 anon=0 swap=0
7f40f7b3e000-7f40f7c89000 r--p 0913c000 00:23 992197                     /usr/lib/libLLVM.so.23.1 rss=308 pss=308 pd=308 anon=308 swap=1016
7f40f7c89000-7f40f7c90000 rw-p 09286000 00:23 992197                     /usr/lib/libLLVM.so.23.1 rss=4 pss=4 pd=4 anon=4 swap=16
7f40f7e00000-7f40f7e1b000 r--p 00000000 00:23 992286                     /usr/lib/libgallium-26.2.5-arch3.1.so rss=108 pss=9 pd=0 anon=0 swap=0
7f40f7e1b000-7f40fa76e000 r-xp 0001b000 00:23 992286                     /usr/lib/libgallium-26.2.5-arch3.1.so rss=10732 pss=1060 pd=0 anon=0 swap=0
7f40fa76e000-7f40fb9f1000 r--p 0296e000 00:23 992286                     /usr/lib/libgallium-26.2.5-arch3.1.so rss=3532 pss=342 pd=0 anon=0 swap=0
7f40fb9f1000-7f40fbb6f000 r--p 03bf1000 00:23 992286                     /usr/lib/libgallium-26.2.5-arch3.1.so rss=268 pss=268 pd=268 anon=268 swap=1180
7f40fbb6f000-7f40fbbad000 rw-p 03d6f000 00:23 992286                     /usr/lib/libgallium-26.2.5-arch3.1.so rss=68 pss=21 pd=16 anon=16 swap=144
Rss:              184508 kB
Pss:              108775 kB
Pss_Dirty:         63852 kB
Pss_Anon:          63852 kB
Pss_File:          44923 kB
Pss_Shmem:             0 kB
Swap:              30088 kB
SwapPss:           29528 kB
VmRSS:	  184508 kB
RssAnon:	   63852 kB
RssFile:	  120656 kB
RssShmem:	       0 kB
VmSwap:	   29528 kB
Threads:	52
```

## Summarize prior JSONL measurements by label
```
Exit code 1
===== box.jsonl
bg-10s                       n=1 RSS     73 PSS     66 anon    20 thr   40 stub  24.8 | arcade-des:73/66
bg-40s                       n=1 RSS     73 PSS     66 anon    20 thr   38 stub  24.8 | arcade-des:73/66
island-open-idle             n=3 RSS    537 PSS    320 anon   171 thr  142 stub  22.7 | arcade-des:218/122,WebKitNetw:62/33,WebKitWebP:255/163
island-after-skip            n=3 RSS    533 PSS    316 anon   167 thr  140 stub  22.6 | arcade-des:214/117,WebKitNetw:62/34,WebKitWebP:256/164
tool-0-6*7                   n=3 RSS    563 PSS    345 anon   194 thr  138 stub  22.8 | arcade-des:218/122,WebKitNetw:62/34,WebKitWebP:281/188
tool-1-14 gb to mb           n=3 RSS    562 PSS    344 anon   193 thr  138 stub  22.5 | arcade-des:218/122,WebKitNetw:62/34,WebKitWebP:280/187
tool-2-calculator            n=3 RSS    559 PSS    342 anon   190 thr  128 stub  22.5 | arcade-des:218/122,WebKitNetw:62/34,WebKitWebP:277/185
tool-3-timer 3s              n=3 RSS    555 PSS    337 anon   186 thr  127 stub  22.5 | arcade-des:214/117,WebKitNetw:62/34,WebKitWebP:277/185
tool-4-json format           n=2 RSS    256 PSS    150 anon    55 thr   79 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-5-base64                n=2 RSS    256 PSS    150 anon    55 thr   79 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-6-password              n=2 RSS    256 PSS    150 anon    55 thr   77 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-7-qr code               n=2 RSS    256 PSS    150 anon    55 thr   76 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-8-uuid                  n=2 RSS    256 PSS    150 anon    55 thr   76 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-9-color picker          n=2 RSS    256 PSS    150 anon    55 thr   76 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-10-hash                 n=2 RSS    256 PSS    150 anon    55 thr   76 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-11-lorem                n=2 RSS    256 PSS    150 anon    55 thr   76 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-12-regex                n=2 RSS    256 PSS    150 anon    55 thr   76 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-13-diff                 n=2 RSS    256 PSS    150 anon    55 thr   76 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-14-markdown             n=2 RSS    256 PSS    150 anon    55 thr   76 stub  22.4 | arcade-des:193/110,WebKitNetw:62/40
tool-15-csv                  n=2 RSS    
```

## Summarize look/tools JSONL
```
===== look.jsonl
bg-10s                       n=1 RSS     50 PSS     43 anon     9 thr   37 | arcade-loo:50/43
bg-40s                       n=1 RSS     50 PSS     43 anon     9 thr   35 | arcade-loo:50/43
open-big.txt                 n=3 RSS    653 PSS    435 anon   302 thr  134 | arcade-loo:207/109,WebKitNetw:59/32,WebKitWebP:385/292
nav0-big.txt — Arcade Look   n=3 RSS    590 PSS    371 anon   238 thr  135 | arcade-loo:201/103,WebKitNetw:59/32,WebKitWebP:328/235
nav1-big.txt — Arcade Look   n=3 RSS    590 PSS    371 anon   237 thr  132 | arcade-loo:201/103,WebKitNetw:59/32,WebKitWebP:328/234
nav2-big.txt — Arcade Look   n=3 RSS    589 PSS    370 anon   236 thr  130 | arcade-loo:201/103,WebKitNetw:59/32,WebKitWebP:327/233
nav3-big.txt — Arcade Look   n=3 RSS    589 PSS    370 anon   236 thr  130 | arcade-loo:201/103,WebKitNetw:59/32,WebKitWebP:327/233
nav4-big.txt — Arcade Look   n=3 RSS    588 PSS    370 anon   236 thr  130 | arcade-loo:201/103,WebKitNetw:59/32,WebKitWebP:327/233
nav5-big.txt — Arcade Look   n=3 RSS    588 PSS    370 anon   236 thr  130 | arcade-loo:201/103,WebKitNetw:59/32,WebKitWebP:327/233
open-big.jpg-t0              n=3 RSS    637 PSS    418 anon   283 thr  129 | arcade-loo:218/120,WebKitNetw:59/32,WebKitWebP:358/264
open-big.jpg-t1              n=3 RSS    636 PSS    417 anon   283 thr  129 | arcade-loo:218/120,WebKitNetw:59/32,WebKitWebP:358/264
open-big.jpg-t2              n=3 RSS    636 PSS    417 anon   283 thr  129 | arcade-loo:218/120,WebKitNetw:59/32,WebKitWebP:358/264
open-big.jpg-t3              n=3 RSS    636 PSS    417 anon   283 thr  129 | arcade-loo:218/120,WebKitNetw:59/32,WebKitWebP:358/264
open-big.jpg-t4              n=3 RSS    636 PSS    417 anon   283 thr  129 | arcade-loo:218/120,WebKitNetw:59/32,WebKitWebP:358/264
open-big.png-t0              n=3 RSS    601 PSS    383 anon   248 thr  137 | arcade-loo:217/119,WebKitNetw:59/32,WebKitWebP:324/230
open-big.png-t1              n=3 RSS    601 PSS    382 anon   248 thr  137 | arcade-loo:217/119,WebKitNetw:59/32,WebKitWebP:324/230
open-big.png-t2              n=3 RSS    601 PSS    382 anon   248 thr  137 | arcade-loo:217/119,WebKitNetw:59/32,WebKitWebP:324/230
open-big.png-t3              n=3 RSS    601 PSS    382 anon   248 thr  137 | arcade-loo:217/119,WebKitNetw:59/32,WebKitWebP:324/230
open-big.png-t4              n=3 RSS    601 PSS    382 anon   248 thr  137 | arcade-loo:217/119,WebKitNetw:59/32,WebKitWebP:324/230
open-big.pdf-t0              n=3 RSS    713 PSS    
```

## Find how apps are opened via CLI
```
box-real.md:22:- **Never** use `hyprctl dispatch` window-closing commands. Close apps with their own `--hide` or `--quit`, Escape, or the tray.
box-real.md:114:- **BR-9, Window Pin always fails on this desktop** (broken). Steps: focus a floating window (Look), `--show` the Island,
box-real.md:134:  to it ("color pickqr", "rulerrecord"). Keys sent immediately after `--show` (<1.5 s) were partly lost.
shelf.md:18:| Capsule (216x76), `--hide`, `--show`, `--toggle` | yes | CLI + shot | pass |
shelf.md:24:| `--restart`, `--quit`, persistence across restart | yes | CLI | items persisted; see SH-7 |
shelf.md:53:Method: CLI. Capsule mode (after `--hide`), then `--restart`: successor started as `--show --wait-for-exit <pid>` and status reports mode "foreground". A restart should keep the previous mode.
shelf.md:56:Method: private GUI / Xvfb. Panel menu → Dock → Left edge. Move pointer onto the 30×92 tab, wait 650 ms: panel expands to 620×480. Move pointer to (1000,1000), wait 650 ms: panel collapses to 30×92 without any explicit dismissal
shelf.md:61:- Files written only under data/arcade/shelf (sqlite, instance lock, objects), data/arcade/apps/arcade.shelf.json, cache/arcade/handoff, run/arcade sockets (stale arcade.shelf.sock/endpoint left in the private runtime dir after 
shelf.md:62:- No coredumps on `--quit` or `--restart`.
wheel.md:14:| Wheel preview | yes | --preview, pointer leave, explicit focus to Settings | stays open; r-preview*.png and --status |
wheel.md:22:| `--restart` / `--quit` | yes | resident in background and with Settings open | pid changes, comes back as background resident (Settings is not reopened), `--quit` rc 0, `--status` then `{"running":false}` rc 1, no coredumps (`
wheel.md:42:Expected: reject oversize strings, or accept quickly. Actual: 200 KB takes about 2 s and is accepted; the 5 MB name is accepted and written (settings.json 5 MB) and the resident's main thread then spins at 55-75% CPU, 900 MB RSS
wheel.md:45:### WH-4 (wrong result) Import error text for valid non-object JSON; `--status` keeps a stale error
wheel.md:46:Method: `--settings-import` with `[1,2,3]` and `{}` prints "ERROR: Invalid JSON: no error occurred" although the JSON is valid. Expected: "not a settings file". Separately, after a failed import of a missing file `--status` repo
tools.md:33:Method: real AppImage CLI + private Xvfb + `coredumpctl` for the exact test-owned PID. With private resident running, run the installed private `Arcade-Tools.AppImage --show-shor
```

## Write snapshot tool and take real baseline snapshot
```
[real-bg-2225] app        n     RSS     PSS    anon    swap  thr  stubRSS  stubPSS  procs(rss/pss)
               box        2   208.5   121.2    68.4    41.8   61     18.4     18.4  arcade-deskt:180/106,WebKitNetwor:28/14
               clipboard  1   175.3   106.0    69.9     0.0   73     18.5     18.5  clipboard:175/106
               find       1    51.1    46.0    34.9    10.8   31      0.7      0.7  arcade-find:51/45
               lens       1     7.0     4.6     2.0     3.1   10     13.9     13.9  arcade-lens:6/4
               look       2   194.3   111.2    55.9    42.7   63     16.8     16.8  arcade-look:177/104,WebKitNetwor:16/6
               shelf      1    60.0    49.1    21.1    16.0    8      5.5      5.5  arcade-shelf:59/49
               tools      2   253.4   148.0    62.3     9.1   73     21.0     21.0  arcade-tools:193/109,WebKitNetwor:60/38
               wheel      1   143.0    85.7    44.3    16.3   24     16.9     16.9  AppRun.wrapp:142/85
               FLEET     11  1092.4   671.8   361.1   139.8  343    111.8    111.7
               with stubs: RSS  1204.2  PSS   783.5
```

## Inspect Look AppImage runtime stub
```
/home/harneet/Applications/Arcade/Arcade-Look.AppImage --service 
VmRSS:	   17192 kB
RssAnon:	   16784 kB
RssFile:	     408 kB
RssShmem:	       0 kB
VmSwap:	    7492 kB
Threads:	2
400fa010000-400fa8f0000 rw-p  rss=4996 pss=4996 anon=4996 swap=2220
400fb640000-400fbc90000 rw-p  rss=4312 pss=4312 anon=4312 swap=1584
400fa900000-400faed0000 rw-p  rss=3572 pss=3572 anon=3572 swap=1328
400faef0000-400fb370000 rw-p  rss=2600 pss=2600 anon=2600 swap=1428
400fb390000-400fb550000 rw-p  rss=668 pss=668 anon=668 swap=764
400fb570000-400fb620000 rw-p  rss=540 pss=540 anon=540 swap=104
7f5e8a196000-7f5e8a219000 r-xp /home/harneet/Applications/Arcade/Arcade-Look.AppImage rss=376 pss=376 anon=0 swap=0
lrwxrwxrwx 1 harneet harneet 0 Nov  6 19:44 /proc/24731/exe -> /home/harneet/Applications/Arcade/Arcade-Look.AppImage
3
AppImage runtime version: https://github.com/AppImage/type2-runtime/commit/fedfad5
total 0
dr-x------ 2 harneet harneet  6 Nov  6 17:57 .
dr-xr-xr-x 9 harneet harneet  0 Nov  6 17:52 ..
lrwx------ 1 harneet harneet 64 Nov  6 17:57 0 -> /dev/null
lrwx------ 1 harneet harneet 64 Nov  6 17:57 1 -> /dev/null
lrwx------ 1 harneet harneet 64 Nov  6 17:57 2 -> /dev/null
lr-x------ 1 harneet harneet 64 Nov  6 17:57 3 -> /home/harneet/Applications/Arcade/Arcade-Look.AppImage
l-wx------ 1 harneet harneet 64 Nov  6 17:57 4 -> pipe:[118082]
lrwx------ 1 harneet harneet 64 Nov  6 17:57 5 -> /dev/fuse
```

## Compare Find stub and runtime kinds
```
/home/harneet/Applications/Arcade/Arcade-Find.AppImage --background 
VmRSS:	     696 kB
RssAnon:	     436 kB
RssFile:	     260 kB
Threads:	2
lrwxrwxrwx 1 harneet harneet 0 Nov  6 19:44 exe -> /home/harneet/Applications/Arcade/Arcade-Find.AppImage
Arcade-Box.AppImage
Arcade-Clipboard.AppImage
Arcade-Find.AppImage
Arcade-Lens.AppImage
Arcade-Look.AppImage
Arcade-Shelf.AppImage
Arcade-Tools.AppImage
Arcade-Wheel.AppImage
Box: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Look: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Tools: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Clipboard: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Find: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Lens: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Shelf: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Wheel: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of
```

## Inspect Look AppImage runtime stub
```
/home/harneet/Applications/Arcade/Arcade-Look.AppImage --service 
VmRSS:	   17192 kB
RssAnon:	   16784 kB
RssFile:	     408 kB
RssShmem:	       0 kB
VmSwap:	    7492 kB
Threads:	2
400fa010000-400fa8f0000 rw-p  rss=4996 pss=4996 anon=4996 swap=2220
400fb640000-400fbc90000 rw-p  rss=4312 pss=4312 anon=4312 swap=1584
400fa900000-400faed0000 rw-p  rss=3572 pss=3572 anon=3572 swap=1328
400faef0000-400fb370000 rw-p  rss=2600 pss=2600 anon=2600 swap=1428
400fb390000-400fb550000 rw-p  rss=668 pss=668 anon=668 swap=764
400fb570000-400fb620000 rw-p  rss=540 pss=540 anon=540 swap=104
7f5e8a196000-7f5e8a219000 r-xp /home/harneet/Applications/Arcade/Arcade-Look.AppImage rss=376 pss=376 anon=0 swap=0
lrwxrwxrwx 1 harneet harneet 0 Nov  6 19:44 /proc/24731/exe -> /home/harneet/Applications/Arcade/Arcade-Look.AppImage
3
AppImage runtime version: https://github.com/AppImage/type2-runtime/commit/fedfad5
total 0
dr-x------ 2 harneet harneet  6 Nov  6 17:57 .
dr-xr-xr-x 9 harneet harneet  0 Nov  6 17:52 ..
lrwx------ 1 harneet harneet 64 Nov  6 17:57 0 -> /dev/null
lrwx------ 1 harneet harneet 64 Nov  6 17:57 1 -> /dev/null
lrwx------ 1 harneet harneet 64 Nov  6 17:57 2 -> /dev/null
lr-x------ 1 harneet harneet 64 Nov  6 17:57 3 -> /home/harneet/Applications/Arcade/Arcade-Look.AppImage
l-wx------ 1 harneet harneet 64 Nov  6 17:57 4 -> pipe:[118082]
lrwx------ 1 harneet harneet 64 Nov  6 17:57 5 -> /dev/fuse
```

## Compare Find stub and runtime kinds
```
/home/harneet/Applications/Arcade/Arcade-Find.AppImage --background 
VmRSS:	     696 kB
RssAnon:	     436 kB
RssFile:	     260 kB
Threads:	2
lrwxrwxrwx 1 harneet harneet 0 Nov  6 19:44 exe -> /home/harneet/Applications/Arcade/Arcade-Find.AppImage
Arcade-Box.AppImage
Arcade-Clipboard.AppImage
Arcade-Find.AppImage
Arcade-Lens.AppImage
Arcade-Look.AppImage
Arcade-Shelf.AppImage
Arcade-Tools.AppImage
Arcade-Wheel.AppImage
Box: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Look: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Tools: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Clipboard: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Find: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Lens: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Shelf: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of 
Wheel: /bin/bash: line 1: xxd: command not found
     https://github.com/AppImage/type2-runtime/blob/main/LICENSE   * libfuse, licensed under the terms of
```

## Write open/close runner and run for Tools in background
```
                 tools      2   253.4   148.0    62.3     9.1   73     21.0     21.0  arcade-tools:193/109,WebKitNetwor:60/38
                 FLEET     11  1092.5   671.9   361.1   139.8  343    111.8    111.7
                 with stubs: RSS  1204.2  PSS   783.5
open cmd returned after 0.22s
new windows: [('0x56064a11d9c0', 'arcade-tools', 'Arcade Tools', [1228, 1398])] layers: []
                     tools      3   535.2   319.0   182.3     7.9  145     21.2     21.2  arcade-tools:214/117,WebKitNetwor:60/32,WebKitWebPro:259/168
                     FLEET     12  1374.4   840.6   481.4   138.6  415    111.9    111.8
                     with stubs: RSS  1486.3  PSS   952.5
```

## Relaunch Tools in background and measure
```
Left /home/harneet/.local/share/arcade-tools in place: /home/harneet/.local/share/arcade/tools/update-history.jsonl already exists with different contents
Left /home/harneet/.local/share/app.arcadetools in place: /home/harneet/.cache/arcade/tools/webview/mediakeys/v1/salt already exists with different contents
  27156   16142 29024 ././/lib/x86_64-linux-gnu/webkit2gtk-4.1/WebKitNetworkProcess 1 50
  27844   16101 16724 ././/lib/x86_64-linux-gnu/webkit2gtk-4.1/WebKitNetworkProcess 1 46 48
 327167      15 60060 arcade-tools --background
 327173      15 23588 /home/harneet/Applications/Arcade/Arcade-Tools.AppImage --background
[tools-fresh-bg-15s] app        n     RSS     PSS    anon    swap  thr  stubRSS  stubPSS  procs(rss/pss)
                     tools      1    58.7    51.9    11.5     5.4   45     23.0     23.0  arcade-tools:58/51
                     FLEET     10   925.6   603.9   323.4   132.7  322    121.0    120.9
```

## Read isolated harness helpers
```
"""Small driver library for isolated Arcade app runs on Xvfb :94."""
import os, subprocess, time, json, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import homemem
M = '/tmp/claude-1000/-home-harneet-Work-Coding/c7347b9d-c34f-4fc8-b57d-de9a2d5591f6/scratchpad/mem'
E = '/home/harneet/Work/Coding/ARCADE_V1/AUDIT/memory'
BIN = M + '/bin'

def mkenv(app, extra=None):
    out = subprocess.run(['bash', '-c', f'. {BIN}/env.sh {app}; env -0'], capture_output=True).stdout
    env = dict(kv.split('=', 1) for kv in out.decode(errors='replace').split('\0') if '=' in kv)
    env['DBUS_SESSION_BUS_ADDRESS'] = open(f'{M}/pids/dbus-{app}.addr').read().strip()
    env['DISPLAY'] = ':94'
    if extra: env.update(extra)
    return env

def start(app, img, args=(), extra=None):
    env = mkenv(app, extra)
    log = open(f'{M}/logs/{app}.log', 'ab')
    p = subprocess.Popen([img, *args], cwd=env['HOME'], env=env, stdout=log, stderr=log, start_new_session=True)
    open(f'{M}/pids/{app}.launch', 'w').write(str(p.pid))
    return p

def cli(app, img, args=(), timeout=30, extra=None):
    env = mkenv(app, extra)
    try:
        return subprocess.run([img, *args], cwd=env['HOME'], env=env, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        return e

def xdo(*a):
    return subprocess.run(['xdotool', *a], env={**os.environ, 'DISPLAY': ':94'}, capture_output=True, text=True).stdout

def windows(pattern='.'):
    ids = xdo('search', '--name', pattern).split()
    return ids

def wname(w): return xdo('getwindowname', w).strip()

def pixel(w, x, y):
    out = subprocess.run(['import', '-window', str(w), '-crop', '1x1+%d+%d' % (x, y), 'txt:-'], env={**os.environ, 'DISPLAY': ':94'}, capture_output=True, text=True).stdout
    m = re.search(r'#([0-9A-Fa-f]{6})', out)
    return m.group(1) if m else None

def shot(path, w=None):
    subprocess.run(['import', '-window', str(w) if w else 'root', path], env={**os.environ, 'DISPLAY': ':94'}, capture_output=True)

def click(x, y):
    xdo('mousemove', str(x), str(y)); xdo('click', '1')

def key(*k, win=None):
    a = ['key']; 
    if win: a += ['--window', str(win)]
    xdo(*a, *k)

def wmclose(w): subprocess.run([BIN + '/wmclose', str(w)], env={**os.environ, 'DISPLAY': ':94'})

def sample(app, label, maps=False):
    o = homemem.measure(f'{M}/{app}/home', maps); o['label'] = label
    with open(f'{E}/{app}.jsonl', 'a') as f: f.write(json.dumps(o) + '\n')
    return o

def fmt(o):
    t = o['total'
```

## List WebKit rendering env vars
```
WEBKIT_A11Y_BUS_ADDRESS
WEBKIT_DISABLE_COMPOSITING_MODE
WEBKIT_DISABLE_DMABUF_RENDERER
WEBKIT_DISABLE_MEMORY_ATTRIBUTION
WEBKIT_DISABLE_SANDBOX_THIS_IS_DANGEROUS
WEBKIT_DMABUF_RENDERER_DISABLE_GBM
WEBKIT_DMABUF_RENDERER_FORCE_SHM
WEBKIT_DOM
WEBKIT_EGL_PIXEL_LAYOUT
WEBKIT_FEATURE_STATUS_DEVELOPER
WEBKIT_FEATURE_STATUS_EMBEDDER
WEBKIT_FEATURE_STATUS_INTERNAL
WEBKIT_FEATURE_STATUS_MATURE
WEBKIT_FEATURE_STATUS_PREVIEW
WEBKIT_FEATURE_STATUS_STABLE
WEBKIT_FEATURE_STATUS_TESTABLE
WEBKIT_FEATURE_STATUS_UNSTABLE
WEBKIT_FORCE_AT_FORCE_MOUSE_DOWN
WEBKIT_FORCE_AT_MOUSE_DOWN
WEBKIT_FORCE_COMPLEX_TEXT
WEBKIT_FORCE_COMPOSITING_MODE
WEBKIT_FORCE_DMABUF_RENDERER
WEBKIT_FORCE_SANDBOX
WEBKIT_FORCE_VBLANK_TIMER
WEBKIT_GST_ALLOW_PLAYBACK_OF_INVISIBLE_VIDEOS
WEBKIT_GST_CUSTOM_VIDEO_SINK
WEBKIT_GST_DISABLE_FAST_MALLOC
WEBKIT_GST_DISABLE_GL_SINK
WEBKIT_GST_DMABUF_SINK_DISABLED
WEBKIT_GST_HARNESS_DUMP_DIR
WEBKIT_GST_MAX_AVC1_RESOLUTION
WEBKIT_GST_MAX_NUMBER_OF_AUDIO_OUTPUT_CHANNELS
WEBKIT_GST_USE_PLAYBIN3
WEBKIT_GST_USE_VIDEOCONVERT_SCALE
WEBKIT_GST_WORKAROUND_APP_SINK_FLUSH_CAPS
WEBKIT_GST_WORKAROUND_BASE_SINK_POSITION_FLUSH
WEBKIT_HARDWARE_ACCELERATION_POLICY_ALWAYS
WEBKIT_HARDWARE_ACCELERATION_POLICY_NEVER
WEBKIT_HARDWARE_ACCELERATION_POLICY_ON_DEMAND
WEBKIT_INJECTED_BUNDLE_PATH
JSC_IS_CLASS(jscClass)
JSC_IS_VIRTUAL_MACHINE(vm)
JSC_IS_CONTEXT(context)
JSC_IS_EXCEPTION(exception)
JSC_IS_VALUE(value)
AcceleratedBackingStore_DidCreateDMABufBuffer
DMABuf (Supported buffers: 
WEBKIT_DMABUF_RENDERER_DISABLE_GBM
Failed to create EGL image from DMABuf of size %dx%d
Failed to import DMABuf with file descriptor %d
WEBKIT_DMABUF_RENDERER_BUFFER_FORMAT
Invalid format %s set in WEBKIT_DMABUF_RENDERER_BUFFER_FORMAT, ignoring...
WEBKIT_DISABLE_DMABUF_RENDERER
WEBKIT_DMABUF_RENDERER_FORCE_SHM
WEBKIT_FORCE_DMABUF_RENDERER
```

## Clipboard thread names
```
pid=240250
     14 clipboard
     12 tokio-rt-worker
      7 clipbo:traceq0
      5 clipboar:gdrv0
      5 clipboard:gl0
      3 arcade-link-con
      2 notify-rs inoti
      2 arcade-tray-wat
      1 pool-spawner
      1 [pango] fontcon
      1 mDNS_daemon
      1 io.worker.4
      1 io.worker.3
      1 io.worker.2
      1 io.worker.1
      1 io.flutter.rast
      1 io.flutter.io
      1 gmain
      1 gly-global-exec
      1 gdbus
      1 dconf worker
      1 dart:io Process
      1 dart:io EventHa
      1 clipbo:sh_opt0
      1 clipboard:sh5
      1 clipboard:sh4
      1 clipboard:sh3
      1 clipboard:sh2
      1 clipboard:sh1
      1 clipboard:sh0
VmSize:	 1545224 kB
VmRSS:	  185880 kB
RssAnon:	   73528 kB
RssFile:	  112092 kB
VmData:	  455604 kB
VmSwap:	       0 kB
Threads:	76
```

## Read homemem.py and check X tools
```
Exit code 1
#!/usr/bin/env python3
"""homemem.py HOMEDIR [--maps] [--label X] [--jsonl FILE]
Finds all processes whose environ has HOME=HOMEDIR, drops infra (dbus, xdg portals, Xvfb, gvfs, at-spi, etc.)
and the AppImage runtime stub, and reports the app process tree memory."""
import os, sys, json, time, collections
sys.path.insert(0, os.path.dirname(__file__))
import treemem as T

INFRA = ('dbus-','xdg-','Xvfb','gvfs','at-spi','dconf','gnome-keyring','pipewire','wireplumber','xdotool','bash','sh','sleep','timeout','python','fusermount','xdg-desktop-por','xdg-document-p','xdg-permission','gsd-','ibus')
def home_pids(home):
    out = []
    for d in os.listdir('/proc'):
        if not d.isdigit(): continue
        try:
            env = open(f'/proc/{d}/environ','rb').read().split(b'\0')
        except Exception: continue
        if f'HOME={home}'.encode() in env: out.append(int(d))
    return out

def app_pids(home):
    allp = home_pids(home)
    keep, runtime = [], []
    for p in allp:
        n = T.name(p)
        if any(n.startswith(i) for i in INFRA): continue
        try: exe = os.readlink(f'/proc/{p}/exe')
        except Exception: exe = ''
        if n.startswith('Arcade-') and exe.endswith('.AppImage'):
            runtime.append(p); continue
        keep.append(p)
    return keep, runtime

def measure(home, maps=False):
    keep, runtime = app_pids(home)
    procs = []; tot = collections.Counter(); classes = collections.defaultdict(collections.Counter)
    for p in keep:
        st = T.status(p); ro = T.rollup(p)
        rec = dict(pid=p, name=T.name(p), rss=st.get('VmRSS',0), anon=st.get('RssAnon',0), file=st.get('RssFile',0), shmem=st.get('RssShmem',0),
                   swap=st.get('VmSwap',0), threads=st.get('Threads',0), pss=ro.get('Pss',0), pss_anon=ro.get('Pss_Anon',0),
                   pss_file=ro.get('Pss_File',0), pss_shmem=ro.get('Pss_Shmem',0), vmsize=st.get('VmSize',0))
        if maps:
            sm = T.smaps(p)
            rec['maps'] = {k: dict(rss=v['Rss'], pss=v['Pss'], anon=v['Anonymous'], swap=v['Swap'], n=v['n']) for k,v in sm.items()}
            for k, v in sm.items():
                for kk in ('Rss','Pss','Anonymous','Swap','n'): classes[k][kk] += v[kk]
        procs.append(rec)
        for k in ('rss','anon','file','shmem','swap','threads','pss','pss_anon','pss_file','pss_shmem'): tot[k] += rec[k]
    rt = sum(T.status(p).get('VmRSS',0) for p in runtime)
    rtp = sum(T.rollup(p).get('Pss',0) for p in runtime)
    o
```

## Launch two Look lab variants in background
```
== lab look-base {}
bg+8s                  n=1 RSS   50.4 PSS   43.8 anon    9.2 thr  37 | arcade-loo:50/43
== lab look-nocomp {'WEBKIT_DISABLE_COMPOSITING_MODE': '1'}
bg+8s                  n=1 RSS   50.2 PSS   43.7 anon    9.2 thr  37 | arcade-loo:50/43
```

## Lab progress for Look
```
== lab look-base {}
bg+8s                  n=1 RSS   50.4 PSS   43.8 anon    9.2 thr  37 | arcade-loo:50/43
bg+30s                 n=1 RSS   50.4 PSS   43.8 anon    9.2 thr  35 | arcade-loo:50/43
  [first-open] window mapped after 0.58s (cli incl.)
open+4s                n=3 RSS  507.0 PSS  298.3 anon  157.7 thr 131 | WebKitWebP:252/159 arcade-loo:194/106 WebKitNetw:59/32
open+12s               n=3 RSS  495.6 PSS  286.8 anon  146.2 thr 126 | WebKitWebP:246/152 arcade-loo:189/101 WebKitNetw:59/32
closed+3s              n=3 RSS  500.4 PSS  291.6 anon  150.8 thr 118 | WebKitWebP:246/152 arcade-loo:194/106 WebKitNetw:59/32

== lab look-nocomp {'WEBKIT_DISABLE_COMPOSITING_MODE': '1'}
bg+8s                  n=1 RSS   50.2 PSS   43.7 anon    9.2 thr  37 | arcade-loo:50/43
bg+30s                 n=1 RSS   50.2 PSS   43.7 anon    9.2 thr  35 | arcade-loo:50/43
  [first-open] window mapped after 0.58s (cli incl.)
open+4s                n=3 RSS  407.6 PSS  226.3 anon  114.4 thr  78 | WebKitWebP:193/117 arcade-loo:153/75 WebKitNetw:60/33
open+12s               n=3 RSS  398.9 PSS  216.0 anon  102.7 thr  73 | WebKitWebP:186/110 arcade-loo:151/72 WebKitNetw:60/33
closed+3s              n=3 RSS  403.8 PSS  220.8 anon  107.3 thr  64 | WebKitWebP:186/110 arcade-loo:156/76 WebKitNetw:60/33
```

## Lab progress
```
== lab look-base {}
bg+8s                  n=1 RSS   50.4 PSS   43.8 anon    9.2 thr  37 | arcade-loo:50/43
bg+30s                 n=1 RSS   50.4 PSS   43.8 anon    9.2 thr  35 | arcade-loo:50/43
  [first-open] window mapped after 0.58s (cli incl.)
open+4s                n=3 RSS  507.0 PSS  298.3 anon  157.7 thr 131 | WebKitWebP:252/159 arcade-loo:194/106 WebKitNetw:59/32
open+12s               n=3 RSS  495.6 PSS  286.8 anon  146.2 thr 126 | WebKitWebP:246/152 arcade-loo:189/101 WebKitNetw:59/32
closed+3s              n=3 RSS  500.4 PSS  291.6 anon  150.8 thr 118 | WebKitWebP:246/152 arcade-loo:194/106 WebKitNetw:59/32

== lab look-nocomp {'WEBKIT_DISABLE_COMPOSITING_MODE': '1'}
bg+8s                  n=1 RSS   50.2 PSS   43.7 anon    9.2 thr  37 | arcade-loo:50/43
bg+30s                 n=1 RSS   50.2 PSS   43.7 anon    9.2 thr  35 | arcade-loo:50/43
  [first-open] window mapped after 0.58s (cli incl.)
open+4s                n=3 RSS  407.6 PSS  226.3 anon  114.4 thr  78 | WebKitWebP:193/117 arcade-loo:153/75 WebKitNetw:60/33
open+12s               n=3 RSS  398.9 PSS  216.0 anon  102.7 thr  73 | WebKitWebP:186/110 arcade-loo:151/72 WebKitNetw:60/33
closed+3s              n=3 RSS  403.8 PSS  220.8 anon  107.3 thr  64 | WebKitWebP:186/110 arcade-loo:156/76 WebKitNetw:60/33
```

## Check labs and Wheel
```
== lab look-base {}
bg+8s                  n=1 RSS   50.4 PSS   43.8 anon    9.2 thr  37 | arcade-loo:50/43
bg+30s                 n=1 RSS   50.4 PSS   43.8 anon    9.2 thr  35 | arcade-loo:50/43
  [first-open] window mapped after 0.58s (cli incl.)
open+4s                n=3 RSS  507.0 PSS  298.3 anon  157.7 thr 131 | WebKitWebP:252/159 arcade-loo:194/106 WebKitNetw:59/32
open+12s               n=3 RSS  495.6 PSS  286.8 anon  146.2 thr 126 | WebKitWebP:246/152 arcade-loo:189/101 WebKitNetw:59/32
closed+3s              n=3 RSS  500.4 PSS  291.6 anon  150.8 thr 118 | WebKitWebP:246/152 arcade-loo:194/106 WebKitNetw:59/32
closed+40s             n=2 RSS  244.0 PSS  149.4 anon   60.0 thr  72 | arcade-loo:183/110 WebKitNetw:60/38

== lab look-nocomp {'WEBKIT_DISABLE_COMPOSITING_MODE': '1'}
bg+8s                  n=1 RSS   50.2 PSS   43.7 anon    9.2 thr  37 | arcade-loo:50/43
bg+30s                 n=1 RSS   50.2 PSS   43.7 anon    9.2 thr  35 | arcade-loo:50/43
  [first-open] window mapped after 0.58s (cli incl.)
open+4s                n=3 RSS  407.6 PSS  226.3 anon  114.4 thr  78 | WebKitWebP:193/117 arcade-loo:153/75 WebKitNetw:60/33
open+12s               n=3 RSS  398.9 PSS  216.0 anon  102.7 thr  73 | WebKitWebP:186/110 arcade-loo:151/72 WebKitNetw:60/33
closed+3s              n=3 RSS  403.8 PSS  220.8 anon  107.3 thr  64 | WebKitWebP:186/110 arcade-loo:156/76 WebKitNetw:60/33
closed+40s             n=2 RSS  210.1 PSS  120.8 anon   47.6 thr  48 | arcade-loo:149/82 WebKitNetw:60/38

lab.jsonl
lab-look-base.log
lab-look-nocomp.log
look-base-open.png
look-nocomp-open.png
oc-box.log
oc-find.log
oc-lens.log
oc-look.log
oc-shelf.log
oc-tools.log
run_real.log
snap.jsonl
ugrep: warning: oc-wheel.log: No such file or directory
```


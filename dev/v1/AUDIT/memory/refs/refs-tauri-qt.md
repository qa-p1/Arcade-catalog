# Source references (read-only grep/Read)

Base paths: TOOLS=/home/harneet/Work/Coding/Rust/Arcade-tools, BOX=/home/harneet/Work/Coding/Rust/Arcade Box, LOOK=/home/harneet/Work/Coding/Rust/arcade-look, FIND=/home/harneet/Work/Coding/Rust/Arcade-Find, WHEEL=/home/harneet/Work/Coding/C++/Arcade wheel, SHELF=/home/harneet/Work/Coding/C++/Arcade-Shelf

## T1
- TOOLS/src-tauri/src/desktop.rs:1365  `if let tauri::WindowEvent::CloseRequested { api, .. } = event {`
- TOOLS/src-tauri/src/desktop.rs:1366  `api.prevent_close();`
- TOOLS/src-tauri/src/desktop.rs:1367  `request_close(window.app_handle());`
- TOOLS/src-tauri/src/desktop.rs:1369  `if let tauri::WindowEvent::Destroyed = event {`
- TOOLS/src-tauri/src/desktop.rs:1371  `reclaim_resident_memory(window.app_handle().clone());`
- TOOLS/src-tauri/src/desktop.rs:1283  `reclaim_resident_memory(handle);` (second call site; enclosing context not read)
- TOOLS/src-tauri/src/desktop.rs:253  `fn reclaim_resident_memory(app: AppHandle) {` (definition)

## T2
- TOOLS/src-tauri/src/resident/memory.rs:4  `pub fn release_unused_runtime_pages() {`
- TOOLS/src-tauri/src/resident/memory.rs:6  `unsafe { libc::malloc_trim(0) };`
- TOOLS/src-tauri/src/resident/memory.rs:15  `unsafe { libc::madvise(start as *mut libc::c_void, length, libc::MADV_PAGEOUT) };`
- TOOLS/src-tauri/src/resident/memory.rs:20  `pub fn release_unused_runtime_pages() {}` (non-gnu/non-linux stub)
- TOOLS/src-tauri/src/resident/memory.rs:23  `fn library_pages(source: &str) -> Vec<(usize, usize)> {`
- Note: `fn reclaim_resident_memory` is NOT in memory.rs; it is in desktop.rs:253 (see T1).

## T3
- TOOLS/src-tauri/src/desktop.rs:165  `let builder = tauri::WebviewWindowBuilder::from_config(&app, config).ok()?;`
- Only WebviewWindowBuilder hit under TOOLS/src-tauri/src.

## T4
- TOOLS/src-ui/tabs/Home.svelte:69  `const sample = async () => { try { const next = await api.dashboard(); if (!stopped) dashboard = next; } catch { /* keep the last sample */ } };`
- TOOLS/src-ui/tabs/Home.svelte:71  `const timer = setInterval(sample, 2000);`
- TOOLS/src-ui/tabs/Home.svelte:72  `return () => { stopped = true; clearInterval(timer); };`

## T5
- TOOLS/src-tauri/src/tray/mod.rs:128  `std::thread::Builder::new()`
- TOOLS/src-tauri/src/tray/mod.rs:129  `.name("tools-tray".into())`
- "tools-shortcut": NOT FOUND. Grepped `thread::Builder::new()|\.name(` in src-tauri/src/hotkey.rs and src-tauri/src/shortcuts.rs; no hits in either (the only hit in tray/ is above).

## T6
- TOOLS/src/dashboard.rs:47-50  `let pids = entries` ... `.collect::<Vec<_>>();` (PIDs come from each app's endpoint file: line 49 `.filter_map(|(_, endpoint)| endpoint.as_ref().map(|e| Pid::from_u32(e.pid)))`)
- TOOLS/src/dashboard.rs:57  `.with_memory()` (refresh kind; line 58 `.without_tasks()`; line 56 not separately viewed)
- TOOLS/src/dashboard.rs:61  `let mut total_memory_bytes = 0;`
- TOOLS/src/dashboard.rs:77  `let memory_bytes = process.map(|p| p.memory());`
- TOOLS/src/dashboard.rs:82  `total_memory_bytes += memory_bytes.unwrap_or(0);`
- TOOLS/src/dashboard.rs:103  `total_memory_bytes,`
- Path note: there is no src-tauri/src/dashboard.rs in TOOLS; the file is TOOLS/src/dashboard.rs.
- Summary: it sums `process.memory()` (sysinfo) for only the one PID per installed app read from its endpoint file; it does NOT walk child processes (no children enumeration; `without_tasks()` only excludes threads). The tree does not define what sysinfo's `memory()` returns (RSS vs other); that is an external-library assumption, not verified here. AppImage runtime: NOT FOUND in this code (no AppImage reference in the dashboard path; only counts the endpoint PID).

## B1 (BOX/apps/desktop/src-tauri/src/lib.rs)
- lib.rs:139  `static ISLAND_VISIBILITY: Mutex<IslandVisibility> = Mutex::new(IslandVisibility {` (definition)
- lib.rs:1286  `const ISLAND_IDLE_RELEASE: std::time::Duration = std::time::Duration::from_secs(15);` (definition, 15 s)
- lib.rs:1478  `fn schedule_island_release(window: &tauri::WebviewWindow, delay: std::time::Duration) {` (definition)
- lib.rs:1506  `fn reclaim_island_memory(app: tauri::AppHandle) {` (definition; sleeps 500 ms, line 1508 region)
- lib.rs:1519  `fn request_hide_island(window: &tauri::WebviewWindow, release_after: std::time::Duration) {` (definition)
- lib.rs:1034  `request_hide_island(&window, ISLAND_IDLE_RELEASE);` -> release_after = ISLAND_IDLE_RELEASE = 15 s
- lib.rs:1140  `schedule_island_release(&window, ISLAND_IDLE_RELEASE);` -> delay = 15 s
- lib.rs:1278  `request_hide_island(&island, ISLAND_IDLE_RELEASE);` -> release_after = 15 s
- lib.rs:1459  `request_hide_island(&close_window, std::time::Duration::ZERO);` -> release_after = 0
- lib.rs:1469  `reclaim_island_memory(destroyed_app.clone());` (no duration argument)
- lib.rs:1552  `schedule_island_release(&finish, release_after);` (inside request_hide_island; passes through the parameter)
- lib.rs:2044  `request_hide_island(&window, std::time::Duration::ZERO);` -> release_after = 0

## B2 (BOX/apps/desktop/src-tauri/src/dashboard.rs)
- dashboard.rs:12  `const RELEASE_AFTER_CLOSE: Duration = Duration::from_secs(15);` (15 s)
- dashboard.rs:96  `/// Destroys the hidden dashboard after `RELEASE_AFTER_CLOSE` unless it was`
- dashboard.rs:98  `fn schedule_release(window: &tauri::WebviewWindow) {`
- dashboard.rs:101  `std::thread::spawn(move || {`
- dashboard.rs:102  `std::thread::sleep(RELEASE_AFTER_CLOSE);`

## B3 (in-memory job/history state)
- BOX/crates/arcade-core/src/jobs.rs:138  `jobs: HashMap<String, JobEntry>,` (inside `struct QueueState`, line 137); no cap constant seen. Bound: `queue_capacity: usize,` at jobs.rs:149 (queue size, not history).
- BOX/crates/arcade-core/src/jobs.rs:139  `queued: VecDeque<String>,`
- BOX/crates/arcade-core/src/jobs.rs:152  `pub struct JobManager {`
- BOX/apps/desktop/src-tauri/src/link.rs:183  `struct Jobs {`
- BOX/apps/desktop/src-tauri/src/link.rs:184  `running: HashMap<String, LinkJob>,`
- BOX/apps/desktop/src-tauri/src/link.rs:185  `early: VecDeque<JobSnapshot>,` (no explicit size cap found by grep for MAX_/truncate/pop_front limits; line 240 `state.early.pop_front();` is the only removal seen)
- BOX/apps/desktop/src-tauri/src/link.rs:189  `static JOBS: OnceLock<Mutex<Jobs>> = OnceLock::new();`
- BOX/apps/desktop/src-tauri/src/lib.rs:513-516  `fn get_history(...)` ... `.recent_history(50)` (read limit only; history is SQLite via BOX/crates/arcade-core/src/storage.rs:148 `pub fn recent_history(&self, limit: usize)`)
- BOX/apps/desktop/src-tauri/src/clipboard_history.rs:20  `const MAX_ITEMS: usize = 500;`
- BOX/apps/desktop/src-tauri/src/clipboard_history.rs:21  `const MAX_PINNED: usize = 100;`
- BOX/apps/desktop/src-tauri/src/clipboard_history.rs:92  `inner: Arc::new(Mutex::new(history)),` (history loaded into memory)
- BOX/apps/desktop/src-tauri/src/clipboard_history.rs:577  `fn trim_history(state: &mut StoredHistory) {`
- BOX/apps/desktop/src-tauri/src/clipboard_history.rs:578  `expire_items(state);` (then `while state.items.len() > MAX_ITEMS` at line 579)
- Also: BOX/apps/desktop/src-tauri/src/dashboard.rs:30  `static PENDING_PAGE: Mutex<Option<String>> = Mutex::new(None);` (single page string, not a history)

## L1 (LOOK/src-tauri/src/app.rs)
- app.rs:725  `fn schedule_idle_release(app: &AppHandle, since: Instant) {`
- app.rs:727  `let release_after = WEBVIEW_IDLE_RELEASE;`
- app.rs:747  `if let Err(error) = window.destroy() {` (main window, inside schedule_idle_release)
- app.rs:340  `if let Err(error) = window.destroy() {` (second destroy; in the settings path, `.settings_frontend` at line 342; enclosing fn name not read)
- app.rs:757  `let minutes = handle.state::<AppState>().config().idle_minutes;`

## L2 (LOOK/src-tauri/src/mediaserver.rs)
- mediaserver.rs:35  `pub fn start() {` (plain OS thread, not tokio)
- mediaserver.rs:47  `std::thread::spawn(move || {` (accept loop thread; `TcpListener::bind("127.0.0.1:0")` at line 39)
- mediaserver.rs:50  `std::thread::spawn(move || {` (one thread per connection)
- LOOK/src-tauri/src/lib.rs:236  `mediaserver::start();` (only start call)
- Stop: NOT FOUND. No stop/shutdown fn in mediaserver.rs; the only other references are LOOK/src-tauri/src/commands.rs:307 `media_base: crate::mediaserver::base(),`. The listener lives for the process lifetime; preview close does not touch it.

## L3 (in-memory caches, LOOK/src-tauri/src)
- archive.rs:358  `/// Extract one entry into the temp cache and return its path. Cached by archive content.` (on-disk temp cache, no size bound seen)
- fsx.rs:164  `type Cached = (` and fsx.rs:171  `static LAST: std::sync::Mutex<Option<Cached>> = std::sync::Mutex::new(None);` (single last-entry cache)
- link_consumer.rs:40  `struct PipelineCache {`
- link_consumer.rs:52  `pipelines: Mutex<PipelineCache>,`
- link_consumer.rs:206  `cache.entries.clear();` (replaced wholesale on manifest change; no size bound found)
- No LruCache found (grep for `LruCache` returned no hits).

## F1 (FIND/crates/find-core/src/index.rs)
- index.rs:169  `/// Approximate heap bytes used by the index.`
- index.rs:170  `pub fn heap_bytes(&self) -> usize {`
- index.rs:171  `self.parent.capacity() * 4`
- shrink / shrink_to_fit: NOT FOUND. Grepped `shrink` in FIND/crates/find-core/src and FIND/crates/arcade-find/src (and all of FIND --include=*.rs): no hits.

## F2 (FIND/crates/find-core/src/persist.rs)
- persist.rs:1  `//! Saving and loading the index (`index.bin` in the app data folder).`
- persist.rs:122  `pub fn save(path: &Path, index: &Index, fingerprint: u64, complete_at: i64) -> io::Result<()> {` (writes via `File::create(&tmp)` at line 128)
- persist.rs:189  `pub fn load(path: &Path) -> io::Result<(Index, Header)> {`
- persist.rs:253  `let p = dir.join("index.bin");` is inside a #[test] (round-trip test), NOT production code.
- Production path: `index_file()` callers: FIND/crates/arcade-find/src/link.rs:660 `let (index, _) = find_core::persist::load(&self.paths.index_file())`; FIND/crates/arcade-find/src/main.rs:152 `let Ok((index, _)) = find_core::persist::load(&p.index_file()) else {`. The index_file() definition was not read.

## W1 (WHEEL/src/main.cpp)
- main.cpp:416  `QQuickView overlay;`
- main.cpp:439  `QTimer releaseSettings;`
- main.cpp:441  `releaseSettings.setInterval(10000);`
- main.cpp:442  `std::unique_ptr<QQuickView> settings;`
- main.cpp:451  `settings = std::make_unique<QQuickView>();` (settings QQuickView creation)
- main.cpp:479  `QTimer releaseActivity;`
- main.cpp:481  `releaseActivity.setInterval(10000);`
- main.cpp:482  `std::unique_ptr<QQuickView> activity;`
- main.cpp:491  `activity = std::make_unique<QQuickView>();` (activity view creation)

## W2
- NOT FOUND in WHEEL/src/ (no `setGraphicsApi` or `QT_QUICK_BACKEND` in src/). Hits exist only outside src/: WHEEL/packaging/smoke-test.py:22 (`QT_QUICK_BACKEND="software"`), WHEEL/CMakeLists.txt:212 and :241 (`QT_QUICK_BACKEND=software` in test environments).

## W3 (WHEEL/src/platform/linux/LinuxBackend.cpp)
- LinuxBackend.cpp:945  `bool LinuxBackend::prepareOverlay(QQuickWindow *window, QString *error)`
- LinuxBackend.cpp:946  `{`
- LinuxBackend.cpp:947  `if (!window) {`
- LinuxBackend.cpp:948  `if (error) *error = QStringLiteral("The wheel overlay window was not created.");`

## S1 (SHELF/src/main.cpp)
- main.cpp:275  `QImageReader::setAllocationLimit(64);`
- main.cpp:292  `QQuickWindow::setGraphicsApi(QSGRendererInterface::Software);`
- main.cpp:296  `auto *thumbnails = new Shelf::ThumbnailProvider;`
- main.cpp:301  `thumbnails->setCacheLimitBytes(preferences.value("thumbnailQuotaBytes").toLongLong());`

## S2 (SHELF/src)
- ThumbnailProvider.cpp:22  `QCache<QString, QImage> images{64 * 1024}; // Costs in KiB.` (default 64 MiB cap)
- ThumbnailProvider.cpp:121  `void ThumbnailProvider::setCacheLimitBytes(qint64 bytes)`
- ThumbnailProvider.cpp:123  `const int kib = int(qBound<qint64>(0, bytes, 1024LL * 1024 * 1024) / 1024);` (clamped to 0..1 GiB)
- ThumbnailProvider.cpp:125  `if (m_cache->images.maxCost() != kib) m_cache->images.setMaxCost(kib);`
- ThumbnailProvider.h:11  `void setCacheLimitBytes(qint64 bytes);`
- ThumbnailProvider.cpp:2  `#include <QCache>`

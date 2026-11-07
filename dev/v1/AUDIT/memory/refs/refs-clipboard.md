# Arcade-clipboard references (read-only research)

Root: `/home/harneet/Work/Coding/App dev/Arcade-clipboard`

## C1 Linux runner startup, query flags, first frame

- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:16`  `gboolean start_hidden;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:65`  `static void first_frame_cb(MyApplication* self, FlView* view) {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:69`  `if (self->start_hidden) {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:70`  `gtk_widget_realize(window);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:73`  `gtk_widget_show(window);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:128`  `FlView* view = fl_view_new(project);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:139`  `g_signal_connect_swapped(view, "first-frame", G_CALLBACK(first_frame_cb),`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:141`  `gtk_widget_realize(GTK_WIDGET(view));`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:171`  `if (g_strcmp0(*argument, "--version") == 0 || g_strcmp0(*argument, "--arcade-manifest") == 0 ||`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:172`  `g_strcmp0(*argument, "--status") == 0 || g_strcmp0(*argument, "--restart") == 0) {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:173`  `query = TRUE;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:179`  `if (query) {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:180`  `self->start_hidden = TRUE;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:181`  `g_application_set_flags(application, G_APPLICATION_NON_UNIQUE);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:176-177`  `// --version, --arcade-manifest, --status and --restart answer from this` / `// process (Dart prints, or asks over the Link, and exits before any`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/my_application.cc:306`  `? G_APPLICATION_NON_UNIQUE` (constructor flags: NON_UNIQUE only when ARCADE_DATA_DIR is set)

Explanation: `--version`, `--arcade-manifest`, `--status`, `--restart` set `query` and make the process NON_UNIQUE, and nothing in `local_command_line` returns early for them, so the normal activate path (which runs `fl_view_new` at line 128) still builds a full Flutter view; the window stays hidden via `start_hidden`. I did not verify the exact exit point after Dart answers.

## C2 main.cc argument handling

- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:84`  `if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:85`  `fputs(kUsage, stdout);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:86`  `return 0;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:89`  `release_mount_handles();`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:90`  `wait_for_predecessor();`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:91`  `g_autoptr(MyApplication) app = my_application_new();`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:92`  `return g_application_run(G_APPLICATION(app), argc, argv);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:23`  `"  --version           Print the version\n"` (usage text)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:20`  `"  --status            Print one line of JSON: version, whether it runs, Link state\n"` (usage text)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/linux/runner/main.cc:32`  `"  -h, --help          Print this help\n";` (usage text)

Explanation: Only `--help`/`-h` has a fast path (prints usage, returns 0 before GApplication). `--version` and `--status` have no fast path in main.cc; they go through `g_application_run` into the runner's local-command-line code (my_application.cc:179-181). Usage text lines are the only place `--version`/`--status` appear in main.cc.

Also: `release_mount_handles` at main.cc:49 and `wait_for_predecessor` at main.cc:73 (up to 50 x 100 ms loop, main.cc:77-78) run before every launch, including queries.

## C3 Dart image widgets and caches

- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/clipboard_widgets.dart:300`  `child: Image.memory(image.bytes!,` (no cacheWidth/cacheHeight in lines 300-302; uses `height: 280`, `fit: BoxFit.contain`)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/clipboard_widgets.dart:415`  `? Image.memory(snapshot.data!,`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/clipboard_widgets.dart:417`  `cacheWidth: 160,` (only cacheWidth in lib/; no cacheHeight found)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/clipboard_widgets.dart:398`  `late final Future<Uint8List?> _image =` (feeds the FutureBuilder at line 412-413)

- `imageCache`: NOT FOUND (grep -rn "imageCache" apps/flutter_app/lib)
- `PaintingBinding`: NOT FOUND (grep -rn "PaintingBinding" apps/flutter_app/lib)

Explanation: Two `Image.memory` call sites, one without any cache size (line 300, full-size 280 px height) and one with `cacheWidth: 160` (line 417). Neither sets a decode cache size for the 280 px one.

## C4 ClipboardItem fields and what the list renders

- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/models.dart:49`  `class ClipboardItem {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/models.dart:69`  `final String text;` (full text, large for text clips)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/models.dart:72`  `final List<ClipRepresentation> representations;` (holds bytes for image/file)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/models.dart:73`  `final int size;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/models.dart:74`  `final String previewText;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/models.dart:90`  `text: json['text'] as String? ?? '',`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/models.dart:94`  `previewText: json['preview'] as String? ?? '',`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/models.dart:101-102`  `String get preview {` / `final normalized = (previewText.isNotEmpty ? previewText : text)`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/models.dart:140`  `final Uint8List? bytes;` (class ClipRepresentation, starts line 133)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/pages/history.dart:330`  `title: item.preview.isEmpty`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/pages/history.dart:332`  `: item.preview.split('\n').first,`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/overlay/quick_overlay.dart:321`  `title: item.preview.replaceAll(RegExp(r'\s+'), ' ').trim(),`

Explanation: The list UI renders `item.preview` (history.dart:330-332, quick_overlay.dart:321), never `item.text`; grep for `item.text` in lib/pages, lib/clipboard_widgets.dart and lib/overlay found nothing. `item.text` is only used for insert (models.dart:78 `bool get canInsertText => !hasBinaryContent && text.isNotEmpty;`). Server side, the preview is a short string built in store.rs (see C6), so the list gets the short preview when present.

## C5 Long-lived Dart collections and byte holders (AppController)

File: `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/services/app_controller.dart`

- `:61`  `List<ClipboardItem> _items = const [];` (full history; set at :606 `_items = _sortedItems(result);`, no Dart-side cap)
- `:62`  `List<ClipboardItem> _keyboardItems = const [];` (capped: :618 and :622 `limit: 40`)
- `:63`  `List<ClipboardItem> _overlayItems = const [];` (capped: :714 `limit: 250`; :1226 `limit: 250`)
- `:64`  `List<MeshDevice> _devices = const [];`
- `:65`  `List<PairingRequest> _pairings = const [];`
- `:68`  `final Set<String> _approvedPairingSessions = {};`
- `:70`  `final Map<String, String> _errors = {};`
- `:71`  `final Map<String, int> _errorOrder = {};`
- `:169`  `Map<String, Object?>? _photoInput;`
- `:241`  `{required String name, required Uint8List bytes}) =>`
- `:1391`  `'bytes': Uint8List.fromList(utf8.encode(payload.text))`
- `:1451`  `if (bytes is Uint8List &&` (desktop rich capture, format bytes)
- `:1514`  `{Uint8List? bytes, String? mime, String? path, int? size}) async {`

- Thumbnail cache map / bytes cache map: NOT FOUND (grep -n "cache\|Cache" shows only comments at :611-614 about the platform keyboard cache).

Explanation: `_items` has no Dart-side limit and grows with the server's history (bounded only server-side, see C8). `_keyboardItems` and `_overlayItems` are capped at 40 and 250. Image bytes live in `ClipRepresentation.bytes` inside `ClipboardItem.representations`, which is held by `_items`.

## C6 Rust thumbnails and image handling (store.rs)

- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs`: grep -in "thumbnail|resize|image" -> NOT FOUND (no matches).
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:300`  `let preview = history_preview(item)?;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:289`  `.map_err(|_| "Could not encrypt clipboard content for local storage".to_string())?;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1637`  `fn history_preview(item: &WireItem) -> Result<HistoryItem, String> {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1651`  `preview: if item.text.trim().is_empty() {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1658`  `short_preview(&item.text)`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1614`  `fn short_preview(preview: &str) -> String {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/payload.rs:144`  `fn validate_image_dimensions(mime: &str, bytes: &[u8]) -> Result<(), String> {` (reads PNG/JPEG header only, no decode or resize)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/payload.rs:215`  `return Err("Clipboard image exceeds the 16,384-pixel or 64-megapixel limit".into());`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/payload.rs:6`  `pub const MAX_PAYLOAD_BYTES: usize = 16 * 1024 * 1024;`

Explanation: No thumbnail or resize code exists in store.rs; the only image work is header dimension validation in payload.rs. Image bytes are encrypted and stored as representations; I did not trace whether they are kept in memory after the store call returns.

## C7 Rust global and static caches

- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/api.rs:11`  `static CORE: OnceLock<Mutex<Option<Arc<Core>>>> = OnceLock::new();` (singleton Core)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/api.rs:12`  `static LIFECYCLE: OnceLock<RwLock<()>> = OnceLock::new();` (lock, no data)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/api.rs:14`  `static LINK_STARTUP: OnceLock<Mutex<Option<tokio::task::JoinHandle<()>>>> = OnceLock::new();` (startup task handle)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/link.rs:126`  `static EVENTS: OnceLock<Events> = OnceLock::new();` (event queue)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/link.rs:407-408`  `fn picks() -> &'static Mutex<HashMap<u64, Job>> {` / `static PICKS: OnceLock<Mutex<HashMap<u64, Job>>> = OnceLock::new();` (pending picks by id)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/link.rs:773`  `static PRESENCE: OnceLock<Mutex<Option<Arc<Presence>>>> = OnceLock::new();`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/link.rs:774`  `static TRAY_WATCHER: OnceLock<Mutex<Option<TrayHostWatcher>>> = OnceLock::new();`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/link.rs:775`  `static LINK_SETTINGS: OnceLock<Mutex<Option<LinkSettings>>> = OnceLock::new();`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/link.rs:776`  `static SETTINGS_CHANGE: OnceLock<Mutex<()>> = OnceLock::new();`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/link.rs:778`  `static PENDING_SHORTCUTS: OnceLock<Mutex<HashMap<u64, mpsc::Sender<Value>>>> = OnceLock::new();` (pending shortcut replies)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/core.rs:87-106`  `invitations`, `pairings`, `connections`, `transfers`, `candidates`, `next_dial`, `dial_failures` as `StdMutex<HashMap<..>>` fields of the Core struct (per instance, not global). core.rs has no OnceLock/lazy_static/LruCache; link.rs has no LruCache.

Explanation: Global state is singletons holding handles and small maps. The HashMaps in core.rs are per-Core fields, and I found no LRU or byte cache in these three files.

## C8 Retention and size budget

- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:16`  `const MAX_RETAINED_ITEMS: usize = 10_000;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1521`  `INSERT INTO settings(key,value) VALUES ('paused','false'),('retention_hours','24'),('max_items','500');"`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1542`  `INSERT OR IGNORE INTO settings(key,value) VALUES ('paused','false'),('retention_hours','24'),('max_items','500');"`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1005`  `self.prune_count(self.setting("max_items", DEFAULT_MAX_ITEMS))?;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1009`  `fn prune(&mut self, max_items: usize) -> Result<(), String> {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1015`  `let retention: u32 = self.setting("retention_hours", DEFAULT_RETENTION_HOURS);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:1044-1046`  `fn prune_count(&self, max_items: usize) -> Result<(), String> {` / `let max_items = max_items.clamp(1, MAX_RETAINED_ITEMS) as i64;` / `DELETE FROM items WHERE id IN (SELECT id FROM items ORDER BY pinned DESC,created_at DESC,id DESC LIMIT -1 OFFSET ?1)`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/store.rs:711-712`  `if count >= MAX_RETAINED_ITEMS as i64 {` / `return Err("Pin preferences reached their storage limit".into());` (count-based pin cap, not size)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/core.rs:256-258`  `let retention_hours = state` / `.setting("retention_hours", DEFAULT_RETENTION_HOURS);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/core.rs:794`  `let max_items = state.store.setting("max_items", DEFAULT_MAX_ITEMS);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/core.rs:1558`  `"retention_hours" => {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/core.rs:1567`  `"max_items" => {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/portable_settings.rs:47-48`  `|| !(1..=720).contains(&self.retention_hours)` / `|| !(1..=10_000).contains(&self.max_items)`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/services/app_controller.dart:1622`  `_retentionHours = (result['retention_hours'] as num?)?.toInt() ?? 24;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/services/app_controller.dart:1623`  `_maxItems = (result['max_items'] as num?)?.toInt() ?? 500;`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/core/rust/src/payload.rs:6`  `pub const MAX_PAYLOAD_BYTES: usize = 16 * 1024 * 1024;` (per-item cap, not a store budget)

- `budget` / `quota`: NOT FOUND in core/rust/src and apps/flutter_app/lib.
- `storage`: only secure-storage and Link/integration-test uses (e.g. core/rust/src/secret.rs:133, core/rust/src/integration_tests.rs:1); no size-based pruning.

Verdict: CONFIRMED. Pruning is by age (retention_hours, default 24, valid 1-720) and by count (max_items, default 500, clamped to 10_000). No size budget or byte-based pruning exists.

## C9 Wayland clipboard watcher process model

- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/clipboard_bridge.cc:156`  `GSubprocess* process = g_subprocess_newv(values.data(),`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/clipboard_bridge.cc:199`  `ReadCommand({"wl-paste", "--no-newline", "--type", target.first}, kMaximumClipboardBytes - read->total,`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/clipboard_bridge.cc:360`  `ReadCommand({"wl-paste", "--list-types"}, 16384, [read](bool success, std::vector<uint8_t> bytes) {`
- clipboard_bridge.cc: grep for fork/exec/g_spawn/thread/pthread/std::thread -> NOT FOUND (only the g_subprocess calls above and the async ProcessRead callbacks).
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/apps/flutter_app/lib/platform/desktop_adapter.dart:603-606`  `process = await Process.start(` / `helper,` / `['--watcher-events', wlPaste, helper],` (long-lived watcher started from Dart)
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/wl_capture_helper.cc:145`  `int WatcherMain(const char* wl_paste, const char* helper_path, bool events) {`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/wl_capture_helper.cc:158`  `const pid_t child = fork();`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/wl_capture_helper.cc:166-167`  `const_cast<char*>(wl_paste),` / `const_cast<char*>("--watch"),`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/wl_capture_helper.cc:169`  `const_cast<char*>(events ? "--event-worker" : "--worker"),`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/wl_capture_helper.cc:172`  `execv(wl_paste, arguments);`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/wl_capture_helper.cc:185`  `// wl-paste ended; stop any remaining workers and report the exit.`
- `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/wl_capture_helper.cc:228-231`  `if (argc == 4 && std::strcmp(argv[1], "--watcher") == 0) {` / `if (argc == 4 && std::strcmp(argv[1], "--watcher-events") == 0) {`
- CMake: `/home/harneet/Work/Coding/App dev/Arcade-clipboard/platform/desktop/arcade_desktop_bridge/linux/CMakeLists.txt:12`  `add_executable(arcade_clipboard_wl_capture`

Explanation: The bridge's own reads (clipboard_bridge.cc) are one `wl-paste` subprocess per read, async on the GLib main loop, with no thread. The watcher is one long-lived `arcade_clipboard_wl_capture --watcher-events` process started from Dart, which forks and execs `wl-paste --watch` (wl_capture_helper.cc:158-172); the per-event work is the `--event-worker` that wl-paste launches for each change (inferred from the `--watch` argument at line 167 and the comment at line 41, not traced further).

## Summary
All nine items answered from grep/Read output; NOT FOUND items are marked inline (imageCache, PaintingBinding, thumbnail/resize in store.rs, budget/quota, thread/fork in clipboard_bridge.cc).

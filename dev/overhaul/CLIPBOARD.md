# Spec: Arcade Clipboard

**Outcome:**
- Every Clipboard screen uses the Arcade design kit with Clipboard's pink accent, on desktop and mobile. That
  covers the window (history, devices, settings), welcome and pairing, dialogs, and the quick overlay.
- Every verified Clipboard bug is fixed.
- The repo is cleaned up and matches the project standard.
- A new Clipboard release ships.

Prerequisite: Spec 1 (`TOOLS.md`), which provides Arcade Link `v0.4.0` with `design/`. Read `STANDARD.md` first.
Evidence: `AUDIT/keep.md` and `AUDIT/hygiene-and-dev-standard.md` (Clipboard sections; the audit was stopped before it took screenshots of this app).

## Starting point

| | |
|---|---|
| Repo | `qa-p1/Arcade-clipboard`, main at `fdd4788` on 2026-10-28 (release 0.2.5). Start from current main. |
| Toolkit | Flutter (Material 3) app in `apps/flutter_app/` (desktop Linux/Windows/macOS + Android/iOS), with a Rust core (`core/rust`), and a Linux launcher (`platform/linux/launcher`) |
| Link | root `Cargo.toml:13` pins `rev = "4c75f3a…"` |

Today's UI vs. the standard:
- **Theme:**
  - `app.dart:59-120` builds `ColorScheme.fromSeed` from **pine green** `_pine = 0xFF386253` (dark seed `0xFF82B7A0`).
  - Green is Tools' and status colour; Clipboard's accent is pink.
  - Plus scattered literal colours, including other apps' accents copied in by hand (`0xFF7C5CFF`, `0xFF94A8FF`,
    `0xFFF59E0B`).
  - Inter is already bundled (`pubspec.yaml:39-42`).
- **Structure:** everything lives in one 2,956-line `app.dart`:
  - side rail (`_SideRail`, `_NavItem`, `_BrandLockup`, `_StatusPill`) and mobile header;
  - pages: welcome/pairing (`_WelcomeView`, `_JoinVerificationCard`, `_PairingScanner`), clipboard history
    (`_ClipboardPage`, `_ClipboardRow`, `_FilterControl`, empty state), devices (`_DevicesPage`, pairing requests,
    trusted devices), settings (`_SettingsPage`, `_SettingLine`);
  - dialogs: invite, clear history, add clip, clip detail;
  - the quick overlay `MeshOverlay`.
- **Settings:** section labels are uppercase ("PRIVACY", "DESKTOP", "KEYBOARD & SHARING", "APPEARANCE", "STATUS").
  The remote relay field has a Save button.

## Keep (do not remove or flatten)

End-to-end encrypted sync between your own devices; QR pairing and verification; the remote relay; the Android/iOS apps and share bridge; the quick overlay with paste as plain text; pinned clips; trusted-device management.
These get kit styling only. Everything in `AUDIT/keep.md` › "Clipboard — Keep" is also kept. It lists the capabilities with their sources.

## Work

### 1. Adopt the kit

- Vendor `design/dart/arcade_theme.dart` (+ `arcade_icons.dart`) from Link `v0.4.0` into
  `apps/flutter_app/lib/design/` with a hash file. Replace the bundled Inter with the kit's copy (same family
  name). Point the Rust `arcade-link` at `tag = "v0.4.0"` and refresh `Cargo.lock`.
- If Link `design/dart/` has no widget set yet, build it now in Link (Clipboard is the only Flutter app):
  - `ArcadeButton` (variants per STANDARD §5), `ArcadeSwitchRow`, `ArcadeListSection` + `ArcadeRow`;
  - `ArcadeBadge`, `ArcadeKeyChip`, `ArcadeNotice`, `ArcadeEmptyState`, `ArcadeToast` (SnackBar theme);
  - `ArcadeSidebar` + `ArcadeNavItem`, `ArcadePageHead`, `ArcadeSegmented`, `ArcadeSearchField`.

  Each is a thin wrapper over Material widgets themed by `arcadeTheme(brightness, 'arcade.clipboard')`. Tag Link
  `v0.4.x` and vendor that.
- `_lightTheme` / `_darkTheme` → `arcadeTheme(...)`:
  - accent pink `#d91676` / `#f176b3`;
  - neutrals from the kit;
  - Material 3 surfaces mapped so cards, dialogs, menus and inputs match the kit (no tonal tints).
- Every `Color(0x…)` literal becomes a kit token. Other apps' accents (in `arcade_widgets.dart` `ArcadeGlyph` /
  Link labels) come from `ArcadeTokens.accent(appId)`.
- Split `app.dart` by surface: `pages/welcome.dart`, `pages/history.dart`, `pages/devices.dart`,
  `pages/settings.dart`, `overlay/quick_overlay.dart`, `shell.dart`, `dialogs/*.dart`. No behaviour change. This
  is required to make the screens reviewable and is part of the cleanup.

### 1b. Shared conventions (STANDARD §8.1, §10)

- **Words:** every UI string meets STANDARD §8.1:
  - fixed words ("Settings", "Start at login", "Quit Arcade Clipboard", "Install", "Show in folder");
  - error wording "Couldn't …";
  - one tagline, no split-weight app name, window titles "<Thing> — Arcade Clipboard".
- **Formatting:** sizes, dates, durations and counts go through the kit's format helpers. No local formatters
  stay.
- **Identifiers and folders:** move to `dev.arcade.Clipboard` and `arcade/clipboard/` folders, with the verified migration in
  STANDARD §10. Today: `~/.local/share/dev.arcade.clipboard`, `dev.arcade.clipboard.desktop` (already reverse-DNS: rename to `dev.arcade.Clipboard`).
- **Desktop entry:** contents per STANDARD §10.
- **App icon family:** replace every platform icon set: macOS `AppIcon.appiconset` (today the default Flutter logo), Windows `.ico`, Linux, Android `mipmap-*`/adaptive, iOS; plus the README logo with the kit-generated set (STANDARD §8, brand mark and app icons). The tray icon becomes the monochrome glyph.
- **Default shortcut:** follows the STANDARD §10 table. Change: Linux Ctrl+Shift+Space → Ctrl+Alt+V, macOS ⇧⌘V → ⌃⌥V. Existing users keep theirs.
- **Behaviour:**
  - closing a window doesn't quit;
  - start at login goes to the background;
  - tray left click opens, right click shows the menu;
  - a second launch focuses;
  - overlays close on Esc and on focus loss, except Keep items.
- **Command line:** adds whatever STANDARD §10 lists and the app lacks. Existing flags keep working.

### 2. Surfaces

Every control in this app uses its STANDARD §5.1 version: shortcut recorder, settings rows, theme
picker, slider rows, search field, file/output pickers, result panel, context menus, confirm dialogs,
onboarding, keyboard conventions and window behaviour. Any custom variant this app has today is replaced,
not restyled.

**Desktop window (Template A):**
- **Side rail:**
  - becomes the standard 212 px sidebar: brand mark tile + "Arcade Clipboard";
  - nav: History, Devices, Settings;
  - footer: sync status as the status dot + label (from `_StatusPill`), then "Version x.y.z";
  - collapses to 64 px icons below 760 px.
- **History page:**
  - page head "History" with subtitle "N clips · synced with M devices" and actions "Add clip" (secondary) and
    "Clear history…" (danger, confirm);
  - search field + segmented filter (All / Text / Images / Links / Files / Pinned);
  - rows 52 px: thumbnail or type glyph, first line, source device + time, trailing pin/copy;
  - selection uses `accent-soft`;
  - all four data states, with the empty state "Copy something and it shows up here".
- **Devices page:**
  - sections "This device", "Trusted devices", "Pairing requests" as kit lists;
  - pairing requests get a `warn` notice with "Allow" (primary) / "Decline";
  - "Invite a device" is the primary page action (the invite dialog with the QR code uses the kit dialog);
  - empty state "No other devices yet".
- **Settings page**, sections in the standard order, sentence case:
  1. **General:** Appearance (System / Light / Dark segmented), Start at login, desktop options.
  2. **Shortcuts:** the global "open overlay" shortcut + "Keyboard settings", read-only overlay keys.
  3. **Privacy:** history retention, what syncs, "Clear unpinned history…".
  4. **Sync:** remote relay (applies on Enter/blur with inline validation; the Save button goes away), status
     rows.
  5. **Connected apps:** the shared Link page (`ConnectedAppsPage` in `arcade_widgets.dart` moves onto kit
     widgets).
  6. **About:** version, channel, "Updates are managed by Arcade Tools" (desktop), logs, diagnostics, guide,
     licences.
- **Welcome and pairing:** a kit empty-state hero (display type, app mark) with two choices as cards: "Start on
  this device" / "Join your other device". The join verification code is shown in key-chip style mono groups,
  and the scanner frame uses the accent.

**Quick overlay** (`MeshOverlay`, Template B):
- 44 px search field, 40 px rows (`_OverlayClipRow`), selected = `accent-soft` + accent bar;
- footer hint bar from `_KeyboardHint`/`_KeyCap`, rebuilt on the kit key chip: "↵ Paste", "Ctrl+↵ Paste as plain
  text", "Esc Close";
- empty state "Nothing copied yet".

**Mobile (Android/iOS):**
- The same tokens and components.
- Sidebar → bottom navigation (History, Devices, Settings).
- `_MobileHeader` → kit page head.
- Hit targets ≥ 44 px on touch.
- The share bridge sheet uses the kit sheet style.

**Dialogs** (add clip, clip detail, invite, clear history, allow access): kit dialog, primary last, named
verbs ("Clear history", "Allow access"). Destructive actions use destructive style.

**Install prompt and tray** (Linux launcher, desktop adapter): the self-install prompt matches Tools' copy and
order. Tray keeps its current items in the standard order and wording: "Open Arcade Clipboard", "Settings" (from
"Open Settings"), separator, "Restart Arcade Clipboard", "Quit Arcade Clipboard". No new items.

### 3. Verified bugs

The 2026-10-27 audit was stopped before its Clipboard tester ran, so no Clipboard feature was checked by use. Its source review is complete. As part of this spec, use every Clipboard feature listed in `AUDIT/keep.md` › Clipboard with real inputs (the acceptance check below). Fix whatever fails here, with a regression test, before release.

Found by the audit's source and lockfile checks:
- **C1. The macOS app icon is Flutter's default logo** (`macos/Runner/Assets.xcassets/AppIcon.appiconset`).
  Fixed by the icon family in §1b.
- **C2. Android release builds are signed with the debug key** (`android/app/build.gradle.kts:41-43`,
  marked TODO).
  - *Fix:* release signing from a keystore supplied as CI secrets, with debug signing only for debug builds.
  - *Check:* `apksigner verify --print-certs` on the release APK shows the release certificate.
- **C3. The locked dependency `jni_flutter` 1.0.4 has been retracted.** Update it to 1.0.4+1 and re-run
  `pub get --enforce-lockfile` plus the Android build.
- **C4. `docs/STATUS.md:99` onward says AppImage self-install and uninstall aren't implemented**, which
  contradicts the launcher that implements them. Correct the text after checking the release.

### 4. Cleanup

Remove (provably unused):
- the template comment in `android/app/build.gradle.kts:25`;
- the `thiserror` dependency (`core/rust/Cargo.toml:26`; it is never used). Remove it and run all targets
  plus FRB generation.

Leave as they are:
- the generated FRB code, plugin registrants and icons (generator output with real consumers).

Decide and fix:
- `tracing-subscriber` in `services/relay/Cargo.toml:17` is unused. Either add the subscriber in the relay's
  `main.rs` (so relay logs work), or remove the dependency. Prefer adding it: a relay without logs is hard
  to run.

Delete merged remote branches.

### 5. Project standard

- **Early-days docs:** `Original-spec.md` (2,269-line original spec) moves to `docs/dev/history/`.
  `docs/STATUS.md` gets the corrections from C4.
- Add `rust-toolchain.toml`. The manifest says 1.88 while CI uses 1.98.1 and the relay is edition 2024;
  pick 1.98.1 everywhere and set `rust-version` to match. Add a `.flutter-version` (3.47.2).
- Developer docs (`architecture.md`, `development.md`, `ios.md`, `linux.md`, `platforms.md`, `protocol.md`,
  `relay-deployment.md`, `releases.md`, `security.md`) go to `docs/dev/`. They are already lowercase.
- Keep the separate iOS workflow; move desktop releases to the shared `tag.yml` → `release.yml` names.
- `scripts/check` = what CI runs.

### 6. Docs and release

- Retake README and `docs/user/images`: history page, devices, quick overlay, light and dark, plus one mobile
  screenshot.
- `docs/STATUS.md` dated entry, CHANGELOG entry, minor version bump.
- 3-OS CI green (and the Android build job) → merge → release → check that Tools updates Clipboard.

## Acceptance

- [ ] No `Color(0x…)` and no `fontSize:` literal outside `lib/design/`. Light, dark and system all work and
      switch live. Pink accent everywhere the accent is used.
- [ ] `app.dart` is split. `flutter analyze` is clean. Widget and integration tests (`integration_test/`) pass.
- [ ] Real pairing between two isolated profiles works: invite → verify → sync a text, an image and a link →
      pin → clear unpinned. Quick overlay paste works on Linux.
- [ ] Link: "Send to my devices" from Look, Lens and Box, and "Add to Shelf" from a clip still work.
- [ ] Every item in §3 re-checked on the released build. 3-OS CI is green and the release is published.

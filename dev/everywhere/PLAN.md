# Arcade everywhere: the plan

**Status: agreed with the owner on 2026-11-22. This is the final plan for the next round.** It covers the new work
(every Arcade ability reachable from the file manager and the browser, wired by data instead of code), Box's first
proper release (1.0.0), and every leftover from the v1 round. When this plan is done, nothing from v1 is left open
and nothing needs a separate week of local testing: each stage below says how it is tested, and the few checks only
the owner's own computers can do are short prompts in `LOCAL-PROMPTS.md`.

Read `dev/v1/HANDOFF.md` for the state of the fleet when this plan starts and `dev/v1/REAL-USER-RUN.md` for how
real-user checks are done.

---

## 1. The goal in plain words

1. **Use any Arcade ability without opening the app.** Right-click a file in whatever file manager the user has and
   run Box's tools, Lens's recognizers, Look's preview, Shelf, Clipboard and the rest. Right-click anything in the
   browser, or press a button the extension puts on the page (a download button under every YouTube video, a button
   on images), and run the same abilities there.
2. **No hard-coded wiring.** Each app describes what it can do. Connecting those abilities to the other apps, the
   file manager menus and the browser needs no update of anything except the app that gained the ability. A new
   Arcade app shows up everywhere without a Link release or any other app's release.
3. **Everything stays usable alone.** Every app keeps working by itself, as today. The extension is the only piece
   that needs the apps.
4. **Windows, macOS and Linux from the start.**
5. **Box 1.0.0** ships with all of this, built on the rc.7 work.

## 2. What the owner decided (2026-11-22)

| Question | Decision |
|---|---|
| Who decides what an app offers | Each app, as data in its card. No caller hard-codes another app's actions. |
| Two apps doing the same job | Both show the first time; the user can pick a default (and change it). |
| A background helper program | Yes, if it isn't a mess: shipped inside Arcade Tools, starts at login, tiny when idle. |
| Browsers | Chromium family (Chrome, Edge, Brave, Vivaldi, Opera) **and** Firefox family (Firefox, Zen, LibreWolf, Floorp). The owner uses Chrome and Zen. |
| Extension distribution | Not on any store. Chrome: unpacked zip loaded in developer mode. Firefox/Zen: signed as an **unlisted** add-on through the owner's free Mozilla developer account (Firefox and Zen refuse unsigned add-ons permanently), downloaded from GitHub as an `.xpi`. |
| Windows/macOS code signing | Later, step by step. Until then the plain menus (Windows "Show more options" and "Send to", macOS Services/Quick Actions). Stage 9 adds the signed integrations. |
| Lens | Its actions become shareable too (OCR, QR, colour, and the rest work from the browser and file menus). |
| Send to phone | Yes, through Clipboard, within Clipboard's own limits (text 32 KiB, a clip 16 MiB, no folders). Bigger items show the entry greyed out with the reason. |
| YouTube | A proper downloader under every video: video or audio only, quality, video and audio format (MP3 and the rest), audio quality, subtitles, thumbnail, metadata, name, folder. It remembers the last choice. |
| Progress | A small window that doesn't take the screen, can be minimized, and shows when a job is done. |
| Where outputs go | A default folder, with a setting to ask every time. |
| Release order | Link → Tools (with the helper) → Box 1.0 → extension → the other apps one by one. |
| Leftovers | Folded into this plan, each in the stage of the repo it belongs to (section 7). No separate round. |

## 3. What exists today (facts this plan builds on)

- **Link is a rulebook plus a library built into every app** (`Arcade-Link/SPEC.md`): no broker. Each app writes a
  card (`<registry>/<arcade-id>.json`) listing its actions; a running app writes an endpoint file and listens on a
  local socket; callers say `hello` with a token and `invoke` an action; files travel as paths, in-memory content as
  handoff files; a stopped app can run a headless action once (`--arcade-invoke`). Rust crate for Box, Lens, Look,
  Find, Tools and Clipboard's core; Qt module for Wheel and Shelf.
- **The cards are already data, but three layers of hard-coding sit on top:**
  1. Link compiles in the app list, names, taglines, "what these two apps do together" sentences and release URLs
     (`crates/arcade-link/src/manifest.rs:125–205`).
  2. Every app hard-codes which of the other apps' actions it shows. Lens: `crates/lens-actions/src/arcade.rs:282`
     (only `look.preview`, `clipboard.add`, `wheel.add_action`, `shelf.add`, `find.show`, five featured Box image
     presets and `box.open`; any other app: nothing). Same pattern in Find (`crates/arcade-find/src/link.rs`), Look
     (`src-tauri/src/link_consumer.rs`), Shelf (`src/link/PeerHub.cpp`, `src/Controller.cpp`), Wheel
     (`src/providers/ArcadeLinkProvider.cpp`, `src/core/WheelController.cpp`), Clipboard
     (`core/rust/src/link_consumer.rs`), Box (`apps/desktop/src-tauri/src/link.rs`, `screen_capture.rs`,
     `clipboard_history.rs`). Tools hard-codes the app list in its tray glyphs (`src-tauri/src/tray/assets.rs`).
  3. Box's card loses information: no options form (Box's own catalog has one per tool, 6 control types, drawn by
     one generic form `StandardToolForm.svelte`), its types are squeezed into Link's coarser set (a subtitle file
     becomes `file/any`, so the Subtitle tool would show on every file; JSON becomes `file/code`), and only 10 of
     109 tools are marked to show in other apps.
- **Box** has 109 tools in 14 categories (`catalog/tools.json`): Images 15, PDF 13, Audio & Speech 11, Video 11,
  Converters & Calculators 9, Text & Data 8, Developer 7, Screen & Capture 7, Downloads 5, Web & Network 5, Files 5,
  System 5, QR & Barcodes 4, Everyday 4; plus saved pipelines and sandboxed plugins (WASM). Its card publishes every
  implemented tool except screen tools, WASM plugins and tools whose only input is the screen or clipboard. The
  desktop app accepts `--arcade-invoke`, `--toggle`, `--pipelines`, `--dashboard`.
- **Lens** has 26 recognizers and 156 actions; it publishes only `lens.capture`, `lens.capture_and_act`,
  `lens.analyze`, `lens.recognize`, `lens.pin`.
- **Look** already integrates with GNOME Files (Space) and Windows Explorer (built and tested in CI, never run on a
  real Windows desktop).
- **Tools** downloads `catalog.json` from this repo at runtime (`src/catalog.rs`, with a built-in snapshot). That is
  the channel for shared data in this plan.
- **No Windows or macOS build is code-signed today** (no signing secrets in any workflow).
- **Box state:** `v1.0.0-rc.7` (main e40ddcd) published; its Gates failed only "Linux (conformance, the app's own
  checks)" because the upgrade test couldn't start Box 0.4.3 on Ubuntu 22.04 (glibc 2.38). The fix, 33f133d (run that
  test on 24.04), is on `claude/sharp-cori-29w5eg`. Box is on Link 1.0.13 and `url` 2.5.8.

## 4. The design

### 4.1 Cards that carry everything (Link manifest schema 1, additive)

Every field below is optional, so today's apps and readers keep working (readers ignore unknown fields; SPEC §9).
Protocol stays 1.

Per action, new fields:

| Field | Meaning |
|---|---|
| `options` | The action's options form, in Box's catalog form format generalized for every app: `{version, input?, controls:[{key, label, type, default?, choices?:[{value,label}], minimum?, maximum?, step?, placeholder?, help?, showWhen?:{key, equals \| oneOf}, advanced?}]}`. Types: `text`, `number`, `select`, `toggle`, `password`, `directory` (Box's six), plus `file` and `color`. Defaults are the values a one-click run uses. (Built: Link `form` module.) |
| `surfaces` | Where it makes sense: `file-menu`, `folder-menu`, `browser-image`, `browser-link`, `browser-video`, `browser-audio`, `browser-selection`, `browser-page`, `browser-pdf`, `browser-download` (a finished download), `palette` (searchable lists: the browser popup, the Island, Find, Wheel), `screen` (Lens's capture flows). Empty means "derive from `accepts`". |
| `rank` | Per input type, how strongly the app suggests it (0–100). Replaces `featuredFor` (kept as a fallback reader). |
| `group` (exists), `keywords` | For grouping menus ("Convert ▸ Image") and for search in the palettes. Box already has both. |
| `job` | A shared name for what the action does (`image.read-text`), so two apps doing the same job are recognized from their cards (both show until the user picks a default), with `rules` in the catalog only for corrections. |
| `oneClick` | Safe to run with defaults straight from a menu (no form). Actions with effects `overwrites-files`, `deletes-files`, `uploads-content`, `executes-commands` are never one-click. |
| `maxBytes`, `maxItems` | Already in the spec; now filled in by every app (Clipboard: 16 MiB per clip, 32 KiB text). |
| `requires` | Engines or apps it needs (`engine:ffmpeg`, `app:arcade.lens`), so callers can offer "Install FFmpeg" or "Install Arcade Box" instead of hiding the entry. |
| `output` | Where results go by default: `beside` (next to the input), `downloads`, `ask`, `none` (results are shown, not saved). |

New content types (added to SPEC §5.1 and `spec/vectors/content.json`, with the extension table): `file/subtitle`,
`file/csv`, `file/json`, `file/markdown`, `file/html`, `file/svg`, `file/ebook`, `text/markdown`. Each refined type
has a parent (`file/csv` → `file/spreadsheet`, `file/json`/`file/html` → `file/code`, `file/svg` → `file/image`,
`file/ebook` → `file/document`, `file/markdown` → `file/text`, `text/markdown` → `text/plain`) and matches its
parent's patterns, and callers send each input as the type the target's card names (so an app built before a kind
existed never sees it). `text/html` and `network/host` were dropped: `text/rich` already carries HTML, and no action
needs a host type yet. (Built in Link 1.1: refined kinds, `type_for`, `adapt_inputs`, Qt the same.)

### 4.2 The app list becomes data

- `catalog.json` (this repo) gains for each app: `name`, `tagline`, `releases`, `icon` (already there), `pairs`
  (the "what these two do together" sentences, keyed by peer), and `linkActionsHint` (which actions to show in
  install prompts; stage 2). The release page comes from `repo`; Arcade Tools' own entry stays the top-level `tools`
  object. Tools already downloads it; Tools now also writes the copy it has to the shared Arcade folder
  (`<registry parent>/catalog.json`, Link `catalog::write_shared`) so every app and the helper read it locally and
  offline. Connected apps pages list the known apps in today's order, then new catalog apps (the catalog itself must
  stay alphabetical). (Built: Link `catalog` module / Qt `Catalog`; `pairs` in the schema, validator and data.)
- Link's compiled `app_name`, `app_pitch`, `peer_description`, `releases_url` and the `ids::APPS` list become
  fallbacks used only when no `catalog.json` is readable. A card's own `name` and `icon` win over both.
- Tools' tray glyphs come from the card's `icon` (with the compiled glyphs as a fallback).
- **Result:** a new Arcade app is added by publishing its card and one entry in `catalog.json`. No Link release and
  no other app's release.

### 4.3 One shared "what can I do with this?" step (Link `offers`)

A pure function in Link, the same in Rust and Qt (shared conformance vectors, like today's content vectors):

```
offers(input, surface, cards, rules, prefs) -> [Offer]   // grouped, ranked, deduplicated
```

- **Input:** the content (paths with types, text, URL, page), and the surface (`file-menu`, `browser-video`, ...).
- **Cards:** every installed app's card with Link on.
- **Rules:** a `rules` section in `catalog.json` (hide, rename, regroup, boost an action for a type, mark two
  actions as "the same job"), so wiring mistakes are fixed by editing data in this repo.
- **Prefs:** the user's choices in `<arcade config>/offers.json`: a default per job ("Read text from image → Lens"),
  hidden actions, pinned actions, output folder, "ask where to save".
- **Rules for the result:** SPEC §1's "never show a broken entry" still holds; unavailable actions with a `requires`
  show as "Install …" entries instead of disappearing; two actions marked the same job both show until the user picks
  a default, then the default shows first and the other moves under "Other apps"; `maxBytes`/`maxItems` grey an entry
  out with the reason.
- **Every caller uses it:** Lens, Find, Look, Shelf, Wheel, Clipboard, Box's Island, Tools, the helper, the file
  menus and the extension. Section 4.6 lists each hard-coded list that is deleted.
- A caller may still add its **own** actions (Lens's built-in actions, Find's Rename) next to the offers; it just no
  longer chooses which **other** apps' actions to show.

### 4.4 The Arcade helper

**What the user sees:** nothing to install. Arcade Tools installs and updates it. It starts at login and stays tiny
when idle. It draws a small progress window only while jobs run.

**What it is:** a small Rust program built in the Link repository (new crate `crates/arcade-helper`, binary
`arcade-helper`, Link id `arcade.helper`), packaged inside every Tools build (AppImage, setup.exe, dmg), installed
by Tools next to Tools.

**What it does:**

1. **Bridge for the browser.** It is the native messaging host for both browser families (`dev.arcade.helper`). The
   extension asks it for offers and asks it to run them. It only answers our extension IDs (`allowed_origins` with
   the fixed Chrome ID, `allowed_extensions` with the Firefox add-on ID).
2. **Bridge for the file managers.** Menu entries call `arcade-helper menu <paths>` (a quick picker listing the
   offers for those files) or `arcade-helper run <action> <paths>` (a pinned one-click action).
3. **Writes the integrations and keeps them current.** It watches the registry (no polling; SPEC §1.3) and rewrites
   the file-manager entries and browser host files when cards, rules or prefs change, only if content changed.
4. **Runs jobs.** Through Link (resident app, one-shot `--arcade-invoke`, or start the app in the background),
   exactly as SPEC §7. Safety stays with the owning app (SPEC §1.5). Network, upload and command effects ask once
   per action with a preview (SPEC §1.8).
5. **The progress window.** One small window in a screen corner (theme from the design kit, same toolkit as Find
   and Lens): each job with its progress, Cancel, and when done Open, Show in folder, Copy, Send to… (offers on the
   result). Minimize hides it to a notification; a finished job also sends a system notification. Closing it never
   cancels jobs.
6. **Outputs.** File-menu jobs: next to the input by default, never overwriting (Box's rule). Browser jobs: the
   browser's download folder by default. Settings (in Tools' new **Everywhere** page): per-surface folder, or ask
   every time.
7. **Install prompts.** An offer whose app is missing becomes "Install Arcade X" and goes through `tools.install`
   (the user confirms in Tools).

**Not a mess:** one program, one process, owned by Tools, removed by Tools' uninstall (which also removes every
menu entry and host file it wrote, checked by Tools' uninstall test).

### 4.5 File manager menus

Static menu formats can't list per-file offers, so every file manager gets the same two kinds of entries:

- **"Arcade…"**, which opens the helper's quick picker for the selected files: a small searchable popup with all
  offers, grouped, defaults first, with the options form when an action needs one.
- **Pinned actions:** up to 8 one-click actions the user pins in Tools (defaults: the top-ranked one-click offers per
  common type, e.g. Convert image to WebP, Remove background, Compress PDF, Extract audio, Preview in Look, Keep on
  Shelf, Send to phone). Written as real menu entries filtered by type, regenerated when cards or pins change.

| Platform | Mechanism (written by the helper, per user, no admin) |
|---|---|
| Linux, every file manager | "Open With" desktop entries with `MimeType=` for the pinned actions and the picker (works in all of them) |
| Nautilus (GNOME Files) | `~/.local/share/nautilus/scripts/Arcade/` (the Scripts submenu); a `nautilus-python` extension when `python3-nautilus` is installed, for a real top-level "Arcade" submenu |
| Dolphin (KDE) | `~/.local/share/kio/servicemenus/arcade-*.desktop`, marked executable (required on Plasma 6) |
| Nemo (Cinnamon) | `~/.local/share/nemo/actions/arcade-*.nemo_action` |
| Thunar (Xfce) | entries merged into `~/.config/Thunar/uca.xml` with a stable `unique-id` prefix; only our entries are ever touched |
| Caja (MATE) | `~/.config/caja/scripts/Arcade/` |
| Windows Explorer | per-user verbs under `HKCU\Software\Classes\SystemFileAssociations\<ext>\shell\Arcade…` (a cascading "Arcade" menu; on Windows 11 under "Show more options"), plus "Send to → Arcade" shortcuts. Stage 9: a signed sparse package with `IExplorerCommand` for the top-level Windows 11 menu |
| macOS Finder | Services (`NSServices` in the Tools app bundle, calling the helper), which Finder shows under Quick Actions/Services. Stage 9: a signed Action extension for a first-class Finder entry |

Facts verified during planning (sources in section 10): Dolphin's executable-bit rule on Plasma 6; Windows 11
puts unpackaged verbs under "Show more options" and needs package identity (a sparse package) for the top level;
Finder Sync is meant for sync apps and only covers chosen folders, so it is not used. To verify while building:
whether Services work for an unsigned app bundle on current macOS (CI test in stage 2), and the Caja path.

### 4.6 Removing every hard-coded list

| Repo | Delete | Replace with |
|---|---|---|
| Link | compiled app data as the primary source (`manifest.rs:125–205`) | `catalog.json` + cards, compiled as fallback |
| Lens | the per-app `match` in `lens-actions/src/arcade.rs:282`, the `clipboard`/`look` special cases above it | `offers(…, surface "screen" / "palette")`; Lens's own actions stay |
| Find | `crates/arcade-find/src/link.rs` (look.preview, box.pipelines, box.pipeline.run) | `offers(…, "palette")` on results |
| Look | `src-tauri/src/link_consumer.rs` (box.open, box.pipelines, clipboard.add, lens.analyze, wheel.add_action, shelf.add) | `offers` |
| Shelf | `src/link/PeerHub.cpp`, `src/Controller.cpp` (clipboard.add, box.pipelines, box.pipeline.run, wheel.add_action) | Qt `offers` |
| Wheel | `src/providers/ArcadeLinkProvider.cpp`, `src/core/WheelController.cpp` (box.pipelines, look.preview_selection, lens.capture) | Qt `offers`; Wheel's "add any action" lists every offer with `surfaces` containing `palette` |
| Clipboard | `core/rust/src/link_consumer.rs` (look.preview, lens.*, shelf.add) | `offers` |
| Box | `apps/desktop/src-tauri/src/link.rs`, `screen_capture.rs`, `clipboard_history.rs` peer calls | `offers`; Box's own tools stay |
| Tools | tray glyph list (`tray/assets.rs`), any per-app branches found during the stage | card `icon`, `catalog.json` |

`tools.install` calls stay (Tools is the one installer by design), but go through one Link helper function.

### 4.7 The browser extension (new repo `qa-p1/Arcade-browser`)

One codebase, two builds: Manifest V3 for the Chromium family and for Firefox (Firefox MV3 runs a background script
instead of a service worker; the build handles the difference). TypeScript, no framework, the design kit's tokens.

**Surfaces (every item is an offer from the helper; the extension knows no app's actions):**

- **Right-click menus:** on an image, a link, a video or audio element, selected text, the page, and a PDF. Grouped
  as the offers say ("Arcade ▸ Convert ▸ …"), defaults first, with "More…" opening the popup.
- **On-page buttons:**
  - **Under every YouTube video, a Download button** with the full form from Box's downloader card, remembering the
    last choice; also Transcript, Thumbnail and Audio only as offers on `browser-video`. The same button on other
    sites the downloader supports, where the page has a video element.
  - **On images, a small hover button** (setting, on by default) with the image offers (save, remove background,
    upscale, read text, scan QR, palette, send to phone, keep on Shelf…).
  - Button placement per site (CSS selectors) is **data** in `catalog.json` (`browser.sites`), so a YouTube layout
    change is fixed by editing this repo, not by releasing the extension. Selectors are data, not code (MV3 forbids
    remote code; selectors are allowed).
- **The toolbar popup: the Island in the browser.** Search every action of every installed app (including actions
  with no input: calculator, units, currency, time zones, password, QR from the page URL, IP, WHOIS for this site,
  site check), each drawn with its options form from data. Recent jobs and their progress.
- **Selected text, live:** when the selection looks like an amount, a quantity, a time or a date, the menu title shows
  the result ("12 USD ≈ ₹1,002", "5 mi = 8.05 km") from Box's converters, within a 150 ms budget, otherwise a
  plain entry.
- **Finished downloads:** a notification "Downloaded report.pdf · Compress · OCR · Open in Look", from the offers for
  that file (setting, on by default).
- **Send to phone:** on links, images, selections and the page URL, listing the user's devices from Clipboard
  (`clipboard.devices`), within Clipboard's limits.
- **Not connected:** "Install Arcade Tools to connect" with a link; a missing app shows "Install Arcade X".

**Distribution:** each extension release attaches `Arcade-browser-chromium-<v>.zip` (with a fixed `key` so the ID is
the same wherever it's unpacked) and `Arcade-browser-firefox-<v>.xpi` (signed unlisted through `web-ext sign` in the
release workflow with the owner's AMO API key). Tools' **Everywhere** page shows the steps, opens the right page in
the right browser, and shows "Connected" once the extension pings the helper.

**Host files the helper writes** (per user): Chromium family on Linux `~/.config/<browser>/NativeMessagingHosts/`
(google-chrome, chromium, microsoft-edge, BraveSoftware/Brave-Browser, vivaldi, opera), macOS
`~/Library/Application Support/<browser>/NativeMessagingHosts/`, Windows `HKCU\Software\<vendor>\<browser>\NativeMessagingHosts\dev.arcade.helper`;
Firefox family on Linux `~/.mozilla/native-messaging-hosts/` plus the forks' own folders, macOS
`~/Library/Application Support/Mozilla/NativeMessagingHosts/`, Windows `HKCU\Software\Mozilla\NativeMessagingHosts\…`.
**Zen's folder is not documented:** `LOCAL-PROMPTS.md` prompt B finds it on the owner's Zen before stage 5.

### 4.8 What each app brings (so the result is everything the apps can do, not "convert and download")

The cards decide; this is what they will say after this plan, and what the owner should see.

- **Box (109 tools + pipelines):**
  - *Files (file menu):* every Image, PDF, Video, Audio, Text & Data, QR and Files tool on matching files, e.g.
    convert/resize/compress/crop images, remove background, upscale, passport photo, redact, strip metadata,
    watermark, favicon, palette, compare; merge/split/organize/compress/sign/fill/protect/unlock/watermark/OCR PDFs,
    PDF ↔ images, documents to PDF, extract PDF content; video compress to a size, trim, crop, join, GIF, frames,
    extract audio, subtitles, auto-subtitles, inspect; audio convert/trim/join/normalize/denoise/vocals/speed/
    silence/metadata/transcribe; batch rename, duplicates, compare, folder sizes, encrypt; Excel ↔ CSV, CSV
    workbench, JSON/YAML/TOML/XML, Markdown export; hash, encoding; QR/barcode decode.
  - *Browser:* media download (video, audio, formats, subtitles), transcript, thumbnail, all images on the page,
    direct file download, page to PDF or screenshot, page to text/Markdown, site check, WHOIS, QR for the page;
    image tools on any web image (downloaded to a handoff file first); text tools on selections (clean, case,
    statistics, diff, JSON format, JWT, regex, hash, encode/decode, URL inspect, text to speech, QR); live
    converters (calculator, units, currency, time zones, dates, colour).
  - *Palette (popup, Island, Wheel, Find):* everything, including the no-input tools (password, UUID, lorem,
    timer, random, emoji, IP, system info) and saved pipelines.
  - *Screen tools* stay on Box's own shortcuts and the Island (they need a live picker), and are listed in the popup
    as "Open in Box".
- **Lens (26 recognizers, 156 actions):** "Read text", "Scan QR/barcode", "Pick colours", "Find links, emails,
  phone numbers, dates, addresses" and the rest on images (file menu, web images) and on screen regions; its chains;
  "Pin on screen". Lens publishes its action catalog the way Box publishes its tools (generated from its registry,
  with options and ranks).
- **Look:** Preview any file, folder or link (file menu "Preview in Look", browser links); Inspect (file info).
- **Find:** "Search my files for this" on selected text; "Reveal in Find" on files.
- **Shelf:** "Keep on Shelf" for files, folders, links, images, text, the page.
- **Clipboard:** "Copy to Arcade Clipboard" and "Send to phone ▸ <device>" (within limits).
- **Wheel:** "Add to Wheel" for any action, link or file (every offer can become a Wheel slot).
- **Tools:** "Install Arcade X", engine install hints ("Install FFmpeg").

## 5. How it is tested (so no week of local testing)

Every stage adds automated tests that fail before the change and run in CI on every PR and in Gates on every rc:

1. **Link conformance vectors** for the new card fields, types and `offers` (Rust and Qt run the same vectors; one
   vector per rule in 4.3).
2. **Link real-fleet e2e** (`tools/e2e.py`) gains the helper: start the real helper with real app packages in an
   isolated home, ask it for offers for sample files, URLs and selections, run one action per app, check outputs.
3. **File manager tests (Linux CI, Ubuntu 24.04):** install Nautilus, Dolphin, Nemo, Thunar and Caja; run the
   helper's integration writer; validate every file (`desktop-file-validate`, Thunar's XML, Dolphin executable bit);
   run each entry's command on sample files and check the output. Plus an X11 harness test that really right-clicks
   in Nautilus and Dolphin (xdotool, like the real-user desktop) and runs one action.
4. **Windows CI:** the helper writes the verbs and Send to entries; a test invokes each verb on a sample file through
   the shell (`ShellExecuteEx` with the verb) and checks the output; uninstall leaves no key.
5. **macOS CI:** Services registered (`/System/Library/CoreServices/pbs -update`), a test performs the service on a
   sample file (`NSPerformService`) and checks the output.
6. **Browser tests:**
   - Chromium: Playwright with the unpacked extension (`--load-extension`, headed under Xvfb), the real helper and
     real apps. Menus are tested through the extension's own handlers (browser menus can't be clicked by Playwright);
     the YouTube button against a local copy of a YouTube-like page (CI runners get "confirm you're not a bot"
     from YouTube, so live YouTube is checked only in the owner's local run); downloads against a local file server.
   - Firefox: Selenium with geckodriver, the add-on installed as temporary (allowed in test profiles), same
     scenarios.
   - Native messaging end to end with the real host files the helper writes.
7. **Gates** on every rc keep their current jobs (published files, budgets, N-1, conformance, upgrade, delta,
   Windows/macOS installer smoke, Tier 1/Tier 2 desktops) and add the helper and integration checks above.
8. **Real-user run (stage 8)** on the Linux test desktop, as in `dev/v1/REAL-USER-RUN.md`, now with Chromium and
   Firefox and the extension, Nautilus and Dolphin. Windows and macOS: prompts C and D on the owner's PCs, once,
   at the end.

## 6. Stages

Rules from v1 still apply (`dev/v1/HANDOFF.md`): every app release goes rc → Gates (every job green) → Promote →
byte-for-byte check; merge only when every check on the PR head is green; at most 3 apps in flight; at most one
re-run per job and never to hide a failure; no Co-Authored-By, session links or footers; push only to
`claude/sharp-cori-29w5eg`; plain-language reports.

### Stage 0: owner chores (moved: handed over at stage 5)

`LOCAL-PROMPTS.md` prompt A: delete the 12 wip branches; add the note to Lens v0.4.1/v0.4.2; create the empty repo
`qa-p1/Arcade-browser`; create the free Mozilla developer account and put its API key into that repo's secrets
(`AMO_JWT_ISSUER`, `AMO_JWT_SECRET`). Prompt B: Zen's native messaging folder. The owner's instruction: when the
cloud session reaches stage 5 it writes one takeover prompt (A, B, the remaining stages, C and D, everything) and the
owner's local session continues the whole plan from there. Nothing before stage 5 needs the owner's computer.

### Stage 1: Link 1.1.0

1. `url` 2.5.9 (RUSTSEC-2026-0592) in the app template (Link's own crates don't use `url`).
2. Card fields and types (4.1), SPEC sections 3, 5 and 11 updated, vectors added.
3. App data from `catalog.json` with compiled fallback (4.2); `catalog.schema.json` and `scripts/validate.py` in
   this repo gain `pairs`, `rules`, `browser.sites`; Tools' snapshot updated in stage 2.
4. `offers` in Rust and Qt with shared vectors (4.3); `offers.json` prefs read and written through Link.
5. `crates/arcade-helper` (4.4): native messaging host, `menu`/`run`/`picker`, integration writers for every row of
   4.5, progress window, job runner, watcher. Built and tested here; shipped by Tools in stage 2.
6. A one-function `request_install(app)` replacing per-app `tools.install` code.
7. e2e and file-manager tests (5.2, 5.3); Windows/macOS helper tests (5.4, 5.5).
8. Dependabot sweep for Link (#33–#43, #69): merge what is green and safe; for majors needing code (ed25519-dalek 3,
   sha2 0.11, blake2 0.11, base64 0.23, egui 0.37, actions v7/v8) do the change in this stage or close with the reason
   written in the PR. Same rule in every stage below. Done in Link #82 except egui: Find and Lens draw with Link's
   egui design kit, so egui 0.37 moves to stage 4/6 with them.
9. Release through Link's flow (PR → post-merge CI + e2e + desktop harness → tag v1.1.0).

### Stage 2: Tools 1.1.0

1. Link 1.1.0; ship `arcade-helper` in every package; install, update, start at login, uninstall (removes every
   integration it wrote).
2. The **Everywhere** page: helper status, file-manager integrations found and installed, pinned actions, output
   folders, defaults for "same job" pairs, browser setup steps with "Connected" status.
3. Write the shared `catalog.json` copy; tray glyphs from cards.
4. macOS: `NSServices` entries in the Tools bundle calling the helper (CI test 5.5).
5. Leftovers: Look's card says "Not running" for a few seconds after login while Look starts (show "Starting…" while
   its process exists and the endpoint isn't up yet); the tray edge (still checked only by the pixel test: add a
   Tier 2 KDE/xfce panel screenshot check that sees the icon).
6. Dependabot sweep (#24–#38, #52, #61, #62).
7. rc → Gates (plus helper, integration and browser host checks) → Promote.

### Stage 3: Box 1.0.0

1. Start from `claude/sharp-cori-29w5eg` (rc.7 + 33f133d, the upgrade test on 24.04).
2. Link 1.1.0, `url` 2.5.9.
3. Full cards: every tool with `options` from its catalog form, exact types (no more squeezing; `file/subtitle` etc.),
   `surfaces`, `rank` (all 109 tools, not 10), `oneClick`, `requires` from its providers, `output`; presets as
   separate actions as today; pipelines as actions with their own forms.
4. The Island and Box's peer calls use `offers`; Box's hard-coded peer list removed.
5. The downloader card's form matches the YouTube button's needs (media, quality, formats, subtitles, thumbnail,
   metadata, name, folder) and reports progress per file.
6. Leftovers from v1: verify every open item in Box `docs/v1/SPEC.md` "Findings to fix" and `DECISIONS.md` is fixed
   or moved to a backlog with a reason; refresh `docs/STATUS.md` (it stops at 0.4.3) and `docs/v1/PROGRESS.md` (it
   stops at rc.4).
7. Dependabot sweep (#21–#42: resvg 0.50, similar 3, wasmtime-wasi 38, rand 0.10, typescript 7, screencapturekit 11,
   npm group, actions).
8. rc.8 → Gates (all jobs) → Promote 1.0.0. Real-fleet e2e with the helper on the promoted files.

### Stage 4: Lens 1.1.0 (before the extension, so its actions are there)

1. Link 1.1.0; publish Lens's action catalog with options, types and ranks (4.8); `lens.recognize` gains image and
   text inputs for every recognizer; remove the hard-coded list.
2. Backlog: LN-10 (loupe label colour, needs a reproducible test first), RD-LENS-4 (pin menu clipped: give pin menus
   a separate popup surface), SEC-1 (plugins with `read-text` get secret findings: filter secrets unless the plugin
   is granted `read-secrets` explicitly), SEC-2 (files written with umask: write with 0600/0700).
3. Dependabot sweep (#29–#35: eframe 0.36, global-hotkey 0.10, toml 1, tiny-skia 0.12, x11rb 0.14, toolchain).
4. rc → Gates → Promote.

### Stage 5: the browser extension 1.0.0

1. Repo `Arcade-browser` (owner creates it with prompt A at the start of this stage): build for Chromium and Firefox, surfaces in 4.7, tests in 5.6,
   release workflow attaching the zip and the signed `.xpi`.
2. `catalog.json` `browser.sites` for YouTube and the other downloader sites; the image hover rules.
3. Zen's host folder (from prompt B) added to the helper's writer, with a Link patch release if needed.
4. Release 1.0.0 after its CI, the e2e with the released helper and Box, and a check that the `.xpi` is signed.

### Stage 6: the other apps (at most 3 in flight; each: Link 1.1.0, `offers`, delete its list, Dependabot sweep, rc → Gates → Promote)

- **Clipboard 1.1.0:** also `url` 2.5.9; "Send to phone" card with `maxBytes` (16 MiB) and text limit (32 KiB);
  Dependabot #25–#27 proven in this rc (they change the gates/release workflows), #23/#24 (Flutter pub, flutter_lints
  6), #29–#31, #33 (cargo group, chacha20poly1305 0.11, base64 0.23, x25519-dalek 3: the crypto majors need code and
  a sync compatibility test with 1.0.0 peers, since devices pair across versions).
- **Look 1.1.0:** also `url` 2.5.9; "Preview in Look" and "Inspect" with surfaces for links and files; Dependabot
  #26–#35 (zbus 6, lofty 0.25, lzma-rust2 0.25, quick-xml 0.42, cargo and npm groups, actions).
- **Wheel 1.1.0:** Qt `offers`; "Add to Wheel" accepts any offer; Dependabot #20, #22.
- **Find 1.1.0:** offers on results and "Search my files for this"; Dependabot #23–#30 (cosmic-text 0.17,
  accesskit_unix 0.24, x11rb 0.14, smithay-client-toolkit 0.20, cargo group, actions). Leftover: the one unexplained
  main CI failure ("0.4.3 did not load pins/history"): run the upgrade test 20 times in one CI job; if it fails
  again, find the cause before release.
- **Shelf 1.1.0:** Qt `offers`; "Keep on Shelf" for every type; Dependabot #17–#21. Leftovers from its STATUS:
  native drag out, Windows/macOS adapters and large-collection performance get tests or are recorded in a backlog
  with reasons; STATUS.md refreshed (it stops at 2026-11-01).

### Stage 7: catalog and docs

`catalog.json` final data (apps, pairs, rules, sites); each app's README "Use it from anywhere" section; Tools' Learn
guide "Arcade everywhere"; `docs/` user pages for the extension install (Chrome and Firefox/Zen, with pictures);
STATUS files of every repo brought up to date (most stop in early November). Merge this repo's open draft #9 or
close it (owner's call; it's the owner's October report).

### Stage 8: real-user run and fixes

Linux test desktop as in v1, with Chromium and Firefox, the extension, Nautilus and Dolphin: install Tools, set up
the extension, then use every surface of 4.7 and 4.5 on real files and real sites, and every app's offers. Fix what
breaks with tests that fail first; re-release the affected app. Then prompts C (Windows) and D (macOS) on the owner's
PCs; fix what they report the same way. Final report in `dev/everywhere/REAL-USER-RUN.md`, `dev/v1/HANDOFF.md`
superseded by `dev/everywhere/HANDOFF.md`.

### Stage 9 (when the owner has certificates)

Windows: a signed sparse package with `IExplorerCommand` for the top-level Windows 11 menu, and signed installers.
macOS: Developer ID signing and notarization, a Finder Action extension. Not needed for anything above to work.

## 7. Every v1 leftover, and where it is done

| Leftover | Stage |
|---|---|
| Delete 12 wip branches; Lens 0.4.1/0.4.2 note | 0 (prompt A) |
| Box rc.7 Gates failure (upgrade test on 22.04) | 3 (33f133d, rc.8) |
| Box on Link 1.0.13 | 3 |
| RUSTSEC-2026-0592 `url` 2.5.8: Link's template, Box, Clipboard, Look | 1, 3, 6, 6 |
| Clipboard, Look, Wheel on older Link | 6 |
| All open Dependabot PRs (~85 across 9 repos) | each repo's stage |
| Clipboard #25–#27 need an rc to prove; #23/#24/#29–#31/#33 failing | 6 |
| Find's unexplained main CI failure | 6 |
| Look "Not running" while starting after login | 2 |
| Tray edge checked only by a pixel test | 2 |
| Item 15 (an app restarted by itself keeps its start environment): not changed, by decision | recorded in `dev/v1/REAL-USER-RUN.md`; no work |
| Lens backlog LN-10, RD-LENS-4, SEC-1, SEC-2 | 4 |
| Shelf STATUS "not interactively verified" and "remaining" items | 6 (tests or backlog with reasons), 8 (real-user) |
| Box SPEC/DECISIONS open items; stale STATUS/PROGRESS docs | 3, 7 |
| Look's Windows Explorer hook never run on a real Windows | 8 (prompt C) |
| Windows and macOS never had a real-user run | 8 (prompts C, D) |
| Catalog draft PR #9 (owner's October report) | 7 (owner's call) |

## 8. Risks and how the plan handles them

- **File manager formats change** (Dolphin's executable bit on Plasma 6 is one example): the CI file-manager tests
  run against current packages in every Gates run, and "Open With" entries work everywhere as a floor.
- **YouTube changes its page:** the button's placement is data in `catalog.json`; the download itself is yt-dlp in
  Box, updated as an engine.
- **Unsigned Windows/macOS:** Windows SmartScreen and macOS Gatekeeper warn on first run as they do today; the menus
  use mechanisms that don't need signing; stage 9 removes the warnings.
- **Firefox signing:** Mozilla's automatic review can delay an unlisted signature; the release workflow waits for it
  and fails clearly if it's refused. Nothing changes for Chrome.
- **A slow helper makes menus feel slow:** offers are computed from cached cards (no IPC when a menu opens, SPEC §1),
  with a 50 ms budget measured in the e2e.
- **Too many entries:** grouping, defaults first, pinned actions, and "More…" keep menus short; the full list lives
  in the picker and the popup.

## 9. Open items to settle while building (not blocking the start)

- Zen's native messaging folder (prompt B).
- Whether macOS Services work from an unsigned app bundle on the current macOS (stage 2 CI test decides; fallback:
  "Open With" + Finder toolbar script).
- Caja's scripts path on current MATE (stage 1 CI test decides).

## 10. Sources for the platform facts

- Firefox/Zen signing: [Add-on signing in Firefox](https://support.mozilla.org/kb/add-on-signing-in-firefox),
  [Signing and distribution](https://extensionworkshop.com/documentation/publish/signing-and-distribution-overview/),
  [Zen discussion on unsigned add-ons](https://github.com/zen-browser/desktop/discussions/8961).
- Native messaging: [Chrome](https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging),
  [MDN native manifests](https://developer.mozilla.org/en-US/Add-ons/WebExtensions/Native_manifests).
- Windows menus: [Integrate with File Explorer (sparse packages)](https://learn.microsoft.com/en-my/WINDOWS/APPS/desktop/modernize/integrate-packaged-app-with-file-explorer),
  [Extending the Windows 11 context menu](https://blogs.windows.com/windowsdeveloper/2021/07/19/extending-the-context-menu-and-share-dialog-in-windows-11/).
- macOS: [Finder Sync](https://developer.apple.com/library/mac/documentation/General/Conceptual/ExtensibilityPG/Finder.html),
  [Finder Sync is for sync apps (Apple DTS)](https://developer.apple.com/forums/thread/766680).
- Linux: [Dolphin service menus](https://develop.kde.org/docs/apps/dolphin/service-menus/),
  [Arch wiki: Dolphin](https://wiki.archlinux.org/title/Dolphin), [Thunar custom actions](https://docs.xfce.org/xfce/thunar/custom-actions).

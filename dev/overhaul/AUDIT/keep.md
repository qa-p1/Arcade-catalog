# Features and behaviour to preserve

Owner instruction, 2026-10-28: shared standards may change the appearance and behaviour of shared controls, but must preserve useful app-specific capabilities. This is a preservation inventory, not a claim that every item passed this audit. Functional verification belongs in the coverage tables. If an item is broken, repair it rather than deleting it to achieve consistency.

## Tools — Keep

- The owner's preferred 0.3.8 visual direction: restrained surfaces, clear hierarchy, readable spacing, light/dark palettes, consistent sidebar and task-focused pages. Parent screenshots `screens/tools/2009-parent-settings-light.png`, `2010-parent-settings-dark.png`, `2020-parent-home-default-dark.png` and `2064-parent-learn-default-light.png` show the released UI. Source: `src-ui/style.css:3`, `components/Sidebar.svelte:14`.
- Tools remains optional. Keep individual app installation/adoption, update/repair, retained rollback, data-preserving removal, channel and per-app update choices, protocol compatibility holds and explicit review of operations. Source: `src-ui/lib/api.ts:9`, `tabs/Updates.svelte:50`, `docs/STATUS.md:44` onward.
- Preserve unified tray hosting with immediate hand-back and per-app exclusions, the native shortcut sheet and conflict/rebind tools, offline Learn reader and deep links, engine explanations, redacted diagnostics, and portable settings backup/restore. Closing the hub window should keep only required resident services, with the webview released. Sources: `tabs/{Shortcuts,Learn,Settings}.svelte`, `components/TraySettings.svelte`, `docs/STATUS.md:51` onward.

## Box — Keep

- Keep both the compact Island quick panel and full dashboard, contextual tool search, favorites/aliases/history, keyboard-first activation and the packaged `arcade-box` / `arcadebox` CLI. Shared controls must not turn a quick action into a multi-page flow. Sources: `README.md:20,33`, `docs/STATUS.md:55` onward, `apps/desktop/frontend/src/App.svelte`.
- Preserve all 109 tool contracts, typed parameter forms, independently usable core/CLI, progress/cancellation, result actions and engine availability guidance. Preserve precise numerical results even when a friendlier display is added. Source: `docs/tool-catalog.md`, `catalog/`, `crates/arcade-core/`, `docs/STATUS.md:58` onward.
- Keep typed DAG pipelines, saved presets, peer stages and effect approval; sandboxed WASM plugins and the separate worker; local optional engines shared through Link; per-app connection choices. Sources: `docs/{pipeline-model,plugin-model,providers,arcade-link}.md`. The stale UI branch and uncommitted calculator/units work are owner work to preserve for review, not cleanup debris.

## Look — Keep

- Preserve Look's **frameless draggable title bar** and lightweight quick-preview identity. Source: `src/app.ts:126`, `src-tauri/src/app.rs:362` (`decorations(false)`), `src/styles/app.css:162`. A shared title-bar style must retain drag, close, navigation and file actions.
- Keep rich format-specific viewers: image zoom/rotation/metadata, PDF pages and text, audio waveform, video controls, code line numbers/wrapping/text size, Markdown, collapsible JSON, sandboxed HTML, archive/directory and fallback info/hex views. Source: `README.md:39` onward, `src/viewers/`. These viewers should not be flattened to one generic text panel.
- Preserve file-manager preview integration, actions strip, keyboard navigation, plugins, the graceful unsupported-format fallback and idle webview release while Link stays available. Sources: `src/lib/actions-strip.ts`, `README.md:149`, `docs/STATUS.md:25` onward.

## Find — Keep

- Preserve both the layer-shell overlay and the **opaque desktop fallback** for desktops without it. The fallback deliberately composites onto its own background for readability; transparency is not an obligatory standard. Source: `crates/arcade-find/src/ui/desktop.rs:207`, `ui/wayland.rs:61`.
- Keep fast incremental local indexing/search, search-as-you-type, filters, locations/exclusions, recents/pins on an empty query and keyboard selection/actions. Sources: `README.md:39` onward, `crates/find-core/`, `crates/arcade-find/src/ui/`.
- Preserve preview/open/reveal, safe rename, confirmed Trash, copy/paste and drag of real files, and Shelf/Look/Lens/Clipboard handoffs. Portable backups intentionally exclude the index, history and machine-specific integration choices. Source: `README.md:45,133`.

## Lens — Keep

- Preserve **freeze-first capture**, region/window selection where supported, multi-monitor capture and the ranked progressive palette. Recognition is local and several findings can coexist. Source: `README.md:41` onward, `crates/lens-core/src/palette.rs`.
- Preserve **annotation including pixelation, floating pins with zoom/opacity/live refresh where supported, and measure mode**. They are distinct useful workflows, not inconsistent variants of the same dialog. Source: `crates/arcade-lens/src/gui/annotate.rs:69,85,326`, `gui/pins.rs:17,86`, `gui/measure.rs:20`.
- Keep keyboard selection/resizing/action keys, recognizer/action preferences, chains and opt-in plugins; outbound content explanations, secret filtering and command confirmations; OCR engine/language choices and graceful platform capability limits. Sources: `README.md:45,75`, `docs/{PLUGINS,ARCADE_LINK}.md`.

## Shelf — Keep

- Preserve the compact capsule, expanded collection, **dock/edge-tab modes and hover peek**, native placement/resize and the **backdrop** adapters with readable fallback surfaces. Source: `ui/Main.qml:17,23,39,43,169,300,712`. Shared settings chrome must not replace the Shelf's desktop surface with a conventional fixed window.
- Keep Quick Shelf and named/pinned/reorderable collections, references to originals, explicit owned copies for temporary data, undo, duplicate suppression, multi-selection/filter, drag/copy/open/reveal and safe removal that never deletes an original. Source: `README.md:40` onward.
- Preserve quotas, retention, lazy thumbnail workers/cache bounds, picker-only selected-content return, effect confirmations and the distinction between full Shelf backup and Tools metadata/preferences-only backup. Source: `README.md:64,111,113`.

## Wheel — Keep

- Preserve hold → flick → release, center cancellation, whole-slice targets, multiple decks, scrolling between decks and single/double/triple/long-press center gesture groups. This geometry and interaction are the product, not shared-control inconsistency. Source: `README.md:15,43` onward.
- Preserve **geometry settings and live preview**: wheel radius, center radius, slice gap, labels/icons, animation choices and cancel dead zone. Source: `qml/settings/Settings.qml:480,482,484,525`.
- Keep application focus/launch, commands, URLs/files/folders, supported system/media/compositor actions, peer actions, input resolvers and Activity/cancellation. Missing peers retain saved slots with a reason. Keep explicit confirmation before adding an offered action to a chosen slot, and atomic versioned JSON import/export. Source: `README.md:47` onward, `qml/settings/{ActionPicker,LinkActivity}.qml`.

## Clipboard — Keep

- Preserve encrypted local history and peer-to-peer device sync without an account; QR plus six-digit verification, owner-approved membership, offline catch-up and optional non-storing relay. Source: `README.md:17,45` onward, `docs/{protocol,security}.md`.
- Keep deduplication, pins/search, rich text/images/files, keyboard picker and focus-return paste where supported. Received clips must stay in history until explicitly chosen, instead of replacing the clipboard automatically. Source: `README.md:47` onward.
- Preserve **Private mode**, sensitive-source exclusions and denial of outbound clip content while paused; a peer picker returns only selected content, never full history. Backups must continue excluding history, identity keys and devices. Source: `README.md:50,70,119`, `apps/flutter_app/lib/services/link_service.dart:94`, `platform/desktop_adapter.dart:117`.
- Preserve the useful mobile share/keyboard surfaces even though physical-device validation is outstanding. Their platform-specific background constraints must remain visible rather than claiming desktop equivalence. Source: `README.md:52,131` onward.

## Link — Keep

- Preserve independent apps plus optional Tools: local file-based discovery and one socket per resident app, no mandatory central daemon or hub. Source: `README.md:3`.
- Keep capability/effect negotiation, master/per-peer opt-outs, optional-method compatibility, asynchronous cancellation/progress, private bounded handoffs, receipts/ownership rules and tray hand-back/restart grace. Source: `SPEC.md`, `crates/arcade-link/src/`, `qt/`.
- Preserve Rust/Qt conformance vectors, immutable provenance pins and the isolated real-fleet/mock harnesses. Their current coverage gaps require honest reporting and stronger output verification, not removal of the harness. Sources: `spec/vectors/`, `tools/{e2e,stress,leak,real_bench}.py`.

## Catalog — Keep

- Preserve one public data source with seven app entries plus optional Tools, bundles, optional engines, icons and third-party shortcut sheets; machine-readable schemas and standard-library-only validation. Source: `README.md:3,12` onward.
- Preserve honest per-platform `verified` / `ci` / `build-only` / `unsupported` distinctions, canonical shortcut notation, offline-readable ecosystem guides and data/code licensing/provenance separation. Source: `README.md:29,39,55`.
- Keep dated research/QA history as evidence, clearly separated from current status. Retiring a branch or old note must not discard unique owner work or the regression scenarios that exposed past defects.

## Cross-app — Keep

- Preserve context-sensitive actions and end-to-end journeys: Look actions strip, Add to Shelf from real results, Lens analysis/pins, Find preview/search, Clipboard Send to my devices, and confirmed Add to Wheel. Shared UI must keep the original app's focused task and explain side effects.
- Keep standalone operation, useful capability fallbacks, private data boundaries, opt-outs, portable settings allowlists and ownership-preserving install/adoption/rollback. A common standard should make shared controls predictable while retaining each app's capabilities.

All source paths above are relative to the corresponding scratch `src/<repo>/` snapshot. Screenshots are under the audit root. Runtime coverage is reported separately; preservation is not a PASS label.

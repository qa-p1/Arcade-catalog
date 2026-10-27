# Source and project hygiene review (parent-owned)

Snapshot: fresh `origin/main` clones, 2026-10-27 UTC. No product source was edited. Formatting, static analysis, dependency preparation and integrity checks ran only in the scratch clones. Flutter's SDK was copied with copy-on-write into the audit tree before invocation; the installed SDK was not modified. All compiler executions shared `state/build.lock`.

`PROBABLY SAFE` means text/build/CI evidence supports cleanup but no deletion experiment was performed. `NEEDS OWNER CHECK` includes public APIs, platform callbacks, intended baselines and vendored contracts. A single mention is **not** evidence that a trait implementation, externally consumed API, dynamically named asset or test-discovered function is dead.

The complete tracked-file/size/duplicate/marker inventory is in `reports/evidence/<repo>-source-inventory.json`. Raw static candidates (including conservative false positives) are in `reports/evidence/hygiene-candidates.csv` and per-repo candidate JSON. Keep those inventories as research evidence, not an automated deletion list. No compiled target/, node_modules/, dist/ or temporary .bak/.orig/.rej trees were tracked in the ten main snapshots. `Tools/src-tauri/build/tray_assets.rs` is intentional build-script source, not generated build output.

## Tools — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| `src-ui/tokens.css:3`–`:22`, repeated theme definitions at `:27` and `:37` | PROBABLY SAFE | 18 distinct custom properties have no `var(...)` consumers (24 definitions). New `src-ui/style.css` defines its own live palette. `rg` across tracked source/config found no consumer; preserve any shared-token export contract before removing. |
| `src-ui/tokens.json:1` | PROBABLY SAFE | No literal filename reference/import in tracked code, config, CI or docs. It also lacks current Link's Shelf/Find accents. Treat it as an old copied design reference unless the owner wants it kept as documentation. |
| `crates/arcade-shortcuts/tests/fixtures/catalog/` versus `src-tauri/resources/catalog/shortcuts/` | NEEDS OWNER CHECK | 31 matching content groups are intentional deterministic fixtures plus an offline catalog snapshot. Both roles are referenced. Consolidation must preserve offline Learn/shortcuts and deterministic tests; do not delete either tree as junk. |
| `tests/find_artifact.rs:45` | NEEDS OWNER CHECK | Real Find package test remains ignored; neither Tools CI nor the shared workflow names this test or enables `--ignored`. It covers real package cache/rollback behavior absent from a pure mock. Preserve and decide how to run it. |
| `tests/lifecycle.rs:15`, `tests/hub_lifecycle.rs:26`, `tests/link_lifecycle.rs:56`, `tests/maintenance.rs:58`, `tests/find_artifact.rs:48,61` | NEEDS OWNER CHECK | Isolation checks hard-code `/tmp/` instead of checking the isolated root. They reject this audit's valid on-disk private profiles. This is a harness portability gap, not a product runtime failure. |
| `scripts/ui-checks/{races,ux,layout}.mjs`, `harness.mjs` | NEEDS OWNER CHECK | Useful 0.3.8 UI checks exist and are documented locally, but are not npm scripts or CI gates. They use mock API data and Chromium, so they complement rather than establish packaged WebKit correctness. |
| `.github/workflows/ci.yml:94` and Link `tools/e2e.py:122` | NEEDS OWNER CHECK | CI builds/smokes installers but uploads only overlay evidence, not `tools-installer-ubuntu-*`; the latter exists only in the tag Release workflow. The nightly fetcher filters `--branch main`, causing two real Tools hub checks to skip. Current run/log evidence is recorded separately. |
| root `LICENSE` / `COPYING` absent | NEEDS OWNER CHECK | Cargo and npm declare MIT; available full license texts are for the adapted Tauri NSIS template and catalog data, not a main project license file. |
| remote `arcade/wip-local-package-verification` | NEEDS OWNER CHECK | Only extra commit `36456d8` is explicitly titled “WIP (unreviewed, judged unfit) … kept for reference”. Do not merge this draft as a fix. Archive/retain decision belongs to owner. |

Lints: Rustfmt clean; Clippy all workspace targets clean on Rust 1.99; Svelte/TypeScript 0 warnings/errors. Vendored hashes (8 pinned sources) and shortcut JSON pass. No confidently dead private Rust functions or Svelte components were established; private dead code is covered by compiler warnings. CLI output and conditional debug/error diagnostics were not mislabeled as leftover logging.

## Box — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| `apps/desktop/frontend/src/app.css:30,39,41,42,76,81` | PROBABLY SAFE | Four distinct unused custom properties (`--quiet`, `--surface-soft`, `--accent-bright`, `--accent-wash`), six definitions; no `var(...)` use in tracked text. |
| `scripts/validate_shortcuts.py` and `tools/validate_shortcuts.py` | NEEDS OWNER CHECK | Exact SHA-256 duplicates. The documented checker uses scripts/, while both copies are checksum-pinned in `VENDORED.md`. Consolidate only with provenance/checker updates. |
| `crates/arcade-core/src/converter_tools/calculator.rs:213` | NEEDS OWNER CHECK | Implemented `log10` branch is unreachable because the lexer at `:150` stops before digits. This is unfinished reachable input handling, not a branch to delete. Parent reproduced the release failure. |
| large `apps/desktop/frontend/src/App.svelte`, `crates/arcade-core/src/pdf.rs`, `media/video.rs` | NEEDS OWNER CHECK | Roughly 149 KB / 127 KB / 117 KB respectively. They are built and referenced, not junk. Responsibility splitting is an overhaul choice; no dead-module claim is justified. |
| `scripts/smoke-mvp.py:55` | NEEDS OWNER CHECK | Still documented in README and checks independent known answers. It ignores `CARGO_TARGET_DIR` when locating its compiled CLI (`ROOT/target/debug`), so it does not work unchanged with the audit's required target directory. Its “MVP” name alone does not make it obsolete. |
| `scripts/install-local-desktop.py` | NEEDS OWNER CHECK | Referenced by `scripts/run-desktop.sh`; durable local dev installer with ownership guards. Do not remove as an unreferenced one-off and do not run it against the real profile during an audit. |
| main project GPL license text absent | NEEDS OWNER CHECK | Workspace declares `GPL-3.0-or-later`; only Tauri's upstream MIT/Apache template licenses are present. `docs/STATUS.md` already lists the missing main license text as an open release gate. |
| local `fix/ui-and-tools` and uncommitted parser edits | NEEDS OWNER CHECK | Current local UI commit is 61 main commits behind and 1 ahead. Scratch `git merge-tree` succeeds; `git apply --check` confirms the uncommitted calculator/units patch applies to main. Preserve all three pieces of work for owner review; they were not merged, edited or stashed. |

No unused dependency was established for `zxing-cpp`: it exports the actual crate name `zxingcpp` used in `barcode.rs:17`. The raw name-scan candidate is a false positive and must be retained. No unused Svelte component was established. Rustfmt and Svelte check are clean. New local Rust 1.99 Clippy promotes two `collapsible_if` diagnostics at `crates/arcade-contract/src/lib.rs:425,493` to errors; the job stops there, so it is **not** a complete downstream lint pass. The final “build failed, waiting…” line is Cargo coordination output, not a third source error or an app warning. CI pins Rust 1.88 and is green.

## Look — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| `src/viewers/media.css:120` (`--wave`) | PROBABLY SAFE | No `var(--wave)` consumer in tracked source. Review any dynamic CSS property use before removal. |
| `docs/hero.webp` and 12 `docs/screenshots/*.webp` | PROBABLY SAFE | No literal filename references in tracked source, build, CI or Markdown; the current README uses `docs/user/images/`. These are historical presentation assets, not runtime viewer assets. External GitHub links may still use them, so do not classify them as definitely dead. |
| duplicate `scripts/validate_shortcuts.py` / `tools/validate_shortcuts.py` | NEEDS OWNER CHECK | Both are pinned unchanged; update provenance/tests if consolidating. |
| `src-tauri/tests/link_consumer.rs` (9 ignores), `tests/real_shelf.rs:21` | NEEDS OWNER CHECK | Deliberate real-peer/isolated-session checks, not trivial no-op tests. Preserve; report which explicit runner actually executes each. `docs/STATUS.md:57` records an old intermittent settings-window timeout, not proof of a current flake. |
| `src-tauri/windows/README.md:26,27` | PROBABLY SAFE | Copied upstream documentation has two broken relative links after vendoring. Adapt or link upstream; do not delete the installer helpers themselves. |

`kamadak-exif` is **used** as `exif` in `src-tauri/src/imaging.rs:36,39`; retain it. Rustfmt, Clippy and TypeScript all pass; 22 vendored hashes pass. No formatter/linter config for the TypeScript frontend beyond `tsc`, and no local Rust toolchain pin; CI pins Rust 1.88 / Node 22.

## Find — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| `scripts/e2e-linux.sh:15` | NEEDS OWNER CHECK | Hard-coded `mktemp -d /tmp/af-e2e.XXXXXX` ignores `TMPDIR`; the 1M-file fixture/GUI runner must be adapted to an explicit safe root before use here. Not run unmodified. |
| `crates/arcade-find/src/ui/desktop.rs:377` and `docs/STATUS.md` | NEEDS OWNER CHECK | Winit consumes key events but has no `Ime::Commit` handling; the layer-shell text-input protocol is also documented absent. IME/RTL remain unfinished scope, not dead code. |
| 28 single-mention Rust function candidates | NEEDS OWNER CHECK | Mostly trait/window callbacks, public entry points and test-discovered functions. All-target Clippy is clean, so there is no evidence justifying removal. Full list in the candidate JSON. |
| old `arcade/ci-speed`, `arcade/tools-hub` and other merged refs | PROBABLY SAFE | Every fetched non-main remote branch is an ancestor of current main. External references/workflow refs still need checking before future branch deletion. |

No tracked output trees, duplicate content groups or confidently unused dependency/assets found. Rustfmt width is 140 (Lens/Link use 160); workspace Clippy lints are declared centrally. Rustfmt and Clippy pass; 11 vendored checksums/docs validation pass. Main README, status, changelog and dual license files are present.

## Lens — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| duplicate release/shortcut helpers and their tests under `scripts/` and `tools/` | NEEDS OWNER CHECK | Four exact duplicate pairs, all provenance-pinned; do not remove either copy without updating checks and the referenced CLI paths. |
| `crates/lens-actions/tests/arcade.rs:356,461` | NEEDS OWNER CHECK | Intentional isolated mock / real Shelf+Find tests. They are useful integration coverage, not dead tests. Record explicit runner coverage separately. |
| `crates/lens-platform/src/macos_native.rs:1`, `docs/STATUS.md` Limits | NEEDS OWNER CHECK | macOS accessibility window commands/share sheet/UI inspection remain intentionally unimplemented. Hardware/native permission validation cannot be supplied from Linux. |
| main dual license texts absent | NEEDS OWNER CHECK | Cargo declares MIT OR Apache-2.0; no LICENSE/COPYING file is tracked. Vendored license declarations are not the main license texts. |

Rustfmt and workspace/all-target Clippy pass with zero warnings; 28 vendored hashes and docs/shortcuts pass. No unused private module/dependency or unreferenced runtime asset was established. Public recognizer/action dispatch and platform cfgs must not be removed using single-mention scans.

## Shelf — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| `vendor/arcade-link/` duplicated shared schemas/vectors and `scripts` copies | NEEDS OWNER CHECK | Seven exact duplicate groups are provenance-pinned and consumed by CMake/tests/package tooling. The full Qt module is used; its Cargo workspace manifest is provenance scaffolding, not evidence Rust is needed to build Shelf. |
| `benchmarks/cloud-debug.json`, `cloud-milestone.json` | NEEDS OWNER CHECK | Both are explicitly referenced by `docs/TESTING.md:133` / STATUS as historical evidence. Preserve or archive; do not treat old debug timings as a current release regression. |
| `ui/Main.qml:921,1033,1040` | NEEDS OWNER CHECK | QML lint reports four direct width/height assignments under layouts; check actual small-window behavior before editing. |
| `tests/tst_Drag.cpp:80`, `tst_Ui.cpp:294`, platform skips | NEEDS OWNER CHECK | Skips are environmental/platform-specific. Native Wayland drag-out into Nautilus still lacks real compositor coverage, as STATUS says; keep the meaningful X11 and process tests. |
| remote `fix/hyprland-desktop` | NEEDS OWNER CHECK | Two unique historical commits remain by patch ID, although main has later comprehensive implementations. Do not merge or delete based only on age; inspect semantics with the owner. |

No checked-in `.clang-format`, `.clang-tidy` or QML lint configuration/gate. System Qt 6.11 `qmllint` on the six shipped QML files yields 290 warnings: 284 unqualified accesses, 4 layout-positioning warnings, 2 id/member shadows. C++ context-property typing is not provided, so the unqualified counts are analysis/configuration findings, not 284 reproduced user failures. Vendor hashes/upstream comparisons pass. No tracked build output. Root license and third-party notices exist.

## Wheel — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| `scripts/arcade-release.py` / `src/link/tools/arcade-release.py`; shortcut validators | NEEDS OWNER CHECK | Two exact duplicate pairs are intentional vendored helper copies and pass source/hash verification. |
| `qml/settings/ActionPicker.qml:209,248,279,456` and other layout sites | NEEDS OWNER CHECK | 12 QML layout-positioning warnings across shipped files; inspect native layouts before cleanup. |
| `qml/settings/Settings.qml:442,573`, `qml/wheel/WheelView.qml:61,96,102` | NEEDS OWNER CHECK | Five static missing-property warnings involve dynamic QObject/QQuickItem types (`active`, `overlay`, `enter`, `leave`, `settle`). Runtime evaluation is required; do not remove these calls as dead. |
| `tests/tst_ArcadeLinkProvider.cpp` conditional skips; `tst_LinuxTrigger.cpp:113`; `tst_WindowsTrigger.cpp:37,54` | NEEDS OWNER CHECK | Tests require a CLI, durable executable or OS hooks. They are not permanently no-op by source, but CI/desktop coverage must state when hooks could not be installed. |
| remote `arcade/wheel-win-layout-diag` | PROBABLY SAFE | Two commits explicitly called Scratch/not for merge (`c5d706b`, `aa122b2`); later main contains the actual cross-platform layout implementation. Preserve logs if still useful, then owner may retire the branch. |
| root `arcade-wheel` launcher | NEEDS OWNER CHECK | A live POSIX dev launcher into `build/arcade-wheel`, not a committed executable/binary. Its durable environment/RPATH comment is intentional. |

No C++ formatter/linter config or QML lint gate. Qt 6.11 lint on ten shipped QML files: 252 warnings (235 unqualified, 12 layout-positioning, 5 missing-property), zero syntax errors. All vendor comparisons and docs checks pass. A previous CI failure was missing Vulkan headers; current 0.4.5 source removes that dependency and all latest OS jobs are green, so it is not a current build finding.

## Clipboard — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| `core/rust/Cargo.toml:26` (`thiserror`) | PROBABLY SAFE | No `thiserror` identifier or Error derive using it in any tracked Rust/build/test source. No feature wiring relies on it. A future removal should still run all supported targets/FRB generation; no removal experiment was made here. |
| `services/relay/Cargo.toml:17` (`tracing-subscriber`) | PROBABLY SAFE | No `tracing_subscriber` use anywhere in tracked source; relay `main.rs` only calls `run_from_env`. Decide whether the intended fix is adding a subscriber or removing an unused dependency. |
| `apps/flutter_app/android/app/build.gradle.kts:25` | SAFE TO REMOVE | Template comment asks to choose an application ID, immediately followed by the real `dev.arcade.clipboard` ID. Removing that comment cannot affect compilation or behavior. |
| `apps/flutter_app/android/app/build.gradle.kts:41`–`:43` | NEEDS OWNER CHECK | Android release still uses debug signing, explicitly marked TODO. This is unfinished mobile release configuration, not harmless boilerplate to erase. Android/iOS are not locally exercised. |
| `apps/flutter_app/pubspec.lock:328` (`jni_flutter` 1.0.4) | NEEDS OWNER CHECK | Enforced-lockfile dependency preparation reports the version retracted and a 1.0.4+1 successor. Report only; no dependency was upgraded. Exact pub output is in the lint log. |
| `docs/STATUS.md:99` onward AppImage limits | PROBABLY SAFE | Claims self-install/uninstall are not implemented, contradicting its earlier hub section and current launcher implementation. This is obsolete text to replace after release verification, not a missing Linux implementation. |
| generated FRB Dart/Rust, plugin registrants and icons | NEEDS OWNER CHECK | Compiler/analyzer ignore headers are generator output; Dart assets are globbed in pubspec and Android uses resource names. Filename-only scans falsely suggest these are unused. Retain them. |

Rustfmt and Clippy clean, Flutter 3.47.2 / Dart 3.13.2 analysis **0 issues** after `pub get --enforce-lockfile`; all caches/SDK writes in the audit tree. Docs/8 vendored hashes pass. Rust minimum 1.88 is declared, but CI uses 1.98.1 and relay edition 2024 declares 1.85; no root toolchain pin enforces those choices for developers.

## Link — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| `tools/stress.py:70` (`files_exist`) | NEEDS OWNER CHECK | Verbatim function probe accepts `{}`, `outputs: []` and text-only wrong outputs because `all()` sees no file paths. Heavy PDF/OCR/TTS stress checks can count missing files as pass. Preserve the harness, strengthen output contracts later. |
| `tools/leak.py:24` | NEEDS OWNER CHECK | Leak workload counts exit codes only, not OCR/text correctness. Useful memory exercise, insufficient functional verification. No real-user pass is inferred from it. |
| `tools/real_bench.py` handback probe | NEEDS OWNER CHECK | `handback(s, min(args.runs, 10))` caps the advertised `--runs 20` real-fleet probe at 10, below the cloud prompt's 20-run requirement. |
| `tools/e2e.py:122`, `e2e_artifacts.py:60`, `.github/workflows/e2e.yml:127` | NEEDS OWNER CHECK | Main artifact discovery plus `--allow-skips` means green is incomplete coverage. Latest 40469636881: real install 8 pass/8 skip, tools-hub 41 pass/2 skip, shortcuts 20 pass, trayhost 27 pass; deterministic availability intentionally skips 16/16. Tools installer artifacts are in tag release runs, outside the fetcher's branch filter. |
| `crates/arcade-link/src/transport.rs:143` | NEEDS OWNER CHECK | Long runtime paths fall back to literal `/tmp/arcade-<uid>` rather than TMPDIR. The audit kept socket paths under 100 bytes. For tools/tests that promise alternate-root isolation, document/standardize this fallback. |
| `crates/arcade-link/src/engines.rs:250`; Qt Rust-interop skips | NEEDS OWNER CHECK | External engine download is intentionally ignored; Qt tests skip without ARCADE_LINK_CLI. These are prerequisites, not trivial tests. |
| main dual license texts absent; `ARCADE_ECOSYSTEM_PLAN.md:2` broken sibling-plan link | NEEDS OWNER CHECK | Declared MIT OR Apache-2.0 without full root texts. Historical plan points at an absent ARCADE_TOOLS_PLAN.md. Preserve history or link to the catalog copy explicitly. |

Rustfmt and all-target Clippy pass. No private unused dependency/module was established. Public APIs and test callback single-mention candidates must be retained. v0.3.0 is the last tag; consumers correctly pin immutable post-tag commits `3bbbc5d`/`4c75f3a`, rather than mutable branches. Publishing a new shared tag is an owner release decision, not an audit action.

## Catalog — Hygiene

| Candidate / gap | Confidence | Evidence and disposition |
| --- | --- | --- |
| `.github/workflows/ci.yml:3`–`:5` | NEEDS OWNER CHECK | Both every-branch push and pull_request trigger the same three-OS validator. PR #9 has six green checks per update, proving duplicate work. No concurrency/deduplication policy. |
| open PR #9 `qa/stress-2026-10` | NEEDS OWNER CHECK | Draft report asks “please don't merge”; head `3ef9192`. It contains important historical evidence/regression checks but findings predate many released fixes. Keep evidence; do not treat its original verdict as today's result. |
| remote/local `arcade/tools-hub` | PROBABLY SAFE | Local is 16 behind/3 ahead by graph; `git cherry` marks substantive commit `09e96b7` already patch-equivalent to main. No current feature work is established there. External references still require review before branch retirement. |
| `dev/ARCADE_ECOSYSTEM_PLAN.md:6,7` | PROBABLY SAFE | Broken relative SPEC.md/COMPLETION_REPORT.md links after copying from Link. Correct provenance/link targets in a later documentation pass. |
| `dev/HANDOFF.md` historic A–G, plans and release tables | NEEDS OWNER CHECK | Fresh handoff explicitly says A–G are history and landed on Oct 19. Provided local HANDOFF/cloud prompt are older; do not reopen already merged work from those stale files. Keep historical dates/evidence, update only active summaries. |

Validator: 0 warnings. Existing unittest suite passes (exact count in docs-vendor log). Seven app entries plus Tools metadata, 11 engines and 31 third-party shortcut sheets have actual schemas/semantic validation; no tracked build junk or duplicate group found. Data/docs and code/schema licenses are deliberately separate (CC BY 4.0 / MIT).

## Dev standardization comparison

| Repo | Layout / common developer command | Formatting / lint | Toolchain and version source | CI / release differences | Link / docs |
| --- | --- | --- | --- | --- | --- |
| Tools | root Rust core + src-tauri + src-ui; npm dev/build/typecheck; cargo workspace | rustfmt defaults; Clippy; Svelte-check + tsc; manual UI scripts | no root toolchain file; CI Rust 1.88 / Node 24; versions in root Cargo, desktop Cargo, npm, tauri config | CI three checks + separate overlay matrix; manual/tag release rebuilds LTO packages; main lacks fleet installer artifact | Rust 3bbbc5d; separate VENDORED text format; docs/STATUS, user guides, offline snapshots |
| Box | Cargo workspace + apps/cli + apps/desktop/{frontend,src-tauri}; script wrappers | rustfmt edition 2024; Clippy; npm check (Svelte) | only repo with rust-toolchain.toml (1.88); CI Node 24/Python 3.13; app versions duplicated in CLI/desktop/tauri/npm | three OS check jobs; successful main CI invokes stable/nightly release | Rust 3bbbc5d; VENDORED.md hashes; lowercase architecture/tool docs; historical Original spec |
| Look | standalone src-tauri crate + vanilla TS viewers | Rustfmt defaults; Clippy; tsc only | no local pin; CI Rust 1.88 / Node 22; npm/Cargo/tauri versions | separate reusable installer workflow; release via workflow_run of main CI | Rust 3bbbc5d; VENDORED.md; lower-case arcade-link.md |
| Find | two Rust crates, C++/Wayland wrappers in app crate | rustfmt width 140; centralized workspace Clippy | no local toolchain file; CI 1.88; workspace version | check matrix, headless e2e, package matrix, release manifest/publish jobs; manual tag helper | Rust 4c75f3a; dual license files/notices; upper-case architecture/link docs |
| Lens | six-crate Rust workspace | rustfmt width 160; Clippy all targets | no local pin; CI 1.88; workspace version | CI tests/packages/auto stable tag/nightly, portable Windows asset excluded from Tools installs | Rust 4c75f3a; VENDORED format; script/tools duplicate pins |
| Shelf | CMake C++/Qt, src + ui, integrated CTest | C++ warnings only on shelf_core; no formatter/QML lint gate | CMake project is single version source; Qt 6.8.3 CI | Build/test/package matrix in build.yml; manual tag helper; Apple universal package | full Qt bundle vendor/arcade-link with JSON provenance; upper-case docs |
| Wheel | CMake C++/Qt, src + qml + root shell launcher | no formatter/QML lint gate; CTest | CMake version; Qt 6.8.3/OS matrix; release adds +build.<run> | one build.yml-equivalent CI pipeline auto-publishes on main; macOS per architecture | Qt bundle src/link/qt with provenance + adapters; upper-case docs |
| Clipboard | Rust workspace + Flutter under apps/flutter_app + platform bridges + relay | Rustfmt defaults/Clippy; flutter_lints strict analysis with generated code excluded | manifest minimum 1.88 vs CI Rust1.98.1; Flutter3.47.2; Cargo + pubspec versions | reusable desktop CI and release packages; manual tag; separate iOS workflow; action SHAs more consistently pinned | Rust4c75f3a; generated FRB and vendored hotkey manager; lowercase docs; mobile scope |
| Link | Rust library+CLI + Qt port + Python integration harness | rustfmt width160; all-feature/individual-feature CI; Qt tests | minimum/CI1.88; no root toolchain file; workspace0.3.0 | native 3-OS CI plus scheduled Linux real fleet; tag helper; no end-user app release | canonical SPEC, vectors, assets, provenance vendor tool; STATUS + COMPLETION_REPORT |
| Catalog | JSON/docs/shortcut sheets + stdlib Python | semantic validator + unittest; no Python formatter/linter config | Python3.x CI, no runtime pin; catalog.updated date rather than app semver | duplicate push/PR validation matrix; no app packaging/release | separate schemas/licenses; active docs mixed with dated dev records |

Across all ten repos, no SPDX license identifiers appear in the first 30 lines of tracked code files (see `license-headers.json`); that is a consistency choice, not a claim that every file needs a header. License texts/provenance must stay distinct from UI branding. Branch names currently mix `arcade/*`, `claude/*`, `fix/*`, `release/*`, `qa/*`; commit subjects mix imperative prose and occasional conventional prefixes. `.gitignore` conventions vary (root-anchored output dirs, recursive patterns, Python cache exclusions), but the tracked-tree scan found no committed cache/build tree. Existing generated FRB/native platform files, compiled hostile WASM fixtures and offline docs snapshots have real consumers and are not automatic cleanup targets.

## Current warning counts

| Repo | Rustfmt | Clippy source warnings/errors | Frontend / QML / Python | Limitation |
| --- | --- | --- | --- | --- |
| Tools | clean | 0 / 0 | Svelte/TS 0 / 0 | mock UI scripts not run as browser work in this source pass |
| Box | clean | 0 / 2 promoted `collapsible_if` errors | Svelte 0 / 0 | downstream lint stops at arcade-contract; CI Rust1.88 remains green |
| Look | clean | 0 / 0 | TS0 / 0 | no ESLint/Prettier config/gate |
| Find | clean | 0 / 0 | n/a | all-target Linux analysis, OS-specific code relies on CI |
| Lens | clean | 0 / 0 | n/a | all-target Linux analysis, OS-specific code relies on CI |
| Shelf | n/a | not configured | QML290 warnings / 0 syntax errors | Qt6.11 lint vs Qt6.8 release; no generated C++ context-property types |
| Wheel | n/a | not configured | QML252 warnings / 0 syntax errors | Qt6.11 lint vs Qt6.8 release; five dynamic-type warnings need runtime review |
| Clipboard | clean | 0 / 0 | Flutter analyzer0 issues | pub lock reports retracted jni_flutter1.0.4; no upgrade performed |
| Link | clean | 0 / 0 | Python harness checks separately recorded | this local Clippy command is not the CI all-features matrix |
| Catalog | n/a | n/a | semantic validator0 warnings, existing tests pass | no Python style linter configured |

Logs: `reports/evidence/lints/`, `reports/evidence/docs-vendor/`. None of the counts above represents Windows/macOS desktop validation, and old CI failures were not silently converted to current runtime findings.

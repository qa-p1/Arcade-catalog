# Overhaul release validation — 2026-11-03

The overhaul completion pass is verified and released. This is the current
verification record; original app specs and Keep lists remain unchanged. Dates
and older status entries elsewhere describe history.

## Preserved decisions

Keep the per-app toolkits, shared Link design kit, distinct accents, immediate
settings and platform-specific features. Preserve later additions: Box's separate
dashboard and Island, the shared egui/QML controls and contrast fixes, exact date
formatting, capture focus handling, native accessibility/peer tests, current
identities and data migrations, and Tools' version-aware login entry mapping.
Remote branches and uncertain files are not deleted as cleanup.

The owner's additional requirement is automatic routine integration repair in
Tools, without clicking Fix. [Tools PR 20](https://github.com/qa-p1/Arcade-tools/pull/20)
merged after all six checks passed at `dbebbd7`.
Stable release 0.4.5 is published from merge `0ca14e9` and installed. The exact
published AppImage passes startup login preservation, repeated automatic repairs,
registry recovery and desktop-cache refresh for a customized launcher.

## Current releases

| App | Stable version | Verification in this completion pass |
|---|---|---|
| Tools | [0.4.5](https://github.com/qa-p1/Arcade-tools/releases/tag/v0.4.5) | All six PR checks and stable release pass. Every published asset and all four updater selections verified. The actual 0.3.8 helper upgrades the frozen original split legacy/current profile to 0.4.5 with matching installed hash, receipt and successful history. The published AppImage passes the automatic repair/cache gate; installed on the real profile and left resident in the background with busy=false and jobs=0. |
| Box | [0.4.1](https://github.com/qa-p1/Arcade-box/releases/tag/v0.4.1) | All three OS release/package checks passed; every published asset and all four Tools updater platform selections verified. Installed on the real profile with receipt/entries/SQLite backup; actual Hyprland Island is 740×740, floating and pinned, dashboard loads 109 tools and Calculator handoff works. The installed release also passes the real Hyprland WebView catalog → Settings → Calculator → 42 gate with isolated data. |
| Look | [0.4.1](https://github.com/qa-p1/Arcade-look/releases/tag/v0.4.1) | All seven PR checks and stable release pass; published assets/updater verified; installed version opens Settings on the real profile despite legacy/new launcher coexistence. |
| Wheel | [0.5.0](https://github.com/qa-p1/Arcade-wheel/releases/tag/v0.5.0) | Stable release passes after one Intel DMG infrastructure retry; every published asset and updater selection verified; installed on the real profile, overlay toggle/hide and portal registration work on Hyprland. |
| Find | [0.5.3](https://github.com/qa-p1/Arcade-Find/releases/tag/v0.5.3) | Existing release/main checks green; every published asset and all four updater platform selections verified. |
| Lens | [0.4.1](https://github.com/qa-p1/Arcade-lens/releases/tag/v0.4.1) | Test-only history isolation PR 14 merged; main CI green. Existing release bytes and all four updater platform selections verified. |
| Shelf | [0.4.0](https://github.com/qa-p1/Arcade-Shelf/releases/tag/v0.4.0) | Existing release/main checks green; every published asset and all four updater platform selections verified. |
| Clipboard | [0.3.1](https://github.com/qa-p1/Arcade-clipboard/releases/tag/v0.3.1) | Existing release/main checks green; every published asset and all four updater platform selections verified. |

Link's fleet discovery/Link-off profile/test race follow-up (PR 31) is merged;
main CI and ecosystem e2e are green. It changes no product version/protocol.

The updater checks use Tools' actual scheduler, release parser, platform selector,
download and SHA-256 verification against saved real GitHub release responses and
installer bytes. Only transport URLs are redirected to a local fixture server.

All eight installed Linux AppImages match the verified published SHA-256 values.
Receipt versions, CLI links and permanent launcher/login entry paths validate.
The actual Tools core reports all eight as healthy, with zero Home health issues.
Startup/config metadata is backed up before installation; no temporary path was
persisted in the user's startup environment.

## Regressions and release guards

- Tools' new installer used to move its executing AppImage out of the legacy
  cache, installing the inner ELF and triggering a checksum rollback. Installer
  and helper invocations now defer migration. The old gate exercised an extracted
  executable; the corrected real-package gate stages the actual AppImage from
  the old cache and checks that source and installed bytes match.
- Look exited on optional launcher/login migration conflicts. Conflicts are now
  logged and both entries kept. Fresh-profile and upgraded-profile Settings and
  preview checks are required against the actual AppImage.
- Box's Lua regex quoting disabled Hyprland surface rules/shortcut registration;
  the dashboard also lacked event permissions. Linux parses the exact Lua source
  and the actual AppImage must load tools, deliver Settings/tool handoffs and show
  Calculator output 42. Tests do not substitute process survival for UI success.
- Tools maintenance backs up affected integration and preserves healthy custom
  entries, disabled login and future receipt fields. It repairs repeated faults,
  restores registry metadata from the validated installed read-only manifest,
  refreshes Linux desktop caches at startup and after launcher changes,
  limits child repairs to 20 seconds and does not spin on unchanged failures.
  Release startup must read the installed Linux login choice rather than reapply
  an older tray preference; the actual package gate asserts this before faults.
  Both CI packaging and the exact published AppImage are required to pass the
  click-free repeated-deletion/registry-recovery gate before release.

## Final ecosystem acceptance

[Full real-fleet run 41629247480](https://github.com/qa-p1/Arcade-Link/actions/runs/41629247480)
passed all 13 jobs at Link `8751969`, using Tools `0ca14e9`, Box `f0a639b`, Look
`ff0d978`, Wheel `71a9eb6`, Lens `2530e00`, Find `5477f57`, Shelf `3f3d1fd` and
Clipboard `2241f11`. All seven sibling development builds passed; the install
matrix also checks development install suppression at those same commits.

| Real-fleet group | Passed | Failed | Skipped |
|---|---:|---:|---:|
| install | 16 | 0 | 0 |
| shortcuts | 20 | 0 | 0 |
| tools-hub | 42 | 0 | 0 |
| trayhost | 27 | 0 | 0 |
| **Total** | **105** | **0** | **0** |

The separate deterministic contract job passed four checks. Its availability
probe deliberately reports 16 missing-artifact skips because that job downloads
no sibling apps. The real install matrix covers those same 16 checks and passes
all of them; none of the 105 real-fleet checks is skipped or an expected failure.

Tools main CI `41624207807` and stable release `41624281115` are fully green.
Tools' local full check passed 211 Rust tests and 22 UI checks, including Clippy.
The published AppImage passes the same automatic maintenance acceptance gate
required by both PR CI and the exact release bundle. Catalog validation and all
30 validator tests pass locally; its three-OS PR checks gate this record.

Windows and macOS validation is native CI/installer validation, not a claim of
interactive owner-machine testing. Native Windows integration that requires its
setup program remains explicit; maintenance does not silently reinstall apps.

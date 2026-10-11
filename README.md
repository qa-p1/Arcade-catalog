# Arcade catalog

Arcade-catalog is the public data source for Arcade Tools, the optional app
manager. It lists Arcade apps, shared helper programs, install bundles, and
third-party shortcut sheets. It contains data and standard-library-only Python
validation tools; it does not publish releases.

Tools reads the files from the `main` branch through
`raw.githubusercontent.com`:

- [`catalog.json`](https://raw.githubusercontent.com/qa-p1/Arcade-catalog/main/catalog.json)
  lists apps, Arcade Tools itself, bundles, platform status, icons, and minimum
  Tools versions.
- [`engines.json`](https://raw.githubusercontent.com/qa-p1/Arcade-catalog/main/engines.json)
  lists optional system helpers, how to detect them, and which apps use them.
- [`shortcuts/index.json`](https://raw.githubusercontent.com/qa-p1/Arcade-catalog/main/shortcuts/index.json)
  lists the shortcut sheets generated from `shortcuts/*.json`.
- `icons/` contains app icons copied from their app repositories.
- `schema/` describes the catalog, engine list, shortcut sheets, and generated
  shortcut index using JSON Schema draft 2020-12.

## App categories

The catalog uses a small set of categories:

| Value | Title | Use |
| --- | --- | --- |
| `files` | Files and folders | Find, preview, and collect files |
| `capture` | Capture | Select and inspect part of the screen |
| `clipboard` | Clipboard | Keep clipboard history across devices |
| `launcher` | Launcher | Open apps and actions from a radial menu |
| `toolbox` | Toolbox | Run actions on files, media, text, and system tasks |

Platform status is recorded per app and operating system. `verified` means the
app was exercised on a real desktop. `ci` means it was built and tested in CI;
`build-only` means CI built it without running its tests. `unsupported` means
the app does not support that platform.

Shortcut sheets use canonical key names shared with Arcade Link. Modifiers are
written `Ctrl`, `Alt`, `Shift`, and `Super` in that order; macOS uses `Super` for
Command. See [CONTRIBUTING.md](CONTRIBUTING.md) for the notation, sheet rules,
and review checklist.

## Docs

Start with [What Arcade is](docs/index.md). The [FAQ](docs/faq.md) and
[glossary](docs/glossary.md) answer common questions; the other
[ecosystem guides](docs/index.md#learn) cover setup, connections, shortcuts,
privacy, the tray, and uninstalling.

## Licensing

The Python scripts, JSON Schemas, tests, and their fixtures are MIT licensed in
[`LICENSE`](LICENSE). Catalog and engine data, shortcut sheets, and repository
documentation are licensed under CC BY 4.0; the full legal text is in
[`LICENSE-CC-BY-4.0`](LICENSE-CC-BY-4.0). See the
[Creative Commons license page](https://creativecommons.org/licenses/by/4.0/).
App icons are reproduced from the corresponding app repositories listed in the
catalog.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to add an app, engine, or shortcut sheet
and to run the checks locally.

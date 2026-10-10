# Contributing

Make changes in a pull request. Update `catalog.json`'s `updated` date when
catalog data changes. The CI checks use Python's standard library only.

## Add an app

Add the app entry and its icon in the same pull request. Use its exact
`qa-p1/<repository>` name from the app repository's `origin` remote, and check
the app ID against Arcade Link's `ids` module. Keep app entries alphabetical by
display name.

Include every required catalog field. Keep `pitch` to 60 characters or fewer
and write a two- or three-sentence `description` in plain language based on the
app's README. Use one of the documented categories: `files`, `capture`,
`clipboard`, `launcher`, or `toolbox`. Set `minTools` to the supported Tools
version and set `linkProtocol` to `[1]`.

Choose a platform label from the app's `docs/STATUS.md` evidence:

- `verified`: exercised on a real desktop for that platform.
- `ci`: built and tested in CI, but not exercised on a real desktop.
- `build-only`: built in CI without test runs.
- `unsupported`: the app does not support that platform.

Set `resident` according to whether the app normally stays open in the
background. Add screenshots only when the image exists on the app repository's
`main` branch, and link it using a `raw.githubusercontent.com` URL. Use the app's
own icon: copy an SVG when available, or provide a 256×256 PNG when it has no
SVG. Keep it at `icons/<app-id>.svg` or `icons/<app-id>.png`.

If the app needs a shared external helper, add an engine entry only when the
app's source or documentation confirms that it uses the helper. Include package
manager commands only for package names you have checked.

## Add a shortcut sheet

Add `shortcuts/<id>.json` using the format in
[`schema/shortcut-sheet.schema.json`](schema/shortcut-sheet.schema.json).
Choose an official help page or manual as a source, link to it over HTTPS, and
write shortcut titles and descriptions in your own words. Record the exact
application version checked. Match only the platforms and process identifiers
the official source supports; identifiers are matched case-insensitively.

Use a kebab-case sheet ID that matches the filename. Each shortcut ID must be
unique in that sheet. Give each group a kebab-case context such as `global`,
`editor`, or `tabs`. A shortcut title is limited to 80 characters.

Write keys using the shared canonical notation:

- A chord is modifiers followed by one key, joined with `+`: `Ctrl+Shift+P`.
- Modifier order is always `Ctrl`, `Alt`, `Shift`, `Super`. On macOS, `Super`
  means Command and `Alt` means Option.
- A shifted symbol uses its base key: write `Ctrl+Shift+Equal`, not `Ctrl++`.
- A sequence separates chords with one space: `Ctrl+K Ctrl+S`.
- A modifier by itself is valid, for example `Super`.
- Use the exact key names and casing from the shortcut-sheet schema.
- Use `default` for the usual binding and optional OS-specific values for
  differences. An OS value of `null` means that shortcut is unavailable there;
  otherwise the OS value overrides `default`.
- Do not add `rebindable`. Sheets record published behavior; they do not change
  application settings.

Two bindings in the same context conflict on an operating system if they are
equal or if one sequence is a prefix of the other. The validator checks this
across all groups in the sheet.

After changing a sheet, regenerate the index and run the checks:

```sh
python3 scripts/build_index.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

The catalog and schemas use JSON Schema draft 2020-12. Python validation and
tests require no third-party packages.

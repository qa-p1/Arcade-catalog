#!/usr/bin/env python3
"""Validate Arcade catalog data and third-party shortcut sheets."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit

from build_index import IndexBuildError, build_index


ROOT = Path(__file__).resolve().parents[1]
OS_NAMES = ("linux", "windows", "macos")
PLATFORM_STATUSES = {"verified", "ci", "build-only", "unsupported"}
CATEGORIES = {"files", "capture", "clipboard", "launcher", "toolbox"}
APP_ID = re.compile(r"^arcade\.[a-z][a-z0-9-]*$")
BUNDLE_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHEET_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SHORTCUT_ID = re.compile(r"^[a-z0-9][a-z0-9.-]*$")
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)"
    r"(?:\.(0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
DATE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
MODIFIERS = ("Ctrl", "Alt", "Shift", "Super")
KEY_NAMES = {
    "Space", "Enter", "Tab", "Escape", "Backspace", "Delete", "Insert", "Home", "End",
    "PageUp", "PageDown", "Up", "Down", "Left", "Right", "Minus", "Equal", "BracketLeft",
    "BracketRight", "Backslash", "Semicolon", "Quote", "Backquote", "Comma", "Period", "Slash",
    "Print", "Pause", "ScrollLock", "CapsLock", "NumLock", "Menu", "NumpadAdd", "NumpadSubtract",
    "NumpadMultiply", "NumpadDivide", "NumpadDecimal", "NumpadEnter", "VolumeUp", "VolumeDown",
    "VolumeMute", "MediaPlayPause", "MediaNext", "MediaPrevious", "MediaStop", "BrightnessUp",
    "BrightnessDown", "MouseLeft", "MouseRight", "MouseMiddle", "MouseBack", "MouseForward", "WheelUp",
    "WheelDown",
}
MATCH_FIELDS = {"class", "exe", "bundle"}
INSTALL_KEYS = {"arch", "debian", "fedora", "windows", "macos"}
CATALOG_FIELDS = {"schema", "updated", "apps", "tools", "bundles"}
ENGINES_FIELDS = {"schema", "engines"}
INDEX_FIELDS = {"schema", "sheets"}
SHEET_FIELDS = {"schema", "id", "name", "checkedVersion", "sources", "match", "groups"}


class DuplicateJSONKey(ValueError):
    """Raised when an object repeats a member name."""


def _object_from_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJSONKey(f"duplicate object key {key!r}")
        result[key] = value
    return result


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    @staticmethod
    def _location(file: str, path: str) -> str:
        return f"{file}:{path or '$'}"

    def error(self, file: str, path: str, message: str) -> None:
        self.errors.append(f"{self._location(file, path)}: {message}")

    def warning(self, file: str, path: str, message: str) -> None:
        self.warnings.append(f"{self._location(file, path)}: {message}")


def _parse_json_files(root: Path, reporter: Reporter) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for path in sorted(root.rglob("*.json")):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        try:
            parsed[relative] = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_object_from_pairs)
        except (OSError, UnicodeError, json.JSONDecodeError, DuplicateJSONKey) as exc:
            reporter.error(relative, "$", f"invalid JSON: {exc}")
    return parsed


def _required_object(
    value: Any, file: str, path: str, fields: tuple[str, ...], reporter: Reporter
) -> bool:
    if not isinstance(value, dict):
        reporter.error(file, path, "expected an object")
        return False
    for field in fields:
        if field not in value:
            reporter.error(file, f"{path}/{field}", "missing required field")
    return True


def _check_version(value: Any, file: str, path: str, reporter: Reporter) -> None:
    if type(value) is not int or value != 1:
        reporter.error(file, path, "schema must be the integer 1")


def _string_field(
    obj: dict[str, Any], key: str, file: str, path: str, reporter: Reporter, *, nonempty: bool = True
) -> str | None:
    if key not in obj:
        return None
    value = obj[key]
    if not isinstance(value, str):
        reporter.error(file, f"{path}/{key}", "expected a string")
        return None
    if nonempty and not value.strip():
        reporter.error(file, f"{path}/{key}", "must not be empty")
    return value


def _https_url(value: Any, file: str, path: str, reporter: Reporter, *, hosts: set[str] | None = None) -> bool:
    if not isinstance(value, str):
        reporter.error(file, path, "expected an HTTPS URL")
        return False
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        parsed = None
        port = None
    if (
        parsed is None
        or parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or (port not in (None, 443))
        or (hosts is not None and parsed.hostname.lower() not in hosts)
    ):
        requirement = "an HTTPS URL" if hosts is None else f"an HTTPS URL on {', '.join(sorted(hosts))}"
        reporter.error(file, path, f"must be {requirement}")
        return False
    return True


def _check_repo(value: Any, file: str, path: str, reporter: Reporter) -> None:
    if not isinstance(value, str) or not re.fullmatch(r"qa-p1/[^/?#\s]+", value):
        reporter.error(file, path, "repo must be qa-p1/<repository-name>")


def _check_semver(value: Any, file: str, path: str, reporter: Reporter) -> None:
    if not isinstance(value, str) or not SEMVER.fullmatch(value):
        reporter.error(file, path, "expected a semantic version (major.minor.patch)")


def _check_icon(value: Any, root: Path, file: str, path: str, reporter: Reporter) -> None:
    if not isinstance(value, str):
        reporter.error(file, path, "expected a relative icon path")
        return
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts or not value.startswith("icons/") or relative.suffix not in {".svg", ".png"}:
        reporter.error(file, path, "icon must be an SVG or PNG path inside icons/")
        return
    icon_path = root.joinpath(*relative.parts)
    try:
        icon_path.resolve().relative_to(root.resolve())
    except ValueError:
        reporter.error(file, path, "icon path must stay inside the catalog")
        return
    if not icon_path.is_file():
        reporter.error(file, path, f"icon file does not exist: {value}")
        return
    if relative.suffix == ".png":
        try:
            header = icon_path.read_bytes()[:24]
            if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
                reporter.error(file, path, "PNG icon is not a valid PNG file")
                return
            width = int.from_bytes(header[16:20], "big")
            height = int.from_bytes(header[20:24], "big")
            if (width, height) != (256, 256):
                reporter.error(file, path, f"PNG icon must be 256x256 pixels (found {width}x{height})")
        except OSError as exc:
            reporter.error(file, path, f"cannot read PNG icon: {exc}")


def _check_app_id(value: Any, file: str, path: str, reporter: Reporter) -> None:
    if not isinstance(value, str) or not APP_ID.fullmatch(value):
        reporter.error(file, path, "app id must match ^arcade\\.[a-z][a-z0-9-]*$")


def _check_unknown_top_level(
    obj: Any, known: set[str], file: str, reporter: Reporter
) -> None:
    if isinstance(obj, dict):
        for key in sorted(set(obj) - known):
            reporter.warning(file, f"/{key}", "unknown top-level field is allowed")


def _count_sentences(text: str) -> int:
    return len(re.findall(r"[.!?]+(?=\s|$)", text.strip()))


def _validate_app(
    app: Any,
    index: int,
    root: Path,
    reporter: Reporter,
    seen_ids: dict[str, str],
) -> tuple[str | None, str | None]:
    file = "catalog.json"
    path = f"/apps/{index}"
    required = (
        "id", "name", "repo", "pitch", "description", "category", "icon", "screenshots", "platforms",
        "linkProtocol", "minTools", "docs", "resident", "homepage",
    )
    if not _required_object(app, file, path, required, reporter):
        return None, None

    app_id = _string_field(app, "id", file, path, reporter)
    if app_id is not None:
        _check_app_id(app_id, file, f"{path}/id", reporter)
        if app_id in seen_ids:
            reporter.error(file, f"{path}/id", f"duplicate id also used at {seen_ids[app_id]}")
        else:
            seen_ids[app_id] = f"{path}/id"

    name = _string_field(app, "name", file, path, reporter)
    repo = _string_field(app, "repo", file, path, reporter)
    if repo is not None:
        _check_repo(repo, file, f"{path}/repo", reporter)

    pitch = _string_field(app, "pitch", file, path, reporter)
    if pitch is not None and len(pitch) > 60:
        reporter.error(file, f"{path}/pitch", f"must be at most 60 characters (found {len(pitch)})")

    description = _string_field(app, "description", file, path, reporter)
    if description is not None and _count_sentences(description) not in {2, 3}:
        reporter.error(file, f"{path}/description", "must contain two or three sentences")

    category = _string_field(app, "category", file, path, reporter)
    if category is not None and category not in CATEGORIES:
        reporter.error(file, f"{path}/category", f"must be one of {', '.join(sorted(CATEGORIES))}")

    _check_icon(app.get("icon"), root, file, f"{path}/icon", reporter)

    screenshots = app.get("screenshots")
    if "screenshots" in app:
        if not isinstance(screenshots, list):
            reporter.error(file, f"{path}/screenshots", "expected an array of URLs")
        else:
            for shot_index, url in enumerate(screenshots):
                _https_url(
                    url,
                    file,
                    f"{path}/screenshots/{shot_index}",
                    reporter,
                    hosts={"github.com", "raw.githubusercontent.com"},
                )

    platforms = app.get("platforms")
    if "platforms" in app:
        if not isinstance(platforms, dict):
            reporter.error(file, f"{path}/platforms", "expected an object")
        else:
            for os_name in OS_NAMES:
                if os_name not in platforms:
                    reporter.error(file, f"{path}/platforms/{os_name}", "missing platform status")
                elif not isinstance(platforms[os_name], str) or platforms[os_name] not in PLATFORM_STATUSES:
                    reporter.error(
                        file,
                        f"{path}/platforms/{os_name}",
                        f"must be one of {', '.join(sorted(PLATFORM_STATUSES))}",
                    )
            for os_name in sorted(set(platforms) - set(OS_NAMES)):
                reporter.error(file, f"{path}/platforms/{os_name}", "unknown platform")

    if "linkProtocol" in app:
        protocol = app["linkProtocol"]
        if not isinstance(protocol, list):
            reporter.error(file, f"{path}/linkProtocol", "expected an array")
        elif len(protocol) != 1 or type(protocol[0]) is not int or protocol[0] != 1:
            reporter.error(file, f"{path}/linkProtocol", "must be [1]")

    if "minTools" in app:
        _check_semver(app["minTools"], file, f"{path}/minTools", reporter)
    _string_field(app, "docs", file, path, reporter)
    if "resident" in app and type(app["resident"]) is not bool:
        reporter.error(file, f"{path}/resident", "expected a boolean")

    if "homepage" in app:
        _https_url(app["homepage"], file, f"{path}/homepage", reporter, hosts={"github.com"})
    return app_id, name


def _validate_catalog(data: Any, root: Path, reporter: Reporter) -> set[str]:
    file = "catalog.json"
    if not _required_object(data, file, "$", ("schema", "updated", "apps", "tools", "bundles"), reporter):
        return set()
    _check_unknown_top_level(data, CATALOG_FIELDS, file, reporter)
    _check_version(data.get("schema"), file, "/schema", reporter)

    updated = _string_field(data, "updated", file, "$", reporter)
    if updated is not None:
        try:
            if not DATE.fullmatch(updated):
                raise ValueError("expected YYYY-MM-DD")
            dt.date.fromisoformat(updated)
        except ValueError as exc:
            reporter.error(file, "/updated", f"invalid calendar date: {exc}")

    seen_ids: dict[str, str] = {}
    app_ids: set[str] = set()
    apps = data.get("apps")
    names: list[str] = []
    if "apps" in data:
        if not isinstance(apps, list):
            reporter.error(file, "/apps", "expected an array")
        else:
            for index, app in enumerate(apps):
                app_id, name = _validate_app(app, index, root, reporter, seen_ids)
                if app_id is not None:
                    app_ids.add(app_id)
                if name is not None:
                    names.append(name)
            if names and names != sorted(names, key=str.casefold):
                reporter.error(file, "/apps", "apps must be sorted alphabetically by name")

    tools = data.get("tools")
    if "tools" in data:
        if _required_object(tools, file, "/tools", ("id", "name", "repo", "minTools", "icon"), reporter):
            tools_id = _string_field(tools, "id", file, "/tools", reporter)
            if tools_id is not None:
                _check_app_id(tools_id, file, "/tools/id", reporter)
                if tools_id in seen_ids:
                    reporter.error(file, "/tools/id", f"duplicate id also used at {seen_ids[tools_id]}")
                else:
                    seen_ids[tools_id] = "/tools/id"
            _string_field(tools, "name", file, "/tools", reporter)
            repo = _string_field(tools, "repo", file, "/tools", reporter)
            if repo is not None:
                _check_repo(repo, file, "/tools/repo", reporter)
            if "minTools" in tools:
                _check_semver(tools["minTools"], file, "/tools/minTools", reporter)
            _check_icon(tools.get("icon"), root, file, "/tools/icon", reporter)

    bundles = data.get("bundles")
    if "bundles" in data:
        if not isinstance(bundles, list):
            reporter.error(file, "/bundles", "expected an array")
        else:
            bundle_ids: dict[str, str] = {}
            for index, bundle in enumerate(bundles):
                path = f"/bundles/{index}"
                if not _required_object(bundle, file, path, ("id", "title", "description", "apps"), reporter):
                    continue
                bundle_id = _string_field(bundle, "id", file, path, reporter)
                if bundle_id is not None:
                    if not BUNDLE_ID.fullmatch(bundle_id):
                        reporter.error(file, f"{path}/id", "bundle id must be kebab-case")
                    if bundle_id in bundle_ids:
                        reporter.error(file, f"{path}/id", f"duplicate bundle id also used at {bundle_ids[bundle_id]}")
                    else:
                        bundle_ids[bundle_id] = f"{path}/id"
                _string_field(bundle, "title", file, path, reporter)
                _string_field(bundle, "description", file, path, reporter)
                refs = bundle.get("apps")
                if refs == "*":
                    continue
                if not isinstance(refs, list) or not refs:
                    reporter.error(file, f"{path}/apps", 'must be "*" or a non-empty array of app ids')
                    continue
                seen_refs: set[str] = set()
                for ref_index, app_ref in enumerate(refs):
                    ref_path = f"{path}/apps/{ref_index}"
                    if not isinstance(app_ref, str):
                        reporter.error(file, ref_path, "expected an app id string")
                        continue
                    if app_ref == "*":
                        reporter.error(file, ref_path, 'use "*" as the entire apps value')
                    elif app_ref not in app_ids:
                        reporter.error(file, ref_path, f"unknown app id {app_ref!r}")
                    if app_ref in seen_refs:
                        reporter.error(file, ref_path, f"duplicate app reference {app_ref!r}")
                    seen_refs.add(app_ref)
    return app_ids


def _validate_engines(data: Any, app_ids: set[str], reporter: Reporter) -> None:
    file = "engines.json"
    if not _required_object(data, file, "$", ("schema", "engines"), reporter):
        return
    _check_unknown_top_level(data, ENGINES_FIELDS, file, reporter)
    _check_version(data.get("schema"), file, "/schema", reporter)
    engines = data.get("engines")
    if "engines" not in data:
        return
    if not isinstance(engines, list):
        reporter.error(file, "/engines", "expected an array")
        return

    ids: dict[str, str] = {}
    for index, engine in enumerate(engines):
        path = f"/engines/{index}"
        if not _required_object(
            engine, file, path, ("id", "name", "homepage", "detect", "usedBy", "install", "linkDownload"), reporter
        ):
            continue
        engine_id = _string_field(engine, "id", file, path, reporter)
        if engine_id is not None:
            if not re.fullmatch(r"^[a-z][a-z0-9-]*$", engine_id):
                reporter.error(file, f"{path}/id", "engine id must be lowercase kebab-case")
            if engine_id in ids:
                reporter.error(file, f"{path}/id", f"duplicate engine id also used at {ids[engine_id]}")
            else:
                ids[engine_id] = f"{path}/id"
        _string_field(engine, "name", file, path, reporter)
        if "homepage" in engine:
            _https_url(engine["homepage"], file, f"{path}/homepage", reporter)

        detect = engine.get("detect")
        if "detect" in engine and _required_object(detect, file, f"{path}/detect", ("binaries", "versionArgs"), reporter):
            for field in ("binaries", "versionArgs"):
                values = detect.get(field)
                field_path = f"{path}/detect/{field}"
                if field not in detect:
                    continue
                if not isinstance(values, list) or not values:
                    reporter.error(file, field_path, "expected a non-empty array of strings")
                else:
                    for item_index, item in enumerate(values):
                        if not isinstance(item, str) or (field == "binaries" and not item):
                            reporter.error(file, f"{field_path}/{item_index}", "expected a non-empty string")
            if "minVersion" in detect:
                _check_semver(detect["minVersion"], file, f"{path}/detect/minVersion", reporter)

        used_by = engine.get("usedBy")
        if "usedBy" in engine:
            if not isinstance(used_by, list) or not used_by:
                reporter.error(file, f"{path}/usedBy", "expected a non-empty array")
            else:
                for use_index, usage in enumerate(used_by):
                    use_path = f"{path}/usedBy/{use_index}"
                    if not _required_object(usage, file, use_path, ("app", "for"), reporter):
                        continue
                    app_id = _string_field(usage, "app", file, use_path, reporter)
                    if app_id is not None and app_id not in app_ids:
                        reporter.error(file, f"{use_path}/app", f"unknown catalog app {app_id!r}")
                    _string_field(usage, "for", file, use_path, reporter)

        install = engine.get("install")
        if "install" in engine:
            if not isinstance(install, dict):
                reporter.error(file, f"{path}/install", "expected an object")
            else:
                for manager, command in install.items():
                    if manager not in INSTALL_KEYS:
                        reporter.error(file, f"{path}/install/{manager}", "unknown package manager key")
                    if not isinstance(command, str) or not command.strip():
                        reporter.error(file, f"{path}/install/{manager}", "expected a non-empty install command")

        if "linkDownload" in engine:
            if type(engine["linkDownload"]) is not bool:
                reporter.error(file, f"{path}/linkDownload", "expected a boolean")
            elif engine["linkDownload"] and engine_id != "tesseract":
                reporter.error(file, f"{path}/linkDownload", "only the Tesseract engine may be downloaded by Arcade Link")


def _is_key_name(key: str) -> bool:
    return (
        (len(key) == 1 and ("A" <= key <= "Z" or "0" <= key <= "9"))
        or key in KEY_NAMES
        or re.fullmatch(r"F(?:[1-9]|1[0-9]|2[0-4])", key) is not None
        or re.fullmatch(r"Numpad[0-9]", key) is not None
        or re.fullmatch(r"Code[0-9]+", key) is not None
    )


def parse_key_sequence(value: Any) -> tuple[str, ...] | None:
    """Return a canonical sequence's chords, or None when its notation is invalid."""
    if not isinstance(value, str) or not value or value != value.strip():
        return None
    chords = value.split(" ")
    if any(not chord for chord in chords):
        return None
    for chord in chords:
        if chord in MODIFIERS:
            continue
        pieces = chord.split("+")
        if any(not piece for piece in pieces):
            return None
        modifiers, key = pieces[:-1], pieces[-1]
        if any(modifier not in MODIFIERS for modifier in modifiers):
            return None
        if tuple(modifiers) != tuple(modifier for modifier in MODIFIERS if modifier in modifiers):
            return None
        if len(set(modifiers)) != len(modifiers) or not _is_key_name(key):
            return None
    return tuple(chords)


def _sequences_conflict(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    shorter = min(len(left), len(right))
    return left[:shorter] == right[:shorter]


def _string_array(value: Any, file: str, path: str, reporter: Reporter, *, nonempty: bool = True) -> list[str] | None:
    if not isinstance(value, list):
        reporter.error(file, path, "expected an array of strings")
        return None
    if nonempty and not value:
        reporter.error(file, path, "array must not be empty")
    strings: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            reporter.error(file, f"{path}/{index}", "expected a non-empty string")
        else:
            strings.append(item)
    return strings


def _walk_rebindable(value: Any, file: str, path: str, reporter: Reporter) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}/{key}"
            if key == "rebindable":
                reporter.error(file, child_path, "rebindable is not allowed in shortcut sheets")
            _walk_rebindable(child, file, child_path, reporter)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_rebindable(child, file, f"{path}/{index}", reporter)


def _validate_shortcut_sheet(file: str, sheet: Any, reporter: Reporter) -> None:
    required = ("schema", "id", "name", "checkedVersion", "sources", "match", "groups")
    if not _required_object(sheet, file, "$", required, reporter):
        return
    _check_unknown_top_level(sheet, SHEET_FIELDS, file, reporter)
    _walk_rebindable(sheet, file, "$", reporter)
    _check_version(sheet.get("schema"), file, "/schema", reporter)

    sheet_id = _string_field(sheet, "id", file, "$", reporter)
    if sheet_id is not None:
        if not SHEET_ID.fullmatch(sheet_id):
            reporter.error(file, "/id", "sheet id must be lowercase kebab-case")
        if PurePosixPath(file).stem != sheet_id:
            reporter.error(file, "/id", "sheet id must match the file name")
    _string_field(sheet, "name", file, "$", reporter)
    _string_field(sheet, "checkedVersion", file, "$", reporter)

    sources = sheet.get("sources")
    if "sources" in sheet:
        if not isinstance(sources, list) or not sources:
            reporter.error(file, "/sources", "expected a non-empty array of HTTPS URLs")
        else:
            for index, source in enumerate(sources):
                _https_url(source, file, f"/sources/{index}", reporter)

    match = sheet.get("match")
    if "match" in sheet:
        if not isinstance(match, dict):
            reporter.error(file, "/match", "expected an object")
        else:
            present_os = [name for name in OS_NAMES if name in match]
            if not present_os:
                reporter.error(file, "/match", "must include at least one platform matcher")
            for os_name in present_os:
                os_match = match[os_name]
                os_path = f"/match/{os_name}"
                if not isinstance(os_match, dict):
                    reporter.error(file, os_path, "expected an object of match arrays")
                    continue
                present_fields = [field for field in MATCH_FIELDS if field in os_match]
                if not present_fields:
                    reporter.error(file, os_path, "must include at least one class, exe, or bundle array")
                for field in present_fields:
                    _string_array(os_match[field], file, f"{os_path}/{field}", reporter)

    groups = sheet.get("groups")
    if "groups" in sheet:
        if not isinstance(groups, list) or not groups:
            reporter.error(file, "/groups", "expected a non-empty array")
            return
    else:
        return

    shortcut_ids: dict[str, str] = {}
    bindings: dict[tuple[str, str], list[tuple[str, str, list[tuple[str, ...]]]]] = {}
    for group_index, group in enumerate(groups):
        group_path = f"/groups/{group_index}"
        if not _required_object(group, file, group_path, ("title", "context", "shortcuts"), reporter):
            continue
        _string_field(group, "title", file, group_path, reporter)
        context = _string_field(group, "context", file, group_path, reporter)
        if context is not None and not BUNDLE_ID.fullmatch(context):
            reporter.error(file, f"{group_path}/context", "context must be lowercase kebab-case")
        shortcuts = group.get("shortcuts")
        if not isinstance(shortcuts, list) or not shortcuts:
            reporter.error(file, f"{group_path}/shortcuts", "expected a non-empty array")
            continue

        for shortcut_index, shortcut in enumerate(shortcuts):
            shortcut_path = f"{group_path}/shortcuts/{shortcut_index}"
            if not _required_object(shortcut, file, shortcut_path, ("id", "title", "keys"), reporter):
                continue
            shortcut_id = _string_field(shortcut, "id", file, shortcut_path, reporter)
            if shortcut_id is not None:
                if not SHORTCUT_ID.fullmatch(shortcut_id):
                    reporter.error(file, f"{shortcut_path}/id", "shortcut id must match ^[a-z0-9][a-z0-9.-]*$")
                if shortcut_id in shortcut_ids:
                    reporter.error(file, f"{shortcut_path}/id", f"duplicate shortcut id also used at {shortcut_ids[shortcut_id]}")
                else:
                    shortcut_ids[shortcut_id] = f"{shortcut_path}/id"
            title = _string_field(shortcut, "title", file, shortcut_path, reporter)
            if title is not None and len(title) > 80:
                reporter.error(file, f"{shortcut_path}/title", f"must be at most 80 characters (found {len(title)})")

            keys = shortcut.get("keys")
            keys_path = f"{shortcut_path}/keys"
            if "keys" not in shortcut:
                continue
            if not isinstance(keys, dict):
                reporter.error(file, keys_path, "expected a keys object")
                continue
            known_keys = [name for name in ("default", *OS_NAMES) if name in keys]
            if not known_keys:
                reporter.error(file, keys_path, "must define default and/or a platform binding")

            non_null = False
            for binding_name in known_keys:
                value = keys[binding_name]
                binding_path = f"{keys_path}/{binding_name}"
                if value is None:
                    continue
                non_null = True
                sequences = [value] if isinstance(value, str) else value if isinstance(value, list) else None
                if sequences is None:
                    reporter.error(binding_path.rsplit("/", 1)[0] + "/" + binding_name, "expected a key sequence, array of alternatives, or null")
                    continue
                if isinstance(value, list) and not value:
                    reporter.error(binding_path, "alternative array must not be empty")
                    continue
                for alternative_index, sequence in enumerate(sequences):
                    sequence_path = binding_path if isinstance(value, str) else f"{binding_path}/{alternative_index}"
                    parsed = parse_key_sequence(sequence)
                    if parsed is None:
                        reporter.error(
                            file,
                            sequence_path,
                            f"invalid key sequence {sequence!r}; use canonical modifiers Ctrl, Alt, Shift, Super in that order and one supported key per chord",
                        )
            if not non_null:
                reporter.error(file, keys_path, "at least one binding must be non-null")

            if context is None:
                continue
            for os_name in OS_NAMES:
                if os_name in keys:
                    value = keys[os_name]
                else:
                    value = keys.get("default")
                if value is None:
                    continue
                alternatives = [value] if isinstance(value, str) else value if isinstance(value, list) else []
                parsed_alternatives = [
                    parsed for item in alternatives if (parsed := parse_key_sequence(item)) is not None
                ]
                if not parsed_alternatives:
                    continue
                context_os = (context, os_name)
                for previous_id, _previous_path, previous_sequences in bindings.get(context_os, []):
                    conflict = any(
                        _sequences_conflict(current, previous)
                        for current in parsed_alternatives
                        for previous in previous_sequences
                    )
                    if conflict:
                        reporter.error(
                            file,
                            f"{keys_path}/{os_name if os_name in keys else 'default'}",
                            f"binding conflicts with shortcut {previous_id!r} in context {context!r} on {os_name}",
                        )
                if shortcut_id is not None:
                    bindings.setdefault(context_os, []).append((shortcut_id, keys_path, parsed_alternatives))


def _validate_index(data: Any, root: Path, reporter: Reporter) -> None:
    file = "shortcuts/index.json"
    if not _required_object(data, file, "$", ("schema", "sheets"), reporter):
        return
    _check_unknown_top_level(data, INDEX_FIELDS, file, reporter)
    _check_version(data.get("schema"), file, "/schema", reporter)
    sheets = data.get("sheets")
    if not isinstance(sheets, list):
        reporter.error(file, "/sheets", "expected an array")
    else:
        for index, entry in enumerate(sheets):
            path = f"/sheets/{index}"
            if not _required_object(entry, file, path, ("id", "name", "file", "match"), reporter):
                continue
            _string_field(entry, "id", file, path, reporter)
            _string_field(entry, "name", file, path, reporter)
            sheet_file = _string_field(entry, "file", file, path, reporter)
            if sheet_file is not None:
                pure_path = PurePosixPath(sheet_file)
                if pure_path.is_absolute() or ".." in pure_path.parts or not sheet_file.startswith("shortcuts/"):
                    reporter.error(file, f"{path}/file", "file must be a relative path inside shortcuts/")
                elif not (root.joinpath(*pure_path.parts)).is_file():
                    reporter.error(file, f"{path}/file", "referenced shortcut sheet does not exist")
            if not isinstance(entry.get("match"), dict):
                reporter.error(file, f"{path}/match", "expected an object")

    try:
        expected = build_index(root)
    except IndexBuildError as exc:
        reporter.error(file, "/sheets", f"cannot generate expected index: {exc}")
        return
    if data != expected:
        reporter.error(file, "/sheets", "index is stale; run python3 scripts/build_index.py")


def validate_repository(root: Path = ROOT) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a catalog root."""
    root = Path(root).resolve()
    reporter = Reporter()
    parsed = _parse_json_files(root, reporter)

    for required_path in ("catalog.json", "engines.json", "shortcuts/index.json"):
        if required_path not in parsed and not (root / required_path).is_file():
            reporter.error(required_path, "$", "required JSON file is missing")

    app_ids: set[str] = set()
    if "catalog.json" in parsed:
        app_ids = _validate_catalog(parsed["catalog.json"], root, reporter)
    if "engines.json" in parsed:
        _validate_engines(parsed["engines.json"], app_ids, reporter)

    shortcuts_dir = root / "shortcuts"
    if shortcuts_dir.is_dir():
        for path in sorted(shortcuts_dir.glob("*.json")):
            if path.name == "index.json":
                continue
            relative = path.relative_to(root).as_posix()
            if relative in parsed:
                _validate_shortcut_sheet(relative, parsed[relative], reporter)

    if "shortcuts/index.json" in parsed:
        _validate_index(parsed["shortcuts/index.json"], root, reporter)
    return reporter.errors, reporter.warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="catalog root (defaults to this repository)")
    args = parser.parse_args()

    errors, warnings = validate_repository(args.root)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"Validation passed with {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

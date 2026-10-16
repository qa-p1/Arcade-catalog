"""Shared helpers for the 2026-10 stress-test regression checks.

Every check is meant to run inside Arcade Link's isolated runner:

    cd Arcade-Link && python3 tools/e2e.py run -- python3 <this dir>/<check>.py ARGS

The runner provides a private D-Bus, Xvfb, a throwaway keyring and temporary
HOME/XDG/ARCADE_HOME. These checks refuse to run anywhere else, never touch the
real profile, and exit 1 while the bug they describe is present.
"""

import os
import subprocess
import sys
import time
from pathlib import Path


def require_isolation() -> Path:
    root = Path(os.environ.get("ARCADE_E2E_ROOT", "/")).resolve()
    if os.environ.get("ARCADE_E2E_INNER") != "1" or root == Path("/"):
        raise SystemExit("Run through Arcade-Link: python3 tools/e2e.py run -- python3 " + sys.argv[0] + " ...")
    for key in ("HOME", "XDG_CONFIG_HOME", "XDG_DATA_HOME", "XDG_CACHE_HOME"):
        if not Path(os.environ.get(key, "/")).resolve().is_relative_to(root):
            raise SystemExit(f"Refusing non-isolated {key}")
    if not os.environ.get("DBUS_SESSION_BUS_ADDRESS") or not os.environ.get("DISPLAY"):
        raise SystemExit("Link's private D-Bus and Xvfb are required")
    return root


def fail(message: str) -> None:
    print(f"FAIL {Path(sys.argv[0]).stem}: {message}", flush=True)
    raise SystemExit(1)


def ok(message: str) -> None:
    print(f"PASS {Path(sys.argv[0]).stem}: {message}", flush=True)
    raise SystemExit(0)


def wait_for(predicate, timeout: float, step: float = 0.1):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        value = predicate()
        if value:
            return value
        time.sleep(step)
    return predicate()


def children(pid: int) -> list[int]:
    out = subprocess.run(["ps", "-o", "pid=", "--ppid", str(pid)], capture_output=True, text=True).stdout
    return [int(p) for p in out.split()]


def comm(pid: int) -> str:
    try:
        return Path(f"/proc/{pid}/comm").read_text().strip()
    except OSError:
        return ""


def pids_by_exe_suffix(suffix: str) -> list[int]:
    found = []
    for entry in Path("/proc").iterdir():
        if entry.name.isdigit():
            try:
                if os.readlink(entry / "exe").endswith(suffix):
                    found.append(int(entry.name))
            except OSError:
                pass
    return found


def environ(pid: int) -> dict[str, str]:
    raw = Path(f"/proc/{pid}/environ").read_bytes().split(b"\0")
    return dict(item.decode(errors="replace").split("=", 1) for item in raw if b"=" in item)


def install_silently(appimage: str, app_id: str) -> Path:
    """Scripted install (--install --silent --no-launch), as Tools does.

    Returns the installed path recorded in the app's receipt."""
    import json
    if not os.access(appimage, os.X_OK):
        subprocess.run(["chmod", "+x", appimage], check=True)
    result = subprocess.run([appimage, "--install", "--silent", "--no-launch"], capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        raise SystemExit(f"prerequisite install of {appimage} failed: {result.stderr[-400:]}")
    root = Path(os.environ["ARCADE_E2E_ROOT"])
    receipts = sorted(root.rglob(f"installs/{app_id}.json"), key=lambda p: p.stat().st_mtime)
    if not receipts:
        raise SystemExit(f"no install receipt for {app_id} under {root}")
    return Path(json.loads(receipts[-1].read_text())["path"])

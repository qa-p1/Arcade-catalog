#!/usr/bin/env python3
"""F2 (F-TOOLS-ENVLEAK-LAUNCH): apps that Tools starts must get the user's environment.

Tools 0.2.1 runs from its AppImage mount and starts apps with that environment
(LD_LIBRARY_PATH, GTK_THEME, XDG_DATA_DIRS, PYTHONHOME, … pointing into
/tmp/.mount_*). Clipboard then dies with "undefined symbol:
g_once_init_enter_pointer", so tray → "Start all Arcade apps", adoption and the
app card's Open never start Clipboard, and every other app runs with Tools'
libraries and a forced light theme.

The check installs Tools and Clipboard the scripted way, starts Tools in the
background with a tray watcher present, clicks "Start all Arcade apps" in
Tools' tray menu over DBusMenu, and expects Clipboard to be running within 20 s
with no environment variable pointing into Tools' AppImage mount.

Usage (inside Link's runner; scripted installs consume their source, pass copies):
    python3 tools/e2e.py run -- python3 tools_start_all_child_env.py COPY/Arcade-Tools_0.2.1_amd64.AppImage COPY/Arcade-Clipboard-0.1.0-x86_64.AppImage
--control starts the installed Clipboard directly instead (expected PASS: Clipboard itself runs here).
"""

import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import environ, fail, install_silently, ok, require_isolation, wait_for  # noqa: E402

require_isolation()
from sni import Watcher, click, menu_items, pump  # noqa: E402

tools_appimage, clip_appimage = sys.argv[1], sys.argv[2]
control = "--control" in sys.argv
tools = install_silently(tools_appimage, "arcade.tools")
clipboard = install_silently(clip_appimage, "arcade.clipboard")


ROOT = os.environ["ARCADE_E2E_ROOT"]


def clipboard_pids() -> list[int]:
    """Clipboard processes of this isolated session only (HOME under the runner's root)."""
    out = []
    for entry in Path("/proc").iterdir():
        if entry.name.isdigit():
            try:
                if (entry / "comm").read_text().strip() == "clipboard" and \
                        environ(int(entry.name)).get("HOME", "").startswith(ROOT):
                    out.append(int(entry.name))
            except OSError:
                pass
    return out


watcher = Watcher()
if control:
    subprocess.Popen([str(clipboard), "--background"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
else:
    env = dict(os.environ, WEBKIT_DISABLE_COMPOSITING_MODE="1")
    subprocess.Popen([str(tools), "--background"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + 30
    tools_item = None
    while time.monotonic() < deadline and tools_item is None:
        pump(0.5)
        for sender, path in watcher.items:
            try:
                if Path(f"/proc/{watcher.pid_of(sender)}/comm").read_text().strip() == "arcade-tools":
                    tools_item = (sender, path)
            except Exception:
                pass
    if tools_item is None:
        fail("Tools never registered a tray item")
    labels, menu = menu_items(watcher.bus, *tools_item)
    start_all = next((i for label, i in labels.items() if label.lower().startswith("start all")), None)
    if start_all is None:
        fail(f"no 'Start all' entry in Tools' tray menu: {sorted(labels)}")
    click(menu, start_all)

pids = wait_for(clipboard_pids, timeout=20, step=0.5)
problems = []
if not pids:
    problems.append("Clipboard is not running 20 s after 'Start all Arcade apps'")
for pid in pids or []:
    leaked = {k: v for k, v in environ(pid).items()
              if "/tmp/.mount_" in v and k not in ("APPDIR", "APPIMAGE", "ARGV0", "OWD", "PWD")
              and "Clipboard" not in v and "clipboard" not in v}
    if leaked:
        problems.append(f"Clipboard pid {pid} inherited Tools' mount: {sorted(leaked)}")
if problems:
    fail("; ".join(problems))
ok(f"Clipboard running (pids {pids}) with its own environment")

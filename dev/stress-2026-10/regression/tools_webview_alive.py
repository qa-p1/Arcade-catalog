#!/usr/bin/env python3
"""F1 (F-TOOLS-BLANK): the Tools window must render on an X server without DRI3.

On Xvfb (and VNC/xrdp sessions, VMs without 3D) Tools 0.2.1's
WebKitWebProcess crashes (SIGSEGV) about 0.9 s after the window opens, so the
window stays blank, including the "Install Arcade Tools?" prompt drawn inside
it. Look 0.2.1 ships the same libwebkit2gtk and renders fine. Suspected cause:
src-tauri/src/desktop.rs:115-121 sets HardwareAccelerationPolicy::Never after
the webview is built.

Expected: the window's WebKitWebProcess is still alive 8 s after start and
the window is not a single flat colour.

Usage (inside Link's runner, which uses Xvfb):
    python3 tools/e2e.py run -- python3 tools_webview_alive.py PATH/Arcade-Tools_0.2.1_amd64.AppImage [--control]
--control sets WEBKIT_DISABLE_COMPOSITING_MODE=1 (the workaround; expected PASS).
"""

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fail, ok, require_isolation  # noqa: E402

require_isolation()
appimage = sys.argv[1]
if not os.access(appimage, os.X_OK):
    subprocess.run(["chmod", "+x", appimage], check=True)
env = dict(os.environ)
if "--control" in sys.argv:
    env["WEBKIT_DISABLE_COMPOSITING_MODE"] = "1"

started = time.monotonic()
tools = subprocess.Popen([appimage], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)


def web_processes() -> list[int]:
    found = []
    for entry in Path("/proc").iterdir():
        if entry.name.isdigit():
            try:
                if (entry / "comm").read_text().strip().startswith("WebKitWebProces") and \
                        os.getsid(int(entry.name)) == tools.pid:
                    found.append(int(entry.name))
            except OSError:
                pass
    return found


seen = set()
while time.monotonic() - started < 8:
    seen.update(web_processes())
    time.sleep(0.05)
alive = web_processes()

with tempfile.TemporaryDirectory() as tmp:
    shot = Path(tmp) / "screen.png"
    window = subprocess.run(["xdotool", "search", "--onlyvisible", "--name", "^Arcade Tools$"],
                            capture_output=True, text=True).stdout.split()
    colours = None
    if window and subprocess.run(["import", "-window", window[0], str(shot)], capture_output=True).returncode == 0:
        colours = int(subprocess.run(["identify", "-format", "%k", str(shot)], capture_output=True, text=True).stdout or 0)

os.killpg(tools.pid, 9)
problems = []
if not seen:
    problems.append("no WebKitWebProcess was started")
elif not alive:
    problems.append(f"WebKitWebProcess {sorted(seen)} died within 8 s")
if colours is not None and colours <= 2:
    problems.append(f"window is blank ({colours} colours)")
if problems:
    fail("; ".join(problems))
ok(f"web process alive {alive}; window colours {colours}")

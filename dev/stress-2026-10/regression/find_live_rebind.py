#!/usr/bin/env python3
"""F7 (F-FIND-REBIND-LIVE): a shortcut changed over the Link must work at once on X11.

Tools' Shortcuts tab calls app.shortcuts.set on Find. Find 0.3.1 answers
{"applied": true, "via": "native"} and rewrites its manifest, but on X11
neither the old nor the new chord opens Find until Find restarts.

Expected: within 3 s of the call, pressing the new chord shows Find's window.

Usage (inside Link's runner; the scripted install consumes its source, pass a copy):
    python3 tools/e2e.py run -- python3 find_live_rebind.py COPY/Arcade-Find-x86_64.AppImage [--link PATH/arcade-link]
The script also restarts Find and presses the chord again; that half is the
control and is expected to work today.
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fail, install_silently, ok, require_isolation, wait_for  # noqa: E402

require_isolation()
link = sys.argv[sys.argv.index("--link") + 1] if "--link" in sys.argv else "arcade-link"
find = install_silently(sys.argv[1], "arcade.find")
NEW = "Ctrl+Alt+G"


def start():
    proc = subprocess.Popen([str(find), "--background"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not wait_for(lambda: subprocess.run([link, "status", "find"], capture_output=True).returncode == 0, 20, 0.2):
        fail("Find did not answer on the Link")
    time.sleep(1.0)
    return proc


def visible() -> bool:
    r = subprocess.run(["xdotool", "search", "--onlyvisible", "--name", "^Arcade Find$"], capture_output=True, text=True)
    return bool(r.stdout.split())


def chord_opens() -> bool:
    if visible():
        subprocess.run(["xdotool", "key", "Escape"])
        time.sleep(0.5)
    subprocess.run(["xdotool", "key", "ctrl+alt+g"])
    return bool(wait_for(visible, 3, 0.1))


start()
reply = subprocess.run([link, "call", "find", "app.shortcuts.set", "--params",
                        json.dumps({"id": "show", "accelerator": NEW})], capture_output=True, text=True)
if reply.returncode != 0:
    fail(f"app.shortcuts.set failed: {reply.stdout}{reply.stderr}")
live = chord_opens()

# Control: after a restart the stored chord works.
subprocess.run([link, "quit", "find"], capture_output=True)
time.sleep(2)
start()
after_restart = chord_opens()
subprocess.run([link, "quit", "find"], capture_output=True)

if not after_restart:
    fail(f"control failed: {NEW} does not open Find even after a restart (check X11 key grabs in this runner)")
if not live:
    fail(f"{NEW} did not open Find after app.shortcuts.set replied {reply.stdout.strip()!r}; it only works after a restart")
ok(f"{NEW} works immediately and after a restart")

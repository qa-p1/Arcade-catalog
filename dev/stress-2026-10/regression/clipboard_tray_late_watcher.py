#!/usr/bin/env python3
"""F-CLIP-TRAYRACE: Clipboard started at login before the tray must still get a tray icon.

At login, autostart entries and the panel start in parallel. Clipboard 0.1.0
checks NameHasOwner(org.kde.StatusNotifierWatcher) once when it enables
background mode (platform/desktop/arcade_desktop_bridge/linux/lifecycle_bridge.cc,
HandleLifecycleMethod "setBackgroundEnabled" -> TrayHostAvailable). If the
watcher is not there yet, background mode is refused: the window is shown, no
watcher appearance is ever watched, no tray item is registered for the whole
session, and closing the window quits Clipboard.

Expected: within 10 s of the watcher appearing, Clipboard registers its item.

Usage (inside Link's runner; the AppImage is consumed by --install --silent, pass a copy):
    python3 tools/e2e.py run -- python3 clipboard_tray_late_watcher.py /tmp/copy/Arcade-Clipboard-0.1.0-x86_64.AppImage [--control]
--control starts the watcher before Clipboard and is expected to PASS today.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fail, install_silently, ok, require_isolation  # noqa: E402

require_isolation()
import dbus  # noqa: E402
import dbus.service  # noqa: E402
from dbus.mainloop.glib import DBusGMainLoop  # noqa: E402
from gi.repository import GLib  # noqa: E402

DBusGMainLoop(set_as_default=True)
WATCHER = "org.kde.StatusNotifierWatcher"


class Watcher(dbus.service.Object):
    def __init__(self):
        bus = dbus.SessionBus()
        self.name = dbus.service.BusName(WATCHER, bus, do_not_queue=True)
        super().__init__(self.name, "/StatusNotifierWatcher")
        self.items = []

    @dbus.service.method(WATCHER, in_signature="s", out_signature="", sender_keyword="sender")
    def RegisterStatusNotifierItem(self, service, sender=None):
        self.items.append(str(sender) + ("" if str(service).startswith("/") else ":" + str(service)))

    @dbus.service.method(WATCHER, in_signature="s", out_signature="")
    def RegisterStatusNotifierHost(self, service):
        pass

    @dbus.service.method("org.freedesktop.DBus.Properties", in_signature="ss", out_signature="v")
    def Get(self, interface, prop):
        return {"RegisteredStatusNotifierItems": dbus.Array(self.items, signature="s"),
                "IsStatusNotifierHostRegistered": True, "ProtocolVersion": 0}[str(prop)]


app = sys.argv[1]
control = "--control" in sys.argv  # watcher first: proves the check itself (expected PASS)
installed = install_silently(app, "arcade.clipboard")
watcher = Watcher() if control else None
# Login autostart: the app first, the tray host a few seconds later.
proc = subprocess.Popen([str(installed), "--background"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(4)
watcher = watcher or Watcher()
loop = GLib.MainLoop()
GLib.timeout_add_seconds(10, loop.quit)
loop.run()

visible = subprocess.run(["xdotool", "search", "--onlyvisible", "--name", "^Arcade Clipboard$"],
                         capture_output=True, text=True).stdout.split()
alive = proc.poll() is None
proc.terminate()
problems = []
if not watcher.items:
    problems.append("no StatusNotifierItem registered within 10 s after the watcher appeared")
# (A first run shows the mesh set-up window even with --background, so the
# window state is reported but not asserted here.)
if not alive:
    problems.append("Clipboard exited")
if problems:
    fail("; ".join(problems))
ok(f"registered {watcher.items}; visible main windows: {len(visible)}")

#!/usr/bin/python3.12
"""firstpaint.py RUNS — time Tools' window from tray Activate to first painted frame.

Activate = what a left click on the tray icon sends (org.kde.StatusNotifierItem.Activate).
Painted = window mapped and its pixels show >= 20 distinct colours (the blank
WebKit background is one colour). Sampled every ~5 ms with Gdk."""
import sys
import time

import dbus
import gi

gi.require_version("Gdk", "3.0")
gi.require_version("GdkX11", "3.0")
from gi.repository import Gdk, GdkX11  # noqa: E402

bus = dbus.SessionBus()
dbi = dbus.Interface(bus.get_object("org.freedesktop.DBus", "/org/freedesktop/DBus"), "org.freedesktop.DBus")
w = bus.get_object("org.kde.StatusNotifierWatcher", "/StatusNotifierWatcher")
items = w.Get("org.kde.StatusNotifierWatcher", "RegisteredStatusNotifierItems", dbus_interface="org.freedesktop.DBus.Properties")
tools = None
for it in items:
    name, path = str(it).split("/", 1)
    pid = int(dbi.GetConnectionUnixProcessID(name))
    if open(f"/proc/{pid}/comm").read().strip() == "arcade-tools":
        tools = (name, "/" + path)
if not tools:
    sys.exit("Tools tray item not found")
item = dbus.Interface(bus.get_object(*tools), "org.kde.StatusNotifierItem")
display = GdkX11.X11Display.get_default()
screen = Gdk.Screen.get_default()


def tools_window():
    for win in screen.get_window_stack() or []:
        pass
    import subprocess
    out = subprocess.run(["xdotool", "search", "--onlyvisible", "--name", "^Arcade Tools Shortcuts$"], capture_output=True, text=True).stdout.split()
    return int(out[0]) if out else None


def colours(xid):
    win = GdkX11.X11Window.foreign_new_for_display(display, xid)
    if win is None:
        return 0
    w_, h_ = win.get_width(), win.get_height()
    pb = Gdk.pixbuf_get_from_window(win, 0, 0, w_, h_)
    if pb is None:
        return 0
    data = pb.get_pixels()
    step = pb.get_n_channels() * 97
    return len({data[i:i + 3] for i in range(0, len(data) - 3, step)})


import subprocess  # noqa: E402
results = []
for run in range(int(sys.argv[1])):
    x = tools_window()
    if x:
        subprocess.run(["xdotool", "key", "Escape"])
        time.sleep(1.5)
    t0 = time.perf_counter()
    subprocess.run(["xdotool", "key", "super+slash"])
    mapped = painted = None
    while time.perf_counter() - t0 < 10:
        x = tools_window()
        if x and mapped is None:
            mapped = time.perf_counter() - t0
        if x and colours(x) >= 20:
            painted = time.perf_counter() - t0
            break
        time.sleep(0.005)
    results.append((run, mapped and round(mapped * 1000), painted and round(painted * 1000)))
    print(f"run {run}: mapped {results[-1][1]} ms, painted {results[-1][2]} ms", flush=True)
    time.sleep(1)
warm = sorted(p for r, m, p in results[1:] if p)
if warm:
    print(f"warm (runs 2..): n={len(warm)} median {warm[len(warm)//2]} ms p95 {warm[min(len(warm)-1, int(len(warm)*0.95+0.999)-1)]} ms max {warm[-1]} ms")

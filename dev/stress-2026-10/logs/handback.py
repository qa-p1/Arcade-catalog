#!/usr/bin/python3.12
"""handback.py — kill -9 the Tools pid and time until each app's own SNI item is back (poll 10 ms)."""
import dbus, os, signal, sys, time, json
bus = dbus.SessionBus()
dbo = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
dbi = dbus.Interface(dbo, 'org.freedesktop.DBus')
def items():
    w = bus.get_object('org.kde.StatusNotifierWatcher', '/StatusNotifierWatcher')
    lst = w.Get('org.kde.StatusNotifierWatcher', 'RegisteredStatusNotifierItems', dbus_interface='org.freedesktop.DBus.Properties')
    out = {}
    for it in lst:
        svc = str(it).split('/')[0]
        try:
            pid = int(dbi.GetConnectionUnixProcessID(svc)); comm = open(f'/proc/{pid}/comm').read().strip()
        except Exception: comm = '?'
        out[str(it)] = comm
    return out
tools = int(sys.argv[1]); expect = int(sys.argv[2]) if len(sys.argv) > 2 else 7
before = items()
t0 = time.monotonic(); os.kill(tools, signal.SIGKILL)
seen = {}
while time.monotonic() - t0 < 5:
    now = items()
    for k, c in now.items():
        if c not in ('arcade-tools', '?') and k not in seen: seen[k] = (round((time.monotonic()-t0)*1000, 1), c)
    if len(seen) >= expect: break
    time.sleep(0.01)
print(json.dumps({'before': list(before.values()), 'returned': sorted(seen.values()), 'count': len(seen)}))

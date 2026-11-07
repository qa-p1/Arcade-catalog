"""A minimal org.kde.StatusNotifierWatcher for the isolated runner, plus tray-menu helpers.

Link's runner has no panel, so these checks register their own watcher, as a
desktop panel would, and drive an item's DBusMenu the way a user clicks it."""

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DBusGMainLoop(set_as_default=True)
WATCHER = "org.kde.StatusNotifierWatcher"


class Watcher(dbus.service.Object):
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.name = dbus.service.BusName(WATCHER, self.bus, do_not_queue=True)
        super().__init__(self.name, "/StatusNotifierWatcher")
        self.items = []  # (sender, object path)

    @dbus.service.method(WATCHER, in_signature="s", out_signature="", sender_keyword="sender")
    def RegisterStatusNotifierItem(self, service, sender=None):
        service = str(service)
        self.items.append((str(sender), service if service.startswith("/") else "/StatusNotifierItem"))

    @dbus.service.method(WATCHER, in_signature="s", out_signature="")
    def RegisterStatusNotifierHost(self, service):
        pass

    @dbus.service.method("org.freedesktop.DBus.Properties", in_signature="ss", out_signature="v")
    def Get(self, interface, prop):
        return {"RegisteredStatusNotifierItems": dbus.Array([f"{s}{p}" for s, p in self.items], signature="s"),
                "IsStatusNotifierHostRegistered": True, "ProtocolVersion": 0}[str(prop)]

    def pid_of(self, sender: str) -> int:
        dbi = dbus.Interface(self.bus.get_object("org.freedesktop.DBus", "/org/freedesktop/DBus"), "org.freedesktop.DBus")
        return int(dbi.GetConnectionUnixProcessID(sender))


def pump(seconds: float) -> None:
    loop = GLib.MainLoop()
    GLib.timeout_add(int(seconds * 1000), loop.quit)
    loop.run()


def menu_items(bus, sender: str, item_path: str) -> dict[str, int]:
    """Flattened {label: id} of an item's DBusMenu."""
    props = dbus.Interface(bus.get_object(sender, item_path), "org.freedesktop.DBus.Properties")
    menu_path = str(props.Get("org.kde.StatusNotifierItem", "Menu"))
    menu = dbus.Interface(bus.get_object(sender, menu_path), "com.canonical.dbusmenu")
    _, layout = menu.GetLayout(0, -1, ["label"])
    found = {}

    def walk(node):
        node_id, attrs, children = node
        if "label" in attrs:
            found[str(attrs["label"]).replace("_", "")] = int(node_id)
        for child in children:
            walk(child)
    walk(layout)
    return found, menu


def click(menu, item_id: int) -> None:
    menu.Event(item_id, "clicked", dbus.String("", variant_level=1), dbus.UInt32(0))

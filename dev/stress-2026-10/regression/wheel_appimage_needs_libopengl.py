#!/usr/bin/env python3
"""F5 (F-WHEEL-LIBOPENGL): the Wheel AppImage must not depend on the host's libOpenGL.so.0.

Wheel 0.3.1's bundled usr/lib/libLayerShellQtInterface.so.6 has
NEEDED libOpenGL.so.0, which linuxdeploy's exclude list leaves to the host. On a
system without the libopengl0 package (it was missing on the Ubuntu 24.04
image used for this test) a double-click does nothing:
"AppRun.wrapped: error while loading shared libraries: libOpenGL.so.0". GitHub's
runner images ship libopengl0, so CI never sees it.

Expected: every library the bundle needs is either bundled or on the
AppImage base-system list below, which does not include libOpenGL.so.0.

This check reads ELF headers only, so it needs no runner, display or root:
    python3 wheel_appimage_needs_libopengl.py PATH/ArcadeWheel-0.3.1-Linux-x86_64.AppImage
"""

import subprocess
import sys
import tempfile
from pathlib import Path

# Libraries an AppImage may take from any desktop Linux (glibc, X11/XCB, GL
# loaders that ship with Mesa/glvnd's core packages, fontconfig/freetype).
BASE = {
    "libc.so.6", "libm.so.6", "libdl.so.2", "libpthread.so.0", "librt.so.1", "ld-linux-x86-64.so.2",
    "libstdc++.so.6", "libgcc_s.so.1", "libresolv.so.2", "libutil.so.1",
    "libGL.so.1", "libEGL.so.1", "libGLX.so.0", "libGLdispatch.so.0", "libdrm.so.2", "libgbm.so.1",
    "libX11.so.6", "libX11-xcb.so.1", "libxcb.so.1", "libXext.so.6", "libXau.so.6", "libXdmcp.so.6",
    "libfontconfig.so.1", "libfreetype.so.6", "libexpat.so.1", "libz.so.1", "libasound.so.2",
    "libwayland-client.so.0", "libwayland-cursor.so.0", "libwayland-egl.so.1", "libxkbcommon.so.0",
    "libdbus-1.so.3", "libglib-2.0.so.0", "libgobject-2.0.so.0", "libgthread-2.0.so.0", "libgio-2.0.so.0",
}


def needed(path: Path) -> list[str]:
    out = subprocess.run(["readelf", "-d", str(path)], capture_output=True, text=True).stdout
    return [line.split("[", 1)[1].rstrip("]") for line in out.splitlines() if "(NEEDED)" in line]


with tempfile.TemporaryDirectory() as tmp:
    image = Path(tmp) / "wheel.AppImage"
    image.write_bytes(Path(sys.argv[1]).read_bytes())
    image.chmod(0o755)
    subprocess.run([str(image), "--appimage-extract"], cwd=tmp, capture_output=True, check=True)
    root = Path(tmp) / "squashfs-root"
    elfs = [p for p in root.rglob("*") if p.is_file() and p.read_bytes()[:4] == b"\x7fELF"]
    bundled = {p.name for p in elfs} | {p.name for p in root.rglob("*.so*")}
    wanted = {}
    for elf in elfs:
        for lib in needed(elf):
            if lib not in bundled and lib not in BASE and not lib.startswith(("libQt6", "libicu")):
                wanted.setdefault(lib, []).append(str(elf.relative_to(root)))

if "libOpenGL.so.0" in wanted:
    print(f"FAIL wheel_appimage_needs_libopengl: libOpenGL.so.0 is needed by {wanted['libOpenGL.so.0']} but not bundled")
    raise SystemExit(1)
print(f"PASS wheel_appimage_needs_libopengl: no host libOpenGL needed (other unbundled: {sorted(wanted)})")

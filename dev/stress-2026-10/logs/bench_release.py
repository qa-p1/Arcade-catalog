#!/usr/bin/env python3
"""Link v0.3.0 benchmarks/bench.py, pointed at the released (extracted) AppImages.

Same isolation, readiness signals and definitions as bench.py; only the command
lines differ. With --host, Link's fake Tools tray host (`arcade-link tray host`)
runs in the isolated session during every start, so startup with vs without a
tray host can be compared (budget: <= 5 ms added).

    python3 bench_release.py --apps find,lens --runs 20 [--host] --json out.json
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, "/home/qa/link-v030/benchmarks")
sys.path.insert(0, "/home/qa/link-v030/tools")
import bench  # noqa: E402

E = Path("/home/qa/ext")
R = lambda n: E / n / "squashfs-root"  # noqa: E731
bench.APPS.update({
    "box": {"start": [str(R("box") / "AppRun")], "ready": "box",
            "warm": [str(R("box") / "usr/bin/arcade-box"), "run", "arcade.developer.hash", "abc", "--set", "algorithm=sha256", "--json"]},
    "lens": {"start": [str(R("lens") / "AppRun"), "--background"], "ready": "lens",
             "warm": [str(R("lens") / "AppRun"), "--background"]},
    "look": {"start": [str(R("look") / "AppRun"), "--service"], "ready": "look",
             "warm": [str(R("look") / "AppRun"), "--service"]},
    "wheel": {"start": [str(R("wheel") / "AppRun"), "--background"], "ready": "wheel",
              "warm": [str(R("wheel") / "AppRun"), "--status"]},
    "shelf": {"start": [str(R("shelf") / "AppRun"), "--background"], "ready": "shelf",
              "warm": [str(R("shelf") / "AppRun"), "--status"]},
    "find": {"start": [str(R("find") / "AppRun"), "--background"], "ready": "find",
             "warm": [str(R("find") / "AppRun"), "--status"]},
    "clipboard": {"start": [str(R("clipboard") / "AppRun"), "--background"], "ready": "clipboard", "warm": None},
})

LINK = "/home/qa/bin/arcade-link"
_orig_start = bench.start


def start_with_host(app, root, env):
    host = subprocess.Popen([LINK, "tray", "host"], env=env, stdin=subprocess.PIPE,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    time.sleep(0.5)
    try:
        return _orig_start(app, root, env)
    finally:
        start_with_host.hosts.append(host)


start_with_host.hosts = []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apps", default="find,lens,look,box,shelf,wheel,clipboard")
    ap.add_argument("--runs", type=int, default=5)
    ap.add_argument("--host", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()
    if args.host:
        bench.start = start_with_host
    # bench.inner() starts its own Xvfb :97 and keyring; reuse it.
    ns = argparse.Namespace(apps=args.apps, runs=args.runs, json=args.json, compare=None, tolerance=0.05)
    try:
        bench.inner(ns)
    finally:
        for h in start_with_host.hosts:
            try:
                os.killpg(h.pid, 9)
            except ProcessLookupError:
                pass


if __name__ == "__main__":
    main()

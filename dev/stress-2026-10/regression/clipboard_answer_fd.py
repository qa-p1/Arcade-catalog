#!/usr/bin/env python3
"""F-CLIP-ANSWERFD: Clipboard's headless answers must append to stdout, whatever it is.

Clipboard 0.1.0 re-opens stdout through /proc/self/fd/$ARCADE_ANSWER_FD
(apps/flutter_app/lib/main.dart _answerSink, linux/runner/my_application.cc).
A re-opened regular file starts at offset 0, so earlier output in the same file
is overwritten, and a socket stdout cannot be re-opened at all.

Usage (inside Link's runner):
    python3 tools/e2e.py run -- python3 clipboard_answer_fd.py /path/Arcade-Clipboard-0.1.0-x86_64.AppImage
"""

import os
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fail, ok, require_isolation  # noqa: E402

require_isolation()
app = sys.argv[1]
if not os.access(app, os.X_OK):
    subprocess.run(["chmod", "+x", app], check=True)
problems = []

# 1. `{ echo header; app --version; } > file` must keep the header line.
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / "answer.txt"
    with out.open("w") as handle:
        handle.write("header line written first\n")
        handle.flush()
        subprocess.run([app, "--version"], stdout=handle, stderr=subprocess.DEVNULL, timeout=60)
    text = out.read_bytes()
    if not text.startswith(b"header line written first\n") or b"Arcade Clipboard" not in text:
        problems.append(f"redirected file content is {text[:80]!r} (header overwritten or NUL padding)")

# 2. A socket as stdout (journald, many launchers and supervisors) must work.
a, b = socket.socketpair()
result = subprocess.run([app, "--version"], stdout=b, stderr=subprocess.PIPE, timeout=60)
b.close()
answer = a.recv(200)
if result.returncode != 0 or b"Arcade Clipboard" not in answer:
    problems.append(f"socket stdout: rc={result.returncode}, answer={answer!r}, "
                    f"stderr tail={result.stderr.decode(errors='replace').strip().splitlines()[-1:]}")

if problems:
    fail("; ".join(problems))
ok("--version appends to a redirected file and answers on a socket")

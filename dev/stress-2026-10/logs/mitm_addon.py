"""mitmdump addon for the stress test. Mode from /home/qa/mitm-mode:
pass    - forward untouched
slow    - stream bodies > 1 MB at ~2 MB/s (to cut the network mid-download)
corrupt - flip one byte in the middle of bodies > 1 MB (wrong sha256)
Logs every request to /home/qa/logs/mitm.log."""
import time

from mitmproxy import http

LOG = "/home/qa/logs/mitm.log"


def mode() -> str:
    try:
        return open("/home/qa/mitm-mode").read().strip()
    except OSError:
        return "pass"


def log(msg: str) -> None:
    with open(LOG, "a") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + "\n")


def responseheaders(flow: http.HTTPFlow) -> None:
    size = int(flow.response.headers.get("content-length", "0") or 0)
    m = mode()
    log(f"{m} {flow.request.method} {flow.request.pretty_url[:140]} -> {flow.response.status_code} {size}")
    if m == "slow" and size > 1_000_000:
        def throttle(chunk: bytes) -> bytes:
            time.sleep(len(chunk) / 2_000_000)
            return chunk
        flow.response.stream = throttle
    if m == "corrupt" and size > 1_000_000:
        state = {"seen": 0, "done": False}

        def flip(chunk: bytes) -> bytes:
            # flip one byte once the stream passes the middle of the body
            if not state["done"] and chunk and state["seen"] + len(chunk) > size // 2:
                b = bytearray(chunk)
                b[0] ^= 0xFF
                state["done"] = True
                log(f"corrupted streamed byte near offset {state['seen']} of {flow.request.pretty_url[:120]}")
                chunk = bytes(b)
            state["seen"] += len(chunk)
            return chunk
        flow.response.stream = flip


def response(flow: http.HTTPFlow) -> None:
    if mode() == "corrupt" and flow.response.content and len(flow.response.content) > 1_000_000:
        body = bytearray(flow.response.content)
        body[len(body) // 2] ^= 0xFF
        flow.response.content = bytes(body)
        log(f"corrupted byte {len(body)//2} of {flow.request.pretty_url[:120]}")

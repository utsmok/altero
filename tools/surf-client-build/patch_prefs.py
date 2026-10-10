#!/usr/bin/env python3
"""Point a Zotero client source tree at a self-hosted sync server.

Rewrites (or inserts) the two default preferences from
docs/clients.md in a Zotero ``defaults/preferences/*.js`` file:

    pref("extensions.zotero.api.url", "https://example.com/");
    pref("extensions.zotero.streaming.url", "wss://example.com/stream");

The prefs win over ZOTERO_CONFIG.API_URL / ZOTERO_CONFIG.STREAMING_URL at
every call site (syncRunner.js and streamer.js both try the pref first),
so changing this defaults file is enough to redirect a fresh profile.

Usage:
    patch_prefs.py PREFS_FILE API_URL [STREAMING_URL]

STREAMING_URL defaults to API_URL with the scheme mapped https->wss,
http->ws and the path replaced by /stream, matching how the client is
documented to be pointed at altero (docs/clients.md).

Exits non-zero if the prefs are missing from the result for any reason,
so CI fails loudly instead of shipping an unpatched build.
"""

import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

API_PREF = "extensions.zotero.api.url"
STREAMING_PREF = "extensions.zotero.streaming.url"
MARKER = "SURF national Zotero server defaults (injected by altero tools/surf-client-build)"

# Matches pref("...", <anything>); including multi-line values, so small
# upstream restylings of the line do not break the match.
PREF_RE = r'pref\(\s*"%s"\s*,.*?\);'


def derive_streaming_url(api_url: str) -> str:
    parts = urlsplit(api_url)
    scheme = "wss" if parts.scheme == "https" else "ws"
    return urlunsplit((scheme, parts.netloc, "/stream", "", ""))


def normalize_api_url(api_url: str) -> str:
    # The client requires the trailing slash (docs/clients.md).
    return api_url if api_url.endswith("/") else api_url + "/"


def set_pref(text: str, name: str, value: str) -> tuple[str, str]:
    """Return (new_text, 'replaced'|'inserted')."""
    line = f'pref("{name}", "{value}");'
    pattern = re.compile(PREF_RE % re.escape(name), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(line, text, count=1), "replaced"
    if MARKER not in text:
        text += f"\n// {MARKER}\n"
    elif not text.endswith("\n"):
        text += "\n"
    return text + line + "\n", "inserted"


def check(path: Path, api_url: str, streaming_url: str) -> None:
    text = path.read_text()
    for name, value in ((API_PREF, api_url), (STREAMING_PREF, streaming_url)):
        matches = re.findall(PREF_RE % re.escape(name), text)
        if len(matches) != 1 or f'"{value}"' not in matches[0]:
            raise SystemExit(
                f"patch_prefs: {name} not set to {value!r} after patching (found {len(matches)})"
            )


def patch(path: Path, api_url: str, streaming_url: str) -> None:
    api_url = normalize_api_url(api_url)
    text = path.read_text()
    text, api_action = set_pref(text, API_PREF, api_url)
    text, stream_action = set_pref(text, STREAMING_PREF, streaming_url)
    # Atomic-ish write so a failure cannot leave a half-patched file.
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False) as f:
        f.write(text)
    Path(f.name).replace(path)
    print(f"patch_prefs: {API_PREF} {api_action}")
    print(f"patch_prefs: {STREAMING_PREF} {stream_action}")
    check(path, api_url, streaming_url)


def self_test() -> None:
    base = 'pref("extensions.zotero.streaming.enabled", true);\n'

    # Both prefs absent (the real 10.0.5 layout): inserted, once each.
    p = Path(tempfile.mkdtemp()) / "zotero.js"
    p.write_text(base)
    patch(p, "https://zotero.surf.nl", "wss://zotero.surf.nl/stream")
    out = p.read_text()
    assert out.count('pref("extensions.zotero.api.url"') == 1
    assert 'pref("extensions.zotero.streaming.url", "wss://zotero.surf.nl/stream");' in out
    assert out.startswith(base)  # untouched content above the insert

    # Idempotent: second run replaces in place, nothing duplicated.
    patch(p, "https://zotero.surf.nl/", "wss://zotero.surf.nl/stream")
    assert p.read_text() == out

    # Prefs already present upstream (possible future layout): replaced.
    q = Path(tempfile.mkdtemp()) / "zotero.js"
    q.write_text(
        base
        + '\npref("extensions.zotero.api.url", "https://api.zotero.org/");\n'
        + 'pref("extensions.zotero.streaming.url", "wss://stream.zotero.org/");\n'
    )
    patch(q, "https://zotero.surf.nl/", "wss://zotero.surf.nl/stream")
    out = q.read_text()
    assert out.count("zotero.surf.nl") == 2
    assert "api.zotero.org" not in out
    assert "stream.zotero.org" not in out
    assert out.startswith(base)

    # Streaming URL derivation follows scheme and strips any path.
    assert derive_streaming_url("https://host/path/") == "wss://host/stream"
    assert derive_streaming_url("http://host:8000/") == "ws://host:8000/stream"
    assert normalize_api_url("https://host") == "https://host/"

    print("patch_prefs: self-test passed")


def main(argv: list[str]) -> None:
    if argv[:1] == ["--self-test"]:
        self_test()
        return
    if len(argv) not in (2, 3):
        raise SystemExit(__doc__)
    path = Path(argv[0])
    api_url = argv[1]
    streaming_url = argv[2] if len(argv) == 3 else derive_streaming_url(normalize_api_url(api_url))
    patch(path, api_url, streaming_url)


if __name__ == "__main__":
    main(sys.argv[1:])

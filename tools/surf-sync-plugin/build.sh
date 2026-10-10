#!/bin/sh
# Build surf-sync.xpi (manifest.json must sit at the archive root).
# Uses python3's zipfile because zip(1) is not always installed. The XPI is
# written STORED with a compact manifest: the sideload scanner in the pinned
# Zotero 10.0.5 build rejects deflated/pretty-printed variants built with
# `python -m zipfile -c` (see the harness XPI, which is built the same way).
set -e
cd "$(dirname "$0")"
rm -f surf-sync.xpi
python3 - <<'EOF'
import json, zipfile

with open("manifest.json") as f:
    manifest = json.load(f)

with zipfile.ZipFile("surf-sync.xpi", "w") as archive:
    archive.writestr("manifest.json", json.dumps(manifest))
    with open("bootstrap.js", "rb") as bootstrap:
        archive.writestr("bootstrap.js", bootstrap.read())

with zipfile.ZipFile("surf-sync.xpi") as archive:
    for info in archive.infolist():
        print(info.filename, info.file_size, "bytes")
EOF

#!/usr/bin/env python3
"""Entry for news-image-20261124: copy the pre-rendered front page to the output path.

Standard library only. Verifies the embedded PNG (sha256 + 1 MiB cap) before
copying it byte-identically to the destination.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "4cd905376c7bce70f21554bfd11e77d1865256fab6de41eb5cb78dd6fe15941e"
MAX_BYTES = 1024 * 1024


def resolve_output():
    if len(sys.argv) > 1:
        return sys.argv[1]
    env = os.environ.get("ENTRY_OUTPUT") or os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        if os.path.isdir(env) or not env.lower().endswith(".png"):
            return os.path.join(env, "entry.png")
        return env
    return os.path.join("/output", "entry.png")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > MAX_BYTES:
        sys.exit("entry.png exceeds the 1 MiB cap")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        sys.exit("entry.png sha256 mismatch: " + digest)
    dest = resolve_output()
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, dest)
    with open(dest, "rb") as f:
        written = f.read()
    if written != data:
        sys.exit("output is not byte-identical to the source image")
    if os.path.getsize(dest) != len(data):
        sys.exit("output size does not match the source image")
    print("wrote %s (%d bytes, sha256 %s)" % (dest, len(data), digest))


if __name__ == "__main__":
    main()

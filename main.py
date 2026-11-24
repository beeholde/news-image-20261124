#!/usr/bin/env python3
"""news-image-20261124 v2: write the pre-rendered front page to the output.

The entry image is a 1024x1024 PNG, "THE WORLD TODAY — Tuesday 24 November
2026, Late Edition": 42 day-tagged stories across 9 regions, with the CAS
Senegal ruling, Champions League Matchday 5 and the Tuesday market fade as
the three lead stories, plus an explicit DATE CHECK box.

Standard library only. This program checks the bundled image against its
known sha256 and the 1 MiB size limit, copies it to the output path, and
then re-checks the copy byte for byte before exiting.
"""

import hashlib
import os
import shutil
import sys

IMAGE_NAME = "entry.png"
IMAGE_SHA256 = "3222a9c4879a4ad0f72e0f323b831054dacbd4a8b961da0ad2f3bd38b1a6ab7c"
SIZE_LIMIT = 1_000_000


def _digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE_NAME)
    out = os.environ.get("ENTRY_OUTPUT") or "/output/entry.png"
    if len(argv) > 1:
        out = argv[1]

    if os.path.getsize(src) > SIZE_LIMIT:
        raise SystemExit("entry image over the 1 MiB limit")
    if _digest(src) != IMAGE_SHA256:
        raise SystemExit("entry image sha256 does not match the expected value")

    parent = os.path.dirname(os.path.abspath(out))
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, out)
    if os.path.getsize(out) != os.path.getsize(src):
        raise SystemExit("written output size does not match the source image")
    if _digest(out) != IMAGE_SHA256:
        raise SystemExit("written output failed its sha256 check")
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main(sys.argv)

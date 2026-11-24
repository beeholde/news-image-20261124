#!/usr/bin/env python3
"""news-image-20261124: copy the pre-rendered entry image to the output.

Stdlib only. The entry image is a 1024x1024 PNG summing up 24 November
2026 world news ("THE WORLD TODAY" broadsheet, 33 stories, 8 regions,
explicit DATE CHECK). This program verifies the embedded image's sha256
and 1 MiB size cap, then copies it to the output path.
"""

import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "15fdca46822057f61a689b4689b75fb579039cd27369542e4cecb54363ebe793"
MAX_BYTES = 1_000_000
SRC_NAME = "entry.png"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out = os.environ.get("ENTRY_OUTPUT") or "/output/entry.png"
    if len(sys.argv) > 1:
        out = sys.argv[1]

    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png exceeds the 1 MiB cap: %d bytes" % len(data))
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("entry.png sha256 mismatch: %s" % digest)

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    shutil.copyfile(src, out)
    # verify the copy byte-for-byte before reporting success
    with open(out, "rb") as fh:
        if hashlib.sha256(fh.read()).hexdigest() != EXPECTED_SHA256:
            raise SystemExit("output copy failed verification")
    print("wrote %s (%d bytes, sha256 %s)" % (out, len(data), digest))


if __name__ == "__main__":
    main()

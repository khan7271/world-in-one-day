#!/usr/bin/env python3
"""news-image-20261118 entry: copy the repo-held broadsheet image to the
output path. Standard library only, no network, deterministic: the bytes
written are exactly the bytes of entry.png beside this file.

Run:  python3 main.py            (writes /output/entry.png)
      MAKEFUN_OUTPUT_DIR=out python3 main.py   (writes out/entry.png)
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT_PATH = os.path.join(OUT_DIR, "entry.png")
SRC_PATH = os.path.join(HERE, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC_PATH, OUT_PATH)
    print("wrote", OUT_PATH, os.path.getsize(OUT_PATH), "bytes")


if __name__ == "__main__":
    main()

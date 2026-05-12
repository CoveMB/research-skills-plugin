#!/usr/bin/env python3
"""Package this plugin directory as a zip."""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, default=Path("scholarly-research-book-plugin-v1.0.0.zip"))
    args = parser.parse_args()
    root = args.root.resolve()
    out = args.out.resolve()
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(root.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                zf.write(p, root.name + "/" + str(p.relative_to(root)))
    print(f"Wrote {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

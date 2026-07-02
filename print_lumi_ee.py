#!/usr/bin/env python3
"""Print the lumi_ee value from a GUINEA-PIG luminosity.out file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


LUMI_EE_RE = re.compile(r"^lumi_ee=([0-9.eE+-]+);", re.MULTILINE)


def lumi_ee(path: Path) -> str:
    text = path.read_text(encoding="ascii", errors="replace")
    match = LUMI_EE_RE.search(text)
    if match is None:
        raise ValueError(f"Could not find lumi_ee in {path}")
    return match.group(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print the total luminosity from a GUINEA-PIG output file containing lumi_ee."
    )
    parser.add_argument("filename", type=Path, help="GUINEA-PIG luminosity output file")
    args = parser.parse_args()

    # Convert to the correct units
    n_b = 312.0 # number of bunches per pulse
    f_rep = 50.0 # number of collisions/sec
    conv = 1.0e4 # conversion from m-2 to cm-2

    lum_ee_per_bx = float(lumi_ee(args.filename))

    lum_ee_tot = (lum_ee_per_bx*n_b*f_rep/conv)

    print("Luminosity [cm^-2] = %.2e"%(lum_ee_tot))


if __name__ == "__main__":
    main()

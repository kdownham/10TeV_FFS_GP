#!/usr/bin/env python3
"""Print RMS beam sizes from a GUINEA-PIG particle .ini file in nm."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def load_beam(path: Path) -> np.ndarray:
    data = np.loadtxt(path)
    if data.ndim == 1:
        data = data.reshape(1, -1)
    if data.shape[1] < 4:
        raise ValueError(
            f"{path} has {data.shape[1]} columns; expected at least 4 "
            "(energy_GeV, x_um, y_um, z_um, ...)"
        )
    return data


def rms_nm(values_um: np.ndarray) -> float:
    return float(np.std(values_um) * 1000.0)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print RMS x, y, and z beam sizes from a GUINEA-PIG .ini file in nm."
    )
    parser.add_argument("filename", type=Path, help="GUINEA-PIG particle .ini file")
    args = parser.parse_args()

    data = load_beam(args.filename)
    print(f"file={args.filename}")
    print(f"particles={data.shape[0]}")
    print(f"rms_x_nm={rms_nm(data[:, 1]):.12g}")
    print(f"rms_y_nm={rms_nm(data[:, 2]):.12g}")
    print(f"rms_z_nm={rms_nm(data[:, 3]):.12g}")


if __name__ == "__main__":
    main()

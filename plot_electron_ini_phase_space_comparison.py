#!/usr/bin/env python3
"""Compare phase-space scatter plots for electron.ini and electron_placet_SR.ini."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).with_name(".matplotlib")))

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
FILES = {
    "Xsuite": ROOT / "electron.ini",
    "PLACET SR": ROOT / "electron_placet_SR.ini",
}
OUT_PNG = ROOT / "electron_ini_vs_placet_sr_phase_space_scatter.png"


def load_inputs() -> dict[str, np.ndarray]:
    loaded: dict[str, np.ndarray] = {}
    for label, path in FILES.items():
        data = np.loadtxt(path)
        if data.ndim != 2 or data.shape[1] != 6:
            raise ValueError(f"{path} should have six columns, got shape {data.shape}")
        loaded[label] = data
    return loaded


def limits(arrays: list[np.ndarray]) -> tuple[float, float]:
    values = np.concatenate([array[np.isfinite(array)] for array in arrays])
    low = float(np.min(values))
    high = float(np.max(values))
    span = high - low
    if span == 0.0:
        span = 1.0
    pad = 0.055 * span
    return low - pad, high + pad


def rms(values: np.ndarray) -> float:
    return float(np.std(values))


def main() -> None:
    data = load_inputs()
    labels = list(data)
    planes = [
        ("x [um]", "x' [urad]", 1, 4, "x vs x'"),
        ("y [um]", "y' [urad]", 2, 5, "y vs y'"),
        ("z [um]", "energy [GeV]", 3, 0, "z vs energy"),
    ]
    colors = {"Xsuite": "#0f766e", "PLACET SR": "#c2410c"}

    fig, axes = plt.subplots(
        len(planes),
        len(labels),
        figsize=(13.5, 12.0),
        constrained_layout=True,
    )

    for row, (xlabel, ylabel, x_col, y_col, title) in enumerate(planes):
        xlim = limits([data[label][:, x_col] for label in labels])
        ylim = limits([data[label][:, y_col] for label in labels])
        for col, label in enumerate(labels):
            ax = axes[row, col]
            x = data[label][:, x_col]
            y = data[label][:, y_col]
            ax.scatter(
                x,
                y,
                s=1.0,
                alpha=0.16,
                color=colors[label],
                linewidths=0,
                rasterized=True,
            )
            ax.axhline(0.0, color="#404040", linewidth=0.8, alpha=0.55)
            ax.axvline(0.0, color="#404040", linewidth=0.8, alpha=0.55)
            ax.set_xlim(*xlim)
            ax.set_ylim(*ylim)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.grid(True, alpha=0.24)
            ax.set_title(f"{label}: {title}")
            ax.text(
                0.02,
                0.98,
                "\n".join(
                    [
                        f"N={x.size}",
                        f"x mean={np.mean(x):.6g}",
                        f"x rms={rms(x):.6g}",
                        f"y mean={np.mean(y):.6g}",
                        f"y rms={rms(y):.6g}",
                    ]
                ),
                transform=ax.transAxes,
                ha="left",
                va="top",
                fontsize=7.8,
                bbox={"facecolor": "white", "edgecolor": "#d4d4d4", "alpha": 0.88},
            )

    fig.suptitle("electron.ini vs electron_placet_SR.ini phase-space scatter comparison", fontsize=15)
    fig.savefig(OUT_PNG, dpi=170)
    plt.close(fig)
    print(f"wrote={OUT_PNG}")


if __name__ == "__main__":
    main()

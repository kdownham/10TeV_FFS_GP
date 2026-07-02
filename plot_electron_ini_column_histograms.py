#!/usr/bin/env python3
"""Compare column histograms for electron.ini and electron_placet_SR.ini."""

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
OUT_PNG = ROOT / "electron_ini_vs_placet_sr_column_histograms.png"
COLUMNS = [
    ("Energy [GeV]", 0),
    ("x [um]", 1),
    ("y [um]", 2),
    ("z [um]", 3),
    ("x' [urad]", 4),
    ("y' [urad]", 5),
]


def load_inputs() -> dict[str, np.ndarray]:
    loaded: dict[str, np.ndarray] = {}
    for label, path in FILES.items():
        data = np.loadtxt(path)
        if data.ndim != 2 or data.shape[1] != 6:
            raise ValueError(f"{path} should have six columns, got shape {data.shape}")
        loaded[label] = data
    return loaded


def common_bins(values_a: np.ndarray, values_b: np.ndarray, n_bins: int = 160) -> np.ndarray:
    values = np.concatenate([values_a, values_b])
    low = float(np.min(values))
    high = float(np.max(values))
    if low == high:
        low -= 0.5
        high += 0.5
    return np.linspace(low, high, n_bins + 1)


def stats_text(values: np.ndarray) -> str:
    return "\n".join(
        [
            f"N={values.size}",
            f"mean={np.mean(values):.6g}",
            f"rms={np.std(values):.6g}",
        ]
    )


def main() -> None:
    data = load_inputs()
    labels = list(data)
    fig, axes = plt.subplots(
        len(COLUMNS),
        len(labels),
        figsize=(13.5, 18.0),
        sharey="row",
        constrained_layout=True,
    )

    colors = {"Xsuite": "#0f766e", "PLACET SR": "#c2410c"}
    for row, (column_label, column_index) in enumerate(COLUMNS):
        bins = common_bins(*(data[label][:, column_index] for label in labels))
        for col, label in enumerate(labels):
            ax = axes[row, col]
            values = data[label][:, column_index]
            ax.hist(
                values,
                bins=bins,
                color=colors[label],
                alpha=0.82,
                edgecolor="white",
                linewidth=0.15,
            )
            ax.axvline(np.mean(values), color="#202020", linewidth=0.9)
            ax.set_xlabel(column_label)
            ax.grid(True, alpha=0.25)
            ax.text(
                0.02,
                0.98,
                stats_text(values),
                transform=ax.transAxes,
                ha="left",
                va="top",
                fontsize=8.2,
                bbox={"facecolor": "white", "edgecolor": "#d4d4d4", "alpha": 0.9},
            )
            if row == 0:
                ax.set_title(label)
            if col == 0:
                ax.set_ylabel("Number of particles per bin")

    fig.suptitle("electron.ini vs electron_placet_SR.ini column histograms", fontsize=15)
    fig.savefig(OUT_PNG, dpi=170)
    plt.close(fig)
    print(f"wrote={OUT_PNG}")


if __name__ == "__main__":
    main()

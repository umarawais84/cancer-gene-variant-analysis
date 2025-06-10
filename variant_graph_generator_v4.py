#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
┌─────────────────────────────────────────────────────┐
│ Variant Graph Generator                             │
│ Author: Umar Awais                                  │
│ Date: June 5, 2025                                  │
└─────────────────────────────────────────────────────┘
"""

import os
import sys
import importlib.util
from typing import Dict, List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Dependency Check
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def check_and_install_dependencies():
    required = ["numpy", "pandas", "matplotlib"]
    missing = [pkg for pkg in required if importlib.util.find_spec(pkg) is None]
    if missing:
        print(f"Missing required packages: {', '.join(missing)}")
        sys.exit(1)

check_and_install_dependencies()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATA_DIR   = os.path.dirname(os.path.abspath(__file__))
CSV_FILES  = [f"early_late_var{v}.csv" for v in range(16, 22)]
SEQUENCERS = ["China MGISEQ-2000", "DE MiniSeq", "UK HiSeq 2500"]

# Containers for raw percentages
early_data: Dict[str, List[float]] = {seq: [] for seq in SEQUENCERS}
late_data:  Dict[str, List[float]] = {seq: [] for seq in SEQUENCERS}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Load Data
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_variant_data():
    for file in CSV_FILES:
        path = os.path.join(DATA_DIR, file)
        df = pd.read_csv(path, index_col=0).replace(-1, 0)
        for seq in SEQUENCERS:
            early_data[seq].append(df.loc[seq, "early"])
            late_data[seq].append(df.loc[seq, "late"])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Visualization (with averaging)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def create_split_graph():
    variant_nums   = list(range(16, 22))
    variant_labels = [f"Variant {n}" for n in variant_nums]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), sharey=True)
    x = np.arange(len(variant_labels))
    colors = {seq: f"C{i}" for i, seq in enumerate(SEQUENCERS)}

    for ax, dataset, title in zip(
        [ax1, ax2],
        [early_data, late_data],
        ["Early Variants", "Late Variants"]
    ):
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_ylim(0, 100)            # fixed 0–100% scale
        ax.set_xticks(x)
        ax.set_xticklabels(variant_labels)
        ax.grid(axis="y", linestyle="--", alpha=0.3)

        for i in range(len(variant_labels)):
            # count only sequencers with non-zero raw values
            raw_vals = [dataset[seq][i] for seq in SEQUENCERS if dataset[seq][i] > 0]
            count = len(raw_vals)
            if count == 0:
                continue

            bottom = 0
            # each segment = raw_value / count
            for seq in SEQUENCERS:
                raw = dataset[seq][i]
                if raw <= 0:
                    continue
                segment = raw / count
                ax.bar(
                    x[i],
                    segment,
                    bottom=bottom,
                    color=colors[seq],
                    edgecolor="white",
                    linewidth=0.5,
                    alpha=0.8
                )
                bottom += segment

    ax1.set_ylabel("Percentage (%)", fontsize=14)
    fig.suptitle("Variant Distribution by Sequencer (Averaged)", fontsize=16, fontweight="bold")

    # legend
    legend_elements = [Patch(facecolor=colors[seq], edgecolor="white") for seq in SEQUENCERS]
    legend_labels   = SEQUENCERS
    plt.figlegend(
        handles=legend_elements,
        labels=legend_labels,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.02),
        ncol=3,
        frameon=True,
        fontsize=12,
    )

    plt.tight_layout(rect=[0, 0.12, 1, 0.95])
    return fig

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main Execution
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    load_variant_data()
    fig = create_split_graph()
    fig.savefig("variant_distribution_averaged.png", dpi=300, bbox_inches="tight")
    print("✅ Graph saved as 'variant_distribution_averaged.png'")
    plt.show()

if __name__ == "__main__":
    main()

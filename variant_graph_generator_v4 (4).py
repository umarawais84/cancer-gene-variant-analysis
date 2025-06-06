#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
┌─────────────────────────────────────────────────────┐
│ Variant Graph Generator                             │
│ Author: Umar Awais                                  │
│ Date: June 5, 2025                                  │
└─────────────────────────────────────────────────────┘
"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DEPENDENCY MANAGEMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import os
import sys
import importlib.util
from typing import Dict, List, Tuple


def check_and_install_dependencies() -> None:
    """✦ Verify all required dependencies are available"""
    required_packages = ["numpy", "pandas", "matplotlib"]
    missing_packages = []

    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)

    if missing_packages:
        print(f"⚠️  Missing required packages: {', '.join(missing_packages)}")
        install = input("Would you like to install them now? (y/n): ")
        if install.lower() == "y":
            import subprocess

            for package in missing_packages:
                print(f"📦 Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print("✅ All dependencies installed successfully")
        else:
            print("❌ Cannot continue without required dependencies")
            sys.exit(1)


# Run dependency check
check_and_install_dependencies()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# IMPORTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DATA_DIR = os.path.dirname(os.path.abspath(__file__)) # Directory of this script
CSV_FILES = [
    "early_late_var16.csv",
    "early_late_var17.csv",
    "early_late_var18.csv",
    "early_late_var19.csv",
    "early_late_var20.csv",
    "early_late_var21.csv",
]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA PROCESSING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """✦ Replace invalid values (-1) with zeros"""
    return df.replace(-1, 0)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA CONTAINERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SEQUENCERS = ["China MGISEQ-2000", "DE MiniSeq", "UK HiSeq 2500"]

early_data: Dict[str, List[float]] = {seq: [] for seq in SEQUENCERS}
late_data: Dict[str, List[float]] = {seq: [] for seq in SEQUENCERS}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA COLLECTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def load_variant_data() -> None:
    """✦ Load and process data from all variant CSV files"""
    for file in CSV_FILES:
        file_path = os.path.join(DATA_DIR, file)
        var_num = file.split("var")[1].split(".")[0] # Extract variant number

        # Process each file
        df = pd.read_csv(file_path, index_col=0)
        df = clean_data(df)

        # Store data by sequencer
        for sequencer in SEQUENCERS:
            early_data[sequencer].append(df.loc[sequencer, "early"])
            late_data[sequencer].append(df.loc[sequencer, "late"])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# VISUALIZATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def create_split_graph() -> plt.Figure:
    """✦ Create stacked bar charts with early and late data for each variant"""
    variant_nums = list(range(16, 22))
    variant_labels = [f"Variant {num}" for num in variant_nums]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), sharey=True)
    x_positions = np.arange(len(variant_labels))
    colors = {seq: f"C{idx}" for idx, seq in enumerate(SEQUENCERS)}
    
    # Set y-axis limit to 100%
    ax1.set_ylim(0, 100)
    ax2.set_ylim(0, 100)

    # Early variants subplot
    ax1.set_title("Early Variants", fontsize=14, fontweight="bold")

    for var_idx in range(len(variant_labels)):
        bottom = 0
        valid_seqs = [seq for seq in SEQUENCERS if early_data[seq][var_idx] > 0]
        
        if not valid_seqs:
            continue

        for sequencer in SEQUENCERS:
            if early_data[sequencer][var_idx] <= 0:
                continue

            # Use the actual percentage value directly
            segment_height = early_data[sequencer][var_idx]

            ax1.bar(
                x_positions[var_idx],
                segment_height,
                bottom=bottom,
                color=colors[sequencer],
                alpha=0.8,
                edgecolor="white",
                linewidth=0.5,
            )
            bottom += segment_height

    ax1.set_ylabel("Percentage (%)", fontsize=14)
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(variant_labels)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.grid(axis="y", linestyle="--", alpha=0.3)

    # Late variants subplot
    ax2.set_title("Late Variants", fontsize=14, fontweight="bold")

    for var_idx in range(len(variant_labels)):
        bottom = 0
        valid_seqs = [seq for seq in SEQUENCERS if late_data[seq][var_idx] > 0]
        
        if not valid_seqs:
            continue

        for sequencer in SEQUENCERS:
            if late_data[sequencer][var_idx] <= 0:
                continue

            # Use the actual percentage value directly
            segment_height = late_data[sequencer][var_idx]

            ax2.bar(
                x_positions[var_idx],
                segment_height,
                bottom=bottom,
                color=colors[sequencer],
                alpha=0.8,
                edgecolor="white",
                linewidth=0.5,
            )
            bottom += segment_height

    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(variant_labels)
    ax2.grid(axis="y", linestyle="--", alpha=0.3) # Added dotted grid to late variants graph

    fig.suptitle("Variant Distribution by Sequencer", fontsize=16, fontweight="bold")

    # Fix the legend to ensure all sequencers are shown
    legend_elements = [
        Patch(facecolor=colors[seq], edgecolor="white", label=seq) for seq in SEQUENCERS
    ]

    plt.figlegend(
        handles=legend_elements,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.02),
        ncol=3,
        frameon=True,
        fancybox=True,
        shadow=True,
        fontsize=12,
    )

    plt.tight_layout(rect=[0, 0.12, 1, 0.95])

    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN EXECUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main() -> None:
    """✦ Main execution function"""
    load_variant_data()

    # Generate the visualization
    fig = create_split_graph()

    # Make sure all elements are displayed
    plt.rcParams["figure.constrained_layout.use"] = True

    # Save the figure as a high-resolution PNG
    fig.savefig("variant_distribution.png", dpi=300, bbox_inches="tight")
    print("✅ Graph saved as 'variant_distribution.png'")

    # Display the visualization
    plt.show()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
┌─────────────────────────────────────────────────────┐
│ Variant Graph Generator                             │
│ Author: Umar Awais                                  │
│ Date: June 1, 2025                                  │
└─────────────────────────────────────────────────────┘
"""

# ─── DEPENDENCY MANAGEMENT ─────────────────────────────────────────────────
import os
import sys
import importlib.util
from typing import Dict, List, Tuple


# check and install required packages if needed
def check_and_install_dependencies():
    """Verify all required dependencies are available"""
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


# run dependency check
check_and_install_dependencies()

# ─── IMPORTS ─────────────────────────────────────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ─── CONFIGURATION ──────────────────────────────────────────────────────────
DATA_DIR = os.path.dirname(os.path.abspath(__file__)) # directory of this script
CSV_FILES = [
    "early_late_var16.csv",
    "early_late_var17.csv",
    "early_late_var18.csv",
    "early_late_var19.csv",
    "early_late_var20.csv",
    "early_late_var21.csv",
]


# ─── DATA PROCESSING ───────────────────────────────────────────────────────
def clean_data(df):
    """Replace invalid values (-1) with zeros"""
    return df.replace(-1, 0)


# ─── DATA CONTAINERS ────────────────────────────────────────────────────────
SEQUENCERS = ["China MGISEQ-2000", "DE MiniSeq", "UK HiSeq 2500"]

early_data = {seq: [] for seq in SEQUENCERS}
late_data = {seq: [] for seq in SEQUENCERS}


# ─── DATA COLLECTION ───────────────────────────────────────────────────────
def load_variant_data():
    """Load and process data from all variant CSV files"""
    for file in CSV_FILES:
        file_path = os.path.join(DATA_DIR, file)
        # extract variant number from filename
        var_num = file.split("var")[1].split(".")[0]

        # process each file
        df = pd.read_csv(file_path, index_col=0)
        df = clean_data(df)

        # store data by sequencer
        for sequencer in SEQUENCERS:
            early_data[sequencer].append(df.loc[sequencer, "early"])
            late_data[sequencer].append(df.loc[sequencer, "late"])


# ─── VISUALIZATION SETUP ────────────────────────────────────────────────────
def setup_visualization():
    """Configure visualization parameters"""
    # create variant labels (16-21)
    variant_labels = [f"Variant {num}" for num in range(16, 22)]

    # setup figure with appropriate dimensions
    plt.figure(figsize=(12, 8))

    return variant_labels


# execute data loading
load_variant_data()

# setup visualization environment
variant_labels = setup_visualization()


# ─── CHART RENDERING ───────────────────────────────────────────────────────
def create_stacked_bar_chart(variant_labels):
    """Create stacked bar chart visualization"""
    # bar styling parameters
    BAR_WIDTH = 0.3
    x_positions = np.arange(len(variant_labels))

    # generate visualization for each sequencer
    for idx, sequencer in enumerate(SEQUENCERS):
        # calculate position offset for each sequencer group
        pos = x_positions - BAR_WIDTH + (idx * BAR_WIDTH)

        # early data bars (bottom layer)
        plt.bar(
            pos,
            early_data[sequencer],
            width=BAR_WIDTH,
            label=f"{sequencer} (Early)",
            color=f"C{idx}",
            alpha=0.7,
        )

        # late data bars (top layer)
        plt.bar(
            pos,
            late_data[sequencer],
            width=BAR_WIDTH,
            label=f"{sequencer} (Late)",
            bottom=early_data[sequencer],
            color=f"C{idx}",
            alpha=1.0,
            hatch="///",
        )

    # chart aesthetics
    plt.xlabel("Variants", fontsize=14)
    plt.ylabel("Percentage (%)", fontsize=14)
    plt.title("Variant Distribution by Sequencer (Early vs Late)", fontsize=16)
    plt.xticks(x_positions - BAR_WIDTH / 2, variant_labels, fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    return plt


# ─── MAIN EXECUTION ────────────────────────────────────────────────────────
def main():
    """Main execution function"""
    # generate the chart
    plt = create_stacked_bar_chart(variant_labels)

    # finalize and save output
    plt.tight_layout()
    plt.savefig("variant_distribution.png", dpi=300)
    print("✓ Graph saved as 'variant_distribution.png'")

    # display the visualization
    plt.show()


if __name__ == "__main__":
    main()

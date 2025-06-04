#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
┌─────────────────────────────────────────────────────┐
│ Variant Graph Generator                             │
│ Author: Umar Awais                                  │
│ Date: June 3, 2025                                  │
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
    """✦ Create a split bar chart with early and late data separated"""
    # Create variant labels (16-21)
    variant_nums = list(range(16, 22))
    variant_labels = [f"Variant {num}" for num in variant_nums]
    
    # Set up figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8), sharey=True)
    
    # Bar styling parameters
    bar_width = 0.25
    x_positions = np.arange(len(variant_labels))
    
    # LEFT SUBPLOT: Early Data (Solid)
    # ──────────────────────────────────────────────────────────────────────
    ax1.set_title("Early Variants", fontsize=14, fontweight='bold')
    
    for idx, sequencer in enumerate(SEQUENCERS):
        # Calculate position offset for each sequencer
        pos = x_positions + (idx - 1) * bar_width
        
        # Plot early data bars
        ax1.bar(
            pos,
            early_data[sequencer],
            width=bar_width,
            label=f"{sequencer}",
            color=f"C{idx}",
            alpha=0.8,
        )
    
    ax1.set_ylabel("Percentage (%)", fontsize=14)
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(variant_labels)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    # RIGHT SUBPLOT: Late Data (Hatched)
    # ──────────────────────────────────────────────────────────────────────
    ax2.set_title("Late Variants", fontsize=14, fontweight='bold')
    
    for idx, sequencer in enumerate(SEQUENCERS):
        # Calculate position offset for each sequencer
        pos = x_positions + (idx - 1) * bar_width
        
        # Plot late data bars with hatching
        ax2.bar(
            pos,
            late_data[sequencer],
            width=bar_width,
            label=f"{sequencer}",
            color=f"C{idx}",
            alpha=0.8,
            hatch="///"
        )
    
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels(variant_labels)
    
    # SHARED FIGURE ELEMENTS
    # ──────────────────────────────────────────────────────────────────────
    fig.suptitle("Variant Distribution by Sequencer", fontsize=16, fontweight='bold')
    
    # Only show legend once for the entire figure
    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(
        handles, 
        labels, 
        loc="upper center", 
        bbox_to_anchor=(0.5, 0.03), 
        ncol=len(SEQUENCERS)
    )
    
    plt.tight_layout(rect=[0, 0.08, 1, 0.95]) # Adjust for legend at bottom
    
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN EXECUTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main() -> None:
    """✦ Main execution function"""
    # Load the data
    load_variant_data()
    
    # Generate the visualization
    fig = create_split_graph()
    
    # Save the figure as a high-resolution PNG
    fig.savefig("variant_distribution.png", dpi=300, bbox_inches="tight")
    print("✅ Graph saved as 'variant_distribution.png'")
    
    # Display the visualization
    plt.show()


if __name__ == "__main__":
    main()
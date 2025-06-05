#!/usr/bin/env python3
import pandas as pd
import os

# Load Excel data
excel_path = 'early_late_groups_3_locations.xlsx'
excel_df = pd.read_excel(excel_path)
print("Excel data (first 3 rows):")
print(excel_df.head(3))
print("\n")

# Sequencers
SEQUENCERS = ["China MGISEQ-2000", "DE MiniSeq", "UK HiSeq 2500"]

# Load CSV data
csv_files = [f for f in os.listdir('.') if f.startswith('early_late_var') and f.endswith('.csv')]
csv_files.sort()

print("CSV data:")
for file in csv_files:
    print(f"=== {file} ===")
    df = pd.read_csv(file, index_col=0)
    # Replace -1 with 0
    df = df.replace(-1, 0)
    print(df)
    print()

print("Comparing percentages between Excel and CSV files:")
for file in csv_files:
    var_num = file.split("var")[1].split(".")[0]
    print(f"\nVariant {var_num}:")
    
    csv_df = pd.read_csv(file, index_col=0)
    csv_df = csv_df.replace(-1, 0)
    
    excel_early_col = f"early var{var_num}"
    excel_late_col = f"late var{var_num}"
    
    for seq in SEQUENCERS:
        excel_early = excel_df.loc[excel_df["Unnamed: 0"] == seq, excel_early_col].values[0]
        excel_late = excel_df.loc[excel_df["Unnamed: 0"] == seq, excel_late_col].values[0]
        
        csv_early = csv_df.loc[seq, "early"] if csv_df.loc[seq, "early"] != -1 else 0
        csv_late = csv_df.loc[seq, "late"]
        
        print(f"{seq}:")
        print(f"  Early: Excel={excel_early}, CSV={csv_early}")
        print(f"  Late: Excel={excel_late}, CSV={csv_late}")

print("\nChecking how data is displayed in the graph:")
print("In our current implementation, we calculate:")
print("segment_height = data[sequencer][var_idx] / total_seqs")
print("Where total_seqs is the number of sequencers with non-zero values")
print("\nThis means we're adjusting the percentages to sum to 100% per variant.")

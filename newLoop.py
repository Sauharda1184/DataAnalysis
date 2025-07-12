import pandas as pd
import os
import matplotlib.pyplot as plt

# Define dataset directories
base_path = "/home/sauharda/Desktop/webExtract"

# A Python dictionary to hold the dataset paths for NO2 and SO2
datasets = {
    "NO2": os.path.join(base_path, "NO2", "Extracted files"),
    "SO2": os.path.join(base_path, "SO2", "Extracted files")
}

# Define output directories for summaries
output_dirs = {
    "NO2": os.path.join(base_path, "no2_summary"),
    "SO2": os.path.join(base_path, "so2_summary")
}

# Create output directories if they don't exist
for output_dir in output_dirs.values():
    os.makedirs(output_dir, exist_ok=True)

# Process each gas (NO2 and SO2)
for gas, folder in datasets.items():
    print(f"\nProcessing {gas} data from folder: {folder}")

    for filename in sorted(os.listdir(folder)):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder, filename)
            print(f"Reading: {filename}")

            try:
                # Read CSV file
                df = pd.read_csv(file_path, low_memory=False)

                # Verify required columns are present
                required_cols = {'State Code', 'County Code', 'Sample Duration', 'Arithmetic Mean', '1st Max Value'}
                if not required_cols.issubset(df.columns):
                    print(f"Skipping {filename}: missing required columns.")
                    continue

                # Extract year from filename
                year = filename[-8:-4]

                # Create countyfips column
                df['countyfips'] = df['State Code'] * 1000 + df['County Code']

                # Normalize Sample Duration column
                df['Sample Duration'] = df['Sample Duration'].astype(str).str.strip().str.upper()

                # Filter only 1 HOUR rows
                df_1hr = df[df['Sample Duration'] == '1 HOUR']

                print(f"{filename}: total rows = {len(df)}, '1 HOUR' rows = {len(df_1hr)}")

                # Group and summarize
                summary = df_1hr.groupby('countyfips').agg(
                    mean_val=pd.NamedAgg(column='Arithmetic Mean', aggfunc='mean'),
                    max_val=pd.NamedAgg(column='1st Max Value', aggfunc='mean')
                ).reset_index()

                # Add year column as string
                summary['year'] = str(year)

                # Show preview
                print(summary.head())

                # Save to output folder
                output_path = os.path.join(output_dirs[gas], f"{gas}_{year}_summary.csv")
                summary.to_csv(output_path, index=False)
                print(f"Saved summary to: {output_path}")

            except Exception as e:
                print(f"Error reading {filename}: {e}")

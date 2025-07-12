import pandas as pd
import os
import traceback

# Define base dataset path
base_path = "/home/sauharda/Desktop/webExtract"

# Paths for NO2 and SO2 extracted files
datasets = {
    "NO2": os.path.join(base_path, "NO2", "Extracted files"),
    "SO2": os.path.join(base_path, "SO2", "Extracted files")
}

# Output directories for summaries
output_dirs = {
    "NO2": os.path.join(base_path, "no2_summary"),
    "SO2": os.path.join(base_path, "so2_summary")
}

# Ensure output directories exist
for path in output_dirs.values():
    os.makedirs(path, exist_ok=True)

# Loop through each pollutant
for gas, folder in datasets.items():
    print(f"\nProcessing {gas} data from folder: {folder}")
    
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            print(f"Reading: {filename}")
            try:
                file_path = os.path.join(folder, filename)
                df = pd.read_csv(file_path, low_memory=False)

                # Ensure necessary columns exist
                required_cols = {'State Code', 'County Code', 'Sample Duration', 'Arithmetic Mean', '1st Max Value'}
                if not required_cols.issubset(df.columns):
                    print(f"Skipping {filename}: Missing one or more required columns.")
                    continue

                # Convert codes to integers
                df['State Code'] = pd.to_numeric(df['State Code'], errors='coerce')
                df['County Code'] = pd.to_numeric(df['County Code'], errors='coerce')
                df = df.dropna(subset=['State Code', 'County Code'])

                df['State Code'] = df['State Code'].astype(int)
                df['County Code'] = df['County Code'].astype(int)

                # Create countyfips column
                df['countyfips'] = df['State Code'] * 1000 + df['County Code']

                # Filter rows for '1 HOUR'
                df_1hr = df[df['Sample Duration'] == '1 HOUR']

                # Extract year from filename
                year = filename[-8:-4]
                print(f"Extracted year: {year} (type: {type(year)})")

                # Group and summarize
                summary = df_1hr.groupby('countyfips').agg(
                    mean_val=pd.NamedAgg(column='Arithmetic Mean', aggfunc='mean'),
                    max_val=pd.NamedAgg(column='1st Max Value', aggfunc='mean')
                ).reset_index()

                # Add year column to summary
                summary['year'] = int(year)

                # Output path
                output_path = os.path.join(output_dirs[gas], f"{gas}_{year}_summary.csv")
                summary.to_csv(output_path, index=False)
                print(f"Saved summary to: {output_path}")

            except Exception as e:
                print(f"Error reading {filename}: {e}")
                traceback.print_exc()

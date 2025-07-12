import pandas as pd
import os
import matplotlib.pyplot as plt

#  Defininig dataset directories 
base_path = "/home/sauharda/Desktop/webExtract"
datasets = {
    "NO2": os.path.join(base_path, "NO2", "Extracted files"),
    "SO2": os.path.join(base_path, "SO2", "Extracted files")
}

#  Loop over both NO2 and SO2 
for gas, folder in datasets.items():
    print(f"\nProcessing {gas} data from folder: {folder}")
    
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder, filename)
            print(f"Reading: {filename}")
            
            try:
                df = pd.read_csv(file_path)

                # Make sure required columns exist
                if not {'State Code', 'County Code', 'Sample Duration', 'Arithmetic Mean', '1st Max Value'}.issubset(df.columns):
                    print(f" Skipping {filename}: missing required columns.")
                    continue

                # Create countyfips column
                df['countyfips'] = df['State Code'] * 1000 + df['County Code']

                # Filter Sample Duration for "1 HOUR"
                df_1hr = df[df['Sample Duration'] == '1 HOUR']

                # Group and summarize
                summary = df_1hr.groupby('countyfips').agg(
                    mean_val=pd.NamedAgg(column='Arithmetic Mean', aggfunc='mean'),
                    max_val=pd.NamedAgg(column='1st Max Value', aggfunc='mean')
                ).reset_index()

                # Displays summary head
                print(summary.head())

                # Saving Summary to CSV
                year = filename[-8:-4]  # extract 2000 from daily_42401_2000.csv
                summary.to_csv(f"{gas}_{year}_summary.csv", index=False)

            except Exception as e:
                print(f" Error reading {filename}: {e}")

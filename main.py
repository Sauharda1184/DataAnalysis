import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Loading the dataset
df = pd.read_csv('/home/sauharda/Desktop/webExtract/NO2/Extracted files/daily_42602_2000.csv')
print(df.head())


# Creating a new column countyfips i.e State.Code * 1000 + County.Code
df['countyfips'] = df['State Code'] * 1000 + df['County Code']

print(df['countyfips'].head())

# Filter only the rows where Sample Duration is '1 HOUR'
df_1hr = df[df['Sample Duration'] == '1 HOUR']

summary = df_1hr.groupby('countyfips').agg(
    no2_mean = pd.NamedAgg(column='Arithmetic Mean', aggfunc='mean'),
    no2_max = pd.NamedAgg(column = '1st Max Value', aggfunc='mean'),
).reset_index()





print(summary.head())

plt.figure(figsize=(8, 6))
plt.scatter(summary['no2_mean'], summary['no2_max'], alpha=0.7)
plt.title("NO₂: Mean vs. 1st Max Value (2000)")
plt.xlabel("Mean NO₂ (Arithmetic Mean)")
plt.ylabel("Mean 1st Max NO₂ Value")
plt.grid(True)
plt.tight_layout()
plt.show()
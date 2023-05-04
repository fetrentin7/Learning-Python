import matplotlib as mpl
import csv
import numpy as np
import pandas as pd

df = pd.read_csv(r'C:\TrabalhoPython\pythonProject1\f12022\f1_drivers_points (1).csv')

# print coluna com header [[]]
print(df[['driver']].to_string(index=False))

data_driver = df.loc[(df['nationality'] == 'GER')]
# print(data_driver)

f_df = df.loc[(df['laps_led'] > 300)]
print(f_df)

group = df.groupby(['nationality', 'laps_led', 'age', 'wins', 'podiums']).sum().reset_index()
print(group)

group_age = df.groupby(['age', 'wins']).sum()
print(group_age)

with open('new.csv', 'r', encoding='UTF8') as f:
    writer = csv.writer(f)

    writer.writerow(f_df)
    writer.writerow(group)

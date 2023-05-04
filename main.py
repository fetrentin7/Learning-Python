import matplotlib as mpl
import csv
import numpy as np
import pandas as pd

df = pd.read_csv(r'C:\TrabalhoPython\pythonProject1\f12022\f1_drivers_points (1).csv')

# print coluna com header [[]]
print(df[['driver']].to_string(index=False))

data_driver = df.loc[(df['nationality'] == 'GER')]
print(data_driver)

f_df = df.loc[(df['laps_led'] > 300)]
print(f_df)

group = df.groupby(['nationality', 'laps_led', 'age', 'wins', 'podiums']).sum().reset_index()
print(group)

group_age = df.groupby(['age', 'wins']).sum()
print(group_age)


new_df = pd.concat([data_driver, f_df, group, group_age])

data_driver.to_csv('output.csv', index=False)


f_df.to_csv('output.csv', mode='a', index=False)

with open('output.csv', mode='a', newline='') as f:
    f.write('\n')
    group.to_csv(f, index=False)

# Append group_age to the output file
group_age.to_csv('output.csv', mode='a', index=False)



import matplotlib.pyplot as mpl
import csv
import numpy as np
import pandas as pd

df = pd.read_csv(r'C:\TrabalhoPython\pythonProject1\f12022\f1_drivers_points (1).csv')

# print coluna com header [[]]
print(df[['driver']].to_string(index=False))

data_driver = df.loc[(df['nationality'] == 'GER')]
print(data_driver)

data_points = df.loc[(df['points'] > 245)]
x = data_points['driver']
y = data_points['points']

mpl.bar(x, y)
mpl.xlabel('Driver')
mpl.ylabel('Points')
mpl.title('Data points above 245')
mpl.show()

data_driver = df.loc[df['nationality'] == 'GER']
points_by_driver = data_driver.groupby('driver')['points'].sum()

mpl.bar(points_by_driver.index, points_by_driver.values)

mpl.title('Total Points by German Drivers')
mpl.xlabel('Driver')
mpl.ylabel('Total Points')

mpl.show()

data_driver = df.loc[df['nationality'] == 'GER']

mpl.bar(points_by_driver.index, points_by_driver.values)

mpl.title('Total Points by German Drivers')
mpl.xlabel('Driver')
mpl.ylabel('Total Points')

mpl.show()

f_df = df.loc[(df['laps_led'] > 300)]
print(f_df)

group = df.groupby(['nationality', 'laps_led', 'age', 'wins', 'podiums']).sum().reset_index()
print(group)

group_age = df.groupby(['age']).agg({'points': 'sum', 'age': 'size'})
group_age.columns = ['total_points', 'frequency']
age = group_age.index
points = group_age['total_points']
freq = group_age['frequency']

fig, ax1 = mpl.subplots()

color = 'tab:red'
ax1.set_xlabel('Age')
ax1.set_ylabel('Total Points', color=color)
ax1.bar(age, points, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()

color = 'tab:blue'
ax2.set_ylabel('Frequency', color=color)
ax2.bar(age, freq, alpha=0.5, color=color)
ax2.tick_params(axis='y', labelcolor=color)

mpl.title('Total points and frequency by age')
mpl.show()

new_df = pd.concat([data_driver, f_df, group, group_age])

data_driver.to_csv('output.csv', index=False)

f_df.to_csv('output.csv', mode='a', index=False)

with open('output.csv', mode='a', newline='') as f:
    f.write('\n')
    group.to_csv(f, index=False)

group_age.to_csv('output.csv', mode='a', index=False)

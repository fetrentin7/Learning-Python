import matplotlib as mpl
import csv
import numpy as np
import pandas as pd

df = pd.read_csv(r'C:\TrabalhoPython\pythonProject1\f12022\f1_drivers_points (1).csv')

# printa coluna com header [[]]
print(df[['driver']].to_string(index=False))

data_driver = df.loc[(df['nationality'] == 'GER')]
print(data_driver)


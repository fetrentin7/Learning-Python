
import matplotlib as mpl
import csv
import numpy as np
import pandas as pd

df = pd.read_csv('circuits.csv')
df_circuitRef = df[(df['circuitRef'] =='albert_park') & (df['name'] == 'Australian Grand Prix')]


print(df.circuitRef.unique())
print(df_circuitRef)


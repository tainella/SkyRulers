import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as plt

filename = "C:\\My_files\\S7\\test_answer.csv"
with open ("C:\\My_files\\S7\\test_answer.csv", "r") as file:
    df=pd.read_csv(file)
sns.set_style("darkgrid")
sns.lineplot(data = df, x = "date", y = "param")
plt.show()
df['toronto_time'] = pd.to_datetime(df['toronto_time']).dt.strftime('%H:%M:%S')
sns.scatterplot(df['toronto_time'], df['description'])
plt.show()
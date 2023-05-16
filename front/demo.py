import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

df = pd.read_csv('C:\\My_files\\S7\\SkyRulers\\front\\test_answer.csv', parse_dates=['flight_datetime'])
#df = pd.read_csv('C:\\My_files\\S7\\SkyRulers\\front\\test_answer_3column.csv', parse_dates=['flight_datetime'])

rolling1 = df["predictions"].rolling(1000)
if len(df.columns.to_list()) == 3:
    rolling2 = df["true"].rolling(15000)

df['flight_datetime']=pd.to_datetime(df['flight_datetime'])
df.sort_values(by="flight_datetime", inplace=True)
df.index=df['flight_datetime']
#df['flight_datetime']=df['flight_datetime'].astype('datetime64[as]')
fig, ax=plt.subplots()
data=df.resample('W').sum()
x_dates=data.index.strftime("%Y-%m-%d").unique()
ax.set_xticklabels(labels=x_dates, rotation=20)
# if len(df.columns.to_list()) == 3:
#     ax1 = sns.lineplot(data=data['true'], color='g', label = "true values")
#     ax2 = sns.lineplot(data = pd.DataFrame(rolling2.mean()), label = 'rolling_mean_prediction')
#     ax3 = sns.lineplot(data = pd.DataFrame(rolling2.std()),label = 'rolling_std_prediction')

ax = sns.lineplot(data=data['predictions'], color='r', label = 'prediction')
ax5 = sns.lineplot(data = pd.DataFrame(rolling1.mean()), label = 'rolling_std_prediction', color = "grey")
ax6 = sns.lineplot(data = pd.DataFrame(rolling1.std()), label = 'rolling_std_prediction', color = "yellow")
ax.set (xlabel='Time', ylabel='Parametr', title='Sensor readings')

sns.set_theme(style="darkgrid")
plt.legend()
plt.show()
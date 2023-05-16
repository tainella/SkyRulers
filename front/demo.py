import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

#df = pd.read_csv('C:\\My_files\\S7\\test_answer.csv')
# years = mdates.YearLocator()   # every year
# months = mdates.MonthLocator()  # every month
# years_fmt = mdates.DateFormatter('%Y-%m') #This is a format. Will be clear in Screenshot
df = pd.read_csv('C:\\My_files\\S7\\test_answer.csv', parse_dates=['flight_datetime'])

df['flight_datetime']=pd.to_datetime(df['flight_datetime'])
df.sort_values(by="flight_datetime", inplace=True)
df.index=df['flight_datetime']
#df['flight_datetime']=df['flight_datetime'].astype('datetime64[as]')
fig, ax=plt.subplots()


data=df.resample('W').sum()
x_dates=data.index.strftime("%Y-%m-%d").unique()
ax.set_xticklabels(labels=x_dates, rotation=60)
sns.set_theme(style="darkgrid")
sns.lineplot(x = "flight_datetime", y = "predictions", data=data['predictions'])
plt.show()
# print("здесь")
# axes.xaxis.set_major_locator(months)
# axes.xaxis.set_major_formatter(years_fmt)
# axes.xaxis.set_minor_locator(months)
# print("или тут")
# plt.xticks(rotation = 'vertical')



#sns.scatterplot(x="total_bill", y="tip", data=t)

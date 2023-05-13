import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import plotly.express as px
import datetime

data = pd.DataFrame({'Original_data':[11, 17, 16, 18, 22, 25, 26, 24, 29], #значения параметра
        'Predicted_data':[5, 7, 7, 9, 12, 9, 9, 4, 8] #значения параметра
        })

original_data = data["Original_data"]
predicted_data = data["Predicted_data"]

time = np.arange(5) #шкала времени

#add lines to plot
plt.plot(original_data, label='original_data', color='green')
plt.plot(predicted_data, label='predicted_data', color='red')

a=0
b=0
for i in data:
    for j in data[i]:
        a = min(j,a) 
        b= max(j,b)
ylist = list(range(a,b))
print(ylist)
datelist = pd.date_range(datetime.date(1950, 12, 22), datetime.date(2022, 12, 25), periods = 1).tolist()
plt.xticks(datelist)
plt.yticks(ylist)

#names of axes
plt.xlabel('time')
plt.ylabel('parametr')

#place legend in center right of plot
plt.legend( title='Metric') 

plt.show()
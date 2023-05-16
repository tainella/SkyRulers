import pandas as pd
import matplotlib.pyplot as plt

# Sample DataFrame with datetime and values columns
data = {
    'datetime': ['2023-01-01 12:00:00', '2023-01-02 10:00:00', '2023-01-03 15:00:00', '2023-01-04 18:00:00'],
    'values': [10, 15, 12, 8]
}
df = pd.DataFrame(data)
df['datetime'] = pd.to_datetime(df['datetime'])

# Plotting the line graph
plt.plot(df['datetime'], df['values'])
plt.xlabel('Datetime')
plt.ylabel('Values')
plt.title('Line Graph')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
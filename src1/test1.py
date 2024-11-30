import pandas as pd
import matplotlib.pyplot as plt


data=pd.read_csv('./data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)
data=data.set_index('timestamp')
daily_close_pct_change = data['close'].pct_change()
wealth_index = 1000 * (1 + daily_close_pct_change).cumprod()
previous_peaks = wealth_index.cummax()
drawdown = (wealth_index - previous_peaks) / previous_peaks
drawdown.plot()
print(drawdown.head())
plt.figure(figsize=(12, 6))
plt.plot(drawdown.index, drawdown, label='Wealth Index', color='blue')
plt.title('Wealth Index Over Time')
plt.xlabel('Time')
plt.show()


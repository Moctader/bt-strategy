import pandas as pd
import ffn
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('./data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv')

# Parse 'timestamp' as datetime and set it as the index
data['timestamp'] = pd.to_datetime(data['timestamp'])
prices = data[['timestamp', 'close']]
prices.set_index('timestamp', inplace=True)

# Calculate statistics using ffn
stats = prices.calc_stats()
stats.display()

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Plot the prices
ax1.plot(prices.index, prices['close'], label='Prices', color='blue')
ax1.set_title('Prices Over Time')
ax1.set_xlabel('Time')
ax1.set_ylabel('Price')
ax1.grid(True)
ax1.legend()

# Plot the drawdown
drawdown = stats.prices.to_drawdown_series()
ax2.plot(drawdown.index, drawdown, label='Drawdown', color='red')
ax2.set_title('Drawdown Over Time')
ax2.set_xlabel('Time')
ax2.set_ylabel('Drawdown')
ax2.grid(True)
ax2.legend()

# Adjust layout and show the plot
plt.tight_layout()
plt.show()
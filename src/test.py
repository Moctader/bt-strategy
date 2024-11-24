import pandas as pd
import ffn
import numpy as np
import yfinance as yf

# Download AAPL stock data for the last 3 years
data = yf.download('AAPL', start='2021-01-01', end='2024-01-01')

# Calculate 10-day and 50-day moving averages
data['MA10'] = data['Close'].rolling(window=40).mean()
data['MA50'] = data['Close'].rolling(window=100).mean()

# Generate signals: 1 for Buy, -1 for Sell, 0 for Hold
data['Signal'] = 0
data.loc[data['MA10'] > data['MA50'], 'Signal'] = 1  # Buy signal
data.loc[data['MA10'] < data['MA50'], 'Signal'] = -1 # Sell signal

# Calculate daily returns
data['Return'] = data['Close'].pct_change()

# Calculate strategy return
data['Strategy_Return'] = data['Signal'].shift(1) * data['Return']

# Analyze performance using ffn
strategy_data = pd.DataFrame({'Strategy': data['Strategy_Return']})
stats = strategy_data.calc_stats()

# Print a detailed performance report
print(stats.display())

# Plot strategy performance
stats.plot()
print(data['Strategy_Return'] )
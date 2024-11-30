import pandas as pd
import yfinance as yf
import ffn
import matplotlib.pyplot as plt

# Function to fetch data in chunks
def fetch_data_in_chunks(ticker, start_date, end_date, interval, chunk_size):
    all_data = []
    current_start = pd.to_datetime(start_date)
    current_end = current_start + pd.Timedelta(days=chunk_size)
    
    while current_start < pd.to_datetime(end_date):
        if current_end > pd.to_datetime(end_date):
            current_end = pd.to_datetime(end_date)
        
        data = yf.download(ticker, start=current_start.strftime('%Y-%m-%d'), end=current_end.strftime('%Y-%m-%d'), interval=interval)
        all_data.append(data)
        
        current_start = current_end
        current_end = current_start + pd.Timedelta(days=chunk_size)
    
    return pd.concat(all_data)

# Fetch intraday data using yfinance in chunks
ticker = 'AAPL'  # Example ticker
data = fetch_data_in_chunks(ticker, start_date='2020-09-01', end_date='2020-09-02', interval='1m', chunk_size=7)

# Check if data is empty
if data.empty:
    raise ValueError("No data fetched. Ensure the date range is within the last 30 days.")

# Use the 'Close' prices
prices = data[['Close']]
prices.columns = ['close']

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
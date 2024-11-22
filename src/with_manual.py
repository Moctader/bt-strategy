import pandas as pd
import numpy as np

# Load predictions data
data = pd.read_csv('EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# Calculate trading minutes per day
trading_minutes_per_day = data['close'].resample('D').count()
trading_days = (trading_minutes_per_day > 0).sum()  # Count only days with trading activity
average_minutes_per_day = trading_minutes_per_day[trading_minutes_per_day > 0].mean()

# Calculate total trading years in the dataset
minutes_per_year = trading_days * average_minutes_per_day
total_minutes = len(data)
years = total_minutes / minutes_per_year

# Calculate returns and cumulative returns
price_series = data['close']
returns = price_series.pct_change().dropna()
cumulative_returns = (1 + returns).cumprod() - 1
total_return = cumulative_returns.iloc[-1]

# Calculate annualized return (CAGR)
cagr = (1 + total_return) ** (1 / years) - 1

# Calculate Sharpe ratio based on minute data
risk_free_rate = 0.00
excess_returns = returns - (risk_free_rate / minutes_per_year)
sharpe_ratio = (np.sqrt(minutes_per_year) * excess_returns.mean() / excess_returns.std())

# Calculate max drawdown
rolling_max = price_series.cummax()
drawdown = (price_series - rolling_max) / rolling_max
max_drawdown = drawdown.min()

# Calculate periodic statistics based on minute data
mean_return = returns.mean() * minutes_per_year  # Annualized mean return
volatility = returns.std() * np.sqrt(minutes_per_year)  # Annualized volatility
skewness = returns.skew()
kurtosis = returns.kurtosis()
best_minute = returns.max()
worst_minute = returns.min()

# Display the results
print(f"Number of trading days: {trading_days}")
print(f"Average trading minutes per day: {average_minutes_per_day:.2f}")
print(f"Annual risk-free rate considered: {risk_free_rate:.2%}")
print("Summary:")
print(f"Total Return      Sharpe  CAGR    Max Drawdown")
print(f"--------------  --------  ------  --------------")
print(f"{total_return:.2%}          {sharpe_ratio:.2f}  {cagr:.2%}  {max_drawdown:.2%}")

print("\nPeriodic:")
print(f"        minute       monthly    yearly")
print(f"------  ----------  ---------  --------")
print(f"sharpe  {sharpe_ratio:.2f}      -          -")
print(f"mean    {mean_return:.2%}  -          -")
print(f"vol     {volatility:.2%}    -          -")
print(f"skew    {skewness:.2f}       -          -")
print(f"kurt    {kurtosis:.2f}       -          -")
print(f"best    {best_minute:.2%}     -          -")
print(f"worst   {worst_minute:.2%}    -          -")


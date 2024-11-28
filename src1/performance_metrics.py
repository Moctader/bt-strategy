# import pandas as pd
# import numpy as np

# def calculate_performance_metrics(df):
#     df['timestamp'] = pd.to_datetime(df['timestamp'])
#     df.set_index('timestamp', inplace=True)

#     # Calculate periodic returns using capital or cumulative_pnl
#     df['returns'] = df['cumulative_pnl'].pct_change().replace([float('inf'), -float('inf')], float('nan')).fillna(0)

#     # Calculate Sharpe Ratio
#     sharpe_ratio_value = sharpe_ratio(df)

#     # Calculate drawdown
#     max_drawdown_value = max_drawdown(df)

#     # Calculate CAGR
#     cagr_value = CAGR(df)

#     print(df)
#     # Print strategy performance
#     print('***** STRATEGY PERFORMANCE *****')
#     print('--------------------------------')
#     print(f'CAGR: {cagr_value:.2f} %')
#     print(f'Sharpe ratio: {sharpe_ratio_value:.2f}')
#     print(f'Maximum drawdown: {max_drawdown_value:.2f} %')
#     print('--------------------------------')

# def average_trading_minutes_per_day(df):
#     df['date'] = df.index.date
#     trades_per_day = df.groupby('date').size().mean()
#     return trades_per_day

# def CAGR(df):
#     df = df.copy()
#     trades_per_day = average_trading_minutes_per_day(df)
#     num_years = len(df) / (trades_per_day * 252)  # Adjusting for average trades per minute
#     start_value = df['capital'].iloc[0]
#     end_value = df['capital'].iloc[-1]
#     if start_value <= 0 or end_value <= 0:
#         return float('nan')
#     cagr = ((end_value / start_value) ** (1 / num_years) - 1) * 100
#     return round(cagr, 2)

# def sharpe_ratio(df):
#     returns = df['cumulative_pnl'].pct_change().replace([float('inf'), -float('inf')], float('nan')).dropna()
#     risk_free_rate = 0.0
#     print("Returns:", returns.describe())  # Debugging statement
#     if returns.std() == 0:
#         return float('nan')
#     trades_per_day = average_trading_minutes_per_day(df)
#     annualization_factor = (trades_per_day * 252) ** 0.5  # Annualize for minute-based data
#     sharpe_ratio = (returns.mean() - risk_free_rate) / returns.std() * annualization_factor
#     return round(sharpe_ratio, 2)

# def max_drawdown(df):
#     cumulative_max = df['capital'].cummax()
#     drawdown = (df['capital'] - cumulative_max) / cumulative_max
#     print("Drawdown:", drawdown.describe())  # Debugging statement
#     max_drawdown = drawdown.min()
#     return round(max_drawdown * 100, 2)
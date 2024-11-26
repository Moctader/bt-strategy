import pandas as pd
from signals import GenerateSignal
from strategy import TradingStrategy
from performance_metrics import CAGR, sharpe_ratio, max_drawdown

# Load data
df = pd.read_csv('../data/data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(100000)
df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime format
df.set_index('Date', inplace=True)  

# Initialize the GenerateSignal class with the data
signal_generator = GenerateSignal(df, wick_size=0.2, atr_period=20, slippage=0.1, size=1)

# Generate signals
signals = signal_generator.generate_signals()
resulting_trades = signal_generator.get_dataframe()
strategy = TradingStrategy(resulting_trades, signals, atr_sl=1)
resulting_trades = strategy.execute()

# Plot
strategy.plot_cumulative_returns()
strategy.plot_signals()





# Assuming these variables are defined and available
strategy_results = strategy.calculate_cumulative_returns()
str_profits = [trade['result'] for trade in strategy.trade.values() if trade['result'] > 0]
str_losses = [trade['result'] for trade in strategy.trade.values() if trade['result'] < 0]
str_be = [trade['result'] for trade in strategy.trade.values() if trade['result'] == 0]
account_size = 10000

# Strategy performance
print('***** STRATEGY PERFORMANCE *****')
print('--------------------------------')
print('CAGR:', CAGR(strategy_results, df), '%')
print('Sharpe ratio:', sharpe_ratio(strategy_results))
print('Maximum drawdown:', max_drawdown(strategy_results), '% \n')
print('Number of trades:', len(str_profits + str_losses + str_be))
print('Number of profits:', len(str_profits))
print('Number of losses:', len(str_losses))
print('Number of breakevens:', len(str_be), '\n')
print('Winning percentage:', round(len(str_profits) / (len(str_profits) + len(str_losses)) * 100, 2), '%')
print('ROI:', round(strategy_results['cumulative_return'].iloc[-1]) - account_size)
print('--------------------------------')
print('Average profitable trade:', round(sum(str_profits) / len(str_profits), 2))
print('Average losing trade:', round(sum(str_losses) / len(str_losses), 2))
print('Max profitable trade:', round(max(str_profits), 2))
print('Max losing trade:', round(min(str_losses), 2))


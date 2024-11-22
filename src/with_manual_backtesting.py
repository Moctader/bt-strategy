import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from buy_sell_close import SignalGenerator, Strategy, PnLCalculator

# Load data
data = pd.read_csv('EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# Initialize classes
signal_generator = SignalGenerator()
strategy = Strategy()
pnl_calculator = PnLCalculator()

# Generate signals
signals = signal_generator.generate_signals(data)

# Execute the strategy
transactions = strategy.execute(signals)

# Calculate PnL
pnl_data = pnl_calculator.calculate(transactions)

# Convert PnL data to a DataFrame
pnl_df = pd.DataFrame(pnl_data)

# Ensure that we have a timestamp for each transaction (match them with original data)
pnl_df['timestamp'] = data.index[:len(pnl_df)].values
pnl_df.set_index('timestamp', inplace=True)

# Calculate cumulative PnL
pnl_df['cumulative_pnl'] = pnl_df['cumulative_pnl'].cumsum().fillna(0)
equity_curve = pnl_df['cumulative_pnl'] + strategy.capital  # Starting capital + cumulative PnL
equity_curve.name = 'Equity Curve'

# Handle NaN and Inf
equity_curve.replace([np.inf, -np.inf], np.nan, inplace=True)
equity_curve.dropna(inplace=True)

# Ensure equity curve has valid data
if equity_curve.isnull().all():
    print("Equity curve has no valid data after cleaning.")
else:
    # Calculate returns from the equity curve
    returns = equity_curve.pct_change().dropna()

    # Handle potential issues with extreme values or divisions by zero
    returns.replace([np.inf, -np.inf], np.nan, inplace=True)
    returns.dropna(inplace=True)

    # Debug prints
    print("Cleaned Equity Curve:")
    print(equity_curve.head())
    print("Cleaned Returns:")
    print(returns.head())

    # Calculate performance metrics manually
    total_return = equity_curve.iloc[-1] / equity_curve.iloc[0] - 1
    trading_minutes_per_day = data['close'].resample('D').count()
    trading_days = (trading_minutes_per_day > 0).sum()  # Count only days with trading activity
    average_minutes_per_day = trading_minutes_per_day[trading_minutes_per_day > 0].mean()
    minutes_per_year = trading_days * average_minutes_per_day
    total_minutes = len(data)
    years = total_minutes / minutes_per_year
    cagr = (1 + total_return) ** (1 / years) - 1
    risk_free_rate = 0.00
    excess_returns = returns - (risk_free_rate / minutes_per_year)
    sharpe_ratio = (np.sqrt(minutes_per_year) * excess_returns.mean() / excess_returns.std())
    rolling_max = equity_curve.cummax()
    drawdown = (equity_curve - rolling_max) / rolling_max
    max_drawdown = drawdown.min()
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

    # Plot the equity curve
    equity_curve.plot(figsize=(10, 6), title='Equity Curve for the Strategy', grid=True)
    plt.xlabel('Time')
    plt.ylabel('Equity Value')
    plt.show()
import numpy as np
import pandas as pd
import ffn
from buy_sell_close import SignalGenerator, Strategy, PnLCalculator
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)


signal_generator = SignalGenerator()
strategy = Strategy()
pnl_calculator = PnLCalculator()

signals = signal_generator.generate_signals(data)
transactions = strategy.execute(signals)
pnl_data = pnl_calculator.calculate(transactions)
pnl_df = pd.DataFrame(pnl_data)

# Ensure that we have a timestamp for each transaction (match them with original data)
pnl_df['timestamp'] = data.index[:len(pnl_df)].values
pnl_df.set_index('timestamp', inplace=True)

# Calculate PnL and cumulative PnL
pnl_df['cumulative_pnl'] = pnl_df['cumulative_pnl'].cumsum().fillna(0)

# Ensure that cumulative PnL makes sense
if pnl_df['cumulative_pnl'].isnull().all() or (pnl_df['cumulative_pnl'] == 0).all():
    print("Cumulative PnL contains only NaN or zero values. Check PnL calculation.")
else:
    equity_curve = pnl_df['cumulative_pnl'] + strategy.capital  # Starting capital + cumulative PnL
    equity_curve.name = 'Equity Curve'

    # Handle NaN and Inf
    equity_curve.replace([np.inf, -np.inf], np.nan, inplace=True)
    equity_curve.dropna(inplace=True)

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

        # Use ffn to calculate performance metrics if returns are valid
        if not returns.empty and np.isfinite(returns).all():
            stats = returns.calc_stats()
            stats.display()

            # Plot the equity curve
            equity_curve.plot(figsize=(10, 6), title='Equity Curve for the Strategy', grid=True)
            plt.xlabel('Time')
            plt.ylabel('Equity Value')
            plt.show()
        else:
            print("Returns contain invalid data.")

import pandas as pd
import ffn
from signals import SignalGenerator
from strategy_v0 import strategy_v0 
from PnLCalculator import PnLCalculator
from plotting import plot_transactions
from profit_and_loss import ProfitAndLoss

# Load predictions
data = pd.read_csv('../src/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)

# Initialize SignalGenerator and Strategy
signal_generator = SignalGenerator()
strategy = strategy_v0()
pnl_calculator = PnLCalculator()
profit_and_loss = ProfitAndLoss()

# Generate signals
signals = signal_generator.generate_signals(data)
signals = pd.DataFrame(signals)

# Check how many signals are -1
num_negative_signals = (signals['signal'] == -1).sum()
print(f"Number of -1 signals: {num_negative_signals}")

# Execute strategy
strategy_df = strategy.execute(signals)
strategy_df = pd.DataFrame(strategy_df)
print(strategy_df)

# Calculate PnL
results = profit_and_loss.calculate(strategy_df)
df = pd.DataFrame(results)
df.index = pd.to_datetime(data['timestamp'].iloc[:len(df)])
print(df)

# Plot transactions
plot_transactions(strategy_df)

# Calculate returns from price data
price_data = df['price']
returns = ffn.to_returns(price_data).dropna()

# Use ffn to calculate performance metrics
perf = returns.calc_stats()

# Display performance summary
print(perf.display())

# Display results
# signals_df = pd.DataFrame(signals)
# print(df[10:40])
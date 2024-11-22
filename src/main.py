import pandas as pd
from buy_sell_s import SignalGenerator, Strategy, PnLCalculator
from plotting import plot_strategy_results

# Load predictions
predictions = pd.read_csv('predictions.csv').head(100)

# Initialize SignalGenerator and Strategy
signal_generator = SignalGenerator()
strategy = Strategy()
pnl_calculator = PnLCalculator()



# Generate signals
signals = signal_generator.generate_signals(predictions)
strategy_df = strategy.execute(signals)



# Calculate PnL
results = pnl_calculator.calculate(strategy_df)
df = pd.DataFrame(results)
plot_strategy_results(df)






# Display results
signals_df = pd.DataFrame(signals)
print(predictions)
print(signals_df)
print(signals_df[signals_df['signal'] == -1])
print(pd.DataFrame(strategy_df))
print(df)
print("\nFirst 15 rows of the results:")
print(df.head(15))


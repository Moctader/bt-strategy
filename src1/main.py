import pandas as pd
import ffn
from signals import SignalGenerator
from strategy_v0 import strategy_v0
from plotting import plot_transactions
from profit_and_loss import ProfitAndLoss

def main():
    data = pd.read_csv('./data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10_000)

    # Initialize key components
    signal_generator = SignalGenerator()
    strategy = strategy_v0()
    profit_and_loss = ProfitAndLoss()

    signals = signal_generator.generate_signals(data)
    strategy_df = pd.DataFrame(strategy.execute(pd.DataFrame(signals)))
    results = profit_and_loss.calculate(strategy_df)
    df = pd.DataFrame(results)


    # Align the index with the timestamp from the original data
    df.index = pd.to_datetime(data['timestamp'].iloc[:len(df)])
    plot_transactions(strategy_df)




    # Calculate returns based on share price data
    price_data = df['share_price']
    returns = ffn.to_returns(price_data).dropna()

    # Use the 'ffn' library to calculate performance metrics
    perf = returns.calc_stats()

    # Display a summary of the performance metrics
    print(perf.display())

    # Additional output for debugging or analysis
    print(strategy_df)
    print(df)


if __name__ == "__main__":
    main()

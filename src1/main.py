import pandas as pd
import ffn
from signals import SignalGenerator
from strategy_v0 import strategy_v0
from plotting import plot_transactions
from profit_and_loss import ProfitAndLoss
from plotting import plot_portfolio_values, plot_drawdown, plot_drawdown_vs_stock_price, plot_portfolio_values_and_drawdown
from performance_metrics import calculate_performance_metrics

def main():
    # Load data and set the index to the timestamp column
    data = pd.read_csv('./data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)

    # Initialize key components
    signal_generator = SignalGenerator()
    strategy = strategy_v0()
    profit_and_loss = ProfitAndLoss()

    # Generate signals
    signals = signal_generator.generate_signals(data, column_name='close')
    strategy_df = strategy.execute(pd.DataFrame(signals))
    results = profit_and_loss.calculate(pd.DataFrame(strategy_df))


    calculate_performance_metrics(pd.DataFrame(results))    
    plot_transactions(pd.DataFrame(results))    



if __name__ == "__main__":
    main()

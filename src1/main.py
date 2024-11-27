import pandas as pd
import ffn
from signals import SignalGenerator
from strategy_v0 import strategy_v0
from plotting import plot_transactions
from profit_and_loss import ProfitAndLoss
from plotting import plot_portfolio_values, plot_drawdown, plot_drawdown_vs_stock_price, plot_portfolio_values_and_drawdown

def main():
    # Load data and set the index to the timestamp column
    data = pd.read_csv('./data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)

    # Initialize key components
    signal_generator = SignalGenerator()
    strategy = strategy_v0()
    profit_and_loss = ProfitAndLoss()

    # Generate signals
    signals = signal_generator.generate_signals(data, column_name='close')

    # Execute strategy
    strategy_df, portfolio_values = strategy.execute(pd.DataFrame(signals))
    # Calculate profit and loss
    results = profit_and_loss.calculate(pd.DataFrame(strategy_df))
    df = pd.DataFrame(results)
    print(df)

    portfolio_values_df = pd.DataFrame(portfolio_values, columns=['timestamp', 'portfolio_value'])
    portfolio_series = pd.Series(portfolio_values_df['portfolio_value'].values, index=portfolio_values_df['timestamp'])
    
    # Calculate drawdown
    cumulative_max = portfolio_series.cummax()
    drawdown = (portfolio_series - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min()

    # Calculate returns based on portfolio values
    returns = portfolio_series.pct_change().dropna()

    # Calculate Sharpe ratio
    risk_free_rate = 0.0 
    average_return = returns.mean()
    return_std = returns.std()
    sharpe_ratio = (average_return - risk_free_rate) / return_std

    print(f'Sharpe Ratio: {sharpe_ratio}')
    print(f'Max Drawdown: {max_drawdown}')

    plot_transactions(df)
    profit_and_loss.save_to_yaml()



if __name__ == "__main__":
    main()

import pandas as pd
import ffn
from signals import SignalGenerator
from strategy_v0 import strategy_v0
from plotting import plot_transactions
from profit_and_loss import ProfitAndLoss
from plotting import plot_portfolio_values, plot_drawdown, plot_drawdown_vs_stock_price, plot_portfolio_values_and_drawdown

def main():
    data = pd.read_csv('./data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)

    # Initialize key components
    signal_generator = SignalGenerator()
    strategy = strategy_v0()
    profit_and_loss = ProfitAndLoss()

    signals = signal_generator.generate_signals(data)
    strategy_df, portfolio_values = strategy.execute(pd.DataFrame(signals))
    results = profit_and_loss.calculate(pd.DataFrame(strategy_df))
    df = pd.DataFrame(results)

    # Align the index with the timestamp from the original data
    df.index = pd.to_datetime(data['timestamp'].iloc[:len(df)])

    # Calculate drawdown
    portfolio_series = pd.Series(portfolio_values)
    cumulative_max = portfolio_series.cummax()
    drawdown = (portfolio_series - cumulative_max) / cumulative_max


    # Calculate returns based on portfolio values
    returns = portfolio_series.pct_change().dropna()
    # Calculate Sharpe ratio
    risk_free_rate = 0.0 
    average_return = returns.mean()
    return_std = returns.std()
    sharpe_ratio = (average_return - risk_free_rate) / return_std

    print(f'Sharpe Ratio: {sharpe_ratio}')

    price_data = df['share_price']
    returns = ffn.to_returns(price_data).dropna()

    perf = returns.calc_stats()

    # Display a summary of the performance metrics
    print(perf.display())
    
    profit_and_loss.save_to_yaml()



    # Plot portfolio values
    plot_transactions(df)
    # plot_portfolio_values(portfolio_values)
    # plot_drawdown(drawdown)
    # plot_portfolio_values_and_drawdown(portfolio_values, drawdown)

    # Plot drawdown against stock price
    # plot_drawdown_vs_stock_price(df, drawdown)

if __name__ == "__main__":
    main()
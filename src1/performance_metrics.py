import pandas as pd

def calculate_performance_metrics(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Calculate periodic returns using capital or cumulative_pnl
    df['returns'] = df['cumulative_pnl'].pct_change().replace([float('inf'), -float('inf')], float('nan')).fillna(0)

    # Calculate Sharpe Ratio
    risk_free_rate = 0.0
    average_return = df['returns'].mean()
    return_std = df['returns'].std()

    # Annualize the Sharpe ratio for minute-based data
    minutes_per_year = 525600  
    sharpe_ratio = (average_return - risk_free_rate) / return_std * (minutes_per_year ** 0.5)

    # Calculate drawdown
    cumulative_max = df['capital'].cummax()
    df['drawdown'] = (df['capital'] - cumulative_max) / cumulative_max
    max_drawdown = df['drawdown'].min()

    # Calculate CAGR
    start_value = df['capital'].iloc[0]
    end_value = df['capital'].iloc[-1]
    num_years = (df.index[-1] - df.index[0]).total_seconds() / (365.25 * 24 * 60 * 60)
    cagr = ((end_value / start_value) ** (1 / num_years) - 1) * 100

    print(df)
    # # Print strategy performance
    # print('***** STRATEGY PERFORMANCE *****')
    # print('--------------------------------')
    # print(f'CAGR: {cagr:.2f} %')
    # print(f'Sharpe ratio: {sharpe_ratio:.2f}')
    # print(f'Maximum drawdown: {max_drawdown:.2f} %')
    # print('--------------------------------')

   
import pandas as pd

def calculate_performance_metrics(df):
    # Convert timestamp to datetime and set it as the index
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Calculate periodic returns using capital or cumulative_pnl
    df['returns'] = df['cumulative_pnl'].pct_change().replace([float('inf'), -float('inf')], float('nan')).fillna(0)

    # Calculate Sharpe Ratio
    risk_free_rate = 0.0
    average_return = df['returns'].mean()
    return_std = df['returns'].std()

    # Handle cases where return_std is zero to avoid division by zero
    if return_std == 0:
        sharpe_ratio = float('nan')
    else:
        sharpe_ratio = (average_return - risk_free_rate) / return_std

    print(f'Sharpe Ratio: {sharpe_ratio}')

    # Calculate drawdown
    cumulative_max = df['capital'].cummax()
    df['drawdown'] = (df['capital'] - cumulative_max) / cumulative_max

    # Display metrics
    print(df)
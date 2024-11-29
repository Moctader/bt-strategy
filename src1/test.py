import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_performance_metrics(df):
    # Ensure the 'capital' column exists in the DataFrame
    if 'capital' not in df.columns:
        raise ValueError("The DataFrame must contain a 'capital' column.")

    # Calculate cumulative max and drawdown
    cumulative_max = df['capital'].cummax()
    drawdown = (df['capital'] - cumulative_max) / cumulative_max
    df['drawdown'] = drawdown
    max_drawdown = drawdown.min() * 100

    # Identify Peak and Trough Values
    peak_value = cumulative_max.max()
    trough_value = df['capital'][df['capital'].idxmin()]
    drawdown_value = (trough_value - peak_value) / peak_value * 100

    # Print maximum drawdown
    print(f'Maximum Drawdown: {max_drawdown:.2f}%')
    print(f'Peak Value: {peak_value}')
    print(f'Trough Value: {trough_value}')
    print(f'Drawdown Value: {drawdown_value:.2f}%')

    # Plot capital and drawdown
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['capital'], label='Capital')
    plt.title('Capital Over Time')
    plt.xlabel('Time')
    plt.ylabel('Capital')
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['drawdown'], color='red', label='Drawdown')
    plt.title('Drawdown Over Time')
    plt.xlabel('Time')
    plt.ylabel('Drawdown')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

    return {
        'Maximum Drawdown': max_drawdown,
        'Peak Value': peak_value,
        'Trough Value': trough_value,
        'Drawdown Value': drawdown_value
    }

# Example DataFrame based on provided output
data = {
    'timestamp': [
        '2019-01-02 00:26:00', '2019-01-02 00:27:00', '2019-01-02 00:28:00', '2019-01-02 00:30:00', '2019-01-02 00:31:00',
        '2019-01-10 23:08:00', '2019-01-10 23:11:00', '2019-01-10 23:12:00', '2019-01-10 23:16:00', '2019-01-10 23:17:00'
    ],
    'signal': ['buy', 'sell', 'buy', 'sell', 'buy', 'sell', 'buy', 'hold', 'sell', 'hold'],
    'price': [1.14568, 1.14578, 1.14575, 1.14604, 1.14589, 1.15242, 1.15230, 1.15233, 1.15261, 1.15255],
    'capital': [2.75824, 100006.72820, 2.23095, 100030.04027, 3.01039, 151663.18466, 2.06786, 2.06786, 151701.98562, 151701.98562],
    'position': [87282.0, 0.0, 87283.0, 0.0, 87292.0, 0.0, 131616.0, 131616.0, 0.0, 0.0],
    'pnl': [0.00000, 6.72820, 0.00000, 23.31207, 0.00000, 16.42456, 0.00000, 0.00000, 38.80096, 0.00000],
    'cumulative_pnl': [0.00000, 6.72820, 6.72820, 30.04027, 30.04027, 51663.18466, 51663.18466, 51663.18466, 51701.98562, 51701.98562]
}

df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Calculate performance metrics
metrics = calculate_performance_metrics(df)
print(metrics)
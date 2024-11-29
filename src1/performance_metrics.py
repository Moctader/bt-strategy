import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def calculate_performance_metrics(df):
    # Calculate portfolio value
    df['portfolio_value'] = df['capital'] + (df['position'] * df['price'])
    
    # Calculate cumulative return
    df['cumulative_return'] = (df['portfolio_value'] / df['portfolio_value'].iloc[0]) - 1
    
    # Calculate cumulative max and drawdown
    cumulative_return = df['cumulative_return']
    cumulative_max = cumulative_return.cummax()
    drawdown = (cumulative_return - cumulative_max) / cumulative_max
    df['drawdown'] = drawdown












    # Identify Peak and Trough Values
    peak_value = df['portfolio_value'].max()
    trough_value = df['portfolio_value'].min()
    drawdown_value = (trough_value - peak_value) / peak_value * 100

    # Print maximum drawdown
    print(f'Maximum Drawdown: {drawdown_value:.2f}%')
    print(f'Peak Value: {peak_value}')
    print(f'Trough Value: {trough_value}')

    # Plot portfolio value and drawdown
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Portfolio Value', color='blue')
    ax1.plot(df.index, df['portfolio_value'], color='blue', label='Portfolio Value')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Drawdown', color='red')
    ax2.plot(df.index, df['drawdown'], color='red', label='Drawdown')
    ax2.tick_params(axis='y', labelcolor='red')

    fig.tight_layout()
    plt.title('Portfolio Value and Drawdown Over Time')
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['drawdown'], color='red', label='Drawdown')
    plt.title('Drawdown Over Time')
    plt.xlabel('Time')
    plt.ylabel('Drawdown')
    plt.grid(True)
    plt.legend()
    plt.show()

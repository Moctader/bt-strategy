import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ffn

def calculate_performance_metrics(df):
    # Calculate portfolio value using 'close' price
    df['portfolio_value'] = df['capital'] + (df['position'] * df['close'])
    # Create a DataFrame with the portfolio value series
    portfolio_values = df[['portfolio_value']]
    portfolio_values.index = pd.to_datetime(portfolio_values.index)
    
    # Calculate statistics using ffn
    stats = portfolio_values.calc_stats()
    stats.display()
    
    # Calculate drawdown series
    drawdown = stats.prices.to_drawdown_series()
    analyze_portfolio(portfolio_values, drawdown)
    return df



def analyze_portfolio(portfolio_values, drawdown):
 
    
    # Plot the portfolio performance and drawdowns
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Plot the portfolio values
    ax1.plot(portfolio_values.index, portfolio_values['portfolio_value'], label='Portfolio Value', color='blue')
    ax1.set_title('Portfolio Value Over Time')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Portfolio Value')
    ax1.grid(True)
    ax1.legend()

    # Plot the drawdown
    ax2.plot(drawdown.index, drawdown, label='Drawdown', color='red')
    ax2.set_title('Drawdown Over Time')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Drawdown')
    ax2.grid(True)
    ax2.legend()

    # Adjust layout and show the plot
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Sample data
    data = pd.DataFrame({
        'timestamp': pd.date_range(start='1/1/2020', periods=10, freq='D'),
        'close': [1.1, 1.2, 1.3, 1.2, 1.3, 1.4, 1.3, 1.4, 1.5, 1.6],
        'capital': [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        'position': [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
    })
    data.set_index('timestamp', inplace=True)

    # Calculate performance metrics
    results = calculate_performance_metrics(data)
    print(results)
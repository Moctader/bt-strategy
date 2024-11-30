import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import ffn


def calculate_performance_metrics(df):
    # Calculate portfolio value
    df['portfolio_value'] = df['capital'] + (df['position'] * df['price'])
    analyze_portfolio(df)
    # Step 1: Calculate cumulative max (previous peak)
    df['Prev_Peak'] = df['portfolio_value'].cummax()
    
    # Step 2: Calculate drawdown (percentage decline from previous peak)
    df['Drawdown'] = (df['portfolio_value'] - df['Prev_Peak']) / df['Prev_Peak']

    
    #draw_drawdown_chart(df)

    return df

def draw_drawdown_chart(df):
    # Convert index to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index)
    
    # Plot only the negative drawdowns (losses from peak)
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Drawdown'], color='blue', linewidth=1)
    
    # Title and labels
    plt.title('Portfolio Drawdown Over Time', fontsize=14)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Drawdown (Percentage)', fontsize=12)
    
    # Format x-axis for better readability
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.xticks(rotation=45)
    
    # Grid and layout for better aesthetics
    plt.grid(True)
    plt.tight_layout()
    plt.show()




def analyze_portfolio(df):
    # Create a DataFrame with the portfolio value series
    portfolio_values = df[['portfolio_value']]
    portfolio_values.index = pd.to_datetime(portfolio_values.index)
    
    # Calculate statistics using ffn
    stats = portfolio_values.calc_stats()
    stats.display()
    
    # Calculate drawdown series
    drawdown = stats.prices.to_drawdown_series()
    
    # Plot the portfolio performance and drawdowns
    stats.plot()

    # Create a figure with two subplots
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

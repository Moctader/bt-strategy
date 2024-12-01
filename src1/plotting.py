import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

def plot_transactions(df):
    buy_signals = df[df['signal'] == 'buy_long_position']
    sell_signals = df[df['signal'] == 'sell_long_position']
    short_signals = df[df['signal'] == 'short_position_sell']
    buy_back_signals = df[df['signal'] == 'buy_back']
    hold_signals = df[df['signal'] == 'hold']

    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, 
                        subplot_titles=('Price with Trading Signals', 
                                        'Cumulative PnL Over Time'),
                        vertical_spacing=0.15,
                        row_heights=[0.7, 0.3])

    # Add price line
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['price'], mode='lines', name='Price', line=dict(color='blue')),
        row=1, col=1
    )

    # Add buy signals
    fig.add_trace(
        go.Scatter(x=buy_signals['timestamp'], y=buy_signals['price'], mode='markers', name='Buy', marker=dict(symbol='triangle-up', color='green', size=10)),
        row=1, col=1
    )

    # Add sell signals
    fig.add_trace(
        go.Scatter(x=sell_signals['timestamp'], y=sell_signals['price'], mode='markers', name='Sell', marker=dict(symbol='triangle-down', color='red', size=10)),
        row=1, col=1
    )

    # Add short signals
    fig.add_trace(
        go.Scatter(x=short_signals['timestamp'], y=short_signals['price'], mode='markers', name='Short', marker=dict(symbol='triangle-left', color='orange', size=10)),
        row=1, col=1
    )

    # Add buy back signals
    fig.add_trace(
        go.Scatter(x=buy_back_signals['timestamp'], y=buy_back_signals['price'], mode='markers', name='Buy Back', marker=dict(symbol='triangle-right', color='purple', size=10)),
        row=1, col=1
    )

    # Add hold signals
    fig.add_trace(
        go.Scatter(x=hold_signals['timestamp'], y=hold_signals['price'], mode='markers', name='Hold', marker=dict(symbol='circle', color='blue', size=10)),
        row=1, col=1
    )

    # Add Cumulative PnL
    fig.add_trace(
        go.Scatter(x=df['timestamp'], y=df['cumulative_pnl'], mode='lines', name='Cumulative PnL', line=dict(color='purple')),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        height=800,
        showlegend=True,
        template='plotly_white',
        xaxis_rangeslider_visible=False
    )

    # Update y-axes labels
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="PnL", row=2, col=1)

    # Show the plot
    fig.show()












def plot_portfolio_values(portfolio_values):
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio_values, label='Portfolio Value', color='blue', linestyle='-', linewidth=2)
    plt.xlabel('Time')
    plt.ylabel('Portfolio Value')
    plt.title('Portfolio Value Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_drawdown(drawdown):
    plt.figure(figsize=(10, 6))
    plt.plot(drawdown, label='Drawdown', color='red', linestyle='-', linewidth=2)
    plt.xlabel('Time')
    plt.ylabel('Drawdown')
    plt.title('Drawdown Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_drawdown_vs_stock_price(df, drawdown):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Stock Price', color=color)
    ax1.plot(df.index, df['price'], color=color, label='Stock Price')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Drawdown', color=color)  # we already handled the x-label with ax1
    ax2.plot(df.index, drawdown, color=color, label='Drawdown')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Drawdown and Stock Price Over Time')
    fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
    plt.grid(True)
    plt.show()




def plot_portfolio_values_and_drawdown(portfolio_values, drawdown):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Portfolio Value', color=color)
    ax1.plot(portfolio_values, label='Portfolio Value', color=color, linestyle='-', linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Drawdown', color=color)  # we already handled the x-label with ax1
    ax2.plot(drawdown, label='Drawdown', color=color, linestyle='-', linewidth=2)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Portfolio Value and Drawdown Over Time')
    fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
    plt.grid(True)
    plt.show()
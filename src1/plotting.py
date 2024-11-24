import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_transactions(df):
    buy_signals = df[df['action'] == 'buy']
    sell_signals = df[df['action'] == 'sell']
    short_sell_signals = df[df['action'] == 'short_sell']
    cover_short_signals = df[df['action'] == 'cover_short']

    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, 
                        subplot_titles=('Price with Trading Signals', 
                                        'Cumulative PnL Over Time'),
                        vertical_spacing=0.15,
                        row_heights=[0.7, 0.3])

    # Add price line
    fig.add_trace(
        go.Scatter(x=df.index, y=df['share_price'], mode='lines', name='Price', line=dict(color='blue')),
        row=1, col=1
    )

    # Add buy signals
    fig.add_trace(
        go.Scatter(x=buy_signals.index, y=buy_signals['share_price'], mode='markers', name='Buy', marker=dict(symbol='triangle-up', color='green', size=10)),
        row=1, col=1
    )

    # Add sell signals
    fig.add_trace(
        go.Scatter(x=sell_signals.index, y=sell_signals['share_price'], mode='markers', name='Sell', marker=dict(symbol='triangle-down', color='red', size=10)),
        row=1, col=1
    )

    # Add short sell signals
    fig.add_trace(
        go.Scatter(x=short_sell_signals.index, y=short_sell_signals['share_price'], mode='markers', name='Short Sell', marker=dict(symbol='x', color='orange', size=10)),
        row=1, col=1
    )

    # Add cover short signals
    fig.add_trace(
        go.Scatter(x=cover_short_signals.index, y=cover_short_signals['share_price'], mode='markers', name='Cover Short', marker=dict(symbol='circle', color='purple', size=10)),
        row=1, col=1
    )

    # Add Cumulative PnL
    fig.add_trace(
        go.Scatter(x=df.index, y=df['cumulative_pnl'], mode='lines', name='Cumulative PnL', line=dict(color='purple')),
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
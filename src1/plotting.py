import plotly.graph_objects as go

def plot_transactions(df):
    buy_signals = df[df['action'] == 'buy']
    sell_signals = df[df['action'] == 'sell']
    short_sell_signals = df[df['action'] == 'short_sell']
    cover_short_signals = df[df['action'] == 'cover_short']

    fig = go.Figure()

    # Add price line
    fig.add_trace(go.Scatter(x=df.index, y=df['price'], mode='lines', name='Price', line=dict(color='blue')))

    # Add buy signals
    fig.add_trace(go.Scatter(x=buy_signals.index, y=buy_signals['price'], mode='markers', name='Buy', marker=dict(symbol='triangle-up', color='green', size=10)))

    # Add sell signals
    fig.add_trace(go.Scatter(x=sell_signals.index, y=sell_signals['price'], mode='markers', name='Sell', marker=dict(symbol='triangle-down', color='red', size=10)))

    # Add short sell signals
    fig.add_trace(go.Scatter(x=short_sell_signals.index, y=short_sell_signals['price'], mode='markers', name='Short Sell', marker=dict(symbol='x', color='orange', size=10)))

    # Add cover short signals
    fig.add_trace(go.Scatter(x=cover_short_signals.index, y=cover_short_signals['price'], mode='markers', name='Cover Short', marker=dict(symbol='circle', color='purple', size=10)))

    # Update layout
    fig.update_layout(
        title='Transactions',
        xaxis_title='Date',
        yaxis_title='Price',
        legend_title='Action',
        template='plotly_white'
    )

    fig.show()
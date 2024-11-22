import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_strategy_results(df):
    # Create figure with secondary y-axis
    fig = make_subplots(rows=2, cols=1, 
                        subplot_titles=('Price with Trading Actions', 
                                        'Cumulative PnL Over Time'),
                        vertical_spacing=0.15,
                        row_heights=[0.7, 0.3])

    # Add Price line
    fig.add_trace(
        go.Scatter(x=df.index, y=df['price'],
                   name='Price', line=dict(color='blue')),
        row=1, col=1
    )

    # Add buy actions
    buy_actions = df[df['action'] == 'buy']
    fig.add_trace(
        go.Scatter(x=buy_actions.index, y=buy_actions['price'],
                   name='Buy Action',
                   mode='markers',
                   marker=dict(symbol='triangle-up', size=10, color='green')),
        row=1, col=1
    )

    # Add sell actions
    sell_actions = df[df['action'] == 'sell']
    fig.add_trace(
        go.Scatter(x=sell_actions.index, y=sell_actions['price'],
                   name='Sell Action',
                   mode='markers',
                   marker=dict(symbol='triangle-down', size=10, color='red')),
        row=1, col=1
    )

    # Add short sell actions
    short_sell_actions = df[df['action'] == 'short_sell']
    fig.add_trace(
        go.Scatter(x=short_sell_actions.index, y=short_sell_actions['price'],
                   name='Short Sell Action',
                   mode='markers',
                   marker=dict(symbol='triangle-left', size=10, color='orange')),
        row=1, col=1
    )

    # Add cover short actions
    cover_short_actions = df[df['action'] == 'cover_short']
    fig.add_trace(
        go.Scatter(x=cover_short_actions.index, y=cover_short_actions['price'],
                   name='Cover Short Action',
                   mode='markers',
                   marker=dict(symbol='triangle-right', size=10, color='purple')),
        row=1, col=1
    )

    # Add hold actions
    hold_actions = df[df['action'] == 'hold']
    fig.add_trace(
        go.Scatter(x=hold_actions.index, y=hold_actions['price'],
                   name='Hold Action',
                   mode='markers',
                   marker=dict(symbol='circle', size=10, color='grey')),
        row=1, col=1
    )

    # Add Cumulative PnL
    fig.add_trace(
        go.Scatter(x=df.index, y=df['cumulative_pnl'],
                   name='Cumulative PnL', line=dict(color='purple')),
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


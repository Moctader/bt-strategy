import matplotlib.pyplot as plt
from strategy import TradingStrategy


def plot_cumulative_returns(trades_df):

    plt.figure(figsize=(14, 7))
    plt.plot(trades_df['date_of_trade'], trades_df['cumulative_return'], label='Cumulative Return', color='blue')
    plt.title('Cumulative Return of the Trading Strategy')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_signals(signals_df):
    plt.figure(figsize=(14, 7))
    plt.plot(self.df.index, self.df['Close'], label='Price', color='blue')

    buy_signals = self.signals_df[self.signals_df['Signal'] == 'Buy']
    sell_signals = self.signals_df[self.signals_df['Signal'] == 'Sell']

    plt.scatter(buy_signals.index, buy_signals['Entry_Price'], marker='^', color='green', label='Buy', s=100)
    plt.scatter(sell_signals.index, sell_signals['Entry_Price'], marker='v', color='red', label='Sell', s=100)

    plt.title('Price Chart with Buy and Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()








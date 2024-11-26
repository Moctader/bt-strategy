import numpy as np
import pandas as pd

class GenerateSignal:
    def __init__(self, df, wick_size=0.2, atr_period=20, slippage=0, size=1):
        self.df = df.copy()
        self.wick_size = wick_size
        self.atr_period = atr_period
        self.slippage = float(slippage) / 10000
        self.size = float(size) * 10000
        self.df['ATR'] = None
        self.df['average_bar'] = None
        self.df['small_wick'] = None
        self.df['spread'] = self.slippage
        self.df['size'] = self.size

    def average_bar_size(self):
        self.df['candle_size'] = self.df['High'] - self.df['Low']
        self.df['average_bar'] = self.df['candle_size'].rolling(20).mean()

    def small_wick(self):
        self.df['small_wick'] = np.where(
            (self.df['Close'] > self.df['Open']) &
            ((self.df['High'] - self.df['Close']) <= ((self.df['High'] - self.df['Low']) * self.wick_size)) &
            ((self.df['Open'] - self.df['Low']) <= ((self.df['High'] - self.df['Low']) * self.wick_size)) |
            (self.df['Close'] < self.df['Open']) &
            ((self.df['High'] - self.df['Open']) <= ((self.df['High'] - self.df['Low']) * self.wick_size)) &
            ((self.df['Close'] - self.df['Low']) <= ((self.df['High'] - self.df['Low']) * self.wick_size)),
            True, False
        )

    def calculate_atr(self):
        self.df['High-Low'] = abs(self.df['High'] - self.df['Low'])
        self.df['High-PrevClose'] = abs(self.df['High'] - self.df['Close'].shift(1))
        self.df['Low-PrevClose'] = abs(self.df['Low'] - self.df['Close'].shift(1))
        self.df['TR'] = self.df[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1, skipna=False)
        self.df['ATR'] = self.df['TR'].rolling(self.atr_period).mean()
        self.df.drop(['High-Low', 'High-PrevClose', 'Low-PrevClose'], axis=1, inplace=True)

    def generate_signals(self):
        self.calculate_atr()
        self.average_bar_size()
        self.small_wick()

        signals = []
        for i in range(20, len(self.df)):
            if (self.df['High'][i - 1] - self.df['Low'][i - 1]) >= 4 * self.df['average_bar'][i - 1] and self.df['small_wick'][i - 1]:
                if self.df['Close'][i - 1] > self.df['Open'][i - 1]:
                    signals.append((self.df.index[i], 'Buy', self.df['Close'][i]))
                elif self.df['Close'][i - 1] < self.df['Open'][i - 1]:
                    signals.append((self.df.index[i], 'Sell', self.df['Close'][i]))

        # Convert the list of signals into a DataFrame with proper column names
        signals_df = pd.DataFrame(signals, columns=['Date', 'Signal', 'Entry_Price'])

        # Convert the 'Date' column to datetime format
        signals_df['Date'] = pd.to_datetime(signals_df['Date'])

        # Set the 'Date' column as the index
        signals_df.set_index('Date', inplace=True)

        return signals_df

    def get_dataframe(self):
        return self.df
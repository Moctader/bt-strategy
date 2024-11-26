import pandas as pd
import matplotlib.pyplot as plt

class TradingStrategy:
    def __init__(self, df, signals_df, atr_sl=1):
        self.df = df
        self.signals_df = signals_df
        self.atr_sl = atr_sl
        self.open_trade = []
        self.trade = {}
        self.long_take_profit = []
        self.short_take_profit = []
        self.long_stop_loss = []
        self.short_stop_loss = []
        self.long_entry_price = []
        self.short_entry_price = []

    def execute(self):
        for index, signal in self.signals_df.iterrows():
            date = index
            action = signal['Signal']
            entry_price = signal['Entry_Price']
            i = self.df.index.get_loc(date)
            
            # Use match-case for Buy or Sell
            match action:
                case 'Buy':
                    if len(self.open_trade) == 0:
                        self._open_trade(i, date, entry_price, 'Buy')
                        
                case 'Sell':
                    if len(self.open_trade) == 0:
                        self._open_trade(i, date, entry_price, 'Sell')

            # Check for trade exits
            self._exit_trades(i)
            
            # Check for duration-based exits
            self._check_trade_duration(i)
        
        return self.trade

    def _open_trade(self, index, date, entry_price, signal):
        atr = self.df['ATR'][index]
        trade_data = {
            'ID': index,
            'date_of_trade': date,
            'entry_price': entry_price,
            'signal': signal,
            'result': 0,
            'TP': entry_price + atr * 4 * self.atr_sl if signal == 'Buy' else entry_price - atr * 4 * self.atr_sl,
            'SL': entry_price - atr * self.atr_sl if signal == 'Buy' else entry_price + atr * self.atr_sl
        }
        self.trade[index] = trade_data
        self.open_trade.append(index)
        
        if signal == 'Buy':
            self.long_take_profit.append(trade_data['TP'])
            self.long_stop_loss.append(trade_data['SL'])
            self.long_entry_price.append(trade_data['entry_price'])
        elif signal == 'Sell':
            self.short_take_profit.append(trade_data['TP'])
            self.short_stop_loss.append(trade_data['SL'])
            self.short_entry_price.append(trade_data['entry_price'])

    def _exit_trades(self, index):
        close_price = self.df['Close'][index]
        
        # Check if a long trade meets take profit or stop loss conditions
        if any(tp <= close_price for tp in self.long_take_profit):
            self._handle_exit(index, 'Buy', 'TP', close_price)
        if any(sl >= close_price for sl in self.long_stop_loss):
            self._handle_exit(index, 'Buy', 'SL', close_price)
        
        # Check if a short trade meets take profit or stop loss conditions
        if any(tp >= close_price for tp in self.short_take_profit):
            self._handle_exit(index, 'Sell', 'TP', close_price)
        if any(sl <= close_price for sl in self.short_stop_loss):
            self._handle_exit(index, 'Sell', 'SL', close_price)

    def _handle_exit(self, index, signal, exit_type, close_price):
        for j in list(self.open_trade):
            if self.trade[j].get('result', 0) == 0 and self.trade[j].get('signal', '') == signal:
                if exit_type == 'TP' and ((signal == 'Buy' and close_price >= self.trade[j]['TP']) or 
                                          (signal == 'Sell' and close_price <= self.trade[j]['TP'])):
                    profit = (self.trade[j]['TP'] - self.trade[j]['entry_price'] - self.df['spread'][index]) if signal == 'Buy' \
                             else (self.trade[j]['entry_price'] - self.trade[j]['TP'] - self.df['spread'][index])
                    self.trade[j].update({'result': profit * self.df['size'][index]})
                    self._remove_trade(j, signal)

                elif exit_type == 'SL' and ((signal == 'Buy' and close_price <= self.trade[j]['SL']) or 
                                            (signal == 'Sell' and close_price >= self.trade[j]['SL'])):
                    loss = (self.trade[j]['SL'] - self.trade[j]['entry_price'] - self.df['spread'][index]) if signal == 'Buy' \
                           else (self.trade[j]['entry_price'] - self.trade[j]['SL'] - self.df['spread'][index])
                    self.trade[j].update({'result': loss * self.df['size'][index]})
                    self._remove_trade(j, signal)

    def _remove_trade(self, trade_id, signal):
        self.open_trade.remove(trade_id)
        if signal == 'Buy':
            self.long_take_profit.remove(self.trade[trade_id]['TP'])
            self.long_stop_loss.remove(self.trade[trade_id]['SL'])
        elif signal == 'Sell':
            self.short_take_profit.remove(self.trade[trade_id]['TP'])
            self.short_stop_loss.remove(self.trade[trade_id]['SL'])

    def _check_trade_duration(self, index):
        if len(self.open_trade) == 0:
            return
        
        for j in list(self.open_trade):
            trade_duration_minutes = (self.df.index[index] - self.trade[j]['date_of_trade']).total_seconds() / 60
            if trade_duration_minutes >= 12 * 60 and self.trade[j].get('result', 0) == 0:
                close_price = self.df['Close'][index]
                signal = self.trade[j]['signal']
                
                if signal == 'Buy':
                    profit = (close_price - self.trade[j]['entry_price'] - self.df['spread'][index])
                    self.trade[j].update({'result': profit * self.df['size'][index]})
                elif signal == 'Sell':
                    loss = (self.trade[j]['entry_price'] - close_price - self.df['spread'][index])
                    self.trade[j].update({'result': loss * self.df['size'][index]})
                
                self._remove_trade(j, signal)

    def calculate_cumulative_returns(self):
        # Create a DataFrame from the trades dictionary
        trades_df = pd.DataFrame.from_dict(self.trade, orient='index')

        # Sort the DataFrame by the date of trade
        trades_df.sort_values(by='date_of_trade', inplace=True)

        # Calculate cumulative returns
        trades_df['cumulative_return'] = trades_df['result'].cumsum()

        return trades_df

    def plot_cumulative_returns(self):
        trades_df = self.calculate_cumulative_returns()

        plt.figure(figsize=(14, 7))
        plt.plot(trades_df['date_of_trade'], trades_df['cumulative_return'], label='Cumulative Return', color='blue')
        plt.title('Cumulative Return of the Trading Strategy')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Return')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_signals(self):
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








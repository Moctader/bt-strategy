from trade_manager import TradeManager

class strategy_v0:
    def __init__(self):
        self.trade_manager = TradeManager()  

    def execute(self, signals):
        transactions = []  

        for index, signal_data in signals.iterrows():
            self.signal = signal_data['signal']  
            self.share_price = signal_data['close']  
            self.previous_share_price = signals['close'].iloc[index - 1] if index > 0 else self.share_price  
            self.timestamp = signal_data['timestamp']
            
            match self.signal:
                # 1: Buy Signal
                case 1 if self.trade_manager.capital > self.share_price + self.trade_manager.transaction_fee and self.trade_manager.in_position == None:
                    # Buy if there's enough capital
                    self.trade_manager.buy(transactions, self.share_price, self.timestamp)
                    self.trade_manager.in_position = 'long'  # Enter long in_position
                    self.trade_manager.buy_price = self.share_price  # Store the buy price

                # -1: Sell Signal (exit long in_position)
                case -1 if self.trade_manager.in_position == 'long'and self.trade_manager.position > 0 and self.trade_manager.in_position != 'short':
                    # Sell everything to exit the long in_position
                    self.trade_manager.sell(transactions, self.share_price, self.timestamp)
                    self.trade_manager.in_position = None  # Exit the long in_position

                # -1: Sell Signal for short in_position (waiting for the short signal)
                case -1 if self.trade_manager.in_position != 'short' and self.trade_manager.in_position != 'long':
                    # Enter short in_position: Borrow shares and sell them at the current price
                    self.trade_manager.in_position = 'short'  # Now in a short in_position
                    self.trade_manager.borrow_share_and_sell_immediately(transactions, self.share_price, self.timestamp)

                # 1: Sell Signal (to close the short in_position and take profit/loss)
                case -1 if self.trade_manager.in_position == 'short':
                    # Buy back the borrowed shares to close the short in_position
                    self.trade_manager.buy_back_borrowed_shares(transactions, self.share_price, self.timestamp)
                    self.trade_manager.in_position = None  

                # Hold signal: Hold the current in_position without any transaction
                case 0:
                    self.trade_manager.hold(transactions, self.share_price, self.timestamp)
                ## End of match
        return transactions
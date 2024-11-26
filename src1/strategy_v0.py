from trade_manager import TradeManager  

class strategy_v0:
    def __init__(self, stop_loss_threshold=0.05, take_profit_threshold=0.1):
        self.trade_manager = TradeManager()  
        self.stop_loss_threshold = stop_loss_threshold  
        self.take_profit_threshold = take_profit_threshold  

    def execute(self, signals):
        transactions = []  
        portfolio_values = []  

        for index, signal_data in signals.iterrows():
            self.signal = signal_data['signal']  
            self.share_price = signal_data['close']  
            self.previous_share_price = signals['close'].iloc[index - 1] if index > 0 else self.share_price  

            # If in short sell position, wait until previous_share_price > share_price to cover short
            if self.trade_manager.in_short_position:
                if self.previous_share_price is not None and self.previous_share_price > self.share_price:
                    self.trade_manager.cover_short(transactions, self.share_price)  
                else:
                    self.trade_manager.hold(transactions, self.share_price)  
                continue

            match self.signal:
                # Buy signal: Buy if there is enough capital to cover the share price and transaction fee
                case 1 if self.trade_manager.capital > self.share_price + self.trade_manager.transaction_fee:
                    self.trade_manager.buy(transactions, self.share_price)

                # Sell signal: Sell if there is an existing position
                case -1 if self.trade_manager.position > 0:
                    self.trade_manager.sell(transactions, self.share_price)

                # Short sell signal: Initiate a short sell if there is no existing position and not already in a short position
                case -1 if self.trade_manager.position == 0 and not self.trade_manager.in_short_position:
                    self.trade_manager.short_sell(transactions, self.share_price)

                # Exit signal: Exit the current position
                case 2:
                    self.trade_manager.exit(transactions, self.share_price)

                # Hold signal: Hold the current position without any transaction
                case 3:
                    self.trade_manager.hold(transactions, self.share_price)

            # Calculate portfolio value
            portfolio_value = self.trade_manager.capital + (self.trade_manager.position * self.share_price)
            portfolio_values.append(portfolio_value)  

        return transactions, portfolio_values  
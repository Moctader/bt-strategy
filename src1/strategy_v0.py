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
            self.timestamp= signal_data['timestamp']
            match self.signal:
                # Buy signal: Buy if there is enough capital to cover the share price and transaction fee
                case 1 if self.trade_manager.capital > self.share_price + self.trade_manager.transaction_fee:
                    self.trade_manager.buy(transactions, self.share_price, self.timestamp)

                # Sell signal: Sell if there is an existing position
                case -1 if self.trade_manager.position > 0:
                    self.trade_manager.sell(transactions, self.share_price, self.timestamp)

                # Hold signal: Hold the current position without any transaction
                case 0:
                    self.trade_manager.hold(transactions, self.share_price, self.timestamp)
 

        return transactions  

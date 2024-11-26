from trade_manager import TradeManager
trade_manager = TradeManager()

class strategy_v0:

    def execute(self, signals):
        transactions = []
        portfolio_values = []

        for index, signal_data in signals.iterrows():
            self.signal = signal_data['signal']
            self.share_price = signal_data['close']
            
            # Calculate previous share price if index is greater than 0
            if index > 0:
                self.previous_share_price = signals['close'].iloc[index - 1]
            else:
                self.previous_share_price = None

            # If in short sell position, wait until previous_share_price > share_price to cover short
            if trade_manager.in_short_position:
                if self.previous_share_price is not None and self.previous_share_price > self.share_price:
                    trade_manager.cover_short(transactions, self.share_price)
                else:
                    trade_manager.hold(transactions, self.share_price)
                continue

            match self.signal:
                case 1 if trade_manager.capital > self.share_price + trade_manager.transaction_fee:
                    trade_manager.buy(transactions, self.share_price)
                case -1 if trade_manager.position > 0:
                    trade_manager.sell(transactions, self.share_price)
                case -1 if trade_manager.position == 0 and not trade_manager.in_short_position:
                    trade_manager.short_sell(transactions, self.share_price)
                case 2:
                    trade_manager.exit(transactions, self.share_price)
                case 3:
                    trade_manager.adjust(transactions, self.share_price)
                case 4:
                    trade_manager.hold(transactions, self.share_price)
                case _:
                    trade_manager.hold(transactions, self.share_price)

            # Calculate portfolio value
            portfolio_value = trade_manager.capital + (trade_manager.position * self.share_price)
            portfolio_values.append(portfolio_value)

        return transactions, portfolio_values
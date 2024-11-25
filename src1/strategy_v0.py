from trade_manager import TradeManager
trade_manager = TradeManager()

class strategy_v0:

    def execute(self, signals):
        transactions = []
        portfolio_values = []

        for index, signal_data in signals.iterrows():
            self.signal = signal_data['signal']
            self.share_price = signal_data['close']
            self.next_share_price = signals['close'].shift(-1).iloc[index]

            # If in short sell position, wait until next_share_price > share_price to cover short
            if trade_manager.in_short_position:
                if self.next_share_price > self.share_price:
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
                case _:
                    trade_manager.hold(transactions, self.share_price)


            # calculating protfolio value
            latest_known_value = self.share_price
            portfolio_value = trade_manager.capital + (trade_manager.position * latest_known_value)
            portfolio_values.append(portfolio_value)

        return transactions, portfolio_values
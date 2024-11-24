from trade_manager import TradeManager
trade_manager = TradeManager()

class strategy_v0:

    def execute(self, signals):
        transactions = []

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

        return transactions
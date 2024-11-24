from PnLCalculator import PnLCalculator
PnLCalculator = PnLCalculator()


class strategy_v0:

    def execute(self, signals):
        transactions = []

        for index, signal_data in signals.iterrows():
            self.signal = signal_data['signal']
            self.share_price = signal_data['close']
            self.next_share_price = signals['close'].shift(-1).iloc[index]
            

            # If in short sell position, wait until next_share_price > share_price to cover short
            if PnLCalculator.in_short_position:
                if self.next_share_price > self.share_price:
                    PnLCalculator.cover_short(transactions, self.share_price)
                else:
                    PnLCalculator.hold(transactions, self.share_price)
                continue

            if self.signal == 1 and PnLCalculator.capital > self.share_price + PnLCalculator.transaction_fee:
                PnLCalculator.buy(transactions, self.share_price)
            elif self.signal == -1 and PnLCalculator.position > 0:
                PnLCalculator.sell(transactions, self.share_price)
            elif self.signal == -1 and PnLCalculator.position == 0 and not PnLCalculator.in_short_position:
                PnLCalculator.short_sell(transactions, self.share_price)
            else:
                PnLCalculator.hold(transactions, self.share_price)

        return transactions

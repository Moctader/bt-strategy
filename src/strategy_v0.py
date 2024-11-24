class Strategy:
    def __init__(self, initial_capital=100000, transaction_fee=2):
        self.capital = initial_capital
        self.transaction_fee = transaction_fee
        self.position = 0
        self.shares = 0
        self.borrowed_shares = 0
        self.in_short_position = False
        self.buy_prices = 0
        self.borrowed_shares_liquidation = 0

    def add_transaction(self, transactions, action, shares, price, profit=0, in_short_position=None):
        transaction = {
            'action': action,
            'shares': shares,
            'price': price,
            'capital': self.capital,
            'position': self.position,
            'profit': profit,
            'in_short_position': self.in_short_position if in_short_position is None else in_short_position
        }
        transactions.append(transaction)

    def buy(self, transactions, share_price):
        number_of_shares = (self.capital - self.transaction_fee) // share_price
        self.position += number_of_shares
        self.capital -= number_of_shares * share_price + self.transaction_fee
        self.buy_prices += number_of_shares * share_price
        self.add_transaction(transactions, 'buy', number_of_shares, share_price)

    def sell(self, transactions, share_price):
        total_sell_price = self.position * share_price
        profit = total_sell_price - (self.buy_prices + self.transaction_fee)
        if profit > 0:
            self.capital += total_sell_price - self.transaction_fee
            self.add_transaction(transactions, 'sell', self.position, share_price, profit)
            self.position = 0  # Reset position after selling
            self.buy_prices = 0

    def short_sell(self, transactions, share_price):
        self.in_short_position = True
        self.borrowed_shares = 10
        self.borrowed_shares_liquidation = self.borrowed_shares * share_price
        self.capital -= self.transaction_fee  # Deduct transaction fee for short sell
        self.add_transaction(transactions, 'short_sell', self.borrowed_shares, share_price)

    def cover_short(self, transactions, share_price):
        short_sell_profit = self.borrowed_shares_liquidation - self.borrowed_shares * share_price
        if short_sell_profit > 0:
            self.capital += short_sell_profit
            self.add_transaction(transactions, 'cover_short', self.borrowed_shares, share_price, short_sell_profit, False)
            self.borrowed_shares = 0
            self.in_short_position = False  # Turn off flag after covering short

    def hold(self, transactions, share_price):
        self.add_transaction(transactions, 'hold', self.position, share_price)

    def execute(self, signals):
        transactions = []

        for signal_data in signals:
            signal = signal_data['signal']
            share_price = signal_data['prediction']
            next_share_price = signal_data['next_prediction']

            # If in short sell position, wait until next_share_price > share_price to cover short
            if self.in_short_position:
                if next_share_price > share_price:
                    self.cover_short(transactions, share_price)
                else:
                    self.hold(transactions, share_price)
                continue

            if signal == 1 and self.capital > share_price + self.transaction_fee:
                self.buy(transactions, share_price)
            elif signal == -1 and self.position > 0:
                self.sell(transactions, share_price)
            elif signal == -1 and self.position == 0 and not self.in_short_position:
                self.short_sell(transactions, share_price)
            else:
                self.hold(transactions, share_price)

        return transactions




class Strategy_v1:
    def __init__(self, initial_capital=100000, transaction_fee=2):
        self.capital = initial_capital
        self.transaction_fee = transaction_fee
        self.position = 0
        self.shares = 0
        self.borrowed_shares = 0
        self.flag = False
        self.buy_prices = 0
        self.borrowed_shares_liquidation = 0

    def execute(self, signals):
        transactions = []

        for signal_data in signals:
            signal = signal_data['signal']
            share_price = signal_data['prediction']
            next_share_price = signal_data['next_prediction']

            if signal == 1 and self.capital > share_price + self.transaction_fee:
                # Buy shares if the signal is 1 and there is enough capital
                number_of_shares = (self.capital - self.transaction_fee) // share_price
                self.position += number_of_shares
                self.capital -= number_of_shares * share_price + self.transaction_fee
                self.buy_prices += number_of_shares * share_price

                transactions.append({
                    'action': 'buy',
                    'shares': number_of_shares,
                    'price': share_price,
                    'capital': self.capital,
                    'position': self.position
                })

            elif signal == -1:
                # Check if there's a position to sell
                if self.position > 0:
                    total_sell_price = self.position * share_price
                    profit = total_sell_price - (self.buy_prices + self.transaction_fee)
                    if profit > 0:
                        self.capital += total_sell_price - self.transaction_fee
                        transactions.append({
                            'action': 'sell',
                            'shares': self.position,
                            'price': share_price,
                            'capital': self.capital,
                            'profit': profit,
                            'position': 0
                        })
                        self.position = 0  # Reset position after selling
                        self.buy_prices = 0
                    else:
                        # If profit condition is not fulfilled, go for short selling
                        self.flag = True
                        self.borrowed_shares = 10
                        self.borrowed_shares_liquidation = self.borrowed_shares * share_price
                        self.capital -= self.transaction_fee  # Deduct transaction fee for short sell
                        transactions.append({
                            'action': 'short_sell',
                            'shares': self.borrowed_shares,
                            'price': share_price,
                            'capital': self.capital,
                            'flag': self.flag
                        })

                        if self.flag:
                            # If in short sell position, wait until next_share_price > share_price to cover short
                            if next_share_price > share_price:
                                short_sell_profit = self.borrowed_shares_liquidation - self.borrowed_shares * share_price
                                if short_sell_profit > 0:
                                    self.capital += short_sell_profit
                                    transactions.append({
                                        'action': 'cover_short',
                                        'shares': self.borrowed_shares,
                                        'price': share_price,
                                        'capital': self.capital,
                                        'profit': short_sell_profit,
                                        'flag': False
                                    })
                                    self.borrowed_shares_liquidation = 0
                                    self.borrowed_shares = 0
                                    self.flag = False  # Turn off flag after covering short
                            else:
                                # Hold condition during short sell
                                transactions.append({
                                    'action': 'hold',
                                    'shares': self.position,
                                    'price': share_price,
                                    'capital': self.capital,
                                    'position': self.position,
                                    'flag': self.flag
                                })
                            continue

                elif self.position == 0 and signal== -1 and not self.flag:
                    # Short selling scenario
                    self.flag = True
                    self.borrowed_shares = 10
                    self.borrowed_shares_liquidation = self.borrowed_shares * share_price
                    self.capital -= self.transaction_fee  # Deduct transaction fee for short sell
                    transactions.append({
                        'action': 'short_sell',
                        'shares': self.borrowed_shares,
                        'price': share_price,
                        'capital': self.capital,
                        'flag': self.flag
                    })


                    if self.flag:
                        # If in short sell position, wait until next_share_price > share_price to cover short
                        if next_share_price > share_price:
                            short_sell_profit = self.borrowed_shares_liquidation - self.borrowed_shares * share_price
                            if short_sell_profit > 0:
                                self.capital += short_sell_profit
                                transactions.append({
                                    'action': 'cover_short',
                                    'shares': self.borrowed_shares,
                                    'price': share_price,
                                    'capital': self.capital,
                                    'profit': short_sell_profit,
                                    'flag': False
                                })
                                self.borrowed_shares_liquidation = 0
                                self.borrowed_shares = 0
                                self.flag = False  # Turn off flag after covering short
                        else:
                            # Hold condition during short sell
                            transactions.append({
                                'action': 'hold',
                                'shares': self.position,
                                'price': share_price,
                                'capital': self.capital,
                                'position': self.position,
                                'flag': self.flag
                            })
                        continue

            else:
                # Hold condition
                transactions.append({
                    'action': 'hold',
                    'shares': self.position,
                    'price': share_price,
                    'capital': self.capital,
                    'position': self.position,
                    'flag': self.flag
                })

        return transactions
class TradeManager:
    def __init__(self):
        self.capital = 100000
        self.transaction_fee = 2
        self.position = 0
        self.shares = 0
        self.buy_prices = 0

    # Add transaction data to the transactions list
    def add_transaction(self, transactions, action, shares, price, timestamp, profit=0):
        transaction = {
            'action': action,
            'shares': shares,
            'share_price': price,
            'capital': self.capital,
            'position': self.position,
            'profit': profit,
            'timestamp': timestamp
        }
        transactions.append(transaction)
    
    # Buy shares based on the available capital and transaction fee 
    def buy(self, transactions, share_price, timestamp):
        number_of_shares = (self.capital - self.transaction_fee) // share_price
        self.position += number_of_shares
        self.capital -= number_of_shares * share_price 
        self.buy_prices += number_of_shares * share_price
        self.add_transaction(transactions, 'buy', number_of_shares, share_price, timestamp)

    # Sell shares based on the current position and share price 
    def sell(self, transactions, share_price, timestamp):
        total_sell_price = self.position * share_price
        profit = total_sell_price - (self.buy_prices + self.transaction_fee)
        self.capital += total_sell_price - self.transaction_fee
        self.position = 0  
        self.buy_prices = 0
        self.add_transaction(transactions, 'sell', self.position, share_price, timestamp, profit)

    # Hold the current position without any transaction 
    def hold(self, transactions, share_price, timestamp):
        self.add_transaction(transactions, 'hold', self.position, share_price, timestamp)
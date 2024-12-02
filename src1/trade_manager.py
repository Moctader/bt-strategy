class TradeManager:
    def __init__(self):
        self.capital = 100000  # Initial capital
        self.transaction_fee = 2  # Transaction fee per trade
        self.position = 0  # Current position (number of shares)
        self.shares = 0  # Total number of shares in hand (used for long position)
        self.buy_prices = 0  # Total cost of shares purchased for long positions
        self.profit_loss = 0  # Accumulated profit/loss from trades
        self.borrowed_shares = 0  # Number of shares borrowed for short selling
        self.liquidated_borrow_shares = 0  # Amount liquidated from borrowed shares
        self.in_position = None

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
        self.capital -= number_of_shares * share_price + self.transaction_fee  
        self.buy_prices += number_of_shares * share_price 
        self.add_transaction(transactions, 'buy_long_position', number_of_shares, share_price, timestamp)

    # Sell shares based on the current position and share price
    def sell(self, transactions, share_price, timestamp):
        total_sell_price = self.position * share_price
        profit_loss = total_sell_price - self.buy_prices - self.transaction_fee
        self.capital += total_sell_price - self.transaction_fee  
        self.position = 0  
        self.buy_prices = 0  
        self.add_transaction(transactions, 'sell_long_position', self.position, share_price, timestamp, profit_loss)

    # Hold the current position without any transaction
    def hold(self, transactions, share_price, timestamp):
        self.add_transaction(transactions, 'hold', self.position, share_price, timestamp)

    # Borrow shares for short selling (simulated)
    def borrow_share_and_sell_immediately(self, transactions, share_price, timestamp):
        self.borrowed_shares = 100
        self.liquidated_borrow_shares = self.borrowed_shares * share_price 
        self.capital += self.liquidated_borrow_shares - self.transaction_fee  
        self.add_transaction(transactions, 'short_position_sell', self.borrowed_shares, share_price, timestamp)

    # Buy back borrowed shares to close the short position
    def buy_back_borrowed_shares(self, transactions, share_price, timestamp):
        cost_to_buy_back = self.borrowed_shares * share_price
        profit_loss = self.liquidated_borrow_shares - cost_to_buy_back - self.transaction_fee  
        self.capital -= cost_to_buy_back + self.transaction_fee  # Deduct cost to buy back and transaction fee
        self.add_transaction(transactions, 'buy_back', self.borrowed_shares, share_price, timestamp, profit_loss)
        self.borrowed_shares = 0 
        self.liquidated_borrow_shares = 0

import pandas as pd

class PnLCalculator:
    def add_pnl_data(self, pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, profit=0, in_short_position=None):
        pnl_data.append({
            'action': action,
            'shares': shares,
            'price': price,
            'capital': capital,
            'position': position,
            'point_pnl': point_pnl,
            'cumulative_pnl': cumulative_pnl,
            'profit': profit,
            'in_short_position': in_short_position
        })

    def handle_buy(self, pnl_data, transaction, cumulative_pnl):
        point_pnl = 0  # No immediate profit/loss when buying
        self.add_pnl_data(pnl_data, 'buy', transaction['shares'], transaction['price'], transaction['capital'], transaction['position'], point_pnl, cumulative_pnl)

    def handle_sell(self, pnl_data, transaction, cumulative_pnl):
        point_pnl = transaction['profit']  # Profit calculated during the sell
        cumulative_pnl += point_pnl  # Update cumulative PnL
        self.add_pnl_data(pnl_data, 'sell', transaction['shares'], transaction['price'], transaction['capital'], transaction['position'], point_pnl, cumulative_pnl, transaction['profit'])
        return cumulative_pnl

    def handle_short_sell(self, pnl_data, transaction, cumulative_pnl):
        point_pnl = 0  # No immediate profit/loss when initiating a short sell
        self.add_pnl_data(pnl_data, 'short_sell', transaction['shares'], transaction['price'], transaction['capital'], transaction['position'], point_pnl, cumulative_pnl, in_short_position=transaction['in_short_position'])

    def handle_cover_short(self, pnl_data, transaction, cumulative_pnl):
        point_pnl = transaction['profit']  # Profit from covering the short position
        cumulative_pnl += point_pnl  # Update cumulative PnL
        self.add_pnl_data(pnl_data, 'cover_short', transaction['shares'], transaction['price'], transaction['capital'], transaction['position'], point_pnl, cumulative_pnl, transaction['profit'], transaction['in_short_position'])
        return cumulative_pnl

    def handle_hold(self, pnl_data, transaction, cumulative_pnl):
        point_pnl = 0  # No immediate profit/loss when holding
        self.add_pnl_data(pnl_data, 'hold', transaction['shares'], transaction['price'], transaction['capital'], transaction['position'], point_pnl, cumulative_pnl, in_short_position=transaction['in_short_position'])

    def calculate(self, transactions):
        pnl_data = []
        cumulative_pnl = 0

        for transaction in transactions:
            action = transaction['action']
            if action == 'buy':
                self.handle_buy(pnl_data, transaction, cumulative_pnl)
            elif action == 'sell':
                cumulative_pnl = self.handle_sell(pnl_data, transaction, cumulative_pnl)
            elif action == 'short_sell':
                self.handle_short_sell(pnl_data, transaction, cumulative_pnl)
            elif action == 'cover_short':
                cumulative_pnl = self.handle_cover_short(pnl_data, transaction, cumulative_pnl)
            elif action == 'hold':
                self.handle_hold(pnl_data, transaction, cumulative_pnl)

        df = pd.DataFrame(pnl_data)
        df['percentage_return'] = 0.0

        # Calculate percentage return
        df['percentage_return'] = df['point_pnl'] / df['capital'].shift(1) * 100
        df['percentage_return'] = df['percentage_return'].fillna(0)

        return df
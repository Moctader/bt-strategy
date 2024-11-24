class ProfitAndLoss:
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

    def calculate(self, transactions):
        pnl_data = []
        cumulative_pnl = 0

        for index, transaction in transactions.iterrows():
            point_pnl = 0  # Reset point-to-point PnL for each transaction

            action = transaction['action']
            shares = transaction['shares']
            price = transaction['price']
            capital = transaction['capital']
            position = transaction['position']
            profit = transaction.get('profit', 0)
            in_short_position = transaction.get('in_short_position', None)

            if action == 'buy':
                # No immediate profit/loss when buying, so point_pnl is 0
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl)

            elif action == 'sell':
                # Calculate point-to-point PnL for the sell action
                point_pnl = profit  # Profit calculated during the sell
                cumulative_pnl += point_pnl  # Update cumulative PnL
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, profit)

            elif action == 'short_sell':
                # No immediate profit/loss when initiating a short sell, so point_pnl is 0
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, in_short_position=in_short_position)

            elif action == 'cover_short':
                # Calculate point-to-point PnL for covering a short
                point_pnl = profit  # Profit from covering the short position
                cumulative_pnl += point_pnl  # Update cumulative PnL
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, profit, in_short_position)

            elif action == 'hold':
                # No immediate profit/loss when holding, so point_pnl is 0
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, in_short_position=in_short_position)

        return pnl_data
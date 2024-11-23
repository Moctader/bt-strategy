class PnLCalculator:
    def calculate(self, transactions):
        pnl_data = []
        cumulative_pnl = 0

        for transaction in transactions:
            point_pnl = 0  # Reset point-to-point PnL for each transaction

            if transaction['action'] == 'buy':
                # No immediate profit/loss when buying, so point_pnl is 0
                pnl_data.append({
                    'action': 'buy',
                    'shares': transaction['shares'],
                    'price': transaction['price'],
                    'capital': transaction['capital'],
                    'position': transaction['position'],
                    'point_pnl': point_pnl,
                    'cumulative_pnl': cumulative_pnl
                })

            elif transaction['action'] == 'sell':
                # Calculate point-to-point PnL for the sell action
                point_pnl = transaction['profit']  # Profit calculated during the sell
                cumulative_pnl += point_pnl  # Update cumulative PnL

                pnl_data.append({
                    'action': 'sell',
                    'shares': transaction['shares'],
                    'price': transaction['price'],
                    'profit': transaction['profit'],
                    'capital': transaction['capital'],
                    'point_pnl': point_pnl,
                    'cumulative_pnl': cumulative_pnl
                })

            elif transaction['action'] == 'short_sell':
                # No immediate profit/loss when initiating a short sell, so point_pnl is 0
                pnl_data.append({
                    'action': 'short_sell',
                    'shares': transaction['shares'],
                    'price': transaction['price'],
                    'capital': transaction['capital'],
                    'flag': transaction['flag'],
                    'point_pnl': point_pnl,
                    'cumulative_pnl': cumulative_pnl
                })

            elif transaction['action'] == 'cover_short':
                # Calculate point-to-point PnL for covering a short
                point_pnl = transaction['profit']  # Profit from covering the short position
                cumulative_pnl += point_pnl  # Update cumulative PnL

                pnl_data.append({
                    'action': 'cover_short',
                    'shares': transaction['shares'],
                    'price': transaction['price'],
                    'profit': transaction['profit'],
                    'capital': transaction['capital'],
                    'flag': transaction['flag'],
                    'point_pnl': point_pnl,
                    'cumulative_pnl': cumulative_pnl
                })

            elif transaction['action'] == 'hold':
                # No immediate profit/loss when holding, so point_pnl is 0
                pnl_data.append({
                    'action': 'hold',
                    'shares': transaction['shares'],
                    'price': transaction['price'],
                    'capital': transaction['capital'],
                    'position': transaction['position'],
                    'flag': transaction['flag'],
                    'point_pnl': point_pnl,
                    'cumulative_pnl': cumulative_pnl
                })

        return pnl_data
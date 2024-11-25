import yaml
from trade_manager import TradeManager

class ProfitAndLoss:
    def __init__(self):
        self.initial_values = {}
        self.final_values = {}

    def add_pnl_data(self, pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, profit=0, in_short_position=None):
        pnl_data.append({
            'action': action,
            'shares': shares,
            'share_price': price,
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
            price = transaction['share_price']
            capital = transaction['capital']
            position = transaction['position']
            profit = transaction.get('profit', 0)
            in_short_position = transaction.get('in_short_position', None)
            trade_manager = TradeManager()


            # Track initial values
            if index == 0:
                self.initial_values = {
                    'capital': trade_manager.capital,
                    'position': trade_manager.position,
                }

            # Track final values
            if index == len(transactions) - 1:
                self.final_values = {
                    'share_price': price,
                    'capital': capital,
                    'position': position,
                    #'cumulative_pnl': cumulative_pnl,
                    'final_liquid': capital + position * price
                }

            # No immediate profit/loss when buying, so point_pnl is 0
            if action == 'buy':
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl)

            # Calculate point-to-point PnL for the sell action
            elif action == 'sell':
                point_pnl = profit  
                cumulative_pnl += point_pnl  # Update cumulative PnL
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, profit)

            # No immediate profit/loss when initiating a short sell, so point_pnl is 0
            elif action == 'short_sell':
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, in_short_position=in_short_position)

            # Calculate point-to-point PnL for covering a short
            elif action == 'cover_short':
                point_pnl = profit  # Profit from covering the short position
                cumulative_pnl += point_pnl  # Update cumulative PnL
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, profit, in_short_position)

            # No immediate profit/loss when holding, so point_pnl is 0
            elif action == 'hold':
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, in_short_position=in_short_position)

        return pnl_data
    

    def save_to_yaml(self, filename='initial_final_values.yaml'):
        data = {
            'initial_values': self.initial_values,
            'final_values': self.final_values
        }
        with open(filename, 'w') as file:
            yaml.dump(data, file)
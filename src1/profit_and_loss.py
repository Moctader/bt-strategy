import yaml
from trade_manager import TradeManager

class ProfitAndLoss:
    def __init__(self):
        self.initial_values = {}
        self.final_values = {}
        self.trade_manager = TradeManager()
        self.cumulative_pnl = 0  # Initialize cumulative_pnl
        self.final_capital = self.trade_manager.capital + self.cumulative_pnl

    def add_pnl_data(self, pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, timestamp, profit=0):
        pnl_data.append({
            'action': action,
            'shares': shares,
            'share_price': price,
            'capital': capital,
            'position': position,
            'point_pnl': point_pnl,
            'cumulative_pnl': cumulative_pnl,
            'timestamp': timestamp,
            'profit': profit
        })

    def calculate(self, transactions):
        pnl_data = []
        self.cumulative_pnl = 0  # Reset cumulative_pnl

        for index, transaction in transactions.iterrows():
            point_pnl = 0  # Reset point-to-point PnL for each transaction

            action = transaction['action']
            shares = transaction['shares']
            price = transaction['share_price']
            capital = transaction['capital']
            position = transaction['position']
            profit = transaction.get('profit', 0)
            timestamp = transaction['timestamp']

            # Ensure profit is a numeric type
            profit = float(profit)

            # Track initial values
            if index == 0:
                self.initial_values = {
                    'capital': self.trade_manager.capital,
                    'position': self.trade_manager.position,
                }

            # No immediate profit/loss when buying, so point_pnl is 0
            if action == 'buy':
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp)

            # Calculate point-to-point PnL for the sell action
            elif action == 'sell':
                point_pnl = profit  # Profit from selling the position
                self.cumulative_pnl += point_pnl  # Update cumulative PnL
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp, profit)

            # No immediate profit/loss when holding, so point_pnl is 0
            elif action == 'hold':
                self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp)

        # Track final values outside the loop
        self.final_values = {
            'share_price': price,
            'final_capital': self.trade_manager.capital,
            'cumulative_pnl': self.cumulative_pnl,
        }

        return pnl_data

    def save_to_yaml(self, filename='initial_final_values.yaml'):
        data = {
            'initial_values': self.initial_values,
            'final_values': self.final_values
        }
        with open(filename, 'w') as file:
            yaml.dump(data, file)
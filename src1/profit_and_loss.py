import yaml
from trade_manager import TradeManager

class ProfitAndLoss:
    def __init__(self):
        self.trade_manager = TradeManager()
        self.cumulative_pnl = 0  
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

        for index, transaction in transactions.iterrows():
            point_pnl = 0  

            action = transaction['action']
            shares = transaction['shares']
            price = transaction['share_price']
            capital = transaction['capital']
            position = transaction['position']
            profit = transaction.get('profit', 0)
            timestamp = transaction['timestamp']

            profit = float(profit)

            match action:
                case 'buy':
                    self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp)

                case 'sell':
                    point_pnl = profit  
                    self.cumulative_pnl += point_pnl  
                    self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp, profit)

                case 'hold':
                    self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp)

   

        return pnl_data


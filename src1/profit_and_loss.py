import yaml
from trade_manager import TradeManager

class ProfitAndLoss:
    def __init__(self):
        self.trade_manager = TradeManager()
        self.cumulative_pnl = 0  
        self.final_capital = self.trade_manager.capital + self.cumulative_pnl

    def add_pnl_data(self, pnl_data, action, shares, price, capital, position, point_pnl, cumulative_pnl, timestamp, profit=0):
        pnl_data.append({
            'signal': action,
            'price': price,
            'capital': capital,
            'position': position,
            'pnl': point_pnl,
            'cumulative_pnl': cumulative_pnl,
            'timestamp': timestamp,
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
            profit = transaction['profit']
            timestamp = transaction['timestamp']

            profit = float(profit)
            match action:
                case 'buy_long_position': 
                    point_pnl = profit - self.trade_manager.transaction_fee
                    self.cumulative_pnl += point_pnl
                    self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp)

                case 'sell_long_position':
                    point_pnl = profit 
                    self.cumulative_pnl += point_pnl 
                    self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp, profit)

                case 'short_position_sell':
                    point_pnl = profit  - self.trade_manager.transaction_fee
                    self.cumulative_pnl += point_pnl
                    self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp)

                case 'buy_back':
                    point_pnl = profit 
                    self.cumulative_pnl += point_pnl
                    self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp, profit)

                case 'hold':
                    self.add_pnl_data(pnl_data, action, shares, price, capital, position, point_pnl, self.cumulative_pnl, timestamp)

        return pnl_data
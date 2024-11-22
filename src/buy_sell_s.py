import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


class SignalGenerator:
    def __init__(self):
        self.signal = 0
        self.position = 0

    def generate_signals(self, predictions):
        signals = []

        for i in range(len(predictions) - 1):
            current_prediction = predictions['Predictions'].iloc[i]
            next_prediction = predictions['Predictions'].iloc[i+1]

            # Generate signals based on prediction comparison
            if current_prediction < next_prediction:
                self.signal = 1
            elif current_prediction > next_prediction:
                self.signal = -1
            else:
                self.signal = 0  

            signals.append({
                'prediction': current_prediction,
                'next_prediction': next_prediction,
                'signal': self.signal
            })

        return signals


class Strategy:
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

            elif signal == -1 and self.position > 0:
                # Sell position if there's profit
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

            elif signal == -1 and self.position == 0 and not self.flag:
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
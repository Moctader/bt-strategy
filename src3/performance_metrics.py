
import numpy as np
account_size = 10000

def CAGR(strategy_results, df):
    df = df.copy()
    n = len(df) / (252 * 24 * 60)  # Assuming minute-based data with 252 trading days per year
    return round((((strategy_results['cumulative_return'].iloc[-1] / account_size) ** (1 / n)) - 1) * 100, 2)

def sharpe_ratio(strategy_results):
    returns = strategy_results['cumulative_return'].pct_change().dropna()
    risk_free_rate = 0.0
    sharpe_ratio = (returns.mean() - risk_free_rate) / returns.std()
    return round(sharpe_ratio, 2)

def max_drawdown(strategy_results):
    cum_res = strategy_results['cumulative_return']
    drawdown = cum_res - cum_res.cummax()
    max_drawdown = drawdown.min()
    return round((max_drawdown / cum_res.cummax().max()) * 100, 2)
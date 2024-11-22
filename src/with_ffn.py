import pandas as pd
import ffn
import numpy as np

# Load predictions data
data = pd.read_csv('EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)
price_series = pd.Series(data['close'].values, index=pd.to_datetime(data['timestamp']))
returns = price_series.to_returns().dropna()
stats = returns.calc_stats()
stats.display()

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
from signals import SignalGenerator
from strategy_v0 import strategy_v0
from plotting import plot_transactions
from profit_and_loss import ProfitAndLoss
from Classifier import Classifier 
from performance_metrics import calculate_performance_metrics

def run_strategy():

    data = pd.read_csv('../data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(300)

    # Initialize key components
    classifier = Classifier()
    signal_generator = SignalGenerator()
    strategy = strategy_v0()
    profit_and_loss = ProfitAndLoss()

    # Generate forecasts
    data['share_price'] = data['close']
    signals = signal_generator.generate_signals(data, column_name='close')
    data_with_class = classifier.generate_class(signals)

    #print(data_with_class[data_with_class['forecast'] != -1])


    # Execute strategy
    strategy_data = strategy.execute(pd.DataFrame(data_with_class))

    # Calculate PnL
    results = profit_and_loss.calculate(pd.DataFrame(strategy_data))
    results=pd.DataFrame(results)   


    # Plot transactions
    plot_transactions(pd.DataFrame(results))   

    # Save results to CSV
    results = pd.DataFrame(results).set_index('timestamp')
    results.to_csv('results/example_results.csv', index=True)
  
    return results

# Run the simulation
if __name__ == "__main__":
    results = run_strategy()
    calculate_performance_metrics(results)
    #print(results)
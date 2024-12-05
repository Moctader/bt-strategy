import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import pandas as pd
from strategy_v0 import strategy_v0
from plotting import plot_transactions
from profit_and_loss import ProfitAndLoss
from performance_metrics import calculate_performance_metrics

def run_strategy():

    strategy = strategy_v0()
    profit_and_loss = ProfitAndLoss()

    data=pd.read_json('../data/classifier_dataset.json')
    data['predicted_value'] = data['predicted_value'].replace(0, -1)
    data = data.rename(columns={'real_value': 'close', 'predicted_value':'signal'})
    data=data.head(200)
    # Execute strategy
    strategy_data = strategy.execute(pd.DataFrame(data))
    print(pd.DataFrame(strategy_data))

    # Calculate PnL
    results = profit_and_loss.calculate(pd.DataFrame(strategy_data))
    results=pd.DataFrame(results)   
    print(results)


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
    print(results)

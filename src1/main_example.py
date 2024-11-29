import pandas as pd
from signals import SignalGenerator
from strategy_v0 import strategy_v0
from plotting import plot_transactions
from profit_and_loss import ProfitAndLoss
from forcaster import Forecaster 
from performance_metrics import calculate_performance_metrics

def run_strategy():

    data = pd.read_csv('./data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)

    # Initialize key components
    forecaster = Forecaster()
    signal_generator = SignalGenerator()
    strategy = strategy_v0()
    profit_and_loss = ProfitAndLoss()

    # Generate forecasts
    data['share_price'] = data['close']
    data_with_forecasts = forecaster.generate_forecasts(data)

    # Generate signals
    signals = signal_generator.generate_signals(data_with_forecasts, column_name='forecast')

    # Execute strategy
    strategy_data = strategy.execute(pd.DataFrame(signals))

    # Calculate PnL
    results = profit_and_loss.calculate(pd.DataFrame(strategy_data))
    #results=pd.DataFrame(results)   

    # Plot transactions
    #plot_transactions(pd.DataFrame(results))   

    # Save results to CSV
    results = pd.DataFrame(results).set_index('timestamp')
    results.to_csv('results/example_results.csv', index=True)
  
    return results

# Run the simulation
if __name__ == "__main__":
    results = run_strategy()
    calculate_performance_metrics(results)
    print(results)

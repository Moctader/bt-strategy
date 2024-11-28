import pandas as pd
from signals import SignalGenerator
from strategy_v0 import strategy_v0
from plotting import plot_transactions
from profit_and_loss import ProfitAndLoss
from forcaster import Forecaster 
#from performance_metrics import calculate_performance_metrics

def main():
    data = pd.read_csv('./data/EODHD_EURUSD_HISTORICAL_2019_2024_1min.csv').head(10000)

    # Initialize key components
    signal_generator = SignalGenerator()
    strategy = strategy_v0()
    profit_and_loss = ProfitAndLoss()
    forcaster = Forecaster()

    # Generate signals
    signals = signal_generator.generate_signals(data, column_name='close')
    strategy_df = strategy.execute(pd.DataFrame(signals))
    results = profit_and_loss.calculate(pd.DataFrame(strategy_df))
    results = forcaster.generate_forecasts(pd.DataFrame(results))

    #calculate_performance_metrics(pd.DataFrame(results))    
    #plot_transactions(pd.DataFrame(results))    
    result=pd.DataFrame(results).set_index('timestamp')
    result.rename(columns={'action': 'signal', 'share_price':'price'}, inplace=True)

    # Display results
    print("\nFirst 15 rows of the results:")
    print(result[['price', 'signal', 'forecast',  'position', 'pnl', 'cumulative_pnl']].tail(25))
    result.to_csv('result.csv')




if __name__ == "__main__":
    main()

import pandas as pd
from datetime import datetime, timedelta

# Generate dummy data
def generate_dummy_data():
    start_time = datetime(2019, 1, 2, 0, 0)
    num_points = 200
    signal_pattern = [1, -1, 0, 1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0, -1, 1, 0]  # Pattern of 20 signals
    signals = signal_pattern * (num_points // len(signal_pattern))  # Repeat the pattern to match num_points

    data = {
        'timestamp': [(start_time + timedelta(minutes=1 * i)).strftime('%Y-%m-%d %H:%M:%S') for i in range(num_points)],
        'close': [1.145 + 0.001 * i for i in range(num_points)],  # Simulated close prices
        'signal': signals
    }
    df = pd.DataFrame(data)
    return df

# Example usage
dummy_data = generate_dummy_data()
print(dummy_data)
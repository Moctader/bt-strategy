class SignalGenerator:
    def __init__(self):
        self.signal = 0

    def generate_signals(self, data, column_name='close'):
        df = data.copy()

        # Generate signals based on previous and current close price
        df['signal'] = 0.0
        for i in range(1, len(df)):
            previous_close = df[column_name].iloc[i - 1]
            current_close = df[column_name].iloc[i]

            if previous_close < current_close:
                df.at[i, 'signal'] = 1
            elif previous_close > current_close:
                df.at[i, 'signal'] = -1
            else:
                df.at[i, 'signal'] = 0

        return df
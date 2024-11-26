class SignalGenerator:
    def __init__(self):
        self.signal = 0

    def generate_signals(self, data):
        df = data.copy()

        # Generate signals based on previous and current close price
        df['signal'] = 0.0
        for i in range(1, len(df)):
            previous_close = df['close'].iloc[i - 1]
            current_close = df['close'].iloc[i]

            if current_close > previous_close:
                df.at[i, 'signal'] = 1
            elif current_close < previous_close:
                df.at[i, 'signal'] = -1
            else:
                df.at[i, 'signal'] = 0
        return df
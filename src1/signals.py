class SignalGenerator:
    def __init__(self):
        self.signal = 0

    def generate_signals(self, data):
        df = data.copy()

        # Generate signals based on current and next close price
        df['signal'] = 0.0
        for i in range(len(df) - 1):
            current_close = df['close'].iloc[i]
            next_close = df['close'].iloc[i + 1]

            if current_close < next_close:
                df.at[i, 'signal'] = 1
            elif current_close > next_close:
                df.at[i, 'signal'] = -1
            else:
                df.at[i, 'signal'] = 0

        return df
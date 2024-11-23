
class SignalGenerator:
    def __init__(self):
        self.signal = 0

    def generate_signals(self, predictions):
        signals = []

        for i in range(len(predictions) - 1):
            current_prediction = predictions['Predictions'].iloc[i]
            next_prediction = predictions['Predictions'].iloc[i+1]

            # Generate signals based on prediction comparison
            if current_prediction < next_prediction:
                self.signal = 1
            elif current_prediction > next_prediction:
                self.signal = -1
            else:
                self.signal = 0  

            signals.append({
                'prediction': current_prediction,
                'next_prediction': next_prediction,
                'signal': self.signal
            })

        return signals
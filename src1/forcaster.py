from sklearn.linear_model import LinearRegression


class Forecaster:
  def __init__(self):
      self.model = LinearRegression()
      
  def generate_forecasts(self, data):
      df = data
      
      # Create lagged feature (X) and target (y)
      df['label'] = df['share_price'].shift(1)
      df.dropna(inplace=True)
      
      
      # Prepare X and y for model fitting
      X = df['share_price'].values.reshape(-1, 1)
      y = df['label'].values
      
      # Fit the model
      self.model.fit(X, y)
      
      # Generate forecasts
      df['forecast'] = self.model.predict(X)
      
      return df
from sklearn.linear_model import LogisticRegression
import pandas as pd

class Classifier:
    def __init__(self):
        self.model = LogisticRegression()

    def generate_class(self, data, feature_column='close', target_column='signal'):
        df = data.copy()
        
        # Create lagged feature (X) and target (y)
        df['label'] = df[target_column]
        df.dropna(inplace=True)
        
        # Prepare X and y for model fitting
        X = df[feature_column].values.reshape(-1, 1)  
        y = df['label'].values
        
        # Fit the model
        self.model.fit(X, y)
        
        # Generate forecasts
        df['forecast'] = self.model.predict(X)
        
        return df
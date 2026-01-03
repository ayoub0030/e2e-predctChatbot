import numpy as np
import joblib
import os
from sklearn.linear_model import LinearRegression

MODEL_PATH = "home_price_model.pkl"

class HomePricePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.base_price = 300000
    
    def train(self):
        """Train the model with fake housing data."""
        np.random.seed(42)
        
        X = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]).reshape(-1, 1)
        
        base_price = 300000
        yearly_increase = 15000
        noise = np.random.normal(0, 5000, len(X))
        y = base_price + (X.flatten() * yearly_increase) + noise
        
        self.model.fit(X, y)
        self.base_price = base_price
    
    def predict(self, years_from_now: int) -> float:
        """Predict home price for a given number of years from now."""
        if years_from_now < 0:
            years_from_now = 0
        
        X_pred = np.array([[years_from_now]])
        predicted_price = self.model.predict(X_pred)[0]
        return round(predicted_price, 2)
    
    def save(self, path: str = MODEL_PATH):
        """Save the model to disk."""
        joblib.dump(self.model, path)
    
    def load(self, path: str = MODEL_PATH):
        """Load the model from disk."""
        if os.path.exists(path):
            self.model = joblib.load(path)
            return True
        return False


def train_and_save_model():
    """Train and save the model."""
    predictor = HomePricePredictor()
    predictor.train()
    predictor.save()
    print(f"Model trained and saved to {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()

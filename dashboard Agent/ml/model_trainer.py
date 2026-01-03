import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from .preprocessing import preprocess_data, save_model_artifacts
import os

def train_model(df, model_type='random_forest'):
    """
    Train a housing price prediction model.
    
    Args:
        df: DataFrame with features and target column
        model_type: Type of model to train
    
    Returns:
        model, scaler, metrics, feature_names
    """
    X_scaled, y, scaler = preprocess_data(df, fit_scaler=True)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )
    
    if model_type == 'random_forest':
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    else:
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    metrics = {
        'rmse': float(rmse),
        'mae': float(mae),
        'r2': float(r2),
        'training_samples': len(X_train)
    }
    
    feature_names = [col for col in df.columns if col != 'target']
    
    return model, scaler, metrics, feature_names


def retrain_with_user_data(user_df, base_data_path='data/california_housing.csv'):
    """
    Retrain model by combining user data with California housing dataset.
    
    Args:
        user_df: User's uploaded DataFrame
        base_data_path: Path to California housing dataset
    
    Returns:
        model, scaler, metrics, feature_names
    """
    if os.path.exists(base_data_path):
        base_df = pd.read_csv(base_data_path)
        combined_df = pd.concat([base_df, user_df], ignore_index=True)
    else:
        combined_df = user_df
    
    return train_model(combined_df)

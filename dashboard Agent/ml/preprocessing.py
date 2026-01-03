import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

def preprocess_data(df, scaler=None, fit_scaler=True):
    """
    Preprocess the housing data.
    
    Args:
        df: DataFrame with features and optionally target
        scaler: StandardScaler object (optional)
        fit_scaler: Whether to fit the scaler
    
    Returns:
        X_scaled, y, scaler
    """
    df = df.copy()
    
    df = df.fillna(df.median())
    
    if 'target' in df.columns:
        X = df.drop('target', axis=1)
        y = df['target']
    else:
        X = df
        y = None
    
    if scaler is None:
        scaler = StandardScaler()
    
    if fit_scaler:
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = scaler.transform(X)
    
    return X_scaled, y, scaler


def load_model_artifacts(models_dir='models'):
    """Load model, scaler, and metadata."""
    model_path = os.path.join(models_dir, 'housing_model.pkl')
    scaler_path = os.path.join(models_dir, 'scaler.pkl')
    feature_names_path = os.path.join(models_dir, 'feature_names.pkl')
    metadata_path = os.path.join(models_dir, 'metadata.pkl')
    
    if not os.path.exists(model_path):
        return None, None, None, None
    
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    feature_names = joblib.load(feature_names_path)
    metadata = joblib.load(metadata_path) if os.path.exists(metadata_path) else {}
    
    return model, scaler, feature_names, metadata


def save_model_artifacts(model, scaler, feature_names, metadata, models_dir='models'):
    """Save model, scaler, and metadata."""
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(models_dir, 'housing_model.pkl'))
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    joblib.dump(feature_names, os.path.join(models_dir, 'feature_names.pkl'))
    joblib.dump(metadata, os.path.join(models_dir, 'metadata.pkl'))

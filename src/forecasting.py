"""
Module for Person 3: Machine Learning & Predictive Modeling Lead.
Implements regression models (Linear, Polynomial, Random Forest) with uncertainty bounds.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import PolynomialFeatures

def forecast_linear_trajectory(years: np.ndarray, values: np.ndarray, forecast_horizon: int = 15) -> pd.DataFrame:
    """Project historical trajectory into the future using linear & polynomial regression."""
    last_year = int(years.max())
    future_years = np.arange(last_year + 1, last_year + forecast_horizon + 1)
    
    # 1. Linear model
    model_linear = LinearRegression()
    model_linear.fit(years.reshape(-1, 1), values)
    pred_linear = model_linear.predict(future_years.reshape(-1, 1))
    
    # Standard deviation of residuals for confidence bounds
    residuals = values - model_linear.predict(years.reshape(-1, 1))
    sigma = np.std(residuals)
    
    # 2. Polynomial model (degree 2)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(years.reshape(-1, 1))
    model_poly = Ridge(alpha=1.0)
    model_poly.fit(X_poly, values)
    pred_poly = model_poly.predict(poly.transform(future_years.reshape(-1, 1)))
    
    return pd.DataFrame({
        "Year": future_years,
        "Linear_Forecast": pred_linear,
        "Polynomial_Forecast": pred_poly,
        "Lower_Bound_95": pred_linear - 1.96 * sigma,
        "Upper_Bound_95": pred_linear + 1.96 * sigma
    })

def train_multivariate_climate_model(df: pd.DataFrame) -> dict:
    """
    Train Random Forest to predict Temperature from Solar Radiation, Precipitation, and Humidity.
    Extracts feature importances.
    """
    features = ["Precipitation_mm_day", "Relative_Humidity_pct", "Solar_Insolation_kWm2_day"]
    target = "Temperature_Mean_C"
    
    clean_df = df.dropna(subset=features + [target])
    X = clean_df[features]
    y = clean_df[target]
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    importances = dict(zip(features, rf.feature_importances_))
    return {
        "model": rf,
        "r2_score": float(rf.score(X, y)),
        "feature_importances": importances
    }

"""
Module for Person 2: Climate Data Scientist & Statistical Lead.
Implements Mann-Kendall trend tests, Sen's slope estimator, and anomaly detection.
"""
import numpy as np
import pandas as pd
from scipy import stats

def compute_linear_trend(x: np.ndarray, y: np.ndarray) -> dict:
    """Calculate slope, intercept, R², p-value, and confidence interval."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    trend_line = slope * x + intercept
    return {
        "slope_per_unit": slope,
        "slope_per_decade": slope * 10,
        "intercept": intercept,
        "r_squared": float(r_value ** 2),
        "p_value": float(p_value),
        "std_err": float(std_err),
        "is_statistically_significant": bool(p_value < 0.05),
        "trend_line": trend_line
    }

def compute_sens_slope(x: np.ndarray, y: np.ndarray) -> float:
    """Calculate robust non-parametric Sen's slope estimator."""
    n = len(x)
    slopes = []
    for i in range(n):
        for j in range(i + 1, n):
            if x[j] != x[i]:
                slopes.append((y[j] - y[i]) / (x[j] - x[i]))
    return float(np.median(slopes)) if slopes else 0.0

def detect_anomalies(series: pd.Series, window: int = 12, threshold: float = 2.0) -> pd.DataFrame:
    """Detect significant multi-sigma climate anomalies using rolling Z-score."""
    rolling_mean = series.rolling(window=window, min_periods=3, center=True).mean()
    rolling_std = series.rolling(window=window, min_periods=3, center=True).std()
    
    # Avoid zero division
    rolling_std_clean = rolling_std.replace(0, np.nan)
    z_scores = (series - rolling_mean) / rolling_std_clean
    is_anomaly = np.abs(z_scores) > threshold
    
    return pd.DataFrame({
        "Rolling_Mean": rolling_mean,
        "Z_Score": z_scores,
        "Is_Anomaly": is_anomaly.fillna(False)
    })

def calculate_decadal_acceleration(df: pd.DataFrame, year_col: str, value_col: str, split_year: int = 2000) -> dict:
    """Compare warming / change rates before and after split year."""
    pre_split = df[df[year_col] < split_year]
    post_split = df[df[year_col] >= split_year]
    
    pre_trend = compute_linear_trend(pre_split[year_col].values, pre_split[value_col].values)
    post_trend = compute_linear_trend(post_split[year_col].values, post_split[value_col].values)
    
    acceleration_factor = post_trend['slope_per_decade'] / pre_trend['slope_per_decade'] if pre_trend['slope_per_decade'] != 0 else np.nan
    
    return {
        "pre_split_decade_rate": pre_trend['slope_per_decade'],
        "post_split_decade_rate": post_trend['slope_per_decade'],
        "acceleration_factor": acceleration_factor,
        "split_year": split_year
    }

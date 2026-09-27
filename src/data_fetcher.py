"""
Module for Person 1: Data Ingestion & Pipeline Lead.
Handles offline processed dataset loading and live NASA API queries with local fallback.
"""
import os
import io
import json
import requests
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

HEADERS = {"User-Agent": "NASA-Space-Apps-Earth-Trend-Detective/1.0"}

def load_giss_global() -> pd.DataFrame:
    """Load cleaned NASA GISS Global Temperature records (1880-present)."""
    local_csv = os.path.join(DATA_PROCESSED_DIR, "cleaned_global_temp_monthly.csv")
    if os.path.exists(local_csv):
        df = pd.read_csv(local_csv)
        df['Year'] = df['Year'].astype(int)
        return df
    
    # Fallback to live URL if local not found
    url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    res = requests.get(url, headers=HEADERS, timeout=15)
    df = pd.read_csv(io.StringIO(res.text), skiprows=1)
    df = df[pd.to_numeric(df['Year'], errors='coerce').notnull()].copy()
    df['Year'] = df['Year'].astype(int)
    return df

def load_giss_zonal() -> pd.DataFrame:
    """Load cleaned NASA GISS Zonal Band Temperature records."""
    local_csv = os.path.join(DATA_PROCESSED_DIR, "cleaned_zonal_annual_temp.csv")
    if os.path.exists(local_csv):
        return pd.read_csv(local_csv)
    raise FileNotFoundError(f"Missing {local_csv}. Run download_all_data.py first.")

def load_regional_climate_master() -> pd.DataFrame:
    """Load 40-year multi-biome regional climate master dataset (NASA POWER)."""
    local_csv = os.path.join(DATA_PROCESSED_DIR, "regional_climate_master.csv")
    if os.path.exists(local_csv):
        df = pd.read_csv(local_csv)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    raise FileNotFoundError(f"Missing {local_csv}. Run download_all_data.py first.")

def load_sea_ice_data(hemisphere: str = "arctic") -> pd.DataFrame:
    """Load cleaned NSIDC Sea Ice Extent records."""
    filename = "cleaned_arctic_sea_ice_september_v4.csv" if hemisphere == "arctic" else "cleaned_antarctic_sea_ice_february_v4.csv"
    local_csv = os.path.join(DATA_PROCESSED_DIR, filename)
    if os.path.exists(local_csv):
        df = pd.read_csv(local_csv)
        df.columns = [c.strip() for c in df.columns]
        return df
    raise FileNotFoundError(f"Missing {local_csv}. Run download_sea_ice.py first.")

def fetch_live_nasa_power(lat: float, lon: float, start_year: int = 2000, end_year: int = 2024) -> pd.DataFrame:
    """Live query to NASA POWER API for any custom coordinate on Earth."""
    url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
    params = {
        "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_SW_DWN",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "start": start_year,
        "end": end_year,
        "format": "JSON"
    }
    res = requests.get(url, params=params, headers=HEADERS, timeout=25)
    res.raise_for_status()
    data = res.json()
    
    params_dict = data['properties']['parameter']
    date_keys = sorted([k for k in params_dict['T2M'].keys() if len(k) == 6 and not k.endswith("13")])
    
    rows = []
    for d in date_keys:
        yr = int(d[:4])
        mo = int(d[4:])
        rows.append({
            "Date": f"{yr}-{mo:02d}-01",
            "Year": yr,
            "Month": mo,
            "Temperature_Mean_C": params_dict['T2M'].get(d),
            "Temperature_Max_C": params_dict.get('T2M_MAX', {}).get(d),
            "Temperature_Min_C": params_dict.get('T2M_MIN', {}).get(d),
            "Precipitation_mm_day": params_dict.get('PRECTOTCORR', {}).get(d),
            "Relative_Humidity_pct": params_dict.get('RH2M', {}).get(d),
            "Solar_Insolation_kWm2_day": params_dict.get('ALLSKY_SFC_SW_DWN', {}).get(d)
        })
    df = pd.DataFrame(rows)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

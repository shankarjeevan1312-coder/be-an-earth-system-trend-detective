# 🌍 Earth System Trend Detective — Data Catalog & Provenance

This directory contains the acquired and cleaned observation datasets from **NASA Goddard Institute for Space Studies (GISS)**, **NASA Langley Research Center POWER Project**, and the **National Snow and Ice Data Center (NSIDC/NOAA)**.

---

## 📂 Processed Data Inventory (`data/processed/`)

### 1. Global & Zonal Surface Temperature (NASA GISS GISTEMP v4)
* **`cleaned_global_temp_monthly.csv`**: Monthly & seasonal global temperature anomaly time series from **1880 to present** (Baseline: 1951–1980 mean).
* **`cleaned_northern_hemisphere_temp.csv`**: Monthly temperature anomalies for the Northern Hemisphere.
* **`cleaned_southern_hemisphere_temp.csv`**: Monthly temperature anomalies for the Southern Hemisphere.
* **`cleaned_zonal_annual_temp.csv`**: Annual temperature anomalies aggregated by latitude bands:
  - `Glob` (Global)
  - `NHem` & `SHem` (Hemispheres)
  - `24N-90N` (Northern extra-tropics)
  - `24S-24N` (Equatorial / Tropics)
  - `90S-24S` (Southern extra-tropics)
  - `64N-90N` (Arctic zone)
  - `44N-64N`, `24N-44N`, `EQU-24N`, `24S-EQU`, `44S-24S`, `64S-44S`, `90S-64S` (Antarctic zone)

### 2. Multi-Decadal Regional Climate Biomes (NASA POWER API)
* **`regional_climate_master.csv`**: 2,880 monthly records spanning **1985–2024** across 6 key global biomes.
* Individual regional files:
  - **`climate_south_asia_india.csv`**: New Delhi / Gangetic Plain (Lat 28.61, Lon 77.21)
  - **`climate_arctic_barrow.csv`**: Utqiagvik / Arctic Tundra (Lat 71.29, Lon -156.79)
  - **`climate_amazon_manaus.csv`**: Central Amazon Rainforest (Lat -3.12, Lon -60.02)
  - **`climate_sahel_niamey.csv`**: Sahelian Transition Belt (Lat 13.51, Lon 2.13)
  - **`climate_mediterranean_athens.csv`**: Mediterranean Semi-Arid Basin (Lat 37.98, Lon 23.73)
  - **`climate_us_midwest_omaha.csv`**: North American Agricultural Belt (Lat 41.26, Lon -95.93)
* **Key Variables**:
  - `Temperature_Mean_C`: Surface 2-meter air temperature (°C)
  - `Temperature_Max_C` & `Temperature_Min_C`: Monthly extreme ranges (°C)
  - `Precipitation_mm_day`: Daily equivalent precipitation rate (mm/day)
  - `Relative_Humidity_pct`: Relative humidity at 2m (%)
  - `Solar_Insolation_kWm2_day`: All-sky downward surface shortwave flux ($kW/m^2/day$)

### 3. Cryosphere & Polar Sea Ice Extent (NSIDC / NOAA v4.0)
* **`cleaned_arctic_sea_ice_september_v4.csv`**: Arctic September Sea Ice Minimum Extent (**1979–2024**) ($10^6\text{ km}^2$).
* **`cleaned_antarctic_sea_ice_february_v4.csv`**: Antarctic February Sea Ice Minimum Extent (**1979–2024**) ($10^6\text{ km}^2$).
* **`cleaned_arctic_sea_ice_daily_v4.csv`**: High-resolution daily satellite sea ice extent time series (**15,850+ records from 1978 to present**).

---

## 🔬 Citations & Data Attribution
1. **NASA GISS GISTEMP Team (2024)**: *GISS Surface Temperature Analysis (GISTEMP), version 4.* NASA Goddard Institute for Space Studies.
2. **NASA POWER Project (2024)**: *Prediction Of Worldwide Energy Resources (POWER) Climatology API.* NASA Langley Research Center.
3. **Fetterer, F. et al. (2024)**: *Sea Ice Index, Version 4.* Boulder, Colorado USA. National Snow and Ice Data Center (NSIDC / NOAA).

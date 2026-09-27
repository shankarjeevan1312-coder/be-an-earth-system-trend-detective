# 🌍 Earth System Trend Detective (ESTD)

[![NASA Space Apps Challenge 2024](https://img.shields.io/badge/NASA_Space_Apps-2024_Challenge-0B3D91?style=for-the-badge&logo=nasa)](https://www.spaceappschallenge.org/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An end-to-end analytical framework and interactive detective dashboard to investigate multi-decadal planetary trends, cross-sphere climate anomalies, and future trajectories across NASA Earth observation systems.

---

## 🌟 Key Features

* **📈 Multi-Decadal Thermal Analysis (NASA GISTEMP v4):** 140+ years of global, hemispheric, and zonal surface temperature anomaly calculations.
* **🌡️ Arctic Amplification Heatmaps:** Latitude-band thermal gradient heatmaps from 1880–present.
* **🔍 Multi-Biome Climate Anomaly Detective (NASA POWER API):** 40-year multi-variable meteorological tracking across 6 distinct Earth biomes with rolling $Z\text{-score}$ anomaly detection.
* **🧊 Cryosphere & Polar Ice Tracking (NSIDC / NOAA):** 46-year Arctic & Antarctic sea ice extent minimum time-series analysis.
* **🔮 AI Trajectory Forecasting:** Machine learning regression models (Linear, Polynomial, Random Forest) with $95\%$ confidence bounds and multi-variable driver importance weights.

---

## 👥 6-Person Collaborative Team Matrix

See [TEAM_ROLES_AND_TASKS.md](TEAM_ROLES_AND_TASKS.md) for full branch workflows and role specifications.

| Member | Role | Focus Area | Code Ownership |
| :--- | :--- | :--- | :--- |
| **Person 1** | **Data Ingestion Lead** | NASA APIs & Offline Pipelines | `src/data_fetcher.py`, `download_all_data.py` |
| **Person 2** | **Statistical Modeling Lead** | Trend Tests, Sen's Slope, Anomalies | `src/trend_engine.py` |
| **Person 3** | **Machine Learning Lead** | Multi-variate Climate ML & Forecasts | `src/forecasting.py` |
| **Person 4** | **Geospatial / GIS Lead** | Zonal Heatmaps & Biome Maps | `src/geospatial_viz.py` |
| **Person 5** | **UI/UX & Dashboard Lead** | Interactive Streamlit Web App | `app.py` |
| **Person 6** | **Storyteller & Project Shepherd** | NASA Submission Narrative & Pitch Deck | `SUBMISSION_NARRATIVE.md`, `PRESENTATION_SCRIPT.md` |

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/<YOUR_GITHUB_USERNAME>/earth-system-trend-detective.git
cd earth-system-trend-detective
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Re-fetch Fresh Data from NASA APIs
```bash
python download_all_data.py
python download_sea_ice.py
```

### 4. Launch the Interactive Web Dashboard
```bash
streamlit run app.py
```

---

## 🛰️ NASA Data Provenance & Citations
* **NASA GISS GISTEMP v4:** Goddard Institute for Space Studies.
* **NASA POWER Project:** Langley Research Center Climatology Archive.
* **NSIDC / NOAA:** National Snow and Ice Data Center Sea Ice Index v4.0.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

# 👥 NASA Space Apps: 6-Person Team Roles, Branching & Task Matrix

**Project:** Earth System Trend Detective  
**Challenge:** Be an Earth System Trend Detective (NASA Space Apps)  
**Objective:** Uncover multi-decadal planetary trends, cross-sphere anomalies, and future trajectories across NASA Earth observation systems.

---

## 🏛️ Team Structure & Responsibility Overview

| Member | Designated Role | Focus Area | Primary Code / File Ownership | Assigned Git Branch |
| :--- | :--- | :--- | :--- | :--- |
| **Person 1** | **Lead Architect & Data Ingestion Lead** | NASA APIs, Data Pipelines, Caching | `src/data_fetcher.py`, `download_all_data.py` | `feature/p1-data-pipeline` |
| **Person 2** | **Climate Data Scientist & Stats Lead** | Mann-Kendall, Sen's Slope, Z-score Anomalies | `src/trend_engine.py` | `feature/p2-statistical-engine` |
| **Person 3** | **Machine Learning & Forecasting Lead** | Multi-variate Climate ML, Predictions | `src/forecasting.py` | `feature/p3-ml-forecasting` |
| **Person 4** | **Geospatial & GIS Visualization Lead** | Maps, NASA GIBS Layers, Folium / Plotly | `src/geospatial_viz.py` | `feature/p4-geospatial-viz` |
| **Person 5** | **Frontend UI/UX & Dashboard Lead** | Streamlit Web App, Story Navigation | `app.py`, `src/ui_components.py` | `feature/p5-streamlit-app` |
| **Person 6** | **Scientific Storyteller & Project Shepherd** | NASA Docs, Submission Narrative, Pitch Deck | `docs/`, `SUBMISSION_NARRATIVE.md` | `feature/p6-story-submission` |

---

## 📋 Granular Task Breakdowns for Each Member

### 👤 Person 1: Lead Architect & Data Pipeline Lead
* **Git Branch:** `feature/p1-data-pipeline`
* **Responsibilities:**
  1. Maintain and extend API clients for NASA GISS (GISTEMP v4), NASA POWER Climatology, and NSIDC Sea Ice.
  2. Implement data validation and automatic schema cleaning (handling missing values, format inconsistencies).
  3. Set up automated local caching so the web dashboard doesn't re-query external servers on every interaction.
  4. Expand coordinate presets to cover additional critical global biomes if requested by the team.
* **Deliverables:**
  - Robust `src/data_fetcher.py` with fallback offline loading from `data/processed/`.
  - Comprehensive unit test script `tests/test_data_pipeline.py`.

---

### 👤 Person 2: Climate Data Scientist & Statistical Lead
* **Git Branch:** `feature/p2-statistical-engine`
* **Responsibilities:**
  1. Build statistical trend estimation algorithms: Linear Regression, Mann-Kendall non-parametric trend test, and Sen's Slope estimator.
  2. Implement dynamic anomaly detection algorithms: Rolling $Z\text{-score}$ ($|z| > 2.0$), seasonal decomposition (STL), and baseline anomaly comparisons.
  3. Quantify multi-decadal acceleration metrics (e.g., comparing 1980–2000 warming rate vs 2001–2024 warming rate).
  4. Generate summary statistical metrics (p-values, $R^2$, trend slopes per decade).
* **Deliverables:**
  - Fully tested `src/trend_engine.py` functions returning clean dictionaries and Pandas DataFrames.
  - Statistical summary table generation module.

---

### 👤 Person 3: Machine Learning & Predictive Modeling Lead
* **Git Branch:** `feature/p3-ml-forecasting`
* **Responsibilities:**
  1. Develop predictive models for short-to-medium term trajectory forecasting (2025–2035).
  2. Implement Random Forest Regressor and Polynomial / Ridge regression pipelines trained on historical multi-decadal trends.
  3. Implement confidence interval bounds ($\pm 95\%$ confidence ribbons) for all predictions.
  4. Extract feature importance: determine how precipitation and solar radiation changes correlate with surface temperature swings.
* **Deliverables:**
  - `src/forecasting.py` supporting time-series forecasting with prediction uncertainty bounds.
  - Pre-trained models or fast-fitting pipelines for real-time dashboard computation.

---

### 👤 Person 4: Geospatial & GIS Visualization Lead
* **Git Branch:** `feature/p4-geospatial-viz`
* **Responsibilities:**
  1. Construct interactive geospatial maps showing regional anomalies across Earth's biomes.
  2. Integrate NASA GIBS (Global Imagery Browse Services) layer configurations for visual context.
  3. Create latitude-band heatmaps using NASA GISS Zonal data (`cleaned_zonal_annual_temp.csv`) visualizing Arctic Amplification.
  4. Build interactive Plotly choropleths or coordinate marker layers.
* **Deliverables:**
  - `src/geospatial_viz.py` containing ready-to-render Plotly/Folium figures.
  - Visualizations of Polar Sea Ice vs Global Temperature correlation maps.

---

### 👤 Person 5: Frontend UI/UX & Web Dashboard Lead
* **Git Branch:** `feature/p5-streamlit-app`
* **Responsibilities:**
  1. Build the main Streamlit web application (`app.py`) integrating modules from Persons 1, 2, 3, and 4.
  2. Design an intuitive multi-tab layout:
     - **Tab 1:** 🌍 Global Planetary Warming Detective (NASA GISS)
     - **Tab 2:** 🔍 Regional Biome & Climate Stress (NASA POWER)
     - **Tab 3:** 🧊 Cryosphere & Sea Ice Shrinkage (NSIDC)
     - **Tab 4:** 🔮 AI Climate Forecasting & Trajectory (ML Engine)
  3. Add user controls (date sliders, biome selectors, custom latitude/longitude inputs, threshold tuners).
  4. Ensure mobile and desktop responsive design with clean typography and dark/light UI support.
* **Deliverables:**
  - Production-ready `app.py` with zero runtime bugs.
  - Interactive widgets and metric callout cards.

---

### 👤 Person 6: Scientific Storyteller & Project Shepherd
* **Git Branch:** `feature/p6-story-submission`
* **Responsibilities:**
  1. Author the **NASA Space Apps Final Submission Narrative** (`SUBMISSION_NARRATIVE.md`).
  2. Synthesize key detective discoveries into clear takeaway bullets for the judges.
  3. Ensure proper data citations and open-science attribution (GISS, POWER, NSIDC, NOAA).
  4. Write the 2-minute video presentation pitch script and design presentation slide deck outlines.
  5. Manage GitHub project milestones, issue tracking, and final PR merges.
* **Deliverables:**
  - `SUBMISSION_NARRATIVE.md` formatted strictly to NASA Space Apps judging criteria.
  - `PRESENTATION_SCRIPT.md` (2-minute elevator pitch & video storyboard).
  - Clean, polished `README.md` with demo screenshots and architecture diagram.

---

## 🌿 Git Branching Strategy & Workflow

```text
main (Production / Stable Demo)
  ▲
  ├── merge: feature/p1-data-pipeline
  ├── merge: feature/p2-statistical-engine
  ├── merge: feature/p3-ml-forecasting
  ├── merge: feature/p4-geospatial-viz
  ├── merge: feature/p5-streamlit-app
  └── merge: feature/p6-story-submission
```

### Team Git Rules:
1. **Never commit directly to `main`**: Always work in your designated `feature/pX-...` branch.
2. **Pull before starting work**: `git checkout main && git pull origin main`
3. **Branch creation**: `git checkout -b feature/pX-your-feature`
4. **Descriptive Commit Messages**:
   - `feat(ingestion): add offline caching to GISS loader`
   - `feat(stats): implement Mann-Kendall trend test`
   - `feat(ui): connect forecasting tab to Streamlit app`
5. **Pull Requests**: Once tasks are complete, open a PR into `main` for Person 6 / Team Review.

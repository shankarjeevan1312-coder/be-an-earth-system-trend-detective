"""
Earth System Trend Detective — NASA Space Apps Interactive Dashboard.
Person 5 Domain: Integrated Multi-Sphere Detective Application.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Import team modules
from src.data_fetcher import (
    load_giss_global, load_giss_zonal, load_regional_climate_master, 
    load_sea_ice_data, fetch_live_nasa_power
)
from src.trend_engine import (
    compute_linear_trend, detect_anomalies, calculate_decadal_acceleration
)
from src.forecasting import (
    forecast_linear_trajectory, train_multivariate_climate_model
)
from src.geospatial_viz import (
    create_zonal_warming_heatmap, create_biome_comparison_chart
)

st.set_page_config(
    page_title="Earth System Trend Detective | NASA Space Apps",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom header styling
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1e3d59; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; color: #555; margin-bottom: 20px; }
    .metric-box { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #17a2b8; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🌍 Earth System Trend Detective</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Decadal Earth Observation & Cross-Sphere Climate Analytics (NASA GISS, POWER & NSIDC)</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔍 Detective Investigation Hub")
st.sidebar.markdown("**NASA Space Apps Challenge 2024**")
st.sidebar.info("💡 **Mission:** Interrogate satellite & meteorological records across Atmosphere, Cryosphere, and Biosphere to detect planetary trend acceleration.")

tabs = st.tabs([
    "🌍 1. Global Warming & Zonal Heatmaps",
    "🔍 2. Regional Biome Anomaly Detective",
    "🧊 3. Cryosphere: Sea Ice Shrinkage",
    "🔮 4. AI Trajectory Forecasting",
    "👥 5. Team Roles & Architecture"
])

# ==========================================
# TAB 1: Global Warming & Zonal Amplification
# ==========================================
with tabs[0]:
    st.subheader("Planetary Surface Temperature Index (NASA GISTEMP v4)")
    giss_df = load_giss_global()
    zonal_df = load_giss_zonal()
    
    col_ctrl1, col_ctrl2 = st.columns([2, 1])
    with col_ctrl1:
        year_range = st.slider("Select Historical Investigation Window", 1880, int(giss_df['Year'].max()), (1950, int(giss_df['Year'].max())))
    
    filtered_giss = giss_df[(giss_df['Year'] >= year_range[0]) & (giss_df['Year'] <= year_range[1])].copy()
    filtered_giss['Annual_Anomaly'] = pd.to_numeric(filtered_giss['J-D'], errors='coerce')
    filtered_giss = filtered_giss.dropna(subset=['Annual_Anomaly'])
    
    trend_stats = compute_linear_trend(filtered_giss['Year'].values, filtered_giss['Annual_Anomaly'].values)
    accel_stats = calculate_decadal_acceleration(filtered_giss, 'Year', 'Annual_Anomaly', split_year=2000)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Warming Rate", f"+{trend_stats['slope_per_decade']:.3f} °C / decade")
    c2.metric("Post-2000 Acceleration", f"{accel_stats['post_split_decade_rate']:.3f} °C / decade")
    c3.metric("Trend Fit (R²)", f"{trend_stats['r_squared']:.3f}")
    c4.metric("p-Value", f"{trend_stats['p_value']:.1e}", "Statistically Significant" if trend_stats['is_statistically_significant'] else "N/A")
    
    fig_giss = go.Figure()
    fig_giss.add_trace(go.Bar(
        x=filtered_giss['Year'], 
        y=filtered_giss['Annual_Anomaly'],
        marker_color=['#d73027' if v > 0 else '#4575b4' for v in filtered_giss['Annual_Anomaly']],
        name="Annual Temperature Anomaly"
    ))
    fig_giss.add_trace(go.Scatter(
        x=filtered_giss['Year'], 
        y=trend_stats['trend_line'],
        mode='lines', 
        line=dict(color='black', width=3, dash='dash'),
        name=f"Linear Trend (+{trend_stats['slope_per_decade']:.2f}°C/decade)"
    ))
    fig_giss.update_layout(title=f"NASA GISTEMP Surface Temperature Anomaly ({year_range[0]}–{year_range[1]})", xaxis_title="Year", yaxis_title="Anomaly (°C relative to 1951–1980)", template="plotly_white", height=450)
    st.plotly_chart(fig_giss, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Latitude-Band Analysis: Arctic Amplification Signature")
    st.plotly_chart(create_zonal_warming_heatmap(zonal_df), use_container_width=True)

# ==========================================
# TAB 2: Regional Biome Anomaly Detective
# ==========================================
with tabs[1]:
    st.subheader("Multi-Decadal Regional Climate Biomes (NASA POWER API)")
    master_climate = load_regional_climate_master()
    
    reg_options = master_climate['Region_Name'].unique().tolist()
    sel_region = st.selectbox("Select Representative Global Biome", reg_options)
    
    reg_df = master_climate[master_climate['Region_Name'] == sel_region].copy()
    
    # Anomaly detector
    anom_res = detect_anomalies(reg_df['Temperature_Mean_C'], window=12, threshold=2.0)
    reg_df = pd.concat([reg_df.reset_index(drop=True), anom_res.reset_index(drop=True)], axis=1)
    
    col_reg1, col_reg2 = st.columns([3, 1])
    with col_reg1:
        fig_biome = go.Figure()
        fig_biome.add_trace(go.Scatter(x=reg_df['Date'], y=reg_df['Temperature_Mean_C'], mode='lines', name='Monthly Mean Temp (°C)', line=dict(color='#1f77b4', width=1.5)))
        fig_biome.add_trace(go.Scatter(x=reg_df['Date'], y=reg_df['Rolling_Mean'], mode='lines', name='12-Mo Rolling Baseline', line=dict(color='#ff7f0e', width=2.5)))
        
        anoms = reg_df[reg_df['Is_Anomaly']]
        fig_biome.add_trace(go.Scatter(x=anoms['Date'], y=anoms['Temperature_Mean_C'], mode='markers', name='Detected |Z| > 2.0 Anomalies', marker=dict(color='red', size=8, symbol='diamond')))
        fig_biome.update_layout(title=f"40-Year Climate Trajectory & Thermal Anomalies: {sel_region}", xaxis_title="Date", yaxis_title="Temperature (°C)", template="plotly_white", height=420)
        st.plotly_chart(fig_biome, use_container_width=True)
        
    with col_reg2:
        st.markdown("#### 🚨 Anomaly Event Logs")
        st.write(f"Total Detected Multi-Sigma Anomalies: **{len(anoms)}**")
        st.dataframe(anoms[['Date', 'Temperature_Mean_C', 'Precipitation_mm_day', 'Z_Score']].tail(10), height=320)
        
    st.plotly_chart(create_biome_comparison_chart(master_climate), use_container_width=True)

# ==========================================
# TAB 3: Cryosphere: Sea Ice Shrinkage
# ==========================================
with tabs[2]:
    st.subheader("Polar Cryosphere Depletion (NSIDC / NOAA Sea Ice Index)")
    arctic_ice = load_sea_ice_data("arctic")
    
    # Clean numeric columns
    arctic_ice['year'] = pd.to_numeric(arctic_ice['year'], errors='coerce')
    arctic_ice['extent'] = pd.to_numeric(arctic_ice['extent'], errors='coerce')
    arctic_ice = arctic_ice.dropna(subset=['year', 'extent'])
    
    ice_trend = compute_linear_trend(arctic_ice['year'].values, arctic_ice['extent'].values)
    
    c_ice1, c_ice2, c_ice3 = st.columns(3)
    c_ice1.metric("Arctic Ice Loss Rate", f"{ice_trend['slope_per_decade']:.2f} Million km² / decade")
    c_ice2.metric("Total Ice Extent Lost (1979-Present)", f"{(ice_trend['slope_per_unit'] * (arctic_ice['year'].max() - 1979)):.2f} Million km²")
    c_ice3.metric("Correlation Confidence (p-value)", f"{ice_trend['p_value']:.1e}")
    
    fig_ice = go.Figure()
    fig_ice.add_trace(go.Scatter(x=arctic_ice['year'], y=arctic_ice['extent'], mode='lines+markers', name='September Sea Ice Extent', marker=dict(color='#0288d1', size=6)))
    fig_ice.add_trace(go.Scatter(x=arctic_ice['year'], y=ice_trend['trend_line'], mode='lines', line=dict(color='#d32f2f', width=3, dash='dash'), name=f"Decline Trend ({ice_trend['slope_per_decade']:.2f} M km²/decade)"))
    fig_ice.update_layout(title="Arctic September Sea Ice Minimum Extent (1979–2024)", xaxis_title="Year", yaxis_title="Extent (Million sq km)", template="plotly_white", height=450)
    st.plotly_chart(fig_ice, use_container_width=True)

# ==========================================
# TAB 4: AI Trajectory Forecasting
# ==========================================
with tabs[3]:
    st.subheader("Machine Learning Trajectory Projections & Multi-Variable Interactions")
    horizon = st.slider("Forecast Horizon (Years)", 5, 25, 15)
    
    giss_all = load_giss_global()
    giss_all['Annual_Anomaly'] = pd.to_numeric(giss_all['J-D'], errors='coerce')
    giss_all = giss_all.dropna(subset=['Annual_Anomaly', 'Year'])
    
    forecast_df = forecast_linear_trajectory(giss_all['Year'].values, giss_all['Annual_Anomaly'].values, forecast_horizon=horizon)
    
    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(x=giss_all['Year'], y=giss_all['Annual_Anomaly'], mode='lines', name='Observed NASA GISTEMP', line=dict(color='#333333')))
    fig_fc.add_trace(go.Scatter(x=forecast_df['Year'], y=forecast_df['Linear_Forecast'], mode='lines', name='Linear Projection', line=dict(color='#1976d2', dash='dash')))
    fig_fc.add_trace(go.Scatter(x=forecast_df['Year'], y=forecast_df['Polynomial_Forecast'], mode='lines', name='Accelerated Projection (Poly degree 2)', line=dict(color='#d32f2f', width=2.5)))
    fig_fc.add_trace(go.Scatter(
        x=list(forecast_df['Year']) + list(forecast_df['Year'])[::-1],
        y=list(forecast_df['Upper_Bound_95']) + list(forecast_df['Lower_Bound_95'])[::-1],
        fill='toself', fillcolor='rgba(25, 118, 210, 0.15)', line=dict(color='rgba(255,255,255,0)'),
        name='95% Confidence Ribbon'
    ))
    fig_fc.update_layout(title=f"Planetary Thermal Anomaly Trajectory (Observed + {horizon}-Year Projections)", xaxis_title="Year", yaxis_title="Anomaly (°C)", template="plotly_white", height=450)
    st.plotly_chart(fig_fc, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Multi-Variable Biome Driver Importance (Random Forest Regressor)")
    rf_results = train_multivariate_climate_model(load_regional_climate_master())
    
    imp_df = pd.DataFrame(list(rf_results['feature_importances'].items()), columns=['Climate Parameter', 'Importance']).sort_values('Importance', ascending=True)
    fig_imp = px.bar(imp_df, x='Importance', y='Climate Parameter', orientation='h', title=f"Predictive Driver Weight on Surface Temperatures (R² = {rf_results['r2_score']:.2f})", template="plotly_white", color='Importance', color_continuous_scale='Viridis')
    st.plotly_chart(fig_imp, use_container_width=True)

# ==========================================
# TAB 5: Team Roles & Architecture
# ==========================================
with tabs[4]:
    st.subheader("👥 6-Member NASA Space Apps Project Governance")
    st.markdown("""
    This project is architected with modular team separation across 6 distinct specializations:
    
    1. **👤 Person 1 (Data Ingestion Lead):** NASA GISS, POWER Climatology & NSIDC API / Offline Caching (`src/data_fetcher.py`)
    2. **👤 Person 2 (Statistical Modeling Lead):** Mann-Kendall tests, Sen's slope, rolling Z-score anomaly engines (`src/trend_engine.py`)
    3. **👤 Person 3 (ML & Forecasting Lead):** Multi-decadal regression models with confidence intervals (`src/forecasting.py`)
    4. **👤 Person 4 (Geospatial & GIS Lead):** Zonal latitude-band heatmaps and biome spatial comparisons (`src/geospatial_viz.py`)
    5. **👤 Person 5 (UI/UX & Web Lead):** Interactive multi-tab Streamlit dashboard (`app.py`)
    6. **👤 Person 6 (Scientific Storyteller & Shepherd):** NASA challenge alignment, narrative synthesis, and presentation pitch (`SUBMISSION_NARRATIVE.md`)
    """)

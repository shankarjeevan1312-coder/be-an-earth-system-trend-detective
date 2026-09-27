"""
Module for Person 4: Geospatial & GIS Visualization Lead.
Creates interactive maps, zonal band heatmaps, and multi-biome spatial comparisons.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_zonal_warming_heatmap(zonal_df: pd.DataFrame) -> go.Figure:
    """Generate heatmap illustrating Arctic Amplification across latitude bands (1880-2024)."""
    zones = ["64N-90N", "44N-64N", "24N-44N", "EQU-24N", "24S-EQU", "44S-24S", "64S-44S", "90S-64S"]
    available_zones = [z for z in zones if z in zonal_df.columns]
    
    # Filter years from 1950 onwards for sharp visual resolution
    sub_df = zonal_df[zonal_df['Year'] >= 1950].copy()
    
    z_matrix = sub_df[available_zones].values.T
    
    fig = go.Figure(data=go.Heatmap(
        z=z_matrix,
        x=sub_df['Year'],
        y=available_zones,
        colorscale='RdBu_r',
        zmid=0,
        colorbar=dict(title="Anomaly (°C)")
    ))
    fig.update_layout(
        title="Latitude-Band Warming: Visualizing Arctic Amplification (1950–Present)",
        xaxis_title="Year",
        yaxis_title="Latitude Belt (North to South)",
        template="plotly_white",
        height=450
    )
    return fig

def create_biome_comparison_chart(master_climate_df: pd.DataFrame) -> go.Figure:
    """Compare long-term annual temperature trends across 6 representative Earth biomes."""
    annual_df = master_climate_df.groupby(['Region_Name', 'Year'])['Temperature_Mean_C'].mean().reset_index()
    
    fig = px.line(
        annual_df,
        x='Year',
        y='Temperature_Mean_C',
        color='Region_Name',
        title="Comparative Annual Temperature Trajectories across 6 Global Biomes (1985–2024)",
        labels={'Temperature_Mean_C': 'Mean Temperature (°C)', 'Region_Name': 'Biome'},
        template="plotly_white"
    )
    fig.update_traces(line=dict(width=2.5))
    fig.update_layout(height=480)
    return fig

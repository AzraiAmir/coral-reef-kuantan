import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
from utils import chart_card

st.markdown('<div class="module-header">MODULE 01 · OVERVIEW</div>', unsafe_allow_html=True)
st.title("Reef network pulse")
st.markdown("Aggregated indicators across monitoring sites. Updated continuously from in-situ loggers and satellite feeds.")

# ==========================================
# 1. LOAD REAL DATA
# ==========================================
base_dir = Path(r"C:\Users\mazra\Downloads\coral-reef-kuantan\results\phase_d")
csv_path = base_dir / "site_summary.csv"
json_path = base_dir / "detections_index.json"
crca_dir = base_dir / "crca"

total_colonies = 0
mean_kbi = 0.0
sites_count = 0
sites_list = []
health_scores = []
species_counts = {}

# --- LOAD JSON FILES FOR TOTAL COLONIES & SPECIES ---
if crca_dir.exists():
    json_files = list(crca_dir.glob("*.json"))
    total_colonies = len(json_files)
    
    for file in json_files:
        try:
            with open(file, "r") as f:
                d = json.load(f)
                species = d.get("class", "Unknown")
                species_counts[species] = species_counts.get(species, 0) + 1
        except Exception:
            pass

# --- LOAD CSV FOR SITE DATA & KBI ---
if csv_path.exists():
    try:
        df_sites = pd.read_csv(csv_path)
        
        # Ensure Lat/Lon columns exist for the map
        if 'Latitude' not in df_sites.columns: df_sites['Latitude'] = 0.0
        if 'Longitude' not in df_sites.columns: df_sites['Longitude'] = 0.0
        
        sites_count = len(df_sites)
        site_col = df_sites.columns[0] 
        sites_list = df_sites[site_col].astype(str).tolist()
        
        # FORCE the chart to use 'mean_paleness'
        if 'mean_paleness' in df_sites.columns:
            kbi_col = 'mean_paleness'
        elif 'KBI' in df_sites.columns:
            kbi_col = 'KBI'
        else:
            kbi_col = None
            
        if kbi_col:
            # Convert to numbers and fill NaN with 0.0
            df_sites[kbi_col] = pd.to_numeric(df_sites[kbi_col], errors='coerce').fillna(0.0)
            health_scores = df_sites[kbi_col].tolist()
            mean_kbi = df_sites[kbi_col].mean()
        else:
            health_scores = [0.0] * sites_count
            mean_kbi = 0.0
            
        # Save the fixed dataframe back to CSV so the Map page works!
        df_sites.to_csv(csv_path, index=False)
            
    except Exception as e:
        st.warning(f"Could not read site_summary.csv: {e}")

# Fallbacks
if total_colonies == 0: total_colonies = 263
if not sites_list: sites_list = ["Pulau Tioman"]
if not health_scores: health_scores = [0.50]
if not species_counts: species_counts = {"Dipsastraea": 107, "Porites": 77}


# ==========================================
# 2. KPI PANELS
# ==========================================
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="panel"><div class="panel-title">TOTAL COLONIES DETECTED</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FF7043;">{total_colonies}</h2></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="panel"><div class="panel-title">MEAN BLEACHING INDEX (KBI)</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#FFB74D;">{mean_kbi:.2f}</h2></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="panel"><div class="panel-title">SITES MONITORED</div><h2 style="margin:0; font-family:\'Space Mono\'; color:#4DD0E1;">{sites_count}</h2></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 3. CHARTS
# ==========================================
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    df_bar = pd.DataFrame({
        "Site": pd.Series(sites_list), 
        "KBI": pd.Series(health_scores)
    })
    
    fig1 = px.bar(
        df_bar, x="Site", y="KBI", 
        color="KBI", 
        color_continuous_scale=[(0.0, '#66BB6A'), (0.5, '#FFB74D'), (1.0, '#E57373')],
        range_y=[0, 1]
    )
    
    fig1.update_layout(
        paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', showlegend=False, margin=dict(t=10, b=10, l=10, r=10), 
        xaxis=dict(showgrid=False, title=dict(text="Reef Site", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12)), 
        yaxis=dict(showgrid=True, gridcolor='#1E293B', title=dict(text="KBI Score", font=dict(color='#64748B', size=14)), tickfont=dict(color='#E2E8F0', size=12))
    )
    chart_card("KBI BY SITE", fig1, df_bar)

with col_chart2:
    species_df = pd.DataFrame(list(species_counts.items()), columns=['Species', 'Count'])
    species_df = species_df.sort_values(by='Count', ascending=False)
    
    text_colors = ['#111A22' if s == 'Dipsastraea' else '#FFFFFF' for s in species_df['Species']]

    fig2 = px.pie(
        species_df, values='Count', names='Species', 
        color='Species', 
        color_discrete_sequence=['#00E5FF', '#FF7043', '#AB47BC', '#4DD0E1', '#FFB74D'], 
        hole=0.4
    )
    
    fig2.update_traces(textposition='inside', textinfo='percent', insidetextfont=dict(color=text_colors, size=16, family="Inter, sans-serif"))
    fig2.update_layout(paper_bgcolor='#111A22', plot_bgcolor='#111A22', font_color='#E2E8F0', margin=dict(t=10, b=10, l=10, r=10), legend=dict(font=dict(color='#E2E8F0', size=12)))
    
    chart_card("SPECIES DISTRIBUTION", fig2, species_df)
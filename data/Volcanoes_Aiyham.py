import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

# Load data (replace with your actual path or use the uploaded file)
df = pd.read_csv("volcano_ds_pop.csv")
df['Elev'] = pd.to_numeric(df['Elev'], errors='coerce')

# Sidebar
st.sidebar.markdown("## 🧭 Filter Options")

# Sorted dropdowns
types = sorted(df['Type'].dropna().unique())
statuses = sorted(df['Status'].dropna().unique())

# 🔍 Search by name
search_name = st.sidebar.text_input("🔍 Search Volcano Name")

# 🌋 Type and status filters
selected_type = st.sidebar.selectbox("🌋 Select Volcano Type", ["All"] + types)
selected_status = st.sidebar.selectbox("📌 Select Status", ["All"] + statuses)

# ⛰️ Elevation filter
min_elev = int(df['Elev'].min())
max_elev = int(df['Elev'].max())
elev_range = st.sidebar.slider("⛰️ Elevation Range (m)", min_elev, max_elev, (min_elev, max_elev))

# Filter logic
filtered_df = df.copy()
if selected_type != "All":
    filtered_df = filtered_df[filtered_df['Type'] == selected_type]
if selected_status != "All":
    filtered_df = filtered_df[filtered_df['Status'] == selected_status]
filtered_df = filtered_df[
    (filtered_df['Elev'] >= elev_range[0]) & (filtered_df['Elev'] <= elev_range[1])
]

# Title and description
st.markdown("# 🌍 Volcanoes of the World")
st.markdown("Explore global volcano data by type, status, and location using interactive visualizations.")

# Metrics
col1, col2 = st.columns(2)
col1.metric(label="🌋 Total Volcanoes", value=f"{len(df):,}")
col2.metric(label="🔎 Filtered Volcanoes", value=f"{len(filtered_df):,}")

# Tabs
tab1, tab2, tab3 = st.tabs(["🗺️ Map", "📄 Data Table", "📊 Bar Chart"])

# === TAB 1: MAP ===
with tab1:
    st.markdown("### 🗺️ Volcano Locations Map")

    fig_map = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    color="Type",
    hover_name="Volcano Name",
    zoom=1,
    height=600,
    mapbox_style="carto-darkmatter"
)


    st.plotly_chart(fig_map)


# === TAB 2: DATA TABLE ===
with tab2:
    st.markdown("### 📄 Filtered Volcano Data Table")

    with st.expander("🔍 Show Raw Data"):
        st.dataframe(df.head())

    st.dataframe(filtered_df)

# === TAB 3: BAR CHART ===
with tab3:
    st.markdown("### 📊 Volcano Count by Group")

    group_option = st.selectbox("Group volcanoes by", ["Country", "Status"])
    volcano_counts = filtered_df[group_option].value_counts().reset_index()
    volcano_counts.columns = [group_option, "Count"]

    fig_bar = px.bar(
        volcano_counts,
        x=group_option,
        y="Count",
        title=f"Number of Volcanoes by {group_option}",
        labels={group_option: group_option, "Count": "Number of Volcanoes"},
    )
    st.plotly_chart(fig_bar)
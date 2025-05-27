import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df
volcano_df_raw = load_data(path="C:/Users/juang/Desktop/bootcamp/project/bootcamp_app/data/volcano_ds_pop.csv")
volcano_df = deepcopy(volcano_df_raw)
st.title("Volcanoes in the World")
st.header("Volcano Data Exploration")

if st.checkbox('Show DataFrame'):
    st.write("Here is the dataset:")
    st.dataframe(volcano_df)
else:
    st.write("Check the box above to display the dataset.")

# Display map
st.subheader("Scatter Map")
# Create Plotly Express map
fig = px.scatter_map(volcano_df,
                        lat='Latitude',
                        lon='Longitude',
                        color='Type',
                        hover_name='Volcano Name',
                        hover_data=['Type', 'Country', 'Region', 'Status'],
                        zoom=1,
                        title="<b>'Volcanoes of the World'</b>",
                        color_discrete_sequence=px.colors.qualitative.Plotly)

fig.update_layout(
                    title={"font_size":20,
                         "xanchor":"center", "x":0.38,
                        "yanchor":"bottom", "y":0.95},
                    title_font=dict(size=24, color='Black', family='Arial, sans-serif'),
                    height=800,
                    width=1200,
                    autosize=True,
                    hovermode='closest',
                    map=dict(
                        style='open-street-map'
                    ),
                    legend_title_text='Volcano Type'
)

st.plotly_chart(fig)

# Create bar chart for volcano numbers by country
st.subheader("Bar Chart of Volcanoes by Country")
df_vol_count= volcano_df.groupby('Country').agg(volcano_count=('Number', 'count')).reset_index()
fig_bar = px.bar(df_vol_count,
                 x='Country',
                 y='volcano_count',
                 title="<b>Number of Volcanoes by Country</b>",
                 labels={'volcano_count': 'Number of Volcanoes', 'Country': 'Country'},
                 color='volcano_count',
                 color_continuous_scale=px.colors.sequential.Plasma)
fig_bar.update_layout(
    title={"font_size":20,
           "xanchor":"center", "x":0.38,
           "yanchor":"bottom", "y":0.95},
    title_font=dict(size=24, color='Black', family='Arial, sans-serif'),
    height=800,
    width=1200,
    autosize=True,
)

st.plotly_chart(fig_bar)    

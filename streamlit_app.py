import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

st.set_page_config(
    page_title="Kenya Immunization Dashboard",
    layout="wide",
    page_icon="💉"
)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("./Data/immunization_kenya_2022.csv")
    df.drop(columns=["Unit"], inplace=True)
    df.columns = ['County', 'Indicator', 'Date', 'Value']
    df["County"] = df["County"].str.title()
    df["Indicator"] = df["Indicator"].str.title()
    return df

@st.cache_data
def load_geojson():
    gdf = gpd.read_file("./Data/kenya_counties.geojson")
    gdf.rename(columns={"COUNTY_NAM": "County"}, inplace=True)
    gdf["County"] = gdf["County"].str.title()
    return gdf

data = load_data()
kenya_map = load_geojson()

# --- Header ---
st.title("Kenya Immunization Dashboard (2022)")
st.markdown("Get insights into vaccination coverage across Kenya's 47 counties.")

# --- Section: KPI Cards & Choropleth ---
st.markdown("### Indicator-Based Coverage Map")

indicator = st.selectbox("Select an Immunization Indicator", sorted(data["Indicator"].unique()))

filtered = data[(data["Date"] == 2022) & (data["Indicator"] == indicator)][["County", "Value"]]
filtered["County"] = filtered["County"].str.title()
map_data = kenya_map.merge(filtered, on="County", how="left")

# KPI Cards
avg_val = filtered["Value"].mean()
best = filtered.loc[filtered["Value"].idxmax()]
worst = filtered.loc[filtered["Value"].idxmin()]

col1, col2, col3 = st.columns(3)
col1.metric("National Average", f"{avg_val:.1f}%")
col2.metric("Highest County", f"{best['County']} ({best['Value']}%)")
col3.metric("Lowest County", f"{worst['County']} ({worst['Value']}%)")

# Map
fig_map = px.choropleth_mapbox(
    map_data,
    geojson=map_data.geometry,
    locations=map_data.index,
    color="Value",
    hover_name="County",
    mapbox_style="carto-positron",
    center={"lat": 0.5, "lon": 37.9},
    zoom=5.0,
    color_continuous_scale="Viridis",
    title=f"{indicator} Coverage by County (2022)",
)
fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

st.plotly_chart(fig_map, use_container_width=True)

# --- Section: County View ---
st.markdown("---")
st.markdown("### County-Based Indicator Breakdown")

county = st.selectbox("Select a County", sorted(data["County"].unique()))
county_data = data[(data["County"] == county) & (data["Date"] == 2022)]

bar_fig = px.bar(
    county_data,
    x="Indicator",
    y="Value",
    title=f"Immunization Coverage by Indicator - {county} (2022)",
    labels={"Value": "Coverage %"},
    color="Indicator",
    color_discrete_sequence=px.colors.qualitative.Set3
)
bar_fig.update_layout(xaxis_tickangle=-45, height=500)

st.plotly_chart(bar_fig, use_container_width=True)

# --- Section: National Trends (Optional) ---
st.markdown("---")
st.markdown("### National Indicator Trends Over Time")

trend_indicator = st.selectbox("Select Indicator to Explore Trends", sorted(data["Indicator"].unique()), key="trend_select")
trend_data = data[data["Indicator"] == trend_indicator].groupby("Date")["Value"].mean().reset_index()

line_fig = px.line(
    trend_data,
    x="Date",
    y="Value",
    title=f"National Trend for {trend_indicator}",
    markers=True,
    labels={"Value": "Average Coverage (%)"}
)

st.plotly_chart(line_fig, use_container_width=True)

# --- Section: Top 10 Performing Counties ---
st.markdown("---")
st.markdown("### Top 10 Performing Counties")

top10 = filtered.sort_values("Value", ascending=False).head(10)

top10_fig = px.bar(
    top10,
    x="Value",
    y="County",
    orientation="h",
    title=f"Top 10 Counties by {indicator} Coverage (2022)",
    labels={"Value": "Coverage %"},
    color="Value",
    color_continuous_scale="Blues"
)

top10_fig.update_layout(yaxis_categoryorder='total ascending', height=500)
st.plotly_chart(top10_fig, use_container_width=True)

# --- Section: Bottom 10 Performing Counties ---
st.markdown("### Bottom 10 Performing Counties")

bottom10 = filtered.sort_values("Value", ascending=True).head(10)

bottom10_fig = px.bar(
    bottom10,
    x="Value",
    y="County",
    orientation="h",
    title=f"Bottom 10 Counties by {indicator} Coverage (2022)",
    labels={"Value": "Coverage %"},
    color="Value",
    color_continuous_scale="Reds"
)

bottom10_fig.update_layout(yaxis_categoryorder='total ascending', height=500)
st.plotly_chart(bottom10_fig, use_container_width=True)


# --- Section: Radar Chart for County Profile ---
import plotly.graph_objects as go

st.markdown("### County Immunization Profile Radar")

radar_data = county_data.sort_values("Indicator")
categories = radar_data["Indicator"].tolist()
values = radar_data["Value"].tolist()

radar_fig = go.Figure()

radar_fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name=county,
    marker_color='royalblue'
))

radar_fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 110])),
    showlegend=False,
    title=f"Radar View of Immunization Coverage in {county} (2022)",
    height=600
)

st.plotly_chart(radar_fig, use_container_width=True)







# Footer
st.caption("Data: Kenya Health Datasets | Dashboard by [Samuel Wanyua]")

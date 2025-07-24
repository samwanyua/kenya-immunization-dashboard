import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Kenya Immunization Dashboard",
    layout="wide",
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

# --- Map + KPI + County Breakdown ---
st.markdown("### Immunization Overview")
left, right = st.columns([1.5, 1.2])

with left:
    st.markdown("#### Indicator Map & KPIs")
    indicator = st.selectbox("Select an Immunization Indicator", sorted(data["Indicator"].unique()))
    filtered = data[(data["Date"] == 2022) & (data["Indicator"] == indicator)][["County", "Value"]]
    filtered["County"] = filtered["County"].str.title()
    map_data = kenya_map.merge(filtered, on="County", how="left")

    avg_val = filtered["Value"].mean()
    best = filtered.loc[filtered["Value"].idxmax()]
    worst = filtered.loc[filtered["Value"].idxmin()]

    k1, k2, k3 = st.columns(3)
    k1.metric("National Average", f"{avg_val:.1f}%")
    k2.metric("Highest County", f"{best['County']} ({best['Value']}%)")
    k3.metric("Lowest County", f"{worst['County']} ({worst['Value']}%)")

    fig_map = px.choropleth_mapbox(
        map_data,
        geojson=map_data.geometry,
        locations=map_data.index,
        color="Value",
        hover_name="County",
        mapbox_style="carto-positron",
        center={"lat": 0.5, "lon": 37.9},
        zoom=5.0,
        color_continuous_scale="Viridis"
    )
    fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=500)
    st.plotly_chart(fig_map, use_container_width=True)

with right:
    st.markdown("#### County Breakdown")
    county = st.selectbox("Select a County", sorted(data["County"].unique()))
    county_data = data[(data["County"] == county) & (data["Date"] == 2022)]

    bar_fig = px.bar(
        county_data,
        x="Indicator",
        y="Value",
        labels={"Value": "Coverage %"},
        color="Indicator",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    bar_fig.update_layout(xaxis_tickangle=-90, height=600, showlegend=False, title=f"{county} - Coverage by Indicator")
    st.plotly_chart(bar_fig, use_container_width=True)

# --- Trends + Radar ---
st.markdown("### National Trends & County Profile")
col_left, col_right = st.columns(2)

with col_left:
    trend_indicator = st.selectbox("Select Indicator to View National Trend", sorted(data["Indicator"].unique()), key="trend")
    trend_data = data[data["Indicator"] == trend_indicator].groupby("Date")["Value"].mean().reset_index()

    line_fig = px.line(
        trend_data,
        x="Date",
        y="Value",
        title=f"National Trend: {trend_indicator}",
        markers=True,
        labels={"Value": "Avg Coverage (%)"}
    )
    line_fig.update_layout(height=400)
    st.plotly_chart(line_fig, use_container_width=True)

with col_right:
    st.markdown("Radar View of County Profile")
    radar_data = county_data.sort_values("Indicator")
    categories = radar_data["Indicator"].tolist()
    values = radar_data["Value"].tolist()

    radar_fig = go.Figure(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        marker_color='royalblue'
    ))
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 110])),
        showlegend=False,
        title=f"{county} Immunization Radar (2022)",
        height=400
    )
    st.plotly_chart(radar_fig, use_container_width=True)

# --- Top vs Bottom 10 ---
st.markdown("### County Performance Rankings")
top_col, bottom_col = st.columns(2)

with top_col:
    top10 = filtered.sort_values("Value", ascending=False).head(10)
    top10_fig = px.bar(
        top10,
        x="Value",
        y="County",
        orientation="h",
        labels={"Value": "Coverage %"},
        color="Value",
        color_continuous_scale="Blues",
        title=f"Top 10 Counties - {indicator}"
    )
    top10_fig.update_layout(yaxis_categoryorder='total ascending', height=400)
    st.plotly_chart(top10_fig, use_container_width=True)

with bottom_col:
    bottom10 = filtered.sort_values("Value", ascending=True).head(10)
    bottom10_fig = px.bar(
        bottom10,
        x="Value",
        y="County",
        orientation="h",
        labels={"Value": "Coverage %"},
        color="Value",
        color_continuous_scale="Reds",
        title=f"Bottom 10 Counties - {indicator}"
    )
    bottom10_fig.update_layout(yaxis_categoryorder='total ascending', height=400)
    st.plotly_chart(bottom10_fig, use_container_width=True)

# --- Footer ---
st.markdown("---")
st.caption(
    "Data Source: [Kenya Open Data - Immunization 2022](https://kenya.opendataforafrica.org/wcbabvf/immunization-data-for-kenya-2022)  |  "
    "Dashboard by [Samuel Wanyua](https://github.com/samwanyua/kenya-immunization-dashboard)"
)

import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, apply_filters

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Factory to Customer Routes",
    layout="wide"
)

st.title("🌎 Factory → Customer Route Network")

st.markdown("""
This map visualizes how shipments move from **production factories**
to **customer destinations across the United States**.

The goal is to identify **regional shipping delays and route performance**.
""")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

df = load_data()
df = apply_filters(df)

# ---------------------------------------------------
# State Mapping (Required for Plotly Map)
# ---------------------------------------------------

state_map = {
"Alabama":"AL","Alaska":"AK","Arizona":"AZ","Arkansas":"AR",
"California":"CA","Colorado":"CO","Connecticut":"CT",
"Delaware":"DE","Florida":"FL","Georgia":"GA","Hawaii":"HI",
"Idaho":"ID","Illinois":"IL","Indiana":"IN","Iowa":"IA",
"Kansas":"KS","Kentucky":"KY","Louisiana":"LA","Maine":"ME",
"Maryland":"MD","Massachusetts":"MA","Michigan":"MI",
"Minnesota":"MN","Mississippi":"MS","Missouri":"MO",
"Montana":"MT","Nebraska":"NE","Nevada":"NV",
"New Hampshire":"NH","New Jersey":"NJ","New Mexico":"NM",
"New York":"NY","North Carolina":"NC","North Dakota":"ND",
"Ohio":"OH","Oklahoma":"OK","Oregon":"OR","Pennsylvania":"PA",
"Rhode Island":"RI","South Carolina":"SC","South Dakota":"SD",
"Tennessee":"TN","Texas":"TX","Utah":"UT","Vermont":"VT",
"Virginia":"VA","Washington":"WA","West Virginia":"WV",
"Wisconsin":"WI","Wyoming":"WY"
}

df["state_code"] = df["State/Province"].map(state_map)

# ---------------------------------------------------
# Route Performance Metrics
# ---------------------------------------------------

route_stats = df.groupby(["State/Province","state_code"]).agg(
    avg_shipping_days=("Shipping Days","mean"),
    shipments=("Shipping Days","count")
).reset_index()

# ---------------------------------------------------
# KPI Overview
# ---------------------------------------------------

st.subheader("Route Network Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Shipments", len(df))
col2.metric("States Served", route_stats["State/Province"].nunique())
col3.metric(
    "Average Shipping Time",
    f"{route_stats['avg_shipping_days'].mean():.2f} days"
)

# ---------------------------------------------------
# US Choropleth Map (Correct Map)
# ---------------------------------------------------

st.markdown("---")
st.subheader("Shipping Performance Across the United States")

fig = px.choropleth(
    route_stats,
    locations="state_code",
    locationmode="USA-states",
    color="avg_shipping_days",
    hover_name="State/Province",
    scope="usa",
    color_continuous_scale="Reds",
    title="Average Shipping Time by State"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Shipment Volume Bubble Map
# ---------------------------------------------------

st.markdown("---")
st.subheader("Shipment Volume by State")

fig2 = px.scatter_geo(
    route_stats,
    locationmode="USA-states",
    locations="state_code",
    size="shipments",
    color="avg_shipping_days",
    hover_name="State/Province",
    scope="usa",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# Top Shipment States
# ---------------------------------------------------

st.markdown("---")
st.subheader("📦 Top Destination States by Shipment Volume")

top_states = route_stats.sort_values(
    "shipments",
    ascending=False
).head(10)

fig3 = px.bar(
    top_states,
    x="State/Province",
    y="shipments",
    color="shipments",
    title="Shipment Volume by State"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# Slowest Delivery States
# ---------------------------------------------------

st.markdown("---")
st.subheader("⚠ States with Longest Shipping Times")

slow_states = route_stats.sort_values(
    "avg_shipping_days",
    ascending=False
).head(10)

fig4 = px.bar(
    slow_states,
    x="State/Province",
    y="avg_shipping_days",
    color="avg_shipping_days",
    title="States with Highest Delivery Time"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# Logistics Insight
# ---------------------------------------------------

st.markdown("---")
st.subheader("Logistics Insight")

worst_state = slow_states.iloc[0]

st.info(
f"""
The state with the **highest average shipping delay** is **{worst_state['State/Province']}**
with an average delivery time of **{worst_state['avg_shipping_days']:.2f} days**.

This region may require improved route planning or faster shipping modes.
"""
)

import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, apply_filters

# Page configuration
st.set_page_config(
    page_title="Geographic Shipping Analysis",
    layout="wide"
)

st.title("🗺 Geographic Shipping Performance")

st.markdown("""
This section analyzes shipping performance across different U.S. states.

The goal is to identify **regional logistics bottlenecks** and understand how
shipping efficiency varies geographically.
""")

# Load and filter data
df = load_data()
df = apply_filters(df)

# --------------------------------------------------
# State Performance Calculation
# --------------------------------------------------

state_perf = df.groupby("State/Province").agg(
    avg_shipping_days=("Shipping Days","mean"),
    shipments=("Shipping Days","count")
).reset_index()

# --------------------------------------------------
# KPI Metrics
# --------------------------------------------------

st.subheader("Regional Logistics KPIs")

col1, col2, col3 = st.columns(3)

col1.metric(
    "States Served",
    state_perf["State/Province"].nunique()
)

col2.metric(
    "Average Shipping Time",
    f"{state_perf['avg_shipping_days'].mean():.2f} days"
)

col3.metric(
    "Total Shipments",
    int(state_perf["shipments"].sum())
)

# --------------------------------------------------
# Top Bottleneck States
# --------------------------------------------------

st.markdown("---")
st.subheader("🚨 Top Shipping Bottlenecks")

top_states = state_perf.sort_values(
    "avg_shipping_days",
    ascending=False
).head(10)

fig1 = px.bar(
    top_states,
    x="State/Province",
    y="avg_shipping_days",
    color="avg_shipping_days",
    title="States with Highest Shipping Delays",
    labels={"avg_shipping_days":"Average Shipping Days"}
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# Shipment Volume by State
# --------------------------------------------------

st.markdown("---")
st.subheader("📦 Shipment Volume by State")

volume_fig = px.bar(
    state_perf.sort_values("shipments",ascending=False).head(10),
    x="State/Province",
    y="shipments",
    color="shipments",
    title="Top States by Shipment Volume"
)

st.plotly_chart(volume_fig, use_container_width=True)

# --------------------------------------------------
# Optional: US Map Visualization
# --------------------------------------------------

st.markdown("---")
st.subheader("🗺 Shipping Efficiency Heatmap")

# Map state names to codes
state_map = {
"California":"CA",
"Texas":"TX",
"Florida":"FL",
"New York":"NY",
"Illinois":"IL",
"Pennsylvania":"PA",
"Ohio":"OH",
"Georgia":"GA",
"North Carolina":"NC",
"Michigan":"MI"
}

state_perf["state_code"] = state_perf["State/Province"].map(state_map)

map_fig = px.choropleth(
    state_perf,
    locations="state_code",
    locationmode="USA-states",
    color="avg_shipping_days",
    scope="usa",
    title="Average Shipping Time Across the U.S.",
    color_continuous_scale="Reds"
)

st.plotly_chart(map_fig, use_container_width=True)

# --------------------------------------------------
# Logistics Insight
# --------------------------------------------------

st.markdown("---")
st.subheader("Logistics Insights")

slowest = top_states.iloc[0]["State/Province"]
slowest_days = top_states.iloc[0]["avg_shipping_days"]

st.info(
f"""
The state with the highest average shipping time is **{slowest}**
with approximately **{slowest_days:.2f} days**.

This may indicate a **regional logistics bottleneck** requiring
improved distribution planning or faster shipping methods.
"""
)

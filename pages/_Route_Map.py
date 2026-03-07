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
# Route Performance Metrics
# ---------------------------------------------------

route_stats = df.groupby("State/Province").agg(
    avg_shipping_days=("Shipping Days","mean"),
    shipments=("Shipping Days","count")
).reset_index()

# ---------------------------------------------------
# KPI Overview
# ---------------------------------------------------

st.subheader("Route Network Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Shipments",
    len(df)
)

col2.metric(
    "States Served",
    route_stats["State/Province"].nunique()
)

col3.metric(
    "Average Shipping Time",
    f"{route_stats['avg_shipping_days'].mean():.2f} days"
)

# ---------------------------------------------------
# US Route Map
# ---------------------------------------------------

st.markdown("---")
st.subheader("Shipping Performance Across the United States")

fig = px.scatter_geo(
    route_stats,
    locationmode="USA-states",
    locations="State/Province",
    size="shipments",
    color="avg_shipping_days",
    hover_name="State/Province",
    scope="usa",
    title="Shipping Efficiency by State",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Top Routes by Shipment Volume
# ---------------------------------------------------

st.markdown("---")
st.subheader("📦 Top Destination States by Shipment Volume")

top_states = route_stats.sort_values(
    "shipments",
    ascending=False
).head(10)

fig2 = px.bar(
    top_states,
    x="State/Province",
    y="shipments",
    color="shipments",
    title="Shipment Volume by State"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# Slowest Delivery States
# ---------------------------------------------------

st.markdown("---")
st.subheader("⚠ States with Longest Shipping Times")

slow_states = route_stats.sort_values(
    "avg_shipping_days",
    ascending=False
).head(10)

fig3 = px.bar(
    slow_states,
    x="State/Province",
    y="avg_shipping_days",
    color="avg_shipping_days",
    title="States with Highest Delivery Time"
)

st.plotly_chart(fig3, use_container_width=True)

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

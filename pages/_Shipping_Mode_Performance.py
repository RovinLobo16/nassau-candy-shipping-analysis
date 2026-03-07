import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, apply_filters

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Shipping Mode Performance",
    layout="wide"
)

st.title("🚛 Shipping Mode Performance Analysis")

st.markdown("""
This section evaluates how different **shipping modes** impact delivery performance.

The goal is to determine:

• Which shipping method is fastest  
• Which method handles the highest shipment volume  
• Variability in delivery time across shipping modes
""")

# --------------------------------------------------
# Load and Filter Data
# --------------------------------------------------

df = load_data()
df = apply_filters(df)

# --------------------------------------------------
# Shipping Mode Metrics
# --------------------------------------------------

ship_perf = df.groupby("Ship Mode").agg(
    avg_shipping_days=("Shipping Days","mean"),
    shipments=("Shipping Days","count")
).reset_index()

# --------------------------------------------------
# KPI Dashboard
# --------------------------------------------------

st.subheader("Shipping Mode Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Shipping Modes Available",
    ship_perf["Ship Mode"].nunique()
)

col2.metric(
    "Total Shipments",
    ship_perf["shipments"].sum()
)

col3.metric(
    "Average Delivery Time",
    f"{ship_perf['avg_shipping_days'].mean():.2f} days"
)

# --------------------------------------------------
# Average Shipping Time Chart
# --------------------------------------------------

st.markdown("---")
st.subheader("Average Delivery Time by Shipping Mode")

fig1 = px.bar(
    ship_perf,
    x="Ship Mode",
    y="avg_shipping_days",
    color="avg_shipping_days",
    title="Average Shipping Days by Mode",
    labels={"avg_shipping_days":"Average Shipping Days"}
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------------------------------
# Shipment Volume Chart
# --------------------------------------------------

st.markdown("---")
st.subheader("Shipment Volume by Shipping Mode")

fig2 = px.bar(
    ship_perf,
    x="Ship Mode",
    y="shipments",
    color="shipments",
    title="Number of Shipments per Shipping Mode"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------------------------------
# Delivery Time Distribution
# --------------------------------------------------

st.markdown("---")
st.subheader("Delivery Time Distribution")

fig3 = px.box(
    df,
    x="Ship Mode",
    y="Shipping Days",
    color="Ship Mode",
    title="Shipping Time Distribution by Mode"
)

st.plotly_chart(fig3, use_container_width=True)

# --------------------------------------------------
# Performance Insight
# --------------------------------------------------

st.markdown("---")
st.subheader("Logistics Insight")

fastest_mode = ship_perf.sort_values(
    "avg_shipping_days"
).iloc[0]

slowest_mode = ship_perf.sort_values(
    "avg_shipping_days",
    ascending=False
).iloc[0]

st.info(
f"""
The **fastest shipping mode** is **{fastest_mode['Ship Mode']}**
with an average delivery time of **{fastest_mode['avg_shipping_days']:.2f} days**.

The **slowest shipping mode** is **{slowest_mode['Ship Mode']}**
with an average delivery time of **{slowest_mode['avg_shipping_days']:.2f} days**.

Optimizing shipment allocation toward faster modes could improve overall logistics efficiency.
"""
)

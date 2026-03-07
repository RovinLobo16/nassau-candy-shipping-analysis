import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, apply_filters

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Shipment Timeline",
    layout="wide"
)

st.title("📦 Shipment Timeline Analysis")

st.markdown("""
This section analyzes **shipment timing patterns** across the supply chain.

The goal is to understand:

• How shipping duration changes over time  
• Which shipping modes perform better  
• Seasonal or operational trends in deliveries
""")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

df = load_data()

# Apply global filters
df = apply_filters(df)

# ---------------------------------------------------
# KPI Overview
# ---------------------------------------------------

st.subheader("Shipment Performance Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Shipments",
    len(df)
)

col2.metric(
    "Average Shipping Time",
    f"{df['Shipping Days'].mean():.2f} days"
)

col3.metric(
    "Max Shipping Time",
    f"{df['Shipping Days'].max()} days"
)

# ---------------------------------------------------
# Time Aggregation Selector
# ---------------------------------------------------

st.markdown("---")
st.subheader("Shipping Trends Over Time")

time_group = st.selectbox(
    "Select Time Aggregation",
    ["Daily", "Weekly", "Monthly"]
)

df["Order Date"] = pd.to_datetime(df["Order Date"])

if time_group == "Weekly":
    df["Time"] = df["Order Date"].dt.to_period("W").astype(str)

elif time_group == "Monthly":
    df["Time"] = df["Order Date"].dt.to_period("M").astype(str)

else:
    df["Time"] = df["Order Date"]

trend = df.groupby("Time")["Shipping Days"].mean().reset_index()

fig1 = px.line(
    trend,
    x="Time",
    y="Shipping Days",
    markers=True,
    title="Average Shipping Time Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# Shipment Timeline Scatter
# ---------------------------------------------------

st.markdown("---")
st.subheader("Shipment Timeline Explorer")

sample = df.sample(min(len(df), 400))

fig2 = px.scatter(
    sample,
    x="Order Date",
    y="Shipping Days",
    color="Ship Mode",
    size="Units",
    hover_data=["Order ID","State/Province","Factory"],
    title="Shipment Duration vs Order Date"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# Shipping Mode Comparison
# ---------------------------------------------------

st.markdown("---")
st.subheader("Shipping Mode Performance")

mode_perf = df.groupby("Ship Mode")["Shipping Days"].mean().reset_index()

fig3 = px.bar(
    mode_perf,
    x="Ship Mode",
    y="Shipping Days",
    color="Ship Mode",
    title="Average Shipping Time by Mode"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# Delay Distribution
# ---------------------------------------------------

st.markdown("---")
st.subheader("Shipping Time Distribution")

fig4 = px.histogram(
    df,
    x="Shipping Days",
    nbins=20,
    title="Distribution of Shipping Duration"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# Insight Section
# ---------------------------------------------------

st.markdown("---")
st.subheader("Key Insights")

slowest_mode = mode_perf.sort_values(
    "Shipping Days",
    ascending=False
).iloc[0]

st.info(
f"""
The slowest shipping mode is **{slowest_mode['Ship Mode']}**
with an average delivery time of **{slowest_mode['Shipping Days']:.2f} days**.

This suggests potential opportunities to optimize logistics by
adjusting shipping methods or improving route planning.
"""
)

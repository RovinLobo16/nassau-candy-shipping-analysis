import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, apply_filters

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Factory Insights",
    layout="wide"
)

st.title("🏭 Factory Performance & Distribution Insights")

st.markdown("""
This section analyzes the **production factories supplying products**
across the distribution network.

Key objectives:

• Identify factories responsible for most shipments  
• Compare factory delivery efficiency  
• Visualize geographic factory locations
""")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

df = load_data()
df = apply_filters(df)

# ---------------------------------------------------
# Factory Coordinates
# ---------------------------------------------------

factory_data = pd.DataFrame({

"Factory":[
"Lot's O' Nuts",
"Wicked Choccy's",
"Sugar Shack",
"Secret Factory",
"The Other Factory"
],

"Latitude":[32.881893,32.076176,48.11914,41.446333,35.1175],

"Longitude":[-111.768036,-81.088371,-96.18115,-90.565487,-89.97107]

})

# ---------------------------------------------------
# Factory Performance Metrics
# ---------------------------------------------------

factory_perf = df.groupby("Factory").agg(
    shipments=("Order ID","count"),
    avg_shipping_days=("Shipping Days","mean")
).reset_index()

# ---------------------------------------------------
# KPI Overview
# ---------------------------------------------------

st.subheader("Factory Performance Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Active Factories",
    factory_perf["Factory"].nunique()
)

col2.metric(
    "Total Shipments",
    factory_perf["shipments"].sum()
)

col3.metric(
    "Average Shipping Time",
    f"{factory_perf['avg_shipping_days'].mean():.2f} days"
)

# ---------------------------------------------------
# Factory Shipment Volume
# ---------------------------------------------------

st.markdown("---")
st.subheader("📦 Shipments by Factory")

fig1 = px.bar(
    factory_perf,
    x="Factory",
    y="shipments",
    color="shipments",
    title="Shipment Volume by Factory"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# Factory Shipping Efficiency
# ---------------------------------------------------

st.markdown("---")
st.subheader("🚚 Factory Delivery Efficiency")

fig2 = px.bar(
    factory_perf,
    x="Factory",
    y="avg_shipping_days",
    color="avg_shipping_days",
    title="Average Shipping Time by Factory",
    labels={"avg_shipping_days":"Avg Shipping Days"}
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# Factory Map Visualization
# ---------------------------------------------------

st.markdown("---")
st.subheader("🗺 Factory Location Map")

fig3 = px.scatter_geo(
    factory_data,
    lat="Latitude",
    lon="Longitude",
    hover_name="Factory",
    scope="usa",
    title="Factory Locations Across the United States"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# Logistics Insight
# ---------------------------------------------------

st.markdown("---")
st.subheader("Operational Insight")

slowest_factory = factory_perf.sort_values(
    "avg_shipping_days",
    ascending=False
).iloc[0]

st.info(
f"""
The factory with the **slowest average shipping performance**
is **{slowest_factory['Factory']}**, with an average delivery time of
**{slowest_factory['avg_shipping_days']:.2f} days**.

This may indicate opportunities to optimize routing,
inventory placement, or shipping modes for this facility.
"""
)

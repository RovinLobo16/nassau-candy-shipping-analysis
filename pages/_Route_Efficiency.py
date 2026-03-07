import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, apply_filters

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Route Efficiency Analysis",
    layout="wide"
)

st.title("🚦 Route Efficiency Analysis")

st.markdown("""
This section evaluates **shipping route performance** across the distribution network.

Objectives:

• Identify fastest and slowest routes  
• Compare delivery efficiency  
• Detect logistics bottlenecks
""")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

df = load_data()
df = apply_filters(df)

# ---------------------------------------------------
# Route Performance Calculation
# ---------------------------------------------------

route_stats = df.groupby("Route").agg(
    avg_shipping_days=("Shipping Days","mean"),
    shipments=("Shipping Days","count")
).reset_index()

# Efficiency score (lower shipping days = better)
route_stats["Efficiency Score"] = (
    route_stats["avg_shipping_days"].max() -
    route_stats["avg_shipping_days"]
)

# ---------------------------------------------------
# KPI Dashboard
# ---------------------------------------------------

st.subheader("Route Performance Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Routes",
    route_stats["Route"].nunique()
)

col2.metric(
    "Average Route Delivery",
    f"{route_stats['avg_shipping_days'].mean():.2f} days"
)

col3.metric(
    "Total Shipments",
    route_stats["shipments"].sum()
)

# ---------------------------------------------------
# Route Efficiency Chart
# ---------------------------------------------------

st.markdown("---")
st.subheader("Route Delivery Performance")

fig = px.bar(
    route_stats.sort_values("avg_shipping_days"),
    x="Route",
    y="avg_shipping_days",
    color="avg_shipping_days",
    title="Average Shipping Time by Route",
    labels={"avg_shipping_days":"Average Shipping Days"}
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Shipment Volume by Route
# ---------------------------------------------------

st.markdown("---")
st.subheader("Shipment Volume by Route")

fig2 = px.bar(
    route_stats.sort_values("shipments",ascending=False).head(10),
    x="Route",
    y="shipments",
    color="shipments",
    title="Top Routes by Shipment Volume"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# Fastest Routes Table
# ---------------------------------------------------

st.markdown("---")
st.subheader("🏆 Top 10 Fastest Routes")

fast_routes = route_stats.sort_values(
    "avg_shipping_days"
).head(10)

st.dataframe(fast_routes, use_container_width=True)

# ---------------------------------------------------
# Slowest Routes Table
# ---------------------------------------------------

st.markdown("---")
st.subheader("⚠ Bottom 10 Slowest Routes")

slow_routes = route_stats.sort_values(
    "avg_shipping_days",
    ascending=False
).head(10)

st.dataframe(slow_routes, use_container_width=True)

# ---------------------------------------------------
# Route Explorer
# ---------------------------------------------------

st.markdown("---")
st.subheader("Route Performance Explorer")

selected_route = st.selectbox(
    "Select a Route",
    route_stats["Route"].unique()
)

route_detail = df[df["Route"] == selected_route]

fig3 = px.histogram(
    route_detail,
    x="Shipping Days",
    nbins=10,
    title=f"Shipping Time Distribution for {selected_route}"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# Logistics Insight
# ---------------------------------------------------

st.markdown("---")
st.subheader("Operational Insight")

worst_route = slow_routes.iloc[0]

st.warning(
f"""
The slowest route in the network is **{worst_route['Route']}**
with an average delivery time of **{worst_route['avg_shipping_days']:.2f} days**.

This route may benefit from:

• Improved logistics planning  
• Alternative shipping modes  
• Closer factory allocation
"""
)

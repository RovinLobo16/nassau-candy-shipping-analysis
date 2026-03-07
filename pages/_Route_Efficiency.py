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
# Route Aggregation (Requirement)
# ---------------------------------------------------

route_stats = df.groupby("Route").agg(

    shipments=("Shipping Days","count"),

    avg_shipping_days=("Shipping Days","mean"),

    lead_time_variability=("Shipping Days","std"),

    min_delivery=("Shipping Days","min"),

    max_delivery=("Shipping Days","max")

).reset_index()

# Replace NaN variability (routes with 1 shipment)
route_stats["lead_time_variability"] = route_stats[
    "lead_time_variability"
].fillna(0)

# Route Efficiency Score
route_stats["Efficiency Score"] = (
    route_stats["avg_shipping_days"].max()
    - route_stats["avg_shipping_days"]
)

route_stats = route_stats.sort_values("avg_shipping_days")

# ---------------------------------------------------
# KPI Dashboard
# ---------------------------------------------------

st.subheader("Route Performance Overview")

col1, col2, col3, col4 = st.columns(4)

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

col4.metric(
    "Avg Route Variability",
    f"{route_stats['lead_time_variability'].mean():.2f} days"
)

# ---------------------------------------------------
# Route Delivery Chart
# ---------------------------------------------------

st.markdown("---")
st.subheader("Average Shipping Time by Route")

fig = px.bar(
    route_stats.head(20),
    x="Route",
    y="avg_shipping_days",
    color="avg_shipping_days",
    title="Top 20 Routes by Shipping Time",
    labels={"avg_shipping_days":"Average Shipping Days"}
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Shipment Volume
# ---------------------------------------------------

st.markdown("---")
st.subheader("Top Routes by Shipment Volume")

fig2 = px.bar(
    route_stats.sort_values("shipments",ascending=False).head(10),
    x="Route",
    y="shipments",
    color="shipments",
    title="Top Shipment Routes"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# Route Variability Chart (NEW)
# ---------------------------------------------------

st.markdown("---")
st.subheader("Route Lead Time Variability")

fig_var = px.bar(
    route_stats.sort_values(
        "lead_time_variability",
        ascending=False
    ).head(15),
    x="Route",
    y="lead_time_variability",
    color="lead_time_variability",
    title="Routes with Highest Delivery Variability"
)

st.plotly_chart(fig_var, use_container_width=True)

# ---------------------------------------------------
# Fastest & Slowest Routes
# ---------------------------------------------------

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Fastest Routes")

    st.dataframe(
        route_stats.head(10),
        use_container_width=True
    )

with col2:
    st.subheader("⚠ Slowest Routes")

    st.dataframe(
        route_stats.sort_values(
            "avg_shipping_days",
            ascending=False
        ).head(10),
        use_container_width=True
    )

# ---------------------------------------------------
# Efficiency Leaderboard (NEW)
# ---------------------------------------------------

st.markdown("---")
st.subheader("Route Efficiency Leaderboard")

leaderboard = route_stats.sort_values(
    "Efficiency Score",
    ascending=False
).head(10)

st.dataframe(leaderboard, use_container_width=True)

# ---------------------------------------------------
# Route Performance Explorer
# ---------------------------------------------------

st.markdown("---")
st.subheader("Route Performance Explorer")

selected_route = st.selectbox(
    "Select a Route",
    sorted(route_stats["Route"].unique())
)

route_detail = df[df["Route"] == selected_route]

# ---------------------------------------------------
# Route KPIs
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Shipments",
    len(route_detail)
)

col2.metric(
    "Average Delivery",
    f"{route_detail['Shipping Days'].mean():.2f} days"
)

col3.metric(
    "Max Delivery",
    f"{route_detail['Shipping Days'].max():.2f} days"
)

# ---------------------------------------------------
# Distribution Chart
# ---------------------------------------------------

st.markdown("### Shipping Time Distribution")

fig3 = px.histogram(
    route_detail,
    x="Shipping Days",
    nbins=15,
    title=f"Shipping Days Distribution — {selected_route}"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------
# Box Plot
# ---------------------------------------------------

st.markdown("### Route Delivery Spread")

fig4 = px.box(
    route_detail,
    y="Shipping Days",
    points="all",
    title=f"Delivery Time Spread — {selected_route}"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------------------------------
# Timeline Trend
# ---------------------------------------------------

st.markdown("### Shipment Timeline")

trend = route_detail.groupby("Order Date")[
    "Shipping Days"
].mean().reset_index()

fig5 = px.line(
    trend,
    x="Order Date",
    y="Shipping Days",
    markers=True,
    title=f"Delivery Time Trend — {selected_route}"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------
# Operational Insight
# ---------------------------------------------------

st.markdown("---")
st.subheader("Operational Insight")

worst_route = route_stats.sort_values(
    "avg_shipping_days",
    ascending=False
).iloc[0]

st.warning(
f"""
The slowest route in the network is **{worst_route['Route']}**
with an average delivery time of **{worst_route['avg_shipping_days']:.2f} days**.

Possible improvement actions:

• Optimize transportation routes  
• Use faster shipping modes  
• Allocate closer production factories
"""
)

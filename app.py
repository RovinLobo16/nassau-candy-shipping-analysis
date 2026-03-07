import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="Nassau Candy Logistics Intelligence",
    page_icon="🚚",
    layout="wide"
)

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------

df = load_data()
df = apply_filters(df)

# -----------------------------------------------------
# Page Title
# -----------------------------------------------------

st.title("🚚 Nassau Candy Logistics Intelligence Platform")

st.markdown("""
### Factory → Customer Shipping Route Efficiency Analysis

This dashboard analyzes the **logistics performance of Nassau Candy Distributor**.

It helps identify:

• Inefficient shipping routes  
• Regional delivery bottlenecks  
• Shipping mode performance  
• Factory distribution insights  
• Shipment delay risks using AI
""")

# -----------------------------------------------------
# Create Delay Flag
# -----------------------------------------------------

df["Delayed"] = df["Shipping Days"] > df["Shipping Days"].median()

# -----------------------------------------------------
# KPI Dashboard
# -----------------------------------------------------

st.subheader("📊 Logistics Performance Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "📦 Total Orders",
    len(df)
)

col2.metric(
    "⏱ Avg Lead Time",
    f"{df['Shipping Days'].mean():.2f} days"
)

col3.metric(
    "⚠ Delayed Shipments %",
    f"{df['Delayed'].mean()*100:.2f}%"
)

col4.metric(
    "🚛 Unique Routes",
    df["Route"].nunique()
)

col5.metric(
    "🏭 Factories",
    df["Factory"].nunique()
)

# -----------------------------------------------------
# Shipment Trend
# -----------------------------------------------------

st.markdown("---")
st.subheader("📈 Shipment Trend Over Time")

trend = df.groupby("Order Date")["Shipping Days"].mean().reset_index()

fig1 = px.line(
    trend,
    x="Order Date",
    y="Shipping Days",
    markers=True,
    title="Average Shipping Time Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------------------------
# Delay Distribution
# -----------------------------------------------------

st.markdown("---")
st.subheader("⚠ Shipping Delay Distribution")

fig2 = px.histogram(
    df,
    x="Shipping Days",
    nbins=20,
    title="Distribution of Shipping Duration"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------------------
# Route Performance Snapshot
# -----------------------------------------------------

st.markdown("---")
st.subheader("🚦 Route Performance Snapshot")

route_perf = df.groupby("Route")["Shipping Days"].mean().reset_index()

top_routes = route_perf.sort_values("Shipping Days").head(5)
slow_routes = route_perf.sort_values("Shipping Days",ascending=False).head(5)

col1, col2 = st.columns(2)

with col1:
    st.write("🏆 Fastest Routes")
    st.dataframe(top_routes)

with col2:
    st.write("⚠ Slowest Routes")
    st.dataframe(slow_routes)

# -----------------------------------------------------
# Dataset Preview
# -----------------------------------------------------

st.markdown("---")
st.subheader("📋 Dataset Preview")

st.dataframe(df.head(100), use_container_width=True)

# -----------------------------------------------------
# Dashboard Guidance
# -----------------------------------------------------

st.markdown("---")
st.info("""
Use the navigation menu on the left to explore deeper logistics analytics:

• Route Efficiency Analysis  
• Geographic Shipping Analysis  
• Shipping Mode Performance  
• Factory Insights  
• Shipment Timeline  
• Route Network Visualization  
• AI Delay Prediction
""")

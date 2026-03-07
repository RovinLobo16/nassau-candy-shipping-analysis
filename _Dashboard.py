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
# Sidebar Branding
# -----------------------------------------------------

st.sidebar.image("assets/unified_mentor_logo.png", use_container_width=True)

st.sidebar.markdown("## Nassau Candy Logistics Intelligence")

st.sidebar.markdown("""
Advanced analytics platform for monitoring  
**factory-to-customer shipping performance**.
""")

st.sidebar.markdown("---")

# -----------------------------------------------------
# Load Data
# -----------------------------------------------------

df = load_data()
df = apply_filters(df)

# -----------------------------------------------------
# Header with Logo
# -----------------------------------------------------

col_logo, col_title = st.columns([1,6])

with col_logo:
    st.image("assets/unified_mentor_logo.png", width=120)

with col_title:
    st.title("🚚 Nassau Candy Logistics Intelligence Platform")

st.markdown("""
### Factory → Customer Shipping Route Efficiency Dashboard

This system transforms raw logistics data into **actionable supply chain insights**.

The dashboard helps logistics teams:

• Detect inefficient shipping routes  
• Identify regional delivery bottlenecks  
• Compare shipping mode performance  
• Analyze factory distribution patterns  
• Predict shipment delay risks using AI
""")

# -----------------------------------------------------
# Create Delay Flag
# -----------------------------------------------------

df["Delayed"] = df["Shipping Days"] > df["Shipping Days"].median()

# -----------------------------------------------------
# Executive KPI Dashboard
# -----------------------------------------------------

st.markdown("---")
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
# Shipment Trend Analysis
# -----------------------------------------------------

st.markdown("---")
st.subheader("📈 Shipment Lead Time Trend")

trend = df.groupby("Order Date")["Shipping Days"].mean().reset_index()

fig1 = px.line(
    trend,
    x="Order Date",
    y="Shipping Days",
    markers=True,
    title="Average Shipping Time Over Time",
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------------------------
# Shipping Delay Distribution
# -----------------------------------------------------

st.markdown("---")
st.subheader("⚠ Shipping Duration Distribution")

fig2 = px.histogram(
    df,
    x="Shipping Days",
    nbins=25,
    title="Distribution of Shipping Duration"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------------------------
# Route Performance Snapshot
# -----------------------------------------------------

st.markdown("---")
st.subheader("🚦 Route Efficiency Snapshot")

route_perf = df.groupby("Route")["Shipping Days"].mean().reset_index()

fast_routes = route_perf.sort_values("Shipping Days").head(5)
slow_routes = route_perf.sort_values("Shipping Days", ascending=False).head(5)

col1, col2 = st.columns(2)

with col1:
    st.write("🏆 Fastest Routes")
    st.dataframe(fast_routes, use_container_width=True)

with col2:
    st.write("⚠ Slowest Routes")
    st.dataframe(slow_routes, use_container_width=True)

# -----------------------------------------------------
# Route Delay Visualization
# -----------------------------------------------------

st.markdown("---")
st.subheader("🚛 Average Shipping Time by Route")

route_chart = route_perf.sort_values("Shipping Days", ascending=False).head(15)

fig3 = px.bar(
    route_chart,
    x="Route",
    y="Shipping Days",
    title="Top Routes with Highest Shipping Time",
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------------------------------
# Dataset Preview
# -----------------------------------------------------

st.markdown("---")
st.subheader("📋 Dataset Preview")

st.dataframe(df.head(100), use_container_width=True)

# -----------------------------------------------------
# Dashboard Navigation Help
# -----------------------------------------------------

st.markdown("---")

st.success("""
Use the navigation menu on the left to explore deeper analytics:

• Route Efficiency Analysis  
• Geographic Shipping Analysis  
• Shipping Mode Performance  
• Factory Insights  
• Shipment Timeline  
• Route Network Visualization  
• AI Delay Prediction
""")

# -----------------------------------------------------
# Footer Branding
# -----------------------------------------------------

st.markdown("---")

st.markdown(
"""
<center>

### Unified Mentor Data Analytics Project

**Factory-to-Customer Logistics Intelligence Platform**

Developed using **Python, Streamlit, Machine Learning, and Interactive Data Visualization**

</center>
""",
unsafe_allow_html=True
)

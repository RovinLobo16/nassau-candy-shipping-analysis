import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Shipping Route Efficiency Dashboard", layout="wide")

st.title("🚚 Factory-to-Customer Shipping Route Efficiency Dashboard")

st.markdown("""
This dashboard analyzes logistics performance using the **Nassau Candy Distributor dataset**.
The goal is to identify delivery bottlenecks, evaluate route efficiency, and improve shipping performance.
""")

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv("Nassau Candy Distributor.csv")

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

# -----------------------------
# Feature Engineering
# -----------------------------
df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Shipping Days"] = df["Shipping Days"].abs()

# cap unrealistic values
df.loc[df["Shipping Days"] > 30, "Shipping Days"] = 5

# create route
df["Route"] = df["City"] + " → " + df["Region"]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Dashboard Filters")

date_range = st.sidebar.date_input(
    "Order Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

region_filter = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

state_filter = st.sidebar.multiselect(
    "State",
    df["State/Province"].unique(),
    default=df["State/Province"].unique()
)

shipmode_filter = st.sidebar.multiselect(
    "Shipping Mode",
    df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)

delay_threshold = st.sidebar.slider(
    "Delay Threshold (Days)",
    min_value=1,
    max_value=15,
    value=5
)

# Apply filters
df = df[
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1])) &
    (df["Region"].isin(region_filter)) &
    (df["State/Province"].isin(state_filter)) &
    (df["Ship Mode"].isin(shipmode_filter))
]

# -----------------------------
# KPI Calculations
# -----------------------------
shipping_lead_time = df["Shipping Days"].mean()
avg_lead_time = df.groupby("Route")["Shipping Days"].mean().mean()
route_volume = df.groupby("Route")["Order ID"].count().mean()
delay_frequency = (df["Shipping Days"] > delay_threshold).mean() * 100
route_efficiency = (df["Shipping Days"].mean() / df["Shipping Days"].max()) * 100

# -----------------------------
# KPI Section
# -----------------------------
st.markdown("---")
st.header("📊 KPI Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Shipping Lead Time", round(shipping_lead_time,2))
col2.metric("Average Lead Time", round(avg_lead_time,2))
col3.metric("Route Volume", round(route_volume,2))
col4.metric("Delay Frequency", f"{delay_frequency:.2f}%")
col5.metric("Route Efficiency Score", f"{route_efficiency:.2f}")

# -----------------------------
# Route Efficiency Overview
# -----------------------------
st.markdown("---")
st.header("🚦 Route Efficiency Overview")

col1, col2 = st.columns(2)

route_avg = df.groupby("Route")["Shipping Days"].mean().reset_index()

with col1:
    st.subheader("Average Lead Time by Route")
    fig = px.bar(route_avg, x="Route", y="Shipping Days")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Route Performance Leaderboard")
    route_rank = df.groupby("Route")["Shipping Days"].mean().sort_values().reset_index()
    st.dataframe(route_rank)

# -----------------------------
# Geographic Analysis
# -----------------------------
st.markdown("---")
st.header("🗺 Geographic Shipping Analysis")

col1, col2 = st.columns(2)

state_ship = df.groupby("State/Province")["Shipping Days"].mean().reset_index()

with col1:
    st.subheader("US Shipping Efficiency Heatmap")
    fig = px.choropleth(
        state_ship,
        locations="State/Province",
        locationmode="USA-states",
        color="Shipping Days",
        scope="usa"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Regional Bottleneck Analysis")
    city_delay = df.groupby("City")["Shipping Days"].mean().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(city_delay, x="City", y="Shipping Days")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Shipping Mode Comparison
# -----------------------------
st.markdown("---")
st.header("🚚 Shipping Mode Comparison")

ship_mode_perf = df.groupby("Ship Mode")["Shipping Days"].mean().reset_index()

fig = px.bar(ship_mode_perf, x="Ship Mode", y="Shipping Days")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Route Drill Down
# -----------------------------
st.markdown("---")
st.header("🔎 Route Drill-Down Analysis")

col1, col2 = st.columns(2)

state_perf = df.groupby("State/Province")["Shipping Days"].mean().reset_index()

with col1:
    st.subheader("State Level Performance")
    fig = px.bar(state_perf, x="State/Province", y="Shipping Days")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Order Shipment Timeline")
    timeline = df[["Order ID","Order Date","Ship Date","Shipping Days"]].sort_values("Order Date")
    st.dataframe(timeline.head(30))

# -----------------------------
# Sales Analysis
# -----------------------------
st.markdown("---")
st.header("💰 Sales Analysis")

region_sales = df.groupby("Region")["Sales"].sum().reset_index()

fig = px.bar(region_sales, x="Region", y="Sales", color="Region")
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Correlation Analysis
# -----------------------------
st.markdown("---")
st.header("📈 Correlation Analysis")

corr = df[["Sales","Gross Profit","Units","Shipping Days"]].corr()

fig = px.imshow(corr, text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Insights
# -----------------------------
st.markdown("---")
st.header("💡 Key Insights")

st.info("""
• Some regions show longer shipping times indicating logistics inefficiencies.

• First Class shipping generally delivers faster than Standard Class.

• Certain cities consistently experience higher delivery delays.

• Route analysis highlights inefficient delivery routes.

• Sales and profit show strong correlation indicating profitable product segments.
""")

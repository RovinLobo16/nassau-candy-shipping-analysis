import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Shipping Route Efficiency Dashboard", layout="wide")

st.title("🚚 Factory-to-Customer Shipping Route Efficiency Dashboard")

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("Nassau Candy Distributor.csv")

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

# -----------------------------
# Feature Engineering
# -----------------------------

df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
df['Shipping Days'] = df['Shipping Days'].abs()

# Remove unrealistic values
df.loc[df['Shipping Days'] > 30, 'Shipping Days'] = 5

df['Route'] = df['City'] + " → " + df['Region']

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Dashboard Filters")

region = st.sidebar.multiselect(
    "Select Region",
    df['Region'].unique(),
    default=df['Region'].unique()
)

ship_mode = st.sidebar.multiselect(
    "Select Ship Mode",
    df['Ship Mode'].unique(),
    default=df['Ship Mode'].unique()
)

df = df[(df['Region'].isin(region)) & (df['Ship Mode'].isin(ship_mode))]

# -----------------------------
# KPI Calculations
# -----------------------------

shipping_lead_time = df['Shipping Days'].mean()

avg_lead_time = df.groupby('Route')['Shipping Days'].mean().mean()

route_volume = df.groupby('Route')['Order ID'].count().mean()

delay_frequency = (df['Shipping Days'] > 5).mean() * 100

route_efficiency = (df['Shipping Days'].mean() / df['Shipping Days'].max()) * 100

# -----------------------------
# KPI Section
# -----------------------------

st.subheader("Key Logistics KPIs")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Shipping Lead Time", round(shipping_lead_time,2))
col2.metric("Average Lead Time", round(avg_lead_time,2))
col3.metric("Route Volume", round(route_volume,2))
col4.metric("Delay Frequency", f"{delay_frequency:.2f}%")
col5.metric("Route Efficiency Score", f"{route_efficiency:.2f}")

# -----------------------------
# Sales by Region
# -----------------------------

st.subheader("Sales by Region")

region_sales = df.groupby('Region')['Sales'].sum().reset_index()

fig = px.bar(
    region_sales,
    x='Region',
    y='Sales',
    color='Region',
    title="Sales Distribution by Region"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Shipping Time by Region
# -----------------------------

st.subheader("Shipping Time by Region")

region_ship = df.groupby('Region')['Shipping Days'].mean().reset_index()

fig = px.bar(
    region_ship,
    x='Region',
    y='Shipping Days',
    color='Region',
    title="Average Shipping Days by Region"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Shipping Mode Efficiency
# -----------------------------

st.subheader("Shipping Mode Performance")

ship_mode_perf = df.groupby('Ship Mode')['Shipping Days'].mean().reset_index()

fig = px.bar(
    ship_mode_perf,
    x='Ship Mode',
    y='Shipping Days',
    color='Ship Mode',
    title="Shipping Mode Efficiency"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Top Products
# -----------------------------

st.subheader("Top Products by Sales")

top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()

fig = px.bar(
    top_products,
    x='Product Name',
    y='Sales',
    color='Product Name',
    title="Top 10 Products by Sales"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# City Delay Analysis
# -----------------------------

st.subheader("Cities with Highest Shipping Delay")

city_delay = df.groupby('City')['Shipping Days'].mean().sort_values(ascending=False).head(10).reset_index()

fig = px.bar(
    city_delay,
    x='City',
    y='Shipping Days',
    color='City',
    title="Cities with Highest Delivery Delays"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Route Efficiency
# -----------------------------

st.subheader("Shipping Route Efficiency")

route_analysis = df.groupby('Route')['Shipping Days'].mean().sort_values(ascending=False).head(10).reset_index()

fig = px.bar(
    route_analysis,
    x='Route',
    y='Shipping Days',
    color='Route',
    title="Top Routes with Highest Shipping Time"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Shipping Distribution
# -----------------------------

st.subheader("Shipping Days Distribution")

fig = px.histogram(
    df,
    x='Shipping Days',
    color='Region',
    nbins=10,
    title="Distribution of Shipping Days"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Geographic Distribution
# -----------------------------

st.subheader("Geographic Sales Distribution")

city_sales = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(15).reset_index()

fig = px.scatter(
    city_sales,
    x='City',
    y='Sales',
    size='Sales',
    color='Sales',
    title="Top Cities by Sales"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Profit vs Sales Analysis
# -----------------------------

st.subheader("Profit vs Sales Analysis")

fig = px.scatter(
    df,
    x='Sales',
    y='Gross Profit',
    color='Region',
    title="Sales vs Profit Relationship"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Correlation Matrix
# -----------------------------

st.subheader("Correlation Analysis")

corr = df[['Sales','Gross Profit','Units','Shipping Days']].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Feature Correlation Matrix"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Insights
# -----------------------------

st.subheader("Key Insights")

st.write("""
• Some regions experience longer shipping times compared to others.

• First Class shipping provides faster delivery compared to Standard Class.

• Certain cities show higher delivery delays indicating logistics bottlenecks.

• A small number of products contribute most of the revenue.

• Route analysis helps identify inefficient shipping routes.

• Sales and profit show strong correlation indicating profitable product segments.
""")

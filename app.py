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

df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
df['Shipping Days'] = df['Shipping Days'].abs()

# Limit unrealistic values
df.loc[df['Shipping Days'] > 30, 'Shipping Days'] = 5

df['Profit Margin'] = df['Gross Profit'] / df['Sales']

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
# KPI Section
# -----------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"${df['Sales'].sum():,.2f}")
col2.metric("📈 Total Profit", f"${df['Gross Profit'].sum():,.2f}")
col3.metric("📦 Units Sold", int(df['Units'].sum()))
col4.metric("🚚 Avg Shipping Days", round(df['Shipping Days'].mean(),2))

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

df['Route'] = df['City'] + " → " + df['Region']

route = df.groupby('Route')['Shipping Days'].mean().sort_values(ascending=False).head(10).reset_index()

fig = px.bar(
    route,
    x='Route',
    y='Shipping Days',
    color='Route',
    title="Top Routes with Highest Shipping Time"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Shipping Days Distribution
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
# Geographic Shipping Distribution
# -----------------------------

st.subheader("Geographic Shipping Distribution")

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
# Correlation Analysis
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
# Insights Section
# -----------------------------

st.subheader("Key Insights")

st.write("""
• Certain regions experience longer delivery times compared to others.

• First Class shipping provides faster delivery compared to Standard Class.

• Some cities show higher shipping delays indicating logistical bottlenecks.

• A small number of products generate most of the revenue.

• Route analysis helps identify inefficient shipping routes.

• Sales and profit show strong correlation, indicating profitable product segments.
""")

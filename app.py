import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Shipping Route Efficiency Analysis", layout="wide")

st.title("🚚 Shipping Route Efficiency Analysis")

# Load dataset
df = pd.read_csv("Nassau Candy Distributor.csv")

# Convert dates
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

# Feature engineering
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
df['Profit Margin'] = df['Gross Profit'] / df['Sales']
df['Sales per Unit'] = df['Sales'] / df['Units']

# Dataset preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# ========================
# KPI Section
# ========================

st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", round(df['Sales'].sum(),2))
col2.metric("Total Profit", round(df['Gross Profit'].sum(),2))
col3.metric("Total Units Sold", int(df['Units'].sum()))
col4.metric("Avg Shipping Days", round(df['Shipping Days'].mean(),2))

# ========================
# Region Analysis
# ========================

st.subheader("Sales by Region")

region_sales = df.groupby('Region')['Sales'].sum()

fig1, ax1 = plt.subplots()
region_sales.plot(kind='bar', ax=ax1)
ax1.set_ylabel("Sales")
ax1.set_xlabel("Region")

st.pyplot(fig1)

# ========================
# Shipping Time by Region
# ========================

st.subheader("Average Shipping Time by Region")

region_shipping = df.groupby('Region')['Shipping Days'].mean()

fig2, ax2 = plt.subplots()
region_shipping.plot(kind='bar', ax=ax2)
ax2.set_ylabel("Shipping Days")

st.pyplot(fig2)

# ========================
# Shipping Mode Analysis
# ========================

st.subheader("Shipping Mode Efficiency")

ship_mode = df.groupby('Ship Mode')['Shipping Days'].mean()

fig3, ax3 = plt.subplots()
ship_mode.plot(kind='bar', ax=ax3)
ax3.set_ylabel("Average Shipping Days")

st.pyplot(fig3)

# ========================
# Top Products
# ========================

st.subheader("Top 10 Products by Sales")

top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)

fig4, ax4 = plt.subplots(figsize=(10,5))
top_products.plot(kind='bar', ax=ax4)

st.pyplot(fig4)

# ========================
# City Delay Analysis
# ========================

st.subheader("Cities with Highest Shipping Delay")

city_delay = df.groupby('City')['Shipping Days'].mean().sort_values(ascending=False).head(10)

fig5, ax5 = plt.subplots()
city_delay.plot(kind='bar', ax=ax5)

st.pyplot(fig5)

# ========================
# Route Efficiency
# ========================

st.subheader("Shipping Route Efficiency")

df['Route'] = df['City'] + " → " + df['Region']

route_analysis = df.groupby('Route')['Shipping Days'].mean().sort_values(ascending=False).head(10)

fig6, ax6 = plt.subplots(figsize=(10,5))
route_analysis.plot(kind='bar', ax=ax6)

st.pyplot(fig6)

# ========================
# Delivery Efficiency Score
# ========================

st.subheader("Delivery Efficiency Score by Region")

avg_shipping = df['Shipping Days'].mean()
df['Efficiency Score'] = avg_shipping / df['Shipping Days']

eff_region = df.groupby('Region')['Efficiency Score'].mean()

fig7, ax7 = plt.subplots()
eff_region.plot(kind='bar', ax=ax7)

st.pyplot(fig7)

# ========================
# Shipping Delay Distribution
# ========================

st.subheader("Shipping Delay Distribution")

fig8, ax8 = plt.subplots()

sns.histplot(df['Shipping Days'], bins=20, ax=ax8)

st.pyplot(fig8)

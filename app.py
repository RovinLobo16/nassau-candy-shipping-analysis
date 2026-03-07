import streamlit as st
import pandas as pd
from utils import load_data

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Nassau Candy Logistics Dashboard",
    page_icon="🚚",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = load_data()

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🚚 Factory-to-Customer Shipping Route Efficiency Dashboard")

st.markdown("""
This dashboard analyzes **shipping efficiency across the United States**
for **Nassau Candy Distributor**.

### Objectives

• Identify inefficient shipping routes  
• Detect logistics bottlenecks  
• Compare shipping modes  
• Evaluate regional performance  
• Improve supply chain efficiency
""")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("🔎 Dashboard Filters")

start = st.sidebar.date_input(
    "Start Date",
    df["Order Date"].min()
)

end = st.sidebar.date_input(
    "End Date",
    df["Order Date"].max()
)

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

ship_mode = st.sidebar.multiselect(
    "Select Ship Mode",
    options=df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)

delay_threshold = st.sidebar.slider(
    "Delay Threshold (days)",
    min_value=1,
    max_value=10,
    value=5
)

# ---------------------------------------------------
# FIX DATE TYPE (IMPORTANT)
# ---------------------------------------------------

start = pd.to_datetime(start)
end = pd.to_datetime(end)

# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------

filtered_df = df[
    (df["Order Date"] >= start) &
    (df["Order Date"] <= end) &
    (df["Region"].isin(region)) &
    (df["Ship Mode"].isin(ship_mode))
]

# ---------------------------------------------------
# DELAY CALCULATION
# ---------------------------------------------------

filtered_df["Delayed"] = filtered_df["Shipping Days"] > delay_threshold

# ---------------------------------------------------
# KPI METRICS
# ---------------------------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Orders",
    len(filtered_df)
)

col2.metric(
    "Average Lead Time (days)",
    round(filtered_df["Shipping Days"].mean(), 2)
)

col3.metric(
    "Delayed Shipments %",
    round(filtered_df["Delayed"].mean() * 100, 2)
)

col4.metric(
    "Unique Shipping Routes",
    filtered_df["Route"].nunique()
)

# ---------------------------------------------------
# SUMMARY SECTION
# ---------------------------------------------------

st.subheader("📦 Dataset Overview")

st.write(
    "Filtered dataset preview showing the first 100 records."
)

st.dataframe(filtered_df.head(100), use_container_width=True)

# ---------------------------------------------------
# DASHBOARD NAVIGATION MESSAGE
# ---------------------------------------------------

st.success(
"""
Use the navigation menu on the left to explore:

• Route Efficiency Analysis  
• Geographic Shipping Analysis  
• Ship Mode Performance  
• Product & Factory Insights  
• Order Timeline  
• Route Network Map  
"""
)

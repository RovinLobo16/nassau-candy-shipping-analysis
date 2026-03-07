import streamlit as st
from utils import load_data

st.set_page_config(page_title="Nassau Candy Logistics Dashboard", layout="wide")

st.title("🚚 Factory-to-Customer Shipping Route Efficiency Dashboard")

st.markdown("""
This dashboard analyzes **shipping efficiency across the United States**
for Nassau Candy Distributor.

Key objectives:

• Identify inefficient routes  
• Detect geographic bottlenecks  
• Compare shipping modes  
• Improve supply chain performance  
""")

df = load_data()

st.sidebar.header("Filters")

start = st.sidebar.date_input("Start Date", df["Order Date"].min())
end = st.sidebar.date_input("End Date", df["Order Date"].max())

region = st.sidebar.multiselect(
"Region",
df["Region"].unique(),
default=df["Region"].unique()
)

ship_mode = st.sidebar.multiselect(
"Ship Mode",
df["Ship Mode"].unique(),
default=df["Ship Mode"].unique()
)

delay_threshold = st.sidebar.slider("Delay Threshold (days)",1,10,5)

df = df[
(df["Order Date"] >= start) &
(df["Order Date"] <= end) &
(df["Region"].isin(region)) &
(df["Ship Mode"].isin(ship_mode))
]

df["Delayed"] = df["Shipping Days"] > delay_threshold

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Orders", len(df))
col2.metric("Avg Lead Time", round(df["Shipping Days"].mean(),2))
col3.metric("Delayed %", round(df["Delayed"].mean()*100,2))
col4.metric("Unique Routes", df["Route"].nunique())

st.info("Use the navigation panel to explore analytics modules.")

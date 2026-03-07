import streamlit as st
from utils import load_data, apply_filters

st.set_page_config(
    page_title="Nassau Candy Logistics Intelligence",
    layout="wide"
)

df = load_data()
df = apply_filters(df)

st.title("🚚 Nassau Candy Logistics Intelligence Platform")

st.markdown("""
### Factory → Customer Shipping Route Efficiency Analysis

This dashboard transforms shipping data into actionable logistics insights.
""")

df["Delayed"] = df["Shipping Days"] > df["Shipping Days"].median()

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Orders",len(df))
col2.metric("Avg Lead Time",round(df["Shipping Days"].mean(),2))
col3.metric("Delayed %",round(df["Delayed"].mean()*100,2))
col4.metric("Unique Routes",df["Route"].nunique())

st.subheader("Dataset Preview")

st.dataframe(df.head(100),use_container_width=True)

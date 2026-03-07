import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🗺 Geographic Shipping Analysis")

df = pd.read_csv("Nassau Candy Distributor.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

state_ship = df.groupby("State/Province")["Shipping Days"].mean().reset_index()

st.subheader("US Shipping Efficiency Heatmap")

fig = px.choropleth(
    state_ship,
    locations="State/Province",
    locationmode="USA-states",
    color="Shipping Days",
    scope="usa"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Regional Bottleneck Visualization")

city_delay = df.groupby("City")["Shipping Days"].mean().sort_values(ascending=False).head(10).reset_index()

fig = px.bar(city_delay, x="City", y="Shipping Days")

st.plotly_chart(fig, use_container_width=True)

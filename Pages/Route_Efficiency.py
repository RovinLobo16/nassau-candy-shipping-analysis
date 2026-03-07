import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🚦 Route Efficiency Analysis")

df = pd.read_csv("Nassau Candy Distributor.csv")

df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

df["Route"] = df["City"] + " → " + df["Region"]

route_avg = df.groupby("Route")["Shipping Days"].mean().reset_index()

st.subheader("Average Lead Time by Route")

fig = px.bar(route_avg, x="Route", y="Shipping Days")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Route Performance Leaderboard")

route_rank = df.groupby("Route")["Shipping Days"].mean().sort_values().reset_index()

st.dataframe(route_rank)

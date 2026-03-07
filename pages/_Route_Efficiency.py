import streamlit as st
import plotly.express as px
from utils import load_data

st.title("🚦 Route Efficiency Analysis")

df = load_data()

route_stats = df.groupby("Route").agg(
avg_days=("Shipping Days","mean"),
orders=("Shipping Days","count")
).reset_index()

max_days = route_stats["avg_days"].max()

route_stats["Efficiency Score"] = (max_days - route_stats["avg_days"]) / max_days

st.subheader("Average Lead Time by Route")

fig = px.bar(route_stats,x="Route",y="avg_days")

st.plotly_chart(fig,use_container_width=True)

st.subheader("Top 10 Fastest Routes")

st.dataframe(route_stats.sort_values("avg_days").head(10))

st.subheader("Bottom 10 Slowest Routes")

st.dataframe(route_stats.sort_values("avg_days",ascending=False).head(10))

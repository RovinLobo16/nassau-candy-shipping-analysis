import streamlit as st
import plotly.express as px
from utils import load_data

st.title("🗺 Geographic Shipping Analysis")

df = load_data()

state_perf = df.groupby("State/Province").agg(
avg_days=("Shipping Days","mean"),
orders=("Shipping Days","count")
).reset_index()

state_perf["Bottleneck Score"] = state_perf["avg_days"] * state_perf["orders"]

st.subheader("US Shipping Efficiency Heatmap")

fig = px.choropleth(
state_perf,
locations="State/Province",
locationmode="USA-states",
color="avg_days",
scope="usa"
)

st.plotly_chart(fig,use_container_width=True)

st.subheader("Top Bottleneck States")

fig = px.bar(
state_perf.sort_values("Bottleneck Score",ascending=False).head(10),
x="State/Province",
y="Bottleneck Score"
)

st.plotly_chart(fig,use_container_width=True)

import streamlit as st
import plotly.express as px
from utils import load_data, apply_filters

df = apply_filters(load_data())

st.title("🗺 Geographic Shipping Analysis")

state_perf = df.groupby("State/Province")["Shipping Days"].mean().reset_index()

fig = px.bar(
state_perf.sort_values("Shipping Days",ascending=False).head(10),
x="State/Province",
y="Shipping Days"
)

st.plotly_chart(fig,use_container_width=True)

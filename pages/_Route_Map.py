import streamlit as st
import plotly.express as px
from utils import load_data

st.title("🌎 Factory → Customer Route Map")

df = load_data()

fig = px.scatter_geo(
df,
locationmode="USA-states",
locations="State/Province",
color="Shipping Days",
hover_name="Route",
scope="usa"
)

st.plotly_chart(fig,use_container_width=True)

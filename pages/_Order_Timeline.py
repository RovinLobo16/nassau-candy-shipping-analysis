import streamlit as st
import plotly.express as px
from utils import load_data

st.title("📦 Shipment Timeline")

df = load_data()

sample = df.sort_values("Shipping Days").head(300)

fig = px.scatter(
sample,
x="Order Date",
y="Shipping Days",
color="Ship Mode",
hover_data=["Order ID","State/Province"]
)

st.plotly_chart(fig,use_container_width=True)

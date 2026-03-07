import streamlit as st
import plotly.express as px
from utils import load_data

st.title("🚛 Shipping Mode Performance")

df = load_data()

ship_perf = df.groupby("Ship Mode")["Shipping Days"].mean().reset_index()

fig = px.bar(ship_perf,x="Ship Mode",y="Shipping Days",color="Ship Mode")

st.plotly_chart(fig,use_container_width=True)

fig = px.box(df,x="Ship Mode",y="Shipping Days")

st.plotly_chart(fig,use_container_width=True)

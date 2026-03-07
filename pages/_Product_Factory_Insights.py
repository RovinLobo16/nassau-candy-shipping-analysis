import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏭 Factory Insights")

factory_data = pd.DataFrame({

"Factory":[
"Lot's O' Nuts",
"Wicked Choccy's",
"Sugar Shack",
"Secret Factory",
"The Other Factory"
],

"Latitude":[32.881893,32.076176,48.11914,41.446333,35.1175],
"Longitude":[-111.768036,-81.088371,-96.18115,-90.565487,-89.97107]
})

st.dataframe(factory_data)

fig = px.scatter_geo(
factory_data,
lat="Latitude",
lon="Longitude",
hover_name="Factory"
)

st.plotly_chart(fig,use_container_width=True)

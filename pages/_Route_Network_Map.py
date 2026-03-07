import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import load_data

st.title("🌎 Factory → Customer Route Network")

df = load_data()

# Factory coordinates
factory_coords = {
"Lot's O' Nuts": (32.881893, -111.768036),
"Wicked Choccy's": (32.076176, -81.088371),
"Sugar Shack": (48.11914, -96.18115),
"Secret Factory": (41.446333, -90.565487),
"The Other Factory": (35.1175, -89.97107)
}

# Approximate state center coordinates
state_coords = {
"CA": (36.7783,-119.4179),
"TX": (31.9686,-99.9018),
"FL": (27.6648,-81.5158),
"NY": (43.2994,-74.2179),
"IL": (40.6331,-89.3985),
"PA": (41.2033,-77.1945),
"OH": (40.4173,-82.9071)
}

routes = df.groupby(["Factory","State/Province"])["Shipping Days"].mean().reset_index()

fig = go.Figure()

for _,row in routes.iterrows():

    factory = row["Factory"]
    state = row["State/Province"]

    if factory in factory_coords and state in state_coords:

        lat1,lon1 = factory_coords[factory]
        lat2,lon2 = state_coords[state]

        fig.add_trace(go.Scattergeo(
            locationmode="USA-states",
            lon=[lon1,lon2],
            lat=[lat1,lat2],
            mode="lines",
            line=dict(width=1),
            opacity=0.6
        ))

fig.update_layout(
    title="Shipping Routes Across USA",
    geo=dict(scope="usa")
)

st.plotly_chart(fig,use_container_width=True)

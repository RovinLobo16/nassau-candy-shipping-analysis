import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, apply_filters

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Logistics Flow Map",
    layout="wide"
)

st.title("🚚 Animated Logistics Flow Map")

st.markdown("""
This visualization shows **how shipments move from factories to customer destinations across the United States**.

The animation highlights:

• Factory distribution network  
• Customer destination states  
• Shipment routes  
• Logistics flow patterns
""")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

df = load_data()
df = apply_filters(df)

# ---------------------------------------------------
# Factory Coordinates
# ---------------------------------------------------

factory_coords = {
"Lot's O' Nuts": (32.881893, -111.768036),
"Wicked Choccy's": (32.076176, -81.088371),
"Sugar Shack": (48.11914, -96.18115),
"Secret Factory": (41.446333, -90.565487),
"The Other Factory": (35.1175, -89.97107)
}

# ---------------------------------------------------
# State Coordinates (approximate centers)
# ---------------------------------------------------

state_coords = {
"AL": (32.806671, -86.791130),
"CA": (36.116203, -119.681564),
"TX": (31.054487, -97.563461),
"FL": (27.766279, -81.686783),
"NY": (42.165726, -74.948051),
"PA": (40.590752, -77.209755),
"IL": (40.349457, -88.986137),
"OH": (40.388783, -82.764915),
"GA": (33.040619, -83.643074),
"NC": (35.630066, -79.806419)
}

# ---------------------------------------------------
# Create Routes
# ---------------------------------------------------

routes = df.groupby(["Factory","State/Province"]).size().reset_index(name="shipments")

# ---------------------------------------------------
# Build Map
# ---------------------------------------------------

fig = go.Figure()

# Add factory points

for factory,(lat,lon) in factory_coords.items():

    fig.add_trace(go.Scattergeo(
        lon=[lon],
        lat=[lat],
        text=factory,
        mode="markers+text",
        marker=dict(size=10,color="red"),
        name=factory
    ))

# Add routes

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
            line=dict(width=1,color="blue"),
            opacity=0.5,
            showlegend=False
        ))

# ---------------------------------------------------
# Layout
# ---------------------------------------------------

fig.update_layout(
    title="Factory to Customer Logistics Network",
    geo=dict(
        scope="usa",
        projection_type="albers usa",
        showland=True
    ),
    height=700
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Shipment Statistics
# ---------------------------------------------------

st.markdown("---")

st.subheader("Network Overview")

col1,col2,col3 = st.columns(3)

col1.metric("Factories", df["Factory"].nunique())
col2.metric("States Served", df["State/Province"].nunique())
col3.metric("Total Shipments", len(df))

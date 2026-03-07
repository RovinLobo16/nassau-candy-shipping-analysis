import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, apply_filters

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Animated Logistics Flow Map",
    layout="wide"
)

st.title("🚚 Animated Logistics Flow Map")

st.markdown("""
This visualization shows **how shipments move from factories to customer destinations across the United States over time**.

Features:

• Shipment movement animation  
• Factory → Customer flow  
• Route thickness based on shipment volume  
• Logistics network insights
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
# State Coordinates
# ---------------------------------------------------

state_coords = {
"Alabama": (32.806671,-86.791130),
"California": (36.116203,-119.681564),
"Texas": (31.054487,-97.563461),
"Florida": (27.766279,-81.686783),
"New York": (42.165726,-74.948051),
"Illinois": (40.349457,-88.986137),
"Pennsylvania": (40.590752,-77.209755),
"Ohio": (40.388783,-82.764915),
"Georgia": (33.040619,-83.643074),
"North Carolina": (35.630066,-79.806419)
}

# ---------------------------------------------------
# Build Logistics Routes Dataset
# ---------------------------------------------------

routes = []

for _, row in df.iterrows():

    factory = row["Factory"]
    state = row["State/Province"]

    if factory in factory_coords and state in state_coords:

        f_lat, f_lon = factory_coords[factory]
        s_lat, s_lon = state_coords[state]

        routes.append({
            "factory": factory,
            "state": state,
            "order_date": row["Order Date"],
            "lat": s_lat,
            "lon": s_lon,
            "shipping_days": row["Shipping Days"]
        })

routes_df = pd.DataFrame(routes)

# ---------------------------------------------------
# Animated Map
# ---------------------------------------------------

fig = px.scatter_mapbox(
    routes_df,
    lat="lat",
    lon="lon",
    color="shipping_days",
    size_max=15,
    zoom=3,
    hover_name="state",
    hover_data=["factory","shipping_days"],
    animation_frame="order_date",
    height=700,
    color_continuous_scale="Reds"
)

fig.update_layout(
    mapbox_style="carto-darkmatter",
    title="Factory → Customer Logistics Flow"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Logistics Network KPIs
# ---------------------------------------------------

st.markdown("---")

st.subheader("Logistics Network Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Factories", df["Factory"].nunique())
col2.metric("States Served", df["State/Province"].nunique())
col3.metric("Total Shipments", len(df))
col4.metric(
    "Average Shipping Time",
    f"{df['Shipping Days'].mean():.2f} days"
)

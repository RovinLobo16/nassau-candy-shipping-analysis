import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, apply_filters

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Factory → Customer Route Network",
    layout="wide"
)

st.title("🌎 Factory → Customer Shipping Network")

st.markdown("""
This visualization shows how shipments move from **production factories**
to **customer states across the United States**.

Routes are colored based on **average shipping time** and thickness represents **shipment volume**.
""")

# --------------------------------------------------
# Load and Filter Data
# --------------------------------------------------

df = load_data()
df = apply_filters(df)

# --------------------------------------------------
# Factory Coordinates
# --------------------------------------------------

factory_coords = {
"Lot's O' Nuts": (32.881893, -111.768036),
"Wicked Choccy's": (32.076176, -81.088371),
"Sugar Shack": (48.11914, -96.18115),
"Secret Factory": (41.446333, -90.565487),
"The Other Factory": (35.1175, -89.97107)
}

# --------------------------------------------------
# State Coordinates (Expanded)
# --------------------------------------------------

state_coords = {
"CA": (36.77,-119.41),
"TX": (31.96,-99.90),
"FL": (27.66,-81.51),
"NY": (43.00,-75.00),
"IL": (40.00,-89.00),
"PA": (41.20,-77.19),
"OH": (40.41,-82.90),
"GA": (32.16,-82.90),
"NC": (35.78,-79.80),
"MI": (44.31,-85.60)
}

# --------------------------------------------------
# Route Statistics
# --------------------------------------------------

routes = df.groupby(["Factory","State/Province"]).agg(
    avg_shipping_days=("Shipping Days","mean"),
    shipments=("Shipping Days","count")
).reset_index()

# --------------------------------------------------
# KPI Overview
# --------------------------------------------------

st.subheader("Route Network Overview")

col1,col2,col3 = st.columns(3)

col1.metric("Total Routes", len(routes))
col2.metric("Total Shipments", routes["shipments"].sum())
col3.metric("Avg Shipping Time", f"{routes['avg_shipping_days'].mean():.2f} days")

# --------------------------------------------------
# Build Map
# --------------------------------------------------

fig = go.Figure()

for _,row in routes.iterrows():

    factory = row["Factory"]
    state = row["State/Province"]

    if factory in factory_coords and state in state_coords:

        lat1,lon1 = factory_coords[factory]
        lat2,lon2 = state_coords[state]

        delay = row["avg_shipping_days"]
        volume = row["shipments"]

        fig.add_trace(go.Scattergeo(
            lon=[lon1,lon2],
            lat=[lat1,lat2],
            mode="lines",
            line=dict(
                width=1 + volume*0.05,
                color="red" if delay > routes["avg_shipping_days"].mean() else "green"
            ),
            opacity=0.7,
            hoverinfo="text",
            text=f"""
Factory: {factory}<br>
Destination: {state}<br>
Shipments: {volume}<br>
Avg Days: {delay:.2f}
"""
        ))

# --------------------------------------------------
# Add Factory Markers
# --------------------------------------------------

for factory,(lat,lon) in factory_coords.items():

    fig.add_trace(go.Scattergeo(
        lon=[lon],
        lat=[lat],
        mode="markers",
        marker=dict(size=8,color="blue"),
        name=factory
    ))

# --------------------------------------------------
# Layout
# --------------------------------------------------

fig.update_layout(
    title="Factory → Customer Shipping Routes Across USA",
    geo=dict(
        scope="usa",
        projection_type="albers usa",
        showland=True
    ),
    margin=dict(l=0,r=0,t=50,b=0)
)

st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# Route Delay Analysis
# --------------------------------------------------

st.markdown("---")
st.subheader("⚠ Slowest Shipping Routes")

slow_routes = routes.sort_values(
    "avg_shipping_days",
    ascending=False
).head(10)

st.dataframe(slow_routes, use_container_width=True)

# --------------------------------------------------
# Insight Section
# --------------------------------------------------

worst_route = slow_routes.iloc[0]

st.warning(
f"""
The slowest route is **{worst_route['Factory']} → {worst_route['State/Province']}**
with an average delivery time of **{worst_route['avg_shipping_days']:.2f} days**.

This route may require improved logistics planning or faster shipping modes.
"""
)

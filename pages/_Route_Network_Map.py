import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, apply_filters

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="Factory → Customer Route Network",
    layout="wide"
)

st.title("🌎 Factory → Customer Route Network")

st.markdown("""
This map visualizes how shipments move from **production factories**
to **customer destinations across the United States**.

Routes are:
- 🔴 Red → Slower routes  
- 🟢 Green → Faster routes  
- Thickness → Shipment volume  

🔗 Includes real **Google Maps route links**
""")

# --------------------------------------------------
# Load Data
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
# FULL USA STATE COORDINATES (ALL 50 STATES)
# --------------------------------------------------

state_coords = {
"Alabama": (32.806671, -86.791130),
"Alaska": (61.370716, -152.404419),
"Arizona": (33.729759, -111.431221),
"Arkansas": (34.969704, -92.373123),
"California": (36.116203, -119.681564),
"Colorado": (39.059811, -105.311104),
"Connecticut": (41.597782, -72.755371),
"Delaware": (39.318523, -75.507141),
"Florida": (27.766279, -81.686783),
"Georgia": (33.040619, -83.643074),
"Hawaii": (21.094318, -157.498337),
"Idaho": (44.240459, -114.478828),
"Illinois": (40.349457, -88.986137),
"Indiana": (39.849426, -86.258278),
"Iowa": (42.011539, -93.210526),
"Kansas": (38.526600, -96.726486),
"Kentucky": (37.668140, -84.670067),
"Louisiana": (31.169546, -91.867805),
"Maine": (44.693947, -69.381927),
"Maryland": (39.063946, -76.802101),
"Massachusetts": (42.230171, -71.530106),
"Michigan": (43.326618, -84.536095),
"Minnesota": (45.694454, -93.900192),
"Mississippi": (32.741646, -89.678696),
"Missouri": (38.456085, -92.288368),
"Montana": (46.921925, -110.454353),
"Nebraska": (41.125370, -98.268082),
"Nevada": (38.313515, -117.055374),
"New Hampshire": (43.452492, -71.563896),
"New Jersey": (40.298904, -74.521011),
"New Mexico": (34.840515, -106.248482),
"New York": (42.165726, -74.948051),
"North Carolina": (35.630066, -79.806419),
"North Dakota": (47.528912, -99.784012),
"Ohio": (40.388783, -82.764915),
"Oklahoma": (35.565342, -96.928917),
"Oregon": (44.572021, -122.070938),
"Pennsylvania": (40.590752, -77.209755),
"Rhode Island": (41.680893, -71.511780),
"South Carolina": (33.856892, -80.945007),
"South Dakota": (44.299782, -99.438828),
"Tennessee": (35.747845, -86.692345),
"Texas": (31.054487, -97.563461),
"Utah": (40.150032, -111.862434),
"Vermont": (44.045876, -72.710686),
"Virginia": (37.769337, -78.169968),
"Washington": (47.400902, -121.490494),
"West Virginia": (38.491226, -80.954453),
"Wisconsin": (44.268543, -89.616508),
"Wyoming": (42.755966, -107.302490)
}

# --------------------------------------------------
# Route Aggregation (FULLY CORRECT)
# --------------------------------------------------

routes = df.groupby(["Factory","State/Province"]).agg(
    avg_shipping_days=("Shipping Days","mean"),
    shipments=("Shipping Days","count")
).reset_index()

# Remove invalid
routes = routes.dropna(subset=["Factory","State/Province"])

# --------------------------------------------------
# KPI Overview
# --------------------------------------------------

st.subheader("Route Network Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Routes", len(routes))
col2.metric("Total Shipments", routes["shipments"].sum())
col3.metric("Avg Shipping Time", f"{routes['avg_shipping_days'].mean():.2f} days")

# --------------------------------------------------
# Google Maps Link Generator
# --------------------------------------------------

def generate_map_link(lat1, lon1, lat2, lon2):
    return f"https://www.google.com/maps/dir/{lat1},{lon1}/{lat2},{lon2}"

# --------------------------------------------------
# Build Map
# --------------------------------------------------

fig = go.Figure()

avg_delay = routes["avg_shipping_days"].mean()

for _, row in routes.iterrows():

    factory = row["Factory"]
    state = row["State/Province"]

    if factory in factory_coords and state in state_coords:

        lat1, lon1 = factory_coords[factory]
        lat2, lon2 = state_coords[state]

        delay = row["avg_shipping_days"]
        volume = row["shipments"]

        color = "red" if delay > avg_delay else "green"

        fig.add_trace(go.Scattergeo(
            lon=[lon1, lon2],
            lat=[lat1, lat2],
            mode="lines",
            line=dict(
                width=1 + volume * 0.08,
                color=color
            ),
            opacity=0.6,
            hoverinfo="text",
            text=f"""
Factory: {factory}
State: {state}
Shipments: {volume}
Avg Days: {delay:.2f}
"""
        ))

# --------------------------------------------------
# Factory Markers
# --------------------------------------------------

for factory, (lat, lon) in factory_coords.items():
    fig.add_trace(go.Scattergeo(
        lon=[lon],
        lat=[lat],
        mode="markers",
        marker=dict(size=8, color="blue"),
        name=factory
    ))

# --------------------------------------------------
# Layout
# --------------------------------------------------

fig.update_layout(
    geo=dict(scope="usa"),
    margin=dict(l=0, r=0, t=40, b=0),
    title="Factory → Customer Shipping Routes Across USA"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Slow Routes + GOOGLE MAP LINKS
# --------------------------------------------------

st.markdown("---")
st.subheader("⚠ Slowest Shipping Routes")

slow_routes = routes.sort_values(
    "avg_shipping_days",
    ascending=False
).head(10)

# Add links
links = []
for _, row in slow_routes.iterrows():

    factory = row["Factory"]
    state = row["State/Province"]

    if factory in factory_coords and state in state_coords:
        lat1, lon1 = factory_coords[factory]
        lat2, lon2 = state_coords[state]
        link = generate_map_link(lat1, lon1, lat2, lon2)
    else:
        link = None

    links.append(link)

slow_routes["Map"] = links

# Display nicely
for _, row in slow_routes.iterrows():

    st.markdown(f"""
**{row['Factory']} → {row['State/Province']}**  
📦 Shipments: {row['shipments']}  
⏱ Avg Days: {row['avg_shipping_days']:.2f}  
🔗 [Open in Google Maps]({row['Map']})
""")

# --------------------------------------------------
# Insight
# --------------------------------------------------

worst = slow_routes.iloc[0]

st.warning(f"""
🚨 Worst Route: **{worst['Factory']} → {worst['State/Province']}**

Average delivery time: **{worst['avg_shipping_days']:.2f} days**

👉 Recommended:
- Optimize route planning
- Use faster shipping modes
- Relocate inventory closer to demand
""")

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, apply_filters

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(page_title="Route Network", layout="wide")

st.title("🌎 Factory → Customer Route Network")

st.markdown("""
🚀 Advanced logistics visualization with:

- 🎬 Animated route flows  
- 🎯 Route highlighting  
- 📊 Volume-based thickness  
- 🔗 Real Google Maps integration  
""")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = load_data()
df = apply_filters(df)

# --------------------------------------------------
# Coordinates
# --------------------------------------------------

factory_coords = {
"Lot's O' Nuts": (32.88, -111.76),
"Wicked Choccy's": (32.07, -81.08),
"Sugar Shack": (48.11, -96.18),
"Secret Factory": (41.44, -90.56),
"The Other Factory": (35.11, -89.97)
}

state_coords = {
"California": (36.11, -119.68),
"Texas": (31.05, -97.56),
"Florida": (27.76, -81.68),
"New York": (42.16, -74.94),
"Illinois": (40.34, -88.98),
"Pennsylvania": (40.59, -77.20),
"Ohio": (40.38, -82.76),
"Georgia": (33.04, -83.64),
"North Carolina": (35.63, -79.80),
"Michigan": (43.32, -84.53)
}

# --------------------------------------------------
# Route Aggregation
# --------------------------------------------------

routes = df.groupby(["Factory","State/Province"]).agg(
    avg_shipping_days=("Shipping Days","mean"),
    shipments=("Shipping Days","count")
).reset_index()

routes = routes.dropna()

avg_delay = routes["avg_shipping_days"].mean()

# --------------------------------------------------
# 🔥 ROUTE SELECTION (NEW)
# --------------------------------------------------

route_options = routes.apply(
    lambda x: f"{x['Factory']} → {x['State/Province']}", axis=1
)

selected_route = st.selectbox(
    "🎯 Highlight Specific Route (Optional)",
    ["None"] + sorted(route_options.tolist())
)

# --------------------------------------------------
# BUILD MAP WITH ANIMATION
# --------------------------------------------------

fig = go.Figure()

for _, row in routes.iterrows():

    factory = row["Factory"]
    state = row["State/Province"]

    if factory not in factory_coords or state not in state_coords:
        continue

    lat1, lon1 = factory_coords[factory]
    lat2, lon2 = state_coords[state]

    delay = row["avg_shipping_days"]
    volume = row["shipments"]

    route_name = f"{factory} → {state}"

    # 🎯 Highlight logic
    if selected_route != "None" and route_name == selected_route:
        color = "yellow"
        width = 6
        opacity = 1
    else:
        color = "red" if delay > avg_delay else "green"
        width = 1 + (volume / routes["shipments"].max()) * 5
        opacity = 0.5

    # 🎬 Animated dotted flow
    fig.add_trace(go.Scattergeo(
        lon=[lon1, lon2],
        lat=[lat1, lat2],
        mode="lines",
        line=dict(
            width=width,
            color=color,
            dash="dot"   # animation effect
        ),
        opacity=opacity,
        hoverinfo="text",
        text=f"""
🚚 {factory} → {state}
📦 Shipments: {volume}
⏱ Avg Days: {delay:.2f}
"""
    ))

# --------------------------------------------------
# Factory Markers
# --------------------------------------------------

for factory, (lat, lon) in factory_coords.items():
    fig.add_trace(go.Scattergeo(
        lon=[lon],
        lat=[lat],
        mode="markers+text",
        text=[factory],
        textposition="top center",
        marker=dict(size=10, color="blue"),
        name=factory
    ))

# --------------------------------------------------
# Layout
# --------------------------------------------------

fig.update_layout(
    geo=dict(scope="usa"),
    margin=dict(l=0, r=0, t=40, b=0),
    title="🚀 Animated Shipping Network"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# 🔥 TOP ROUTES HIGHLIGHT (NEW)
# --------------------------------------------------

st.markdown("---")
st.subheader("🔥 Top High-Volume Routes")

top_routes = routes.sort_values("shipments", ascending=False).head(5)

for _, row in top_routes.iterrows():

    st.success(f"""
**{row['Factory']} → {row['State/Province']}**

📦 Shipments: {row['shipments']}  
⏱ Avg Days: {row['avg_shipping_days']:.2f}
""")

# --------------------------------------------------
# GOOGLE MAP LINKS
# --------------------------------------------------

def map_link(lat1, lon1, lat2, lon2):
    return f"https://www.google.com/maps/dir/{lat1},{lon1}/{lat2},{lon2}"

st.markdown("---")
st.subheader("🔗 Explore Routes in Google Maps")

for _, row in top_routes.iterrows():

    f = row["Factory"]
    s = row["State/Province"]

    if f in factory_coords and s in state_coords:

        lat1, lon1 = factory_coords[f]
        lat2, lon2 = state_coords[s]

        link = map_link(lat1, lon1, lat2, lon2)

        st.markdown(f"[Open {f} → {s}]({link})")

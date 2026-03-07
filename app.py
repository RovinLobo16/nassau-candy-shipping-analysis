import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Shipping Route Efficiency Dashboard",
    layout="wide"
)

st.title("🚚 Factory-to-Customer Shipping Route Efficiency Analysis")

st.markdown("""
This dashboard analyzes logistics performance using the **Nassau Candy Distributor dataset**.
It identifies delivery delays, route inefficiencies, and regional logistics bottlenecks.
""")

# -----------------------------------
# Load Dataset
# -----------------------------------
df = pd.read_csv("Nassau Candy Distributor.csv")

# -----------------------------------
# Data Cleaning
# -----------------------------------
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)

df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
df["Shipping Days"] = df["Shipping Days"].abs()

# remove unrealistic values
df.loc[df["Shipping Days"] > 30, "Shipping Days"] = 5

# create route
df["Route"] = df["City"] + " → " + df["Region"]

# -----------------------------------
# Sidebar Filters
# -----------------------------------
st.sidebar.header("Dashboard Filters")

date_range = st.sidebar.date_input(
    "Order Date Range",
    [df["Order Date"].min(), df["Order Date"].max()]
)

region_filter = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

state_filter = st.sidebar.multiselect(
    "State",
    df["State/Province"].unique(),
    default=df["State/Province"].unique()
)

shipmode_filter = st.sidebar.multiselect(
    "Ship Mode",
    df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)

delay_threshold = st.sidebar.slider(
    "Delay Threshold (Days)",
    min_value=1,
    max_value=15,
    value=5
)

# apply filters
df = df[
    (df["Order Date"] >= pd.to_datetime(date_range[0])) &
    (df["Order Date"] <= pd.to_datetime(date_range[1])) &
    (df["Region"].isin(region_filter)) &
    (df["State/Province"].isin(state_filter)) &
    (df["Ship Mode"].isin(shipmode_filter))
]

# -----------------------------------
# KPI Metrics
# -----------------------------------
shipping_lead_time = df["Shipping Days"].mean()
avg_lead_time = df.groupby("Route")["Shipping Days"].mean().mean()
route_volume = df.groupby("Route")["Order ID"].count().mean()
delay_frequency = (df["Shipping Days"] > delay_threshold).mean() * 100
route_efficiency = (df["Shipping Days"].mean() / df["Shipping Days"].max()) * 100

st.markdown("---")
st.header("📊 Key Logistics KPIs")

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Shipping Lead Time", round(shipping_lead_time,2))
c2.metric("Average Lead Time", round(avg_lead_time,2))
c3.metric("Route Volume", round(route_volume,2))
c4.metric("Delay Frequency", f"{delay_frequency:.2f}%")
c5.metric("Route Efficiency Score", f"{route_efficiency:.2f}")

# -----------------------------------
# Route Efficiency Overview
# -----------------------------------
st.markdown("---")
st.header("🚦 Route Efficiency Overview")

col1,col2 = st.columns(2)

route_avg = df.groupby("Route")["Shipping Days"].mean().reset_index()

with col1:
    st.subheader("Average Lead Time by Route")
    fig = px.bar(route_avg,x="Route",y="Shipping Days")
    st.plotly_chart(fig,use_container_width=True)

with col2:
    st.subheader("Route Performance Leaderboard")
    route_rank = df.groupby("Route")["Shipping Days"].mean().sort_values().reset_index()
    st.dataframe(route_rank)

# -----------------------------------
# Geographic Shipping Analysis
# -----------------------------------
st.markdown("---")
st.header("🗺 Geographic Shipping Analysis")

col1,col2 = st.columns(2)

state_ship = df.groupby("State/Province")["Shipping Days"].mean().reset_index()

with col1:
    st.subheader("US Shipping Efficiency Heatmap")
    fig = px.choropleth(
        state_ship,
        locations="State/Province",
        locationmode="USA-states",
        color="Shipping Days",
        scope="usa"
    )
    st.plotly_chart(fig,use_container_width=True)

with col2:
    st.subheader("Regional Bottleneck Analysis")
    city_delay = df.groupby("City")["Shipping Days"].mean().sort_values(ascending=False).head(10).reset_index()
    fig = px.bar(city_delay,x="City",y="Shipping Days")
    st.plotly_chart(fig,use_container_width=True)

# -----------------------------------
# Shipping Mode Comparison
# -----------------------------------
st.markdown("---")
st.header("🚚 Shipping Mode Comparison")

ship_mode_perf = df.groupby("Ship Mode")["Shipping Days"].mean().reset_index()

fig = px.bar(ship_mode_perf,x="Ship Mode",y="Shipping Days")
st.plotly_chart(fig,use_container_width=True)

# -----------------------------------
# Route Drill Down
# -----------------------------------
st.markdown("---")
st.header("🔎 Route Drill-Down Analysis")

col1,col2 = st.columns(2)

state_perf = df.groupby("State/Province")["Shipping Days"].mean().reset_index()

with col1:
    st.subheader("State Level Performance")
    fig = px.bar(state_perf,x="State/Province",y="Shipping Days")
    st.plotly_chart(fig,use_container_width=True)

with col2:
    st.subheader("Order Shipment Timeline")
    timeline = df[["Order ID","Order Date","Ship Date","Shipping Days"]].sort_values("Order Date")
    st.dataframe(timeline.head(30))

# -----------------------------------
# Sales Analysis
# -----------------------------------
st.markdown("---")
st.header("💰 Sales Analysis")

region_sales = df.groupby("Region")["Sales"].sum().reset_index()

fig = px.bar(region_sales,x="Region",y="Sales",color="Region")
st.plotly_chart(fig,use_container_width=True)

# -----------------------------------
# Correlation Matrix
# -----------------------------------
st.markdown("---")
st.header("📈 Correlation Analysis")

corr = df[["Sales","Gross Profit","Units","Shipping Days"]].corr()

fig = px.imshow(corr,text_auto=True)
st.plotly_chart(fig,use_container_width=True)

# -----------------------------------
# Factories Coordinates
# -----------------------------------
st.markdown("---")
st.header("🏭 Factories Coordinates")

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

# -----------------------------------
# Products and Factories Correlation
# -----------------------------------
st.markdown("---")
st.header("🍬 Products and Factories Correlation")

product_factory = pd.DataFrame({
"Division":[
"Chocolate","Chocolate","Chocolate","Chocolate","Chocolate",
"Sugar","Sugar","Sugar","Sugar",
"Other","Sugar","Sugar","Other","Other","Other"
],
"Product Name":[
"Wonka Bar – Nutty Crunch Surprise",
"Wonka Bar – Fudge Mallows",
"Wonka Bar – Scrumdiddlyumptious",
"Wonka Bar – Milk Chocolate",
"Wonka Bar – Triple Dazzle Caramel",
"Laffy Taffy",
"SweetTARTS",
"Nerds",
"Fun Dip",
"Fizzy Lifting Drinks",
"Everlasting Gobstopper",
"Hair Toffee",
"Lickable Wallpaper",
"Wonka Gum",
"Kazookles"
],
"Factory":[
"Lot's O' Nuts",
"Lot's O' Nuts",
"Lot's O' Nuts",
"Wicked Choccy's",
"Wicked Choccy's",
"Sugar Shack",
"Sugar Shack",
"Sugar Shack",
"Sugar Shack",
"Sugar Shack",
"Secret Factory",
"The Other Factory",
"Secret Factory",
"Secret Factory",
"The Other Factory"
]
})

st.dataframe(product_factory)

# -----------------------------------
# Insights
# -----------------------------------
st.markdown("---")
st.header("💡 Key Insights")

st.info("""
• Certain regions show higher delivery delays indicating logistics bottlenecks.

• First Class shipping performs significantly faster than Standard Class.

• Some cities consistently experience longer shipping durations.

• Route efficiency analysis helps identify inefficient delivery routes.

• Sales and profit show strong correlation indicating profitable product segments.
""")

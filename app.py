import streamlit as st

st.set_page_config(
    page_title="Shipping Route Efficiency Dashboard",
    layout="wide"
)

st.title("🚚 Factory-to-Customer Shipping Route Efficiency Analysis")

st.markdown("""
### Project Overview

This dashboard analyzes shipping efficiency using the **Nassau Candy Distributor dataset**.

The objective of this project is to:

• Identify inefficient shipping routes  
• Detect logistics bottlenecks  
• Analyze delivery performance across regions  
• Compare shipping modes  
• Improve supply chain efficiency  

Use the sidebar to navigate between analysis pages.
""")

st.header("Dashboard Modules")

st.markdown("""
**1️⃣ Route Efficiency Analysis**

• Average lead time by route  
• Route performance leaderboard  

**2️⃣ Geographic Shipping Analysis**

• US shipping efficiency heatmap  
• Regional bottleneck visualization  

**3️⃣ Product & Factory Insights**

• Factory coordinates  
• Product-factory correlation  

**4️⃣ Logistics Performance**

• Shipping mode comparison  
• State-level performance  
• Order shipment timelines  
""")

st.success("Use the navigation menu on the left to explore the dashboard.")

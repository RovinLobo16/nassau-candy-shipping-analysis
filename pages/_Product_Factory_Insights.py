import streamlit as st
import pandas as pd

st.title("🏭 Product & Factory Insights")

st.subheader("Factories Coordinates")

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

st.subheader("Products and Factories Correlation")

product_factory = pd.DataFrame({
"Division":[
"Chocolate","Chocolate","Chocolate","Chocolate","Chocolate",
"Sugar","Sugar","Sugar","Sugar",
"Other","Sugar","Sugar","Other","Other","Other"
],
"Product":[
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

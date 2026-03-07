import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, apply_filters
from ml_model import train_delay_model

# ----------------------------------------------------
# Page Config
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Delay Prediction",
    layout="wide"
)

st.title("🤖 AI Shipping Delay Prediction")

st.markdown("""
This module uses **Machine Learning (Random Forest)** to predict the risk of shipment delays.

The model learns from historical logistics data and evaluates how factors like:

• Shipping Mode  
• Region  
• Destination State  
• Factory Source  
• Order Size  
• Sales Value  

influence delivery performance.
""")

# ----------------------------------------------------
# Load Data
# ----------------------------------------------------

df = load_data()

# Apply global dashboard filters
df = apply_filters(df)

# ----------------------------------------------------
# Train Model (cached)
# ----------------------------------------------------

@st.cache_resource
def get_model(data):
    return train_delay_model(data)

model, encoders, accuracy = get_model(df)

# ----------------------------------------------------
# Model Performance
# ----------------------------------------------------

st.subheader("Model Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric("Model Accuracy", f"{accuracy:.2%}")

with col2:
    st.metric("Training Records", len(df))

# ----------------------------------------------------
# Feature Importance
# ----------------------------------------------------

st.subheader("Model Feature Importance")

importance = pd.DataFrame({
    "Feature": model.feature_names_in_,
    "Importance": model.feature_importances_
}).sort_values("Importance", ascending=False)

fig = px.bar(
    importance,
    x="Feature",
    y="Importance",
    color="Importance",
    title="Features Driving Shipping Delays"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Prediction Simulator
# ----------------------------------------------------

st.markdown("---")
st.subheader("Shipment Delay Prediction Simulator")

col1, col2 = st.columns(2)

with col1:

    region = st.selectbox(
        "Region",
        sorted(df["Region"].dropna().unique())
    )

    ship = st.selectbox(
        "Shipping Mode",
        sorted(df["Ship Mode"].dropna().unique())
    )

    state = st.selectbox(
        "Destination State",
        sorted(df["State/Province"].dropna().unique())
    )

with col2:

    factory = st.selectbox(
        "Factory Source",
        sorted(df["Factory"].dropna().unique())
    )

    units = st.slider(
        "Units Ordered",
        min_value=1,
        max_value=500,
        value=50
    )

    sales = st.slider(
        "Sales Value ($)",
        min_value=10,
        max_value=10000,
        value=500
    )

# ----------------------------------------------------
# Prepare Prediction Data
# ----------------------------------------------------

input_data = pd.DataFrame({
    "Region":[region],
    "Ship Mode":[ship],
    "State/Province":[state],
    "Factory":[factory],
    "Units":[units],
    "Sales":[sales]
})

for col, encoder in encoders.items():
    input_data[col] = encoder.transform(input_data[col])

# ----------------------------------------------------
# Predict Delay
# ----------------------------------------------------

st.markdown("")

if st.button("Predict Shipment Delay"):

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("Prediction Result")

    if prediction == 1:

        st.error(f"""
⚠ **High Delay Risk**

Predicted delay probability: **{probability:.2%}**
""")

        st.warning("""
Recommended actions:

• Consider faster shipping mode  
• Route from closer factory  
• Reduce shipment size
""")

    else:

        st.success(f"""
✅ **Low Delay Risk**

Predicted delay probability: **{probability:.2%}**
""")

        st.info("""
Shipment is likely to arrive **on time** based on historical patterns.
""")

# ----------------------------------------------------
# Prediction Explanation
# ----------------------------------------------------

st.markdown("---")
st.subheader("How the Model Works")

st.markdown("""
The prediction model uses a **Random Forest classifier** trained on historical shipments.

Key signals used by the model include:

• Shipping mode efficiency  
• Geographic distance patterns  
• Factory distribution network  
• Order size and sales value  
• Regional logistics performance  

The algorithm evaluates these factors to estimate the **probability of delivery delay**.
""")

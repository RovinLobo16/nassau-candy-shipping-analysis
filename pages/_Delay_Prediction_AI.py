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
This module uses **Machine Learning (Random Forest)** to predict shipment delays.
""")

# ----------------------------------------------------
# Load Data (FIXED)
# ----------------------------------------------------

df = load_data()
df = apply_filters(df)

st.write("Dataset shape:", df.shape)

# ----------------------------------------------------
# Train Model
# ----------------------------------------------------

@st.cache_resource
def get_model(data):
    return train_delay_model(data)

try:
    model, encoders, metrics, feature_importance = get_model(df)
except Exception as e:
    st.error(f"Model training failed: {e}")
    st.stop()

# ----------------------------------------------------
# Model Performance
# ----------------------------------------------------

st.subheader("Model Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Accuracy", f"{metrics['accuracy']:.2%}")
col2.metric("Precision", f"{metrics['precision']:.2%}")
col3.metric("Recall", f"{metrics['recall']:.2%}")
col4.metric("F1 Score", f"{metrics['f1_score']:.2%}")

# ----------------------------------------------------
# Feature Importance
# ----------------------------------------------------

st.subheader("Feature Importance")

fig = px.bar(
    feature_importance,
    x="Feature",
    y="Importance",
    color="Importance",
    title="Factors Influencing Shipping Delays"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------
# Prediction Simulator
# ----------------------------------------------------

st.markdown("---")
st.subheader("Shipment Delay Prediction Simulator")

col1, col2 = st.columns(2)

with col1:
    region = st.selectbox("Region", sorted(df["Region"].dropna().unique()))
    ship = st.selectbox("Shipping Mode", sorted(df["Ship Mode"].dropna().unique()))
    state = st.selectbox("Destination State", sorted(df["State/Province"].dropna().unique()))

with col2:
    factory = st.selectbox("Factory", sorted(df["Factory"].dropna().unique()))
    units = st.slider("Units Ordered", 1, 500, 50)
    sales = st.slider("Sales Value ($)", 10, 10000, 500)

# ----------------------------------------------------
# Prepare Input
# ----------------------------------------------------

input_data = pd.DataFrame({
    "Region": [region],
    "Ship Mode": [ship],
    "State/Province": [state],
    "Factory": [factory],
    "Units": [units],
    "Sales": [sales]
})

# SAFE ENCODING
for col, enc in encoders.items():
    try:
        input_data[col] = enc.transform(input_data[col])
    except:
        input_data[col] = 0

# ----------------------------------------------------
# Prediction
# ----------------------------------------------------

if st.button("Predict Shipment Delay"):

    pred = model.predict(input_data)[0]
    prob = model.predict_proba(input_data)[0][1]

    st.subheader("Prediction Result")

    if pred == 1:
        st.error(f"⚠ Shipment likely delayed\n\nProbability: {prob:.2%}")
    else:
        st.success(f"✅ Shipment likely on time\n\nProbability: {prob:.2%}")

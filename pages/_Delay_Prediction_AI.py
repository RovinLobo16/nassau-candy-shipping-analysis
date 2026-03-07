import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from ml_model import train_delay_model

st.title("🤖 AI Shipping Delay Prediction")

df = load_data()

st.subheader("Machine Learning Model Training")

model, encoders, accuracy, importance = train_delay_model(df)

st.metric("Model Accuracy", round(accuracy,3))

st.subheader("Feature Importance")

fig = px.bar(
importance,
x="Feature",
y="Importance",
color="Importance"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Predict Delay for New Shipment")

region = st.selectbox("Region", df["Region"].unique())
ship_mode = st.selectbox("Ship Mode", df["Ship Mode"].unique())
state = st.selectbox("State", df["State/Province"].unique())
factory = st.selectbox("Factory", df["Factory"].dropna().unique())

units = st.slider("Units Ordered",1,500,50)
sales = st.slider("Sales Value",10,10000,500)

input_data = pd.DataFrame({
    "Region":[region],
    "Ship Mode":[ship_mode],
    "State/Province":[state],
    "Factory":[factory],
    "Units":[units],
    "Sales":[sales]
})

for col, encoder in encoders.items():
    input_data[col] = encoder.transform(input_data[col])

prediction = model.predict(input_data)[0]
probability = model.predict_proba(input_data)[0][1]

if st.button("Predict Delay Risk"):

    if prediction == 1:
        st.error(f"⚠ High Delay Risk ({probability:.2%})")
    else:
        st.success(f"✅ Low Delay Risk ({probability:.2%})")

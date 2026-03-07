import streamlit as st
import pandas as pd
from utils import load_data
from ml_model import train_delay_model

df = load_data()

model,encoders,acc = train_delay_model(df)

st.title("🤖 AI Delay Prediction")

st.metric("Model Accuracy",round(acc,3))

region = st.selectbox("Region",df["Region"].unique())
ship = st.selectbox("Ship Mode",df["Ship Mode"].unique())
state = st.selectbox("State",df["State/Province"].unique())
factory = st.selectbox("Factory",df["Factory"].dropna().unique())

units = st.slider("Units",1,500,50)
sales = st.slider("Sales",10,10000,500)

data = pd.DataFrame({
"Region":[region],
"Ship Mode":[ship],
"State/Province":[state],
"Factory":[factory],
"Units":[units],
"Sales":[sales]
})

for col,enc in encoders.items():
    data[col] = enc.transform(data[col])

if st.button("Predict Delay"):

    pred = model.predict(data)[0]

    if pred == 1:
        st.error("⚠ Shipment likely delayed")
    else:
        st.success("✅ Shipment likely on time")

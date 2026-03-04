import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Shipping Route Efficiency Analysis")

df = pd.read_csv("Nassau Candy Distributor.csv")

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)

df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days

st.subheader("Dataset Preview")
st.write(df.head())

st.subheader("Key Metrics")

st.write("Total Sales:", df['Sales'].sum())
st.write("Total Profit:", df['Gross Profit'].sum())
st.write("Average Shipping Days:", round(df['Shipping Days'].mean(),2))

region_analysis = df.groupby('Region').agg({
    'Sales':'sum',
    'Shipping Days':'mean'
}).reset_index()

fig, ax = plt.subplots()

sns.barplot(x='Region', y='Shipping Days', data=region_analysis)

st.pyplot(fig)

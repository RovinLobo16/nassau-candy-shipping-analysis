import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils import load_data

df = load_data()

st.title("📊 Correlation Matrix")

cols = ["Sales","Units","Cost","Gross Profit","Shipping Days"]

corr = df[cols].corr()

fig,ax = plt.subplots()

sns.heatmap(corr,annot=True,cmap="coolwarm",ax=ax)

st.pyplot(fig)

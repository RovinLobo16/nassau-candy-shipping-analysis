import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from utils import load_data, apply_filters

# Page configuration
st.set_page_config(page_title="Correlation Analysis", layout="wide")

st.title("📊 Correlation Analysis Dashboard")

st.markdown("""
This section explores relationships between key business variables such as:

• Sales  
• Units Sold  
• Cost  
• Profit  
• Shipping Time  

Understanding these correlations helps identify **drivers of logistics performance and profitability**.
""")

# Load data
df = load_data()

# Apply global dashboard filters
df = apply_filters(df)

st.markdown("### Dataset Size After Filtering")
st.info(f"Records: **{len(df)} shipments**")

# -----------------------------
# Select numeric variables dynamically
# -----------------------------

numeric_cols = df.select_dtypes(include=['int64','float64']).columns.tolist()

# Remove unwanted numeric columns
exclude_cols = ["Row ID"]
numeric_cols = [col for col in numeric_cols if col not in exclude_cols]

selected_cols = st.multiselect(
    "Select Variables for Correlation Analysis",
    numeric_cols,
    default=["Sales","Units","Cost","Gross Profit","Shipping Days"]
)

if len(selected_cols) < 2:
    st.warning("Please select at least two variables.")
    st.stop()

# -----------------------------
# Correlation Calculation
# -----------------------------

corr = df[selected_cols].corr()

# -----------------------------
# Visualization Layout
# -----------------------------

col1, col2 = st.columns([2,1])

with col1:

    st.subheader("Correlation Heatmap")

    fig, ax = plt.subplots(figsize=(8,6))

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        linewidths=0.5,
        fmt=".2f",
        square=True,
        ax=ax
    )

    st.pyplot(fig)

with col2:

    st.subheader("Correlation Insights")

    strongest = corr.unstack().sort_values(ascending=False)

    strongest = strongest[strongest != 1].drop_duplicates()

    top_corr = strongest.head(5)

    for pair, value in top_corr.items():
        st.write(f"**{pair[0]} ↔ {pair[1]}** : {value:.2f}")

# -----------------------------
# Optional Scatter Relationship
# -----------------------------

st.markdown("---")
st.subheader("Relationship Explorer")

x_var = st.selectbox("X Variable", selected_cols)
y_var = st.selectbox("Y Variable", selected_cols, index=1)

fig2, ax2 = plt.subplots()

sns.scatterplot(data=df, x=x_var, y=y_var)

ax2.set_title(f"{x_var} vs {y_var}")

st.pyplot(fig2)

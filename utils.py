import pandas as pd
import streamlit as st


# --------------------------------------------------
# Load and Prepare Dataset
# --------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("Nassau Candy Distributor.csv")

    # -------------------------------
    # Date Cleaning
    # -------------------------------
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    df = df.dropna(subset=["Order Date", "Ship Date"])

    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    # Remove invalid shipping times
    df = df[df["Shipping Days"] >= 0]

    # -------------------------------
    # NUMERIC CLEANING (CRITICAL FIX)
    # -------------------------------
    for col in ["Units", "Sales"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # -------------------------------
    # Factory Mapping
    # -------------------------------
    factory_map = {

        "Wonka Bar – Nutty Crunch Surprise": "Lot's O' Nuts",
        "Wonka Bar – Fudge Mallows": "Lot's O' Nuts",
        "Wonka Bar – Scrumdiddlyumptious": "Lot's O' Nuts",

        "Wonka Bar – Milk Chocolate": "Wicked Choccy's",
        "Wonka Bar – Triple Dazzle Caramel": "Wicked Choccy's",

        "Laffy Taffy": "Sugar Shack",
        "SweetTARTS": "Sugar Shack",
        "Nerds": "Sugar Shack",
        "Fun Dip": "Sugar Shack",
        "Fizzy Lifting Drinks": "Sugar Shack",

        "Everlasting Gobstopper": "Secret Factory",
        "Lickable Wallpaper": "Secret Factory",
        "Wonka Gum": "Secret Factory",

        "Hair Toffee": "The Other Factory",
        "Kazookles": "The Other Factory"
    }

    df["Factory"] = df["Product Name"].map(factory_map)

    # -------------------------------
    # HANDLE MISSING FACTORIES
    # -------------------------------
    df["Factory"] = df["Factory"].fillna("Unknown Factory")

    # -------------------------------
    # ROUTE CREATION (SAFE)
    # -------------------------------
    df["Route"] = (
        df["Factory"].astype(str) +
        " → " +
        df["State/Province"].astype(str)
    )

    # -------------------------------
    # FINAL CLEAN (IMPORTANT)
    # -------------------------------
    df = df.dropna(subset=["Units", "Sales", "Shipping Days"])

    return df


# --------------------------------------------------
# Dashboard Filters
# --------------------------------------------------

def apply_filters(df):

    st.sidebar.header("🔎 Dashboard Filters")

    # -------------------------------
    # DATE FILTER
    # -------------------------------
    start_date = st.sidebar.date_input(
        "Start Date",
        value=df["Order Date"].min()
    )

    end_date = st.sidebar.date_input(
        "End Date",
        value=df["Order Date"].max()
    )

    # -------------------------------
    # REGION FILTER
    # -------------------------------
    region_options = sorted(df["Region"].dropna().unique())

    region = st.sidebar.multiselect(
        "Region",
        options=region_options,
        default=region_options
    )

    # -------------------------------
    # SHIP MODE FILTER
    # -------------------------------
    ship_options = sorted(df["Ship Mode"].dropna().unique())

    ship_mode = st.sidebar.multiselect(
        "Ship Mode",
        options=ship_options,
        default=ship_options
    )

    # -------------------------------
    # PRODUCT FILTER
    # -------------------------------
    product_options = sorted(df["Product Name"].dropna().unique())

    product = st.sidebar.multiselect(
        "Product",
        options=product_options,
        default=product_options
    )

    # -------------------------------
    # APPLY FILTERS
    # -------------------------------
    filtered_df = df[
        (df["Order Date"] >= pd.to_datetime(start_date)) &
        (df["Order Date"] <= pd.to_datetime(end_date)) &
        (df["Region"].isin(region)) &
        (df["Ship Mode"].isin(ship_mode)) &
        (df["Product Name"].isin(product))
    ]

    # -------------------------------
    # SHOW RECORD COUNT
    # -------------------------------
    st.sidebar.markdown("---")
    st.sidebar.write(f"📊 **Filtered Records:** {len(filtered_df)}")

    return filtered_df

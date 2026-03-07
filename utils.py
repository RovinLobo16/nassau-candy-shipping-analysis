import pandas as pd
import streamlit as st

def load_data():

    df = pd.read_csv("Nassau Candy Distributor.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    df = df.dropna(subset=["Order Date","Ship Date"])

    df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

    df = df[df["Shipping Days"] >= 0]

    factory_map = {

        "Wonka Bar – Nutty Crunch Surprise":"Lot's O' Nuts",
        "Wonka Bar – Fudge Mallows":"Lot's O' Nuts",
        "Wonka Bar – Scrumdiddlyumptious":"Lot's O' Nuts",

        "Wonka Bar – Milk Chocolate":"Wicked Choccy's",
        "Wonka Bar – Triple Dazzle Caramel":"Wicked Choccy's",

        "Laffy Taffy":"Sugar Shack",
        "SweetTARTS":"Sugar Shack",
        "Nerds":"Sugar Shack",
        "Fun Dip":"Sugar Shack",
        "Fizzy Lifting Drinks":"Sugar Shack",

        "Everlasting Gobstopper":"Secret Factory",
        "Lickable Wallpaper":"Secret Factory",
        "Wonka Gum":"Secret Factory",

        "Hair Toffee":"The Other Factory",
        "Kazookles":"The Other Factory"
    }

    df["Factory"] = df["Product Name"].map(factory_map)

    df["Route"] = df["Factory"] + " → " + df["State/Province"]

    return df


def apply_filters(df):

    st.sidebar.header("🔎 Dashboard Filters")

    start = st.sidebar.date_input(
        "Start Date",
        df["Order Date"].min()
    )

    end = st.sidebar.date_input(
        "End Date",
        df["Order Date"].max()
    )

    region = st.sidebar.multiselect(
        "Region",
        df["Region"].unique(),
        default=df["Region"].unique()
    )

    ship = st.sidebar.multiselect(
        "Ship Mode",
        df["Ship Mode"].unique(),
        default=df["Ship Mode"].unique()
    )

    df = df[
        (df["Order Date"] >= pd.to_datetime(start)) &
        (df["Order Date"] <= pd.to_datetime(end)) &
        (df["Region"].isin(region)) &
        (df["Ship Mode"].isin(ship))
    ]

    return df

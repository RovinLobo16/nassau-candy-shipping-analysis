import pandas as pd

def load_data():

    df = pd.read_csv("Nassau Candy Distributor.csv")

    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")

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
    "Hair Toffee":"The Other Factory",
    "Lickable Wallpaper":"Secret Factory",
    "Wonka Gum":"Secret Factory",
    "Kazookles":"The Other Factory"
    }

    df["Factory"] = df["Product Name"].map(factory_map)

    df["Route"] = df["Factory"] + " → " + df["State/Province"]

    return df

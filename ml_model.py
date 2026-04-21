import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def train_delay_model(df):

    def load_data():
    return pd.read_csv("Nassau Candy Distributor.csv")

    # -------------------------------
    # Clean Data (CRITICAL FIX)
    # -------------------------------
    data = data.dropna(subset=[
        "Region",
        "Ship Mode",
        "State/Province",
        "Factory",
        "Units",
        "Sales",
        "Shipping Days"
    ])

    # -------------------------------
    # Target Variable
    # -------------------------------
    threshold = data["Shipping Days"].median()
    data["Delayed"] = (data["Shipping Days"] > threshold).astype(int)

    # -------------------------------
    # Features
    # -------------------------------
    features = [
        "Region",
        "Ship Mode",
        "State/Province",
        "Factory",
        "Units",
        "Sales"
    ]

    X = data[features].copy()
    y = data["Delayed"]

    # Extra safety
    X = X.fillna("Unknown")

    # -------------------------------
    # Encoding
    # -------------------------------
    encoders = {}

    for col in X.columns:
        if X[col].dtype == "object":
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le

    # -------------------------------
    # Train/Test Split
    # -------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # -------------------------------
    # Model
    # -------------------------------
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # -------------------------------
    # Metrics
    # -------------------------------
    preds = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1_score": f1_score(y_test, preds)
    }

    # -------------------------------
    # Feature Importance
    # -------------------------------
    feature_importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False)

    return model, encoders, metrics, feature_importance

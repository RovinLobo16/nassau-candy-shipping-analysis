import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def train_delay_model(df):

    # -------------------------------
    # COPY DATA
    # -------------------------------
    data = df.copy()

    # -------------------------------
    # SAFETY CHECK
    # -------------------------------
    if data.empty:
        raise ValueError("Dataset is empty")

    # -------------------------------
    # REQUIRED COLUMNS
    # -------------------------------
    cols = [
        "Region",
        "Ship Mode",
        "State/Province",
        "Factory",
        "Units",
        "Sales",
        "Shipping Days"
    ]

    data = data[cols].copy()

    # -------------------------------
    # CLEAN DATA
    # -------------------------------
    data = data.replace([np.inf, -np.inf], np.nan)

    # Categorical
    cat_cols = ["Region", "Ship Mode", "State/Province", "Factory"]
    for col in cat_cols:
        data[col] = data[col].astype(str).fillna("Unknown")

    # Numeric
    data["Units"] = pd.to_numeric(data["Units"], errors="coerce")
    data["Sales"] = pd.to_numeric(data["Sales"], errors="coerce")
    data["Shipping Days"] = pd.to_numeric(data["Shipping Days"], errors="coerce")

    # Drop invalid rows
    data = data.dropna()

    # -------------------------------
    # CHECK DATA SIZE
    # -------------------------------
    if len(data) < 50:
        raise ValueError("Not enough data to train model")

    # -------------------------------
    # TARGET VARIABLE
    # -------------------------------
    threshold = data["Shipping Days"].median()
    data["Delayed"] = (data["Shipping Days"] > threshold).astype(int)

    if data["Delayed"].nunique() < 2:
        raise ValueError("Target has only one class")

    # -------------------------------
    # FEATURES
    # -------------------------------
    X = data.drop(columns=["Shipping Days", "Delayed"])
    y = data["Delayed"]

    # -------------------------------
    # ENCODING
    # -------------------------------
    encoders = {}

    for col in X.columns:
        if X[col].dtype == "object":
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            encoders[col] = le

    # -------------------------------
    # TRAIN TEST SPLIT
    # -------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # -------------------------------
    # MODEL
    # -------------------------------
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # -------------------------------
    # METRICS
    # -------------------------------
    preds = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds),
        "recall": recall_score(y_test, preds),
        "f1_score": f1_score(y_test, preds)
    }

    # -------------------------------
    # FEATURE IMPORTANCE
    # -------------------------------
    feature_importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False)

    return model, encoders, metrics, feature_importance

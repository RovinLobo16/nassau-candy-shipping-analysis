import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def train_delay_model(df):

    data = df.copy()

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
    # FORCE NUMERIC CLEANING
    # -------------------------------
    for col in ["Units", "Sales", "Shipping Days"]:
        data[col] = pd.to_numeric(data[col], errors="coerce")

    # -------------------------------
    # DROP INVALID ROWS
    # -------------------------------
    data = data.dropna()

    # -------------------------------
    # TARGET VARIABLE
    # -------------------------------
    threshold = data["Shipping Days"].median()
    data["Delayed"] = (data["Shipping Days"] > threshold).astype(int)

    # -------------------------------
    # FEATURES
    # -------------------------------
    X = data.drop(columns=["Shipping Days", "Delayed"])
    y = data["Delayed"]

    # -------------------------------
    # ENCODE CATEGORICAL
    # -------------------------------
    encoders = {}

    for col in X.columns:
        if X[col].dtype == "object":
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le

    # -------------------------------
    # TRAIN / TEST SPLIT
    # -------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    # -------------------------------
    # MODEL
    # -------------------------------
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    # -------------------------------
    # METRICS
    # -------------------------------
    preds = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, preds),
        "precision": precision_score(y_test, preds, zero_division=0),
        "recall": recall_score(y_test, preds, zero_division=0),
        "f1_score": f1_score(y_test, preds, zero_division=0)
    }

    # -------------------------------
    # FEATURE IMPORTANCE
    # -------------------------------
    feature_importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False)

    return model, encoders, metrics, feature_importance

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


def train_delay_model(df):

    # --------------------------------------------------
    # Copy data to avoid modifying original dataframe
    # --------------------------------------------------

    data = df.copy()

    # --------------------------------------------------
    # Create Delay Target Variable
    # --------------------------------------------------

    threshold = data["Shipping Days"].median()

    data["Delayed"] = (data["Shipping Days"] > threshold).astype(int)

    # --------------------------------------------------
    # Select Features
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Encode Categorical Variables
    # --------------------------------------------------

    encoders = {}

    for col in X.columns:

        if X[col].dtype == "object":

            le = LabelEncoder()

            X[col] = le.fit_transform(X[col].astype(str))

            encoders[col] = le

    # --------------------------------------------------
    # Train Test Split (Stratified)
    # --------------------------------------------------

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # --------------------------------------------------
    # Train Random Forest Model
    # --------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=5,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # --------------------------------------------------
    # Model Evaluation
    # --------------------------------------------------

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(y_test, predictions)

    recall = recall_score(y_test, predictions)

    f1 = f1_score(y_test, predictions)

    # --------------------------------------------------
    # Feature Importance
    # --------------------------------------------------

    feature_importance = pd.DataFrame({
        "Feature": X.columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False)

    # --------------------------------------------------
    # Return Everything Needed for Dashboard
    # --------------------------------------------------

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1
    }

    return model, encoders, metrics, feature_importance

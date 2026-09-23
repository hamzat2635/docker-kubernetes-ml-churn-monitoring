# Telco Customer Churn - model training

import joblib
import pandas as pd

from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# Load the dataset
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

# TotalCharges contains some empty values, so convert it to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# New customers with tenure 0 have no previous TotalCharges
df.loc[
    (df["TotalCharges"].isnull()) & (df["tenure"] == 0),
    "TotalCharges"
] = 0


# Features used by the final model
features = [
    "tenure",
    "InternetService",
    "Contract",
    "MonthlyCharges",
    "TotalCharges",
    "TechSupport",
    "OnlineSecurity",
    "PaperlessBilling",
    "PaymentMethod"
]

X = df[features]
y = df["Churn"].map({"No": 0, "Yes": 1})


# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


numeric_features = [
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

categorical_features = [
    "InternetService",
    "Contract",
    "TechSupport",
    "OnlineSecurity",
    "PaperlessBilling",
    "PaymentMethod"
]


# Fill missing numeric values and scale them
numeric_steps = Pipeline(
    steps=[
        ("missing", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ]
)

# Fill missing text values and convert categories to numbers
categorical_steps = Pipeline(
    steps=[
        ("missing", SimpleImputer(strategy="most_frequent")),
        ("encode", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_steps, numeric_features),
        ("cat", categorical_steps, categorical_features)
    ]
)


# Logistic Regression
logistic_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)

logistic_model.fit(X_train, y_train)

logistic_predictions = logistic_model.predict(X_test)
logistic_probabilities = logistic_model.predict_proba(X_test)[:, 1]

logistic_metrics = {
    "accuracy": accuracy_score(y_test, logistic_predictions),
    "precision": precision_score(y_test, logistic_predictions),
    "recall": recall_score(y_test, logistic_predictions),
    "f1": f1_score(y_test, logistic_predictions),
    "roc_auc": roc_auc_score(y_test, logistic_probabilities)
}

print("\nLogistic Regression")
for metric, value in logistic_metrics.items():
    print(metric, round(value, 4))


# Random Forest
random_forest_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestClassifier(
                n_estimators=300,
                class_weight="balanced",
                random_state=42
            )
        )
    ]
)

random_forest_model.fit(X_train, y_train)

forest_predictions = random_forest_model.predict(X_test)
forest_probabilities = random_forest_model.predict_proba(X_test)[:, 1]

forest_metrics = {
    "accuracy": accuracy_score(y_test, forest_predictions),
    "precision": precision_score(y_test, forest_predictions),
    "recall": recall_score(y_test, forest_predictions),
    "f1": f1_score(y_test, forest_predictions),
    "roc_auc": roc_auc_score(y_test, forest_probabilities)
}

print("\nRandom Forest")
for metric, value in forest_metrics.items():
    print(metric, round(value, 4))


# Logistic Regression is used in the application because it gave
# better recall, F1 score and ROC AUC in this experiment.
model_data = {
    "pipeline": logistic_model,
    "features": features,
    "model_name": "Logistic Regression",
    "model_version": "1.0",
    "metrics": logistic_metrics
}

# Save one copy for training results and one copy for the inference service
Path("model").mkdir(exist_ok=True)
Path("inference-service/model").mkdir(parents=True, exist_ok=True)

joblib.dump(model_data, "model/logistic_regression.joblib")
joblib.dump(
    model_data,
    "inference-service/model/logistic_regression.joblib"
)

print("\nSaved Logistic Regression model.")

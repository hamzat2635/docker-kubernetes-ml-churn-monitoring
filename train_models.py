# =========================================
# TELCO CUSTOMER CHURN - MODEL TRAINING
# =========================================

# Import pandas
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression


from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)


# Load the dataset
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")


# Check if the dataset loaded correctly
print("Dataset loaded successfully")

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

# Check TotalCharges data type
print("\nTotalCharges data type before cleaning:")
print(df["TotalCharges"].dtype)


# Convert TotalCharges to numbers
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)


# Check missing values created after conversion
print("\nMissing TotalCharges values:")
print(df["TotalCharges"].isnull().sum())


# Customers with tenure 0 have no previous TotalCharges
df.loc[
    (df["TotalCharges"].isnull()) &
    (df["tenure"] == 0),
    "TotalCharges"
] = 0


# Check again
print("\nMissing TotalCharges after fixing:")
print(df["TotalCharges"].isnull().sum())

# =========================
# Prepare data for training
# =========================

# X contains the information we use to make predictions
# We remove customerID because it is only an ID
# We also remove Churn because that is what we want to predict

X = df.drop(
    columns=[
        "customerID",
        "Churn"
    ]
)


# y is the value we want to predict
# Convert No and Yes into 0 and 1

y = df["Churn"].map(
    {
        "No": 0,
        "Yes": 1
    }
)


# Check the result

print("\nFeatures shape:")
print(X.shape)

print("\nTarget shape:")
print(y.shape)

print("\nChurn values:")
print(y.value_counts())

# =========================
# Split data into train and test
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# Check the split

print("\nTraining features:")
print(X_train.shape)

print("\nTesting features:")
print(X_test.shape)

print("\nTraining target:")
print(y_train.shape)

print("\nTesting target:")
print(y_test.shape)

# =========================
# Find categorical and numerical columns
# =========================

categorical_columns = X.select_dtypes(
    include=["object", "string"]
).columns

numeric_columns = X.select_dtypes(
    include=["number"]
).columns


print("\nCategorical columns:")
print(categorical_columns)

print("\nNumerical columns:")
print(numeric_columns)

# =========================
# Create the preprocessor
# =========================

preprocessor = ColumnTransformer(
    transformers=[
        
        # Convert text columns into numbers
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_columns
        ),

        # Scale numerical columns
        (
            "num",
            StandardScaler(),
            numeric_columns
        )
    ]
)


print("\nPreprocessor created successfully")

# =========================
# Logistic Regression Model
# =========================

logistic_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", LogisticRegression(max_iter=1000))
    ]
)


# Train the model
logistic_model.fit(
    X_train,
    y_train
)

print("\nLogistic Regression training complete")


# Make predictions
logistic_predictions = logistic_model.predict(
    X_test
)


# Calculate accuracy
logistic_accuracy = accuracy_score(
    y_test,
    logistic_predictions
)


print("\nLogistic Regression Accuracy:")
print(logistic_accuracy * 100)


# Confusion matrix
print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        logistic_predictions
    )
)


# Classification report
print("\nClassification Report:")
print(
    classification_report(
        y_test,
        logistic_predictions,
        target_names=[
            "Stay",
            "Churn"
        ]
    )
)

# =========================
# Random Forest Model
# =========================

random_forest_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestClassifier(
                n_estimators=100,
                random_state=42
            )
        )
    ]
)


# Train the model
random_forest_model.fit(
    X_train,
    y_train
)

print("\nRandom Forest training complete")


# Make predictions
random_forest_predictions = random_forest_model.predict(
    X_test
)


# Calculate accuracy
random_forest_accuracy = accuracy_score(
    y_test,
    random_forest_predictions
)


print("\nRandom Forest Accuracy:")
print(random_forest_accuracy * 100)


# Confusion matrix
print("\nRandom Forest Confusion Matrix:")
print(
    confusion_matrix(
        y_test,
        random_forest_predictions
    )
)


# Classification report
print("\nRandom Forest Classification Report:")
print(
    classification_report(
        y_test,
        random_forest_predictions,
        target_names=[
            "Stay",
            "Churn"
        ]
    )
)
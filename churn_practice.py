# =========================================================
# TELCO CUSTOMER CHURN - MACHINE LEARNING PRACTICE PROJECT
# =========================================================


# =========================
# 1. Import Libraries
# =========================

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)


# =========================
# 2. Load Dataset
# =========================

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")


# =========================
# 3. Initial Dataset Inspection
# =========================

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nDataset information:")
df.info()


# =========================
# 4. Investigate TotalCharges
# =========================

print("\nEmpty TotalCharges:")

print(
    df[df["TotalCharges"].str.strip() == ""]
)

empty_total = df[
    df["TotalCharges"].str.strip() == ""
]

print(
    empty_total[
        [
            "customerID",
            "tenure",
            "MonthlyCharges",
            "TotalCharges",
            "Churn"
        ]
    ]
)


# =========================
# 5. Convert TotalCharges to Numeric
# =========================

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print("\nTotalCharges data type:")
print(df["TotalCharges"].dtype)

print("\nMissing TotalCharges before fix:")
print(df["TotalCharges"].isnull().sum())


# =========================
# 6. Fix Missing TotalCharges
# =========================

# Customers with tenure = 0 have not accumulated
# historical TotalCharges yet.

df.loc[
    (df["TotalCharges"].isnull()) &
    (df["tenure"] == 0),
    "TotalCharges"
] = 0

print(
    "\nMissing TotalCharges after fix:",
    df["TotalCharges"].isnull().sum()
)


# =========================
# 7. Analyze Target Variable: Churn
# =========================

print("\nChurn counts:")
print(df["Churn"].value_counts())

print("\nChurn percentages:")
print(
    df["Churn"].value_counts(
        normalize=True
    ) * 100
)

print("\nUnique Churn values:")
print(df["Churn"].unique())


# =========================================================
# EXPLORATORY DATA ANALYSIS (EDA)
# =========================================================


# =========================
# 8. Contract vs Churn
# =========================

print("\nContract types:")
print(df["Contract"].value_counts())

print("\nContract vs Churn:")
print(
    pd.crosstab(
        df["Contract"],
        df["Churn"]
    )
)

contract_churn = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print("\nContract churn percentages:")
print(contract_churn)


# Contract Churn Visualization

contract_churn["Yes"].plot(
    kind="bar"
)

plt.title(
    "Churn Rate by Contract Type"
)

plt.xlabel(
    "Contract Type"
)

plt.ylabel(
    "Churn Percentage"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()

plt.show()


# =========================
# 9. Tenure vs Churn
# =========================

print("\nTenure statistics by Churn:")

print(
    df.groupby(
        "Churn"
    )["tenure"].agg(
        [
            "count",
            "mean",
            "median",
            "min",
            "max"
        ]
    )
)


# =========================
# 10. Create Tenure Groups
# =========================

df["tenure_group"] = pd.cut(
    df["tenure"],

    bins=[
        -1,
        12,
        24,
        36,
        48,
        60,
        72
    ],

    labels=[
        "0-12",
        "13-24",
        "25-36",
        "37-48",
        "49-60",
        "61-72"
    ]
)


# =========================
# 11. Tenure Group vs Churn
# =========================

tenure_churn = pd.crosstab(
    df["tenure_group"],
    df["Churn"],
    normalize="index"
) * 100

print(
    "\nChurn percentage by tenure group:"
)

print(tenure_churn)


# Tenure Visualization

tenure_churn["Yes"].plot(
    kind="bar"
)

plt.title(
    "Churn Rate by Customer Tenure"
)

plt.xlabel(
    "Tenure (Months)"
)

plt.ylabel(
    "Churn Percentage"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.show()


# =========================
# 12. Monthly Charges vs Churn
# =========================

print(
    "\nMonthly Charges statistics by Churn:"
)

print(
    df.groupby(
        "Churn"
    )["MonthlyCharges"].agg(
        [
            "count",
            "mean",
            "median",
            "min",
            "max"
        ]
    )
)


# Monthly Charges Boxplot

df.boxplot(
    column="MonthlyCharges",
    by="Churn"
)

plt.title(
    "Monthly Charges by Churn"
)

plt.suptitle("")

plt.xlabel(
    "Churn"
)

plt.ylabel(
    "Monthly Charges"
)

plt.tight_layout()

plt.show()


# =========================
# 13. Check Duplicate Rows
# =========================

print("\nDuplicate rows:")
print(df.duplicated().sum())


# =========================
# 14. Check Missing Values
# =========================

print("\nMissing values by column:")
print(df.isnull().sum())


# =========================================================
# MACHINE LEARNING PREPARATION
# =========================================================


# =========================
# 15. Create Features (X)
#    and Target (y)
# =========================

X = df.drop(
    columns=[
        "Churn",
        "customerID",
        "tenure_group"
    ]
)


# Convert:
#
# No  -> 0
# Yes -> 1

y = df["Churn"].map(
    {
        "No": 0,
        "Yes": 1
    }
)


print("\nFeatures shape:")
print(X.shape)

print("\nTarget shape:")
print(y.shape)

print("\nTarget values:")
print(y.value_counts())


# =========================
# 16. Train / Test Split
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining data:")
print(X_train.shape)

print("\nTraining target:")
print(y_train.value_counts())


print("\nTesting data:")
print(X_test.shape)

print("\nTesting target:")
print(y_test.value_counts())


# =========================
# 17. Find Categorical and
#     Numerical Columns
# =========================

categorical_columns = X.select_dtypes(
    include=[
        "object",
        "string"
    ]
).columns


numeric_columns = X.select_dtypes(
    include=[
        "number"
    ]
).columns


print("\nCategorical columns:")
print(categorical_columns)

print("\nNumeric columns:")
print(numeric_columns)


# =========================
# 18. Create Preprocessor
# =========================

preprocessor = ColumnTransformer(
    transformers=[

        # Convert text categories
        # into numerical columns

        (
            "cat",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_columns
        ),

        # Scale numerical variables

        (
            "num",
            StandardScaler(),
            numeric_columns
        )
    ]
)


# =========================
# 19. Apply Preprocessing
# =========================

# Learn preprocessing rules
# from TRAINING data only

X_train_ready = preprocessor.fit_transform(
    X_train
)


# Apply the SAME learned rules
# to testing data

X_test_ready = preprocessor.transform(
    X_test
)


print("\nOriginal training shape:")
print(X_train.shape)

print("\nProcessed training shape:")
print(X_train_ready.shape)

print("\nProcessed testing shape:")
print(X_test_ready.shape)


# =========================================================
# FIRST MACHINE LEARNING MODEL
# =========================================================


# =========================
# 20. Logistic Regression
# =========================

model = LogisticRegression(
    max_iter=1000
)


# Train the model

model.fit(
    X_train_ready,
    y_train
)


print(
    "\nModel training complete."
)


# =========================
# 21. Make Predictions
# =========================

y_pred = model.predict(
    X_test_ready
)


# =========================
# 22. Model Accuracy
# =========================

accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\nAccuracy:")
print(accuracy)


print("\nAccuracy percentage:")
print(accuracy * 100)


# =========================
# 23. Baseline Accuracy
# =========================

# This represents a very simple
# model that always predicts
# the majority class.

baseline_accuracy = (
    y_test
    .value_counts(
        normalize=True
    )
    .max()
)


print("\nBaseline Accuracy:")
print(
    baseline_accuracy * 100
)


# =========================
# 24. Confusion Matrix
# =========================

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# =========================
# 25. Classification Report
# =========================

print(
    "\nClassification Report:"
)

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Stay",
            "Churn"
        ]
    )
)
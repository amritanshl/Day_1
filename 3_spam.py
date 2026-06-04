import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# ==========================================
# STEP 1: GENERATE ENTERPRISE-SCALE DIRTY DATA
# ==========================================
print("=== Step 1: Generating Mock Real-World Dirty Dataset ===")

raw_data = {
    "Employee_ID": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    "Age": [28.0, 34.0, np.nan, 45.0, 52.0, np.nan, 23.0, 39.0, 41.0, 30.0],
    "Annual_Salary": [
        55000.0,
        82000.0,
        61000.0,
        np.nan,
        140000.0,
        95000.0,
        np.nan,
        112000.0,
        88000.0,
        71000.0,
    ],
    "Department": [
        "Engineering",
        "HR",
        "Engineering",
        "Marketing",
        "Executive",
        "Engineering",
        "HR",
        np.nan,
        "Marketing",
        "Engineering",
    ],
    "Remote_Status": [
        "Remote",
        "Hybrid",
        "Onsite",
        "Remote",
        "Onsite",
        "Remote",
        np.nan,
        "Hybrid",
        "Remote",
        "Onsite",
    ],
    "Performance_Rating": [
        "High",
        "Medium",
        "Low",
        "Medium",
        "High",
        "High",
        "Low",
        "Medium",
        "Medium",
        "High",
    ],  # Target Variable
}

df = pd.DataFrame(raw_data)
print("\n--- Raw Input Dataframe ---")
print(df)
print("\n--- Missing Value Count Per Column ---")
print(df.isnull().sum())

# ==========================================
# STEP 2: DATA ARCHITECTURE SEPARATION
# ==========================================
print("\n=== Step 2: Slicing Features and Targets ===")

# Drop unique identifier keys that carry zero statistical weight
X = df.drop(columns=["Employee_ID", "Performance_Rating"])
y = df["Performance_Rating"]

# Programmatically segment feature types to build specialized pathways
numerical_features = ["Age", "Annual_Salary"]
categorical_features = ["Department", "Remote_Status"]

print(f"Numerical Features Pipeline Scope: {numerical_features}")
print(f"Categorical Features Pipeline Scope: {categorical_features}")

# Split data into Training and Test partitions using Stratified logic
# This prevents data leakage during the transformations
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ==========================================
# STEP 3: CONSTRUCT ENCAPSULATED PIPELINES
# ==========================================
print("\n=== Step 3: Configuring Preprocessing Transformers ===")

# Numerical Processing Sub-Engine: Handle missing entries then Standardize ranges
numerical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),  # Robust against potential salary outliers
        ("scaler", StandardScaler()),  # Centers distribution around mean=0, std=1
    ]
)

# Categorical Processing Sub-Engine: Impute missing flags then cross-encode vectors
categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),  # Fills missing values with Mode
        (
            "onehot",
            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
        ),  # Prevents crash on unseen validation categories
    ]
)

# Consolidate processing engines into a singular, comprehensive master executor
preprocessor = ColumnTransformer(
    transformers=[
        ("num_transform", numerical_pipeline, numerical_features),
        ("cat_transform", categorical_pipeline, categorical_features),
    ]
)

# ==========================================
# STEP 4: EXECUTE TRANSFORMATIONS EXCLUSIVELY
# ==========================================
print("\n=== Step 4: Executing Pipeline Pipeline Execution ===")

# Fit parameters ONLY on training set data to eliminate pipeline leakage
X_train_processed = preprocessor.fit_transform(X_train)

# Transform validation/test dataset using the historical calculations derived above
X_test_processed = preprocessor.transform(X_test)

# ==========================================
# STEP 5: OUTPUT EXTRACTION & ANALYSIS
# ==========================================
print("\n=== Step 5: Post-Execution Inspection ===")

# Extract structural columns created dynamically via One-Hot encoding array configurations
encoded_categorical_columns = (
    preprocessor.named_transformers_["cat_transform"]
    .named_steps["onehot"]
    .get_feature_names_out(categorical_features)
    .tolist()
)

all_engineered_features = numerical_features + encoded_categorical_columns

# Construct readable, production analytics DataFrames
X_train_processed_df = pd.DataFrame(
    X_train_processed, columns=all_engineered_features
)
X_test_processed_df = pd.DataFrame(
    X_test_processed, columns=all_engineered_features
)

print(
    f"\nProcessed Shape (Rows, Scaled Columns): {X_train_processed_df.shape}"
)
print("\n--- Final Cleaned & Transformed Training Array Framework ---")
print(X_train_processed_df.round(4))
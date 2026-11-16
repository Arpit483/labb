# IMPORTANT: RUN THIS CELL IN ORDER TO IMPORT YOUR KAGGLE DATA SOURCES,
# THEN FEEL FREE TO DELETE THIS CELL.
# NOTE: THIS NOTEBOOK ENVIRONMENT DIFFERS FROM KAGGLE'S PYTHON
# ENVIRONMENT SO THERE MAY BE MISSING LIBRARIES USED BY YOUR NOTEBOOK.
import os
import kagglehub
try:
    balaka18_email_spam_classification_dataset_csv_path = kagglehub.dataset_download('balaka18/email-spam-classification-dataset-csv')
    balaka18_email_spam_classification_path = kagglehub.notebook_output_download('balaka18/email-spam-classification')
    print('Data source import complete.')
except Exception as e:
    print('Kagglehub download notice:', e)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

# 1. Read dataset
csv_path = "/kaggle/input/email-spam-classification-dataset-csv/emails.csv"
if not os.path.exists(csv_path) and 'balaka18_email_spam_classification_dataset_csv_path' in locals():
    csv_path = os.path.join(balaka18_email_spam_classification_dataset_csv_path, 'emails.csv')

df = pd.read_csv(csv_path)
print("Dataset shape:", df.shape)
print("\nFirst five rows:")
print(df.head())

# 2. Data Cleaning & Preparation
df = df.drop_duplicates()
target_column = df.columns[-1]
id_columns = [
    col for col in df.columns
    if col.strip().lower() in ["email no.", "email no", "email", "email_name", "email name"]
]
X = df.drop(columns=[target_column] + id_columns, errors="ignore")
y = df[target_column]
X = X.apply(pd.to_numeric, errors="coerce")
X = X.replace([np.inf, -np.inf], np.nan)
X = X.fillna(X.median()).fillna(0)
y = pd.to_numeric(y, errors="coerce")
valid_rows = y.notna() & y.isin([0, 1])
X = X.loc[valid_rows]
y = y.loc[valid_rows].astype(int)

print("\nFeatures shape:", X.shape)
print("Target distribution (0 = Not Spam, 1 = Spam):")
print(y.value_counts().sort_index())

# 3. Train Test Split & Normalization
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 4. K-Nearest Neighbors (KNN)
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
knn_pred = knn.predict(X_test_scaled)

# 5. Support Vector Machine (SVM)
svm = SVC(kernel="linear")
svm.fit(X_train_scaled, y_train)
svm_pred = svm.predict(X_test_scaled)

def evaluate_model(name, y_true, y_pred):
    print(f"\n{'=' * 55}\n{name}\n{'=' * 55}")
    print(f"Accuracy : {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision: {precision_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"Recall   : {recall_score(y_true, y_pred, zero_division=0):.4f}")
    print(f"F1-score : {f1_score(y_true, y_pred, zero_division=0):.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_true, y_pred))
    print("\nClassification Report:")
    print(classification_report(
        y_true, y_pred,
        target_names=["Not Spam", "Spam"],
        zero_division=0
    ))

evaluate_model("K-Nearest Neighbors (KNN)", y_test, knn_pred)
evaluate_model("Support Vector Machine (SVM)", y_test, svm_pred)

# 6. Model Comparison
results = pd.DataFrame({
    "Model": ["KNN (k=5)", "SVM (linear kernel)"],
    "Accuracy": [
        accuracy_score(y_test, knn_pred),
        accuracy_score(y_test, svm_pred)
    ],
    "Precision": [
        precision_score(y_test, knn_pred, zero_division=0),
        precision_score(y_test, svm_pred, zero_division=0)
    ],
    "Recall": [
        recall_score(y_test, knn_pred, zero_division=0),
        recall_score(y_test, svm_pred, zero_division=0)
    ],
    "F1-score": [
        f1_score(y_test, knn_pred, zero_division=0),
        f1_score(y_test, svm_pred, zero_division=0)
    ]
})

print("\nModel comparison:")
print(results.to_string(index=False, formatters={
    "Accuracy": "{:.4f}".format,
    "Precision": "{:.4f}".format,
    "Recall": "{:.4f}".format,
    "F1-score": "{:.4f}".format
}))

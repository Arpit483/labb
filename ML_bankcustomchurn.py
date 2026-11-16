import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 1. Read dataset
df = pd.read_csv("/kaggle/input/datasets/barelydedicated/bank-customer-churn-modeling/Churn_Modelling.csv")
print("Original dataset shape:", df.shape)
print(df.head())

# 2. Data Preprocessing
df.drop(columns=["RowNumber", "CustomerId", "Surname"],
        inplace=True, errors="ignore")
df["Gender"] = LabelEncoder().fit_transform(df["Gender"])
df = pd.get_dummies(df, columns=["Geography"], drop_first=True, dtype=int)
X = df.drop("Exited", axis=1)
y = df["Exited"]

# 3. Train Test Split & Normalization
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 4. Neural Network Classifier
model = Sequential([
    Dense(16, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(8, activation="relu"),
    Dense(1, activation="sigmoid")
])
model.compile(optimizer="adam",
              loss="binary_crossentropy",
              metrics=["accuracy"])
model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)

# 5. Prediction & Accuracy
y_pred = (model.predict(X_test) >= 0.5).astype(int)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

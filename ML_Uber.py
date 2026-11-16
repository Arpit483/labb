import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# 1. Read dataset
df = pd.read_csv("/kaggle/input/datasets/yasserh/uber-fares-dataset/uber.csv")
print("Original dataset shape:", df.shape)
print(df.head())

# Filter invalid values
df = df[(df["fare_amount"] > 0) & (df["passenger_count"] > 0)]

# 2. Calculate distance using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    return 6371 * 2 * np.arcsin(np.sqrt(a))

df["distance"] = haversine(
    df["pickup_latitude"], df["pickup_longitude"],
    df["dropoff_latitude"], df["dropoff_longitude"]
)
df = df[df["distance"] < 100]

# 3. Identify outliers using IQR
Q1 = df["fare_amount"].quantile(0.25)
Q3 = df["fare_amount"].quantile(0.75)
IQR = Q3 - Q1
outliers = df[
    (df["fare_amount"] < Q1 - 1.5 * IQR) |
    (df["fare_amount"] > Q3 + 1.5 * IQR)
]
print("Number of outliers:", len(outliers))
sns.boxplot(x=df["fare_amount"])
plt.show()

# Filter outliers
df = df[df["fare_amount"].between(
    Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
)]

# 4. Correlation analysis and Heatmap
print(df.select_dtypes(include="number").corr()["fare_amount"])
sns.heatmap(df.select_dtypes(include="number").corr(),
            annot=True, cmap="coolwarm")
plt.show()

# 5. Features and target split
X = df[[
    "pickup_longitude", "pickup_latitude",
    "dropoff_longitude", "dropoff_latitude",
    "passenger_count", "distance"
]]
y = df["fare_amount"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 6. Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

# 7. Random Forest Regression
rf = RandomForestRegressor(
    n_estimators=100, random_state=42
)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

# 8. Evaluation & Comparison
for name, pred in [
    ("Linear Regression", y_pred_lr),
    ("Random Forest", y_pred_rf)
]:
    print("\n", name)
    print("R2 Score:", r2_score(y_test, pred))
    print("RMSE:", np.sqrt(mean_squared_error(y_test, pred)))
    print("MSE:", mean_squared_error(y_test, pred))

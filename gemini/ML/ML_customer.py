import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage

# 1. Read dataset
df = pd.read_csv("/kaggle/input/datasets/kyanyoga/sample-sales-data/sales_data_sample.csv", encoding="latin1")
print("Original dataset shape:", df.shape)
print(df.head())

# 2. Select numeric columns & Scale
X = df.select_dtypes(include="number").dropna()
X_scaled = StandardScaler().fit_transform(X)

# 3. Elbow Method to find optimal number of clusters
wcss = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss, marker="o")
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.show()

# 4. K-Means Clustering
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df.loc[X.index, "KMeans_Cluster"] = kmeans.fit_predict(X_scaled)
print("K-Means cluster counts:")
print(df["KMeans_Cluster"].value_counts())

# 5. Hierarchical Clustering
hierarchical = AgglomerativeClustering(n_clusters=3)
df.loc[X.index, "Hierarchical_Cluster"] = hierarchical.fit_predict(X_scaled)
print("\nHierarchical cluster counts:")
print(df["Hierarchical_Cluster"].value_counts())

# 6. Dendrogram
sample = X_scaled[:100]
linked = linkage(sample, method="ward")
plt.figure(figsize=(10, 5))
dendrogram(linked)
plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Data Points")
plt.ylabel("Distance")
plt.show()

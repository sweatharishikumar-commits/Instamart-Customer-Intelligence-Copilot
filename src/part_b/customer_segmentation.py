import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
import os
os.makedirs("outputs",exist_ok=True)

#LOAD RFM TABLE &CREATE MATRIX
rfm=pd.read_csv("outputs/rfm_table.csv")
X=rfm[["recency","frequency","monetary"]]
#SCALE DATA
scaler=StandardScaler()
X_scaled=scaler.fit_transform(X)
#K MEANS RUN FOR K="2 TO 8"
results=[]
for k in range(2, 9):
    kmeans=KMeans(n_clusters=k,n_init=10,random_state=42)
    labels=kmeans.fit_predict(X_scaled)
    inertia=kmeans.inertia_
    silhouette=silhouette_score(X_scaled,labels)
    results.append([k,inertia,silhouette])
#RESULT DATAFRAME
k_results=pd.DataFrame(results,columns=["K","Inertia","Silhouette"])
print("\nK MEANS RESULTS")
print(k_results)
#TRAIN FINAL KMEANS
final_k=4
kmeans=KMeans(n_clusters=final_k,n_init=10,random_state=42)
rfm["segment_id"]=kmeans.fit_predict(X_scaled)
#SEGMENT SIZE CHECK
print(rfm["segment_id"].value_counts())
#SEGMENT PROFILE
profile=(rfm.groupby("segment_id")
    .agg(customers=("customer_id","count"),
        mean_recency=("recency","mean"),
        mean_frequency=("frequency","mean"),
        mean_monetary=("monetary","mean")))
print(profile)
#NAME SEGMENTS
segment_names={
    0: "Regular Customers",
    1: "Premium Customers",
    2: "Frequent Loyal Customers",
    3: "Dormant Customers"
}
rfm["segment_name"]=(rfm["segment_id"].map(segment_names))
#CREATE FLAG
premium_segment=(profile["mean_monetary"].idxmax())
print("Premium Segment:",premium_segment)
rfm["is_premium"]=(rfm["segment_id"]==premium_segment)
print(rfm["is_premium"].value_counts())
#PCA
pca=PCA(n_components=2)
pca.fit(X_scaled)
print(pca.explained_variance_ratio_)
print("Total Variance:",pca.explained_variance_ratio_.sum())
#SAVE CUSTOMER SEGMENTS
customer_segments=rfm[["customer_id","recency","frequency","monetary","segment_id","segment_name","is_premium"]]
customer_segments.to_csv("outputs/customer_segments.csv",index=False)
print("customer_segments.csv saved successfully")
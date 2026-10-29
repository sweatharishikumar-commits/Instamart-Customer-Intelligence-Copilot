import pandas as pd
import os

#LOAD CLEAN DATA
customers=pd.read_csv("data/clean/customers.csv")
orders=pd.read_csv("data/clean/orders.csv")

#CONVERT DATE COLUMNS
orders["order_ts"]=pd.to_datetime(orders["order_ts"])
print(orders.dtypes)

#KEEP COMPLETE ORDERS
completed_orders=orders[orders["status"]=="completed"].copy()
print(completed_orders.value_counts())

#SNAPSHOT
snapshot_date=pd.Timestamp("2025-10-01 00:00:00")

#CALCULATE RECENCY
latest_order_df=(completed_orders.groupby("customer_id")["order_ts"].max().reset_index())
latest_order_df.columns=["customer_id","last_order_date"]

#CALCULATE FREQUENCY
frequency_df=(completed_orders.groupby("customer_id")["order_id"].nunique().reset_index())
frequency_df.columns=["customer_id","frequency"]
print(frequency_df.head())

#CALCULATE MONETORY
monetary_df=(completed_orders.groupby("customer_id")["order_amount"].sum().reset_index())
monetary_df.columns=["customer_id","monetary"]

#CALCULATE DAYS
latest_order_df["recency"]=(snapshot_date-latest_order_df["last_order_date"]).dt.days
print(latest_order_df.head())

#MERGE RFM
rfm=latest_order_df.merge(frequency_df,on="customer_id")
rfm=rfm.merge(monetary_df,on="customer_id")
rfm=rfm[["customer_id","recency","frequency","monetary"]]
print("Number of customers:",len(rfm))
print(rfm.head())
print("\nRFM Statistics")
print("Recency Median:",rfm["recency"].median())
print("Recency Min:",rfm["recency"].min())
print("Recency Max:",rfm["recency"].max())
print("Frequency Mean:",round(rfm["frequency"].mean(),2))
print("Frequency Max:",rfm["frequency"].max())
print("Monetary Mean:",round(rfm["monetary"].mean(),2))
print("Monetary Max:",round(rfm["monetary"].max(),2))

os.makedirs("outputs",exist_ok=True)
rfm.to_csv("outputs/rfm_table.csv",index=False)
print("RFM Table saved")

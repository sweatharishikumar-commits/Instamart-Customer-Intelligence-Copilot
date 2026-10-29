import pandas as pd
import os

os.makedirs("data/clean",exist_ok=True)
#READING RAW DATA
orders=pd.read_csv("data/raw/orders.csv")
products=pd.read_csv("data/raw/products.csv")
print(orders.shape)

#CONVERT DATETIME
orders["order_ts"]= pd.to_datetime(orders["order_ts"])
print(orders.dtypes)

#REMOVE EXACT DUPLICATES
before=len(orders)
orders=orders.drop_duplicates()
after=len(orders)
print("Duplicates Removed:",before-after)

#KEEP LAST ORDER & FIX ORDERS AMOUNT
orders=orders.sort_values("order_ts").drop_duplicates(subset="order_id",keep="last")
print("ROWS:",len(orders))
orders["order_amount"]=pd.to_numeric(orders["order_amount"],errors="coerce")
print(orders["order_amount"].isna().sum())    

#PRODUCTS PRICE MERGE
orders=orders.merge(products[["product_id","price_inr","category"]],on="product_id",how="left")

#FILL MISSING ORDER AMOUNT
mask=orders["order_amount"].isna()
orders.loc[mask,"order_amount"]=(orders["price_inr"]*orders["quantity"]*(1-orders["discount_pct"]/100)).round(2)
print("MISSING AMOUNT:",orders["order_amount"].isna().sum())
orders["delivery_minutes"]=pd.to_numeric(orders["delivery_minutes"],errors="coerce")
#REMOVE INVALID DELIVERY
orders.loc[orders["delivery_minutes"]<0,"delivery_minutes"]=pd.NA

#FILL MISSING DELIVERY
completed=orders["status"]=="completed"
orders.loc[completed,"delivery_minutes"]=(orders.loc[completed].groupby("category")["delivery_minutes"].transform(lambda x:x.fillna(x.median())))
print(orders["status"].value_counts())
print("Missing Amount:",orders["order_amount"].isna().sum())
print("Missing Delivery for Completed:",orders.loc[orders["status"]=="completed","delivery_minutes"].isna().sum())

orders.to_csv("data/clean/orders.csv",index=False)
print("CLean Orders Saved")

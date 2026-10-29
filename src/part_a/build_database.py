import pandas as pd
import sqlite3
#CLEANED DATA
customers = pd.read_csv("data/clean/customers.csv")
products = pd.read_csv("data/clean/products.csv")
orders = pd.read_csv("data/clean/orders.csv")

#CREATE DATABASEE
conn = sqlite3.connect("data/instamart.db")

#CREATE TABLES
customers.to_sql("customers",conn,if_exists="replace",index=False)
products.to_sql("products",conn,if_exists="replace", index=False)
orders.to_sql("orders",conn,if_exists="replace",index=False)
conn.close()
print("Database Created Successfully")
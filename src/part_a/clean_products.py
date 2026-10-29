import pandas as pd
import os
os.makedirs("data/clean",exist_ok=True)
products = pd.read_csv("data/raw/products.csv")
products.to_csv("data/clean/products.csv",index=False)
print("Products saved successfully")
print(products.shape)
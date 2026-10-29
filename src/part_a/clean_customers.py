import pandas as pd
import os
customers=pd.read_csv("data/raw/customers.csv")
print(customers.head())
os.makedirs("data/clean",exist_ok=True)

#FUNCTION TO CLEAN GENDER
def clean_gender(gender):
    if pd.isna(gender):
        return "unknown"
    gender = gender.strip().lower()
    if gender in ["male", "m"]:
        return "male"
    elif gender in ["female", "f"]:
        return "female"
    else:
        return "unknown"
    
#CLEANED CITY NAMES
customers["city"]=customers["city"].str.strip().str.title()
print(customers["city"].value_counts())

#CLEANED GENDER
customers["gender"] = customers["gender"].apply(clean_gender)
print(customers["gender"].value_counts())

#CLEAN AGE
customers["age"] = pd.to_numeric(customers["age"], errors="coerce")

#CHECKING INVALID AGE 
customers.loc[~customers["age"].between(10, 100), "age"] =pd.NA
print(customers["age"].isna().sum())

#FILL MISSING AGES WITH MEDIAN
customers["age"]=customers.groupby("city")["age"].transform(lambda x: x.fillna(x.median()))
print(customers["age"].isna().sum())
print(customers["age"].min(),customers["age"].max())
#CONVERT DATE
customers["signup_date"] = pd.to_datetime(customers["signup_date"])
print(customers.dtypes)

customers.to_csv("data/clean/customers.csv", index=False)
print("customers.csv saved successfully")
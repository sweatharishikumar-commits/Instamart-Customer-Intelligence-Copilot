import pandas as pd
customers=pd.read_csv("data/raw/customers.csv")
products=pd.read_csv("data/raw/products.csv")
orders=pd.read_csv("data/raw/orders.csv")

#FUNCTION TO FIND MISSING VALUES
def missing_report(df):
    report = pd.DataFrame({
        "Missing Count": df.isna().sum(),
        "Missing Percent":
            round(df.isna().mean()*100, 2)
    })
    return report

#SHAPES
print("\nSHAPES")
print("\n Customers")
print(customers.shape)
print("\n Products")
print(products.shape)
print("\n Orders")
print(orders.shape)

#COLOUMNS
print("\nCUSTOMER COLUMNS")
print(customers.columns)
print("\nPRODUCT COLUMNS")
print(products.columns)
print("\nORDER COLUMNS")
print(orders.columns)

#DATA TYPES
print("\nCUSTOMERS DATA TYPES")
print(customers.dtypes)
print("\nPRODUCTS DATA TYPES")
print(products.dtypes)
print("\nORDERS DATA TYPES")
print(orders.dtypes)

#MISSING VALUES
print("\nCUSTOMERS")
print(missing_report(customers))
print("\nPRODUCTS")
print(missing_report(products))
print("\nORDERS")
print(missing_report(orders))

#FINDING DUPLICATES
print("\nEXACT DUPLICATE ROWS")
duplicates = orders["order_id"].duplicated().sum()
print("Duplicates:", duplicates)

print("\nPENDING ROWS")
pending_rows = (orders["status"] == "pending").sum()
print("Pending Rows:", pending_rows)

#UNIQUE ORDER IDS
print("\nDISTINCT ORDER IDS")
distinct_orders = orders["order_id"].nunique()
print("Distinct Order IDs:", distinct_orders)

#CHECKING INVALID AMOUNTS AND DELIVERY ITEMS
print("\nINVALID ORDER AMOUNTS")
amounts = pd.to_numeric(orders["order_amount"],errors="coerce")
invalid_amounts = amounts.isna()|(amounts <= 0).sum()
print("Invalid Amounts:", invalid_amounts)

print("\nNEGATIVE DELIVERY TIMES")
delivery = pd.to_numeric(orders["delivery_minutes"],errors="coerce")
negative_delivery = (delivery < 0)|(delivery > 1440).sum()
print("Negative Delivery:", negative_delivery)

#DELIVERY TIME CHECK
print("\nBLANK DELIVERY TIMES")
blank_delivery = (orders["delivery_minutes"].isna().sum())
print("Blank Delivery:", blank_delivery)

#AGE CHECK BLANK AND INVALID
print("\nBLANK AGES")
blank_age = (customers["age"].isna().sum())
print("Blank Age:", blank_age)

print("\nAGES OUTSIDE 10-100")
age_numeric = pd.to_numeric(customers["age"],errors="coerce")
invalid_age = ((~age_numeric.between(10, 100)) & age_numeric.notna()).sum()
print("Invalid Ages:", invalid_age)

#SPELLING CHECK AGE AND GENDER
print("\nRAW CITY SPELLINGS")
print(customers["city"].dropna().unique())

print("\nRAW GENDER SPELLINGS")
print(customers["gender"].dropna().unique())

print("\nBLANK GENDER")
blank_gender = (customers["gender"].isna().sum())
print("Blank Gender:", blank_gender)

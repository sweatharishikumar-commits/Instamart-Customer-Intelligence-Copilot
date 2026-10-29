import pandas as pd
customers = pd.read_csv("data/clean/customers.csv")
orders = pd.read_csv("data/clean/orders.csv")
#CHECKPOINTS
print(customers["gender"].value_counts())
assert len(customers) == 1200
assert customers["age"].isna().sum() == 0
assert customers["gender"].value_counts()["female"] == 610
assert customers["gender"].value_counts()["male"] == 560
assert len(orders) == 12309
assert (orders["status"].eq("completed").sum()) == 11110
assert (orders["status"].eq("cancelled").sum()) == 1199
assert (orders["order_amount"].isna().sum()) == 0
assert (orders.loc[orders["status"]=="completed","delivery_minutes"].isna().sum()) == 0
print("ALL CHECKPOINTS PASSED")
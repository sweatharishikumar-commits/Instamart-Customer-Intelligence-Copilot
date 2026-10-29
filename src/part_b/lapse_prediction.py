import pandas as pd
from sklearn.model_selection import(train_test_split,GridSearchCV)
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import(accuracy_score,precision_score,recall_score,f1_score,confusion_matrix)
from sklearn.utils import resample
import joblib
import os
#LOAD DATA
customers=pd.read_csv("data/clean/customers.csv")
orders=pd.read_csv("data/clean/orders.csv")
products=pd.read_csv("data/clean/products.csv")
orders["order_ts"]=pd.to_datetime(orders["order_ts"])
customers["signup_date"]=pd.to_datetime(customers["signup_date"])
#DEFINE CUTOFF
cutoff=pd.Timestamp("2025-09-01")
#CREATE COHORT
completed=orders[orders["status"]=="completed"].copy()
before_cutoff=completed[completed["order_ts"] < cutoff]
#ELIGIBLE CUSTOMERS
cohort_customers=(before_cutoff["customer_id"].unique())
print("Cohort customers:",len(cohort_customers))
#CREATE LAPSE LABEL
Lapsed = 1
#NO completed order during
#2025-09-01 to 2025-09-30
#CUSTOMERS ACTIVE IN SEPTEMBER
sept_orders=completed[completed["order_ts"] >= cutoff]
active_sept=set(sept_orders["customer_id"])
#TARGET TABLE
target=pd.DataFrame({"customer_id": cohort_customers})
#LAPSED LABEL
target["lapsed"]=(~target["customer_id"].isin(active_sept)).astype(int)
#VALID COUNTS
print(target["lapsed"].value_counts())
print(target["lapsed"].mean())
#BUILD ALL FEATURES
#RECENCY
last_order=(before_cutoff.groupby("customer_id")["order_ts"].max().reset_index())
last_order["recency"]=(cutoff - last_order["order_ts"]).dt.days
recency_df = last_order[["customer_id","recency"]]
#FREQUENCY
frequency_df=(before_cutoff.groupby("customer_id")["order_id"].nunique().reset_index(name="frequency"))
#MONETARY
monetary_df=(before_cutoff.groupby("customer_id")["order_amount"].sum().reset_index(name="monetary"))
#AVERAGE DISCOUNT
discount_df=(before_cutoff.groupby("customer_id")["discount_pct"].mean().reset_index(name="avg_discount"))
#AVERAGE DELIVERY TIME
delivery_df=(before_cutoff.groupby("customer_id")["delivery_minutes"].mean().reset_index(name="avg_delivery"))
#CANCELLATION RATE
#ORDERS BEFORE CUTTOFF
orders_before_cutoff=orders[orders["order_ts"] < cutoff].copy()
#TOTAL ORDERS
total_orders=(orders_before_cutoff.groupby("customer_id").size().reset_index(name="total_orders"))
#CANCELLED ORDERS
cancelled_orders=(orders_before_cutoff[orders_before_cutoff["status"]=="cancelled"].groupby("customer_id").size().reset_index(name="cancelled_orders"))
#MERGE
cancel_df=total_orders.merge(cancelled_orders,on="customer_id",how="left")
cancel_df["cancelled_orders"]=(cancel_df["cancelled_orders"].fillna(0))
cancel_df["cancel_rate"]=(cancel_df["cancelled_orders"]/cancel_df["total_orders"])
cancel_df=cancel_df[["customer_id","cancel_rate"]]
#FAVOURITE CATEGORY
fav_category=(before_cutoff.groupby("customer_id")["category"].agg(lambda x: x.mode().iloc[0]).reset_index(name="favourite_category"))
#TENURE
customers["signup_date"]=pd.to_datetime(customers["signup_date"])
customers["tenure"]=(cutoff-customers["signup_date"]).dt.days
customer_features=customers[["customer_id","city","age","gender","tenure"]]
#MERGE
feature_df=target.copy()
feature_df=feature_df.merge(recency_df,on="customer_id")
feature_df=feature_df.merge(frequency_df,on="customer_id")
feature_df=feature_df.merge(monetary_df,on="customer_id")
feature_df=feature_df.merge(discount_df,on="customer_id")
feature_df=feature_df.merge(delivery_df,on="customer_id")
feature_df=feature_df.merge(cancel_df,on="customer_id")
feature_df=feature_df.merge(fav_category,on="customer_id")
feature_df=feature_df.merge(customer_features,on="customer_id")
print(feature_df.shape)
print(feature_df.head())
#TRAIN AND TEST SPLIT 
X=feature_df.drop(columns=["customer_id","lapsed"])
y=feature_df["lapsed"]
#SPLIT TRAIN TEST
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20,stratify=y,random_state=42)
print("Train:",len(X_train))
print("Test:",len(X_test))
#DEFINE NUMERIC COLUMNS
numeric_features=["recency","frequency","monetary","avg_discount","cancel_rate","avg_delivery","age","tenure"]
categorical_features=["city","gender","favourite_category"]
#TRANSFOMER
preprocessor=ColumnTransformer(transformers=[("num",StandardScaler(),numeric_features),
        ("cat",OneHotEncoder(drop="first",handle_unknown="ignore"),categorical_features)])
#FIT ON TRAINING DATA
X_train_processed=preprocessor.fit_transform(X_train)
X_test_processed=preprocessor.transform(X_test)
#VERIFY SIZE
print("Train shape:",X_train_processed.shape)
print("Test shape:",X_test_processed.shape)
#SCALAR MEAN CHECK
scaler=preprocessor.named_transformers_["num"]
freq_index=numeric_features.index("frequency")
#TRAINING MEAN
print("Scaler Frequency Mean:",scaler.mean_[freq_index])
#COHORT MEAN
print("Full Cohort Frequency Mean:",feature_df["frequency"].mean())
#CHECK MISSING VALUES
print(feature_df.isnull().sum())
assert (feature_df.isnull().sum().sum()==0)
print("No missing values found")
#BASELINE MODEL
#CREATE PIPELINE
log_pipeline=Pipeline([("preprocessor", preprocessor),("classifier",LogisticRegression(max_iter=1000))])
#GRID SEARCH
log_grid=GridSearchCV(log_pipeline,{"classifier__C":[0.01,0.1,1,10,100]},cv=5,scoring="f1",n_jobs=-1)
log_grid.fit(X_train, y_train)
print("\nLOGISTIC REGRESSION")
print("Best Parameters:",log_grid.best_params_)
print("Best CV F1:",log_grid.best_score_)
#RANDOM FOREST TRAINING
rf_pipeline=Pipeline([("preprocessor",preprocessor),("classifier",RandomForestClassifier(n_estimators=100,random_state=42))])
rf_grid=GridSearchCV(rf_pipeline,{"classifier__max_depth":[3,5,8],"classifier__min_samples_leaf":[5,10,20]},cv=5,scoring="f1",n_jobs=-1)
rf_grid.fit(X_train, y_train)
print("\nRANDOM FOREST")
print("Best Parameters:",rf_grid.best_params_)
print("Best CV F1:",rf_grid.best_score_)
#EVALUATION OF LOGISTIC REGRESSION
log_pred=log_grid.predict(X_test)
print("\nLOGISTIC TEST RESULTS")
print("Confusion Matrix")
print(confusion_matrix(y_test, log_pred))
print("Precision:",precision_score(y_test, log_pred))
print("Recall:",recall_score(y_test, log_pred))
print("F1:",f1_score(y_test, log_pred))
#EVALUATION OF RANDOM FOREST
rf_pred=rf_grid.predict(X_test)
print("\nRANDOM FOREST TEST RESULTS")
print("Confusion Matrix")
print(confusion_matrix(y_test, rf_pred))
print("Precision:",precision_score(y_test, rf_pred))
print("Recall:",recall_score(y_test, rf_pred))
print("F1:",f1_score(y_test, rf_pred))
#CLASS BALANCE
train_df=X_train.copy()
train_df["lapsed"]=y_train.values
#SEPARATE CLASSES
majority=train_df[train_df["lapsed"]==0]
minority=train_df[train_df["lapsed"]==1]
#CHECK COUNTS
print(majority.shape[0])
print(minority.shape[0])
#OVERSAMPLE MINORITY
minority_up=resample(minority,replace=True,n_samples=len(majority),random_state=42)
balanced_train = pd.concat([majority, minority_up])
print(balanced_train["lapsed"].value_counts())
#SPLIT X & Y
X_balanced=balanced_train.drop(columns=["lapsed"])
y_balanced=balanced_train["lapsed"]
#RETRAIN LOGISTIC REGRESSION
balanced_model=Pipeline([("preprocessor", preprocessor),("classifier",LogisticRegression(max_iter=1000,C=0.1))])
balanced_model.fit(X_balanced,y_balanced)
#EVALUATE
balanced_pred = balanced_model.predict(X_test)
print("\nBALANCED LOGISTIC")
print("Precision:",precision_score(y_test,balanced_pred))
print("Recall:",recall_score(y_test,balanced_pred))
print("F1:",f1_score(y_test,balanced_pred))
os.makedirs("outputs",exist_ok=True)
#SAVE MODEL
joblib.dump(log_grid.best_estimator_,"outputs/lapse_model.joblib")
print("Model saved")
#RELOAD MODEL
loaded_model=joblib.load("outputs/lapse_model.joblib")
#PREDICTION MATCH
original_pred=log_grid.predict(X_test)
loaded_pred=loaded_model.predict(X_test)
print((original_pred==loaded_pred).all())
#RETENTION LIST CREATION
#TEST CUSTOMERS
test_df=feature_df.loc[X_test.index].copy()
#PREMIUM CUSTOMERS ONLY
segments=pd.read_csv("outputs/customer_segments.csv")
premium_customers=segments[segments["is_premium"] == True][["customer_id"]]
retention=test_df.merge(premium_customers,on="customer_id")
#GET PROBABILITIES
retention["lapse_probability"]=(loaded_model.predict_proba(retention.drop(columns=["customer_id","lapsed"]))[:,1])
#ACTUAL LABEL
retention["actually_lapsed"]=(retention["lapsed"])
#KEEP COLUMNS
retention=retention[["customer_id","lapse_probability","actually_lapsed"]]
#TOP 10
retention=retention.sort_values("lapse_probability",ascending=False).head(10)
retention.to_csv("outputs/retention_list.csv",index=False)
print(retention)
print("Actually lapsed:",retention["actually_lapsed"].sum())
best_model=log_grid.best_estimator_
joblib.dump(best_model,"outputs/lapse_model.joblib")
loaded_model=joblib.load("outputs/lapse_model.joblib")
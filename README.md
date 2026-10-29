            INSTAMART-CUSTOMER-INTELLIGENCE-COPILOT
INTRODUCTION  
    This project develops a Customer Intelligence and Support Copilot for a Swiggy Instamart company which delivers instant groceries.The objective is to transfer raw data into valuable insights and intelligent support solutions.
    This project works by dividing into four parts 

      PART A : DATA FOUNDATION
      This part works on data cleaning and validation on raw data such as customer,product and order.The cleaned data is stored in a SQLite database and analysed using SQL and pandas. 
      
      PART B : CUSTOMER SEGMENTATION AND LAPSE PREDICTION
      The customer behaviour is analysed using RFM(Recency,Frequency,monetary)metrics,Customers are segmented using K-Means Clustering and lapse prediction model is developed to predict the customers.

      Part C : SUPPORT TICKET WITH GUARDRAIL
      This processes customer support tickets by applying input guardrails and privacy protection techniques.Sensitive information is redacted,tickets are classified into categories and they are routed to appropriate support team.

      Part D : POLICY ASSISTANT AND REFUND AGENT
      Finally Retrieval Augmented Generation(RAG)policy is built to answer the policy related questions using company policy documents.A ReAct style refund agent are built to answer policy questions and automate refund decisions.Escalate cases when human evaluation is required.
      
       Together these four parts creates an end-to-end Customer Intelligence and Support Copilot that combines data clean,machine learning,information retrieval and AI agent workflow. 
      
REPRODUCE
    Follow the steps below to reproduce the project results.
Step 1: Create Virtual Environment
python -m venv .venv
Step 2: Activate Virtual Environment
Windows:
.venv\Scripts\activate
Step 3: Install Required Libraries
pip install -r requirements.txt
Step 4: Generate Synthetic Data
python generate_data.py
Expected output:
generated: customers=1200 products=40 orders_raw=13084 tickets=164
Step 5: Audit Raw Data
python src/part_a/audit.py
Step 6: Clean Customer Data
python src/part_a/clean_customers.py
Step 7: Clean Product Data
python src/part_a/clean_products.py
Step 8: Clean Order Data
python src/part_a/clean_orders.py
Step 9: Build SQLite Database
python src/part_a/build_database.py
Step 10: Validate Checkpoints
python src/part_a/validate.py
Expected output:
ALL CHECKPOINTS PASSED
Step 11: Run SQL Queries
python src/part_a/run_queries.py
Step 12: Run Customer Segmentation
python src/part_b/customer_segmentation.py
Step 13: Run Lapse Prediction
python src/part_b/lapse_prediction.py
Outputs:
outputs/customer_segmentation.csv
outputs/lapse_model.joblib
outputs/retention_list.csv
Step 14: Run Support Ticket Triage
python src/part_c/ticket_triage.py
Outputs:
outputs/triage_results.csv
outputs/triage_budget_demo.csv
Step 15: Run Policy Assistant and Refund Agent
python src/part_d/policy_assistant.py
Outputs:
outputs/refund_ledger.jsonl
outputs/agent_runs.jsonl

Part A Data Foundation
Data Audit
The raw datasets were loaded and analysed to identify data quality issues before cleaning.
Orders Dataset Audit
Metric	Value
Raw order rows	13084
Exact duplicate rows	119
Pending rows	656
Distinct order IDs	12309
Non-numeric order amounts	120
Negative delivery times	106
Blank delivery times	2541
Customers Dataset Audit
Metric	Value
Blank ages	61
Ages outside 10–100	6
Distinct raw city spellings	24
Distinct gender spellings	10
Blank gender values	30
Customer Data Cleaning
The following cleaning rules were applied:
1.Standardised city names by removing extra spaces and applying title case.
2.Reduced all city values to six valid cities.
3.Mapped gender spellings into three categories: male, female and unknown.
4.Treated ages outside the range 10–100 as missing.
5.Filled missing ages using the median age of each city.
6.Converted signup_date to datetime format.
Final Customer Summary
Gender	Count
Female	610
Male	560
Unknown	30
All missing ages were successfully imputed and all ages fall between 18 and 60.
Order Data Cleaning
The following cleaning steps were applied:
1.Converted order timestamps to datetime.
2.Removed exact duplicate rows.
3.Retained only the latest record for each duplicate order ID.
4.Converted order_amount to numeric values.
5.Recalculated missing order amounts using product price, quantity and discount percentage.
6.Converted negative delivery times to missing values.
7.Filled missing delivery times for completed orders using category-level median delivery times.
8.Kept delivery times missing for cancelled orders.
Final Order Summary
Metric	Value
Final order rows	12309
Completed orders	11110
Cancelled orders	1199
Missing order amounts	0
Missing delivery times (completed)	0
Missing delivery times (cancelled)	1199
Completed order revenue	INR 2,998,668.80
Validation
The cleaned datasets were validated against the required project checkpoints.
Result:
ALL CHECKPOINTS PASSED
SQL Analysis Results
Q1 - WHERE and HAVING
Customers with completed orders above INR 500 and total spend above INR 8000:
Result: 30 customers
Q2 - Three-Table Join
Revenue by city and product category:
Rows returned: 30
Total revenue: INR 2,998,668.80
Highest revenue combination: Bengaluru / Electronics (INR 233,909.45)
Q3 - Scalar Subquery
Products priced above average catalogue price:
Result: 11 products
Q4 - LEFT JOIN
Customers without completed orders:
Result: 25 customers
Q5 - Common Table Expressions
Customers whose spend exceeds average customer spend:
Result: 550 customers
Average spend: INR 2,552.06
Q6 - Window Functions
Top customer by city:
Bengaluru: C0082 (INR 12,856.20)
Chennai: C0930 (INR 10,151.40)
Delhi: C0291 (INR 13,742.60)
Hyderabad: C0743 (INR 12,730.05)
Mumbai: C0693 (INR 14,766.55)
Pune: C0426 (INR 10,377.10)
Eight rows showed a difference between RANK() and ROW_NUMBER() because tied values receive the same rank while ROW_NUMBER() always assigns unique sequential numbers.
Q7 - Running Revenue
Daily revenue rows: 183
Final cumulative revenue: INR 2,998,668.80
Pandas Cross-Check
The SQL revenue totals were verified using pandas pivot tables.
Examples:
City	Revenue	Mean Order Amount	Completed Orders
Bengaluru	INR 523,643.40	INR 276.47	1894
Mumbai	INR 479,058.50	INR 297.00	1613
Exploratory Analysis
The completed order amount distribution is strongly right-skewed.
Mean: INR 269.91
Median: INR 135.00
Skewness: 4.61
Q1: INR 64.80
Q3: INR 297.00
Upper Outlier Fence: INR 645.30
High Outliers: 897
The strongest correlation was between order_amount and discount_pct (approximately -0.095). However, correlations of this size are weak and do not imply causation.

Part B  Customer Segmentation and Lapse Prediction
     The objective of Part B was to understand customer purchasing behaviour and identify
     customers who are likely to stop ordering in the future.
RFM Analysis
RFM (Recency, Frequency and Monetary) analysis was performed using completed orders.
RFM Summary
Metric	Value
Customers analysed	1175
Median Recency	19 days
Minimum Recency	0 days
Maximum Recency	180 days
Mean Frequency	9.46
Maximum Frequency	33
Mean Monetary Value	INR 2552.06
Maximum Monetary Value	INR 14766.55

Customer Segmentation
The RFM values were standardised using StandardScaler before clustering.
K-Means clustering was applied with values of K ranging from 2 to 8.
After analysing inertia, silhouette scores and business interpretability, K = 4 was selected as the final segmentation model.
Segment Summary
The four customer groups were interpreted as:
Premium Customers
Frequent Loyal Customers
Regular Customers
Dormant Customers
The segment with the highest monetary value was marked as the Premium segment.

Principal Component Analysis (PCA)
PCA was applied to the scaled RFM values to reduce dimensionality.
Explained Variance
Component	Explained Variance
PC1	0.634
PC2	0.218
Total	0.852
The first two principal components explained approximately 85.2% of the total variance.

Lapse Prediction
The objective was to identify customers who were likely to become inactive after the cutoff date of 2025-09-01.
Cohort Summary
Metric	Value
Customers in cohort	1156
Lapsed customers	443
Lapse rate	38.32%
Training rows	924
Test rows	232
Features Used
The model used:
Recency
Frequency
Monetary value
Average discount percentage
Cancellation rate
Average delivery time
Most frequent product category
City
Age
Gender
Customer tenure
Only data before the cutoff date was used to prevent data leakage.

Model Training
Two machine learning models were evaluated:
Logistic Regression
Grid Search was performed with:
C = {0.01, 0.1, 1, 10, 100}

Random Forest
Grid Search was performed with:
max_depth = {3, 5, 8}
min_samples_leaf = {5, 10, 20}

Model Evaluation
Logistic Regression
Metric	Value
Precision	0.655
Recall	0.809
F1 Score	0.724
Random Forest
Metric	Value
Precision	0.680
Recall	0.742
F1 Score	0.710

Selected Model
Logistic Regression was selected as the final model because it achieved strong recall while maintaining a competitive F1 score. High recall is important because identifying potential lapsing customers is more valuable than missing them entirely.

Class Balance Experiment
To address class imbalance, the minority class was oversampled using random duplication of lapsed customers within the training set.
Results
Before balancing:
Precision = 0.655
Recall = 0.809
F1 = 0.724
After balancing:
Precision = 0.592
Recall = 0.944
F1 = 0.727
The largest improvement was observed in recall, meaning the model identified a higher proportion of customers at risk of lapsing.

Model Persistence
The final model was saved using Joblib:
outputs/lapse_model.joblib
The saved model was reloaded successfully and produced identical predictions.

Retention List
Premium customers from the test set were ranked by predicted lapse probability.
Output generated:
outputs/retention_list.csv
This file contains:
customer_id
lapse_probability
actually_lapsed
Limitation
The Premium flag was created using the full observation window and therefore includes information from the lapse evaluation period. For this reason, the retention list should be considered illustrative rather than a leakage-free evaluation

Part C Support Ticket Triage with Guardrails
The objective of Part C was to build a secure and reliable support ticket triage system. The pipeline applies input guardrails, removes sensitive customer information, classifies support tickets using prompts, validates responses and routes tickets to the appropriate support team.

Input Guardrails
Before sending any ticket to the model, validation checks were applied.
Rules:
Empty tickets were skipped.
Very long tickets (more than 400 estimated tokens) were not processed and were flagged for review.
Results
Status	Count
Eligible	156
Skipped Empty	4
Flagged Long	4
All long tickets were estimated at 734 tokens.

Personal Information Redaction
Sensitive information was removed before model processing using regular expressions.
The following replacements were applied:
Email → [EMAIL]
Phone Number → [PHONE]
Order ID → [ORDER_ID]
Redaction Results
Entity	Count
Emails	55
Phones	91
Order IDs	132
Total Replacements	278
Verification checks confirmed that no sensitive information remained after redaction.
Remaining Sensitive Information
Entity	Remaining Count
Emails	0
Phones	0
Order IDs	0

Prompt Engineering
Two classification prompts were designed:
Zero-Shot Prompt
Contains allowed categories
Requires JSON output

Few-Shot Prompt
Contains labelled examples
Includes a fraud classification example
Requires JSON output
Allowed categories:
billing
delivery
technical
fraud

Retry Handling
The mock language model sometimes generated temporary failures.
A retry mechanism was implemented using:
Maximum 3 retries
Exponential backoff
Random jitter
Results
19 transient failures occurred
All failures were successfully recovered
No ticket ended with a permanent error

Output Validation
Every model response was validated.
A response was accepted if:
It contained valid JSON with an allowed category, or
The category could be identified through keyword extraction
Otherwise, the ticket was flagged for human review.
Validation Results
Status	Count
classified_json	135
classified_keyword	12
flagged_invalid_output	9

Prompt Comparison
The complete ticket set was processed using both prompts.
Zero-Shot Results
Metric	Value
Classified Tickets	147
Accuracy	85.7%
Few-Shot Results
Metric	Value
Classified Tickets	147
Accuracy	100%
The few-shot prompt used more tokens but produced significantly better classification performance, eliminating classification errors present in the zero-shot approach.
Token Usage
Metric	Value
Total Tokens Used	12052
Tokens Per Classified Ticket	40.85
Ticket Routing
The final routing rules were:
Human Review
Applied when:
skipped_empty
flagged_long
flagged_invalid_output
budget_exhausted
Priority:
NORMAL
Security Team
Applied when:
category = fraud
Priority:
HIGH
Premium Desk
Applied when:
is_premium = True
Priority:
HIGH

Support Queue
All remaining tickets were routed to:
support_queue
Priority:
NORMAL

Outputs Generated
The following output files were generated:
outputs/triage_results.csv
outputs/triage_budget_demo.csv

Part D Policy RAG Assistant and Refund Agent
The objective of Part D was to build a Retrieval-Augmented Generation (RAG) policy assistant and an automated refund agent. The policy assistant retrieves relevant information from company policy documents, while the refund agent uses tools and business rules to process refund requests.

Document Chunking
The five policy documents were divided into overlapping text chunks to improve retrieval quality.
Chunk Summary
Document	Number of Chunks
refund_policy.txt	4
delivery_policy.txt	3
payment_policy.txt	3
escalation_policy.txt	3
privacy_policy.txt	2
Total Chunks Created: 15

Retrieval System
TF-IDF Vectorization and Cosine Similarity were used to retrieve the most relevant policy chunks for a user query.
Retrieval Evaluation Results
Metric	Result
Expected document found in Top-3 retrieval	12 / 12
Expected fact found in answer	12 / 12
Unanswerable questions handled correctly	2 / 2
The retrieval system successfully identified all required documents and generated correctly grounded answers for every answerable question.

Policy Assistant
The policy assistant uses retrieved policy chunks as context and generates answers only from the provided information.
Example Question:
What delivery time makes a completed order eligible for a full refund?
Answer:
More than 45 minutes.
Source:
refund_policy.txt

Refund Agent
A ReAct-style agent was implemented using the following tools:
get_order()
search_policy()
calculate_refund()
issue_refund()
escalate_to_human()
The agent retrieves order details, checks policy rules, calculates refunds, issues refunds when eligible and escalates high-value refunds when human approval is required.

Refund Agent Results
Scenario	Status	Outcome
S1	REFUND	INR 128.25
S2	REFUND	INR 135.00
S3	ESCALATE	INR 1999.00
S4	DENIED	Delivery within policy limits
S5	DENIED	Order not eligible
S6	NOT_FOUND	Order does not exist
S7	FALLBACK_MAX_ITERATIONS	Human handoff
Safety and Fallback Mechanisms
Three safety mechanisms were implemented:

Maximum Iteration Protection
When the agent exceeds the maximum number of allowed reasoning steps:
FALLBACK_MAX_ITERATIONS
is returned.
Token Limit Protection
When the token limit is exceeded:
FALLBACK_TOKEN_LIMIT
is returned.
Timeout Protection
When the execution time exceeds the specified limit:
FALLBACK_TIMEOUT
is returned.
Demonstration Results
Demo	Status
Token Limit Test	FALLBACK_TOKEN_LIMIT
Timeout Test	FALLBACK_TIMEOUT
Generated Outputs
The following files were generated:
outputs/agent_runs.jsonl
outputs/refund_ledger.jsonl
The state directory stores checkpoint files used for agent recovery and resumption.

Conclusion
Part D successfully combines retrieval, reasoning and tool execution into a complete policy assistant and refund automation workflow. The agent follows business rules, retrieves policy information, processes refund requests and safely handles exceptional situations through fallback mechanisms.

Limitations

The project uses synthetic data generated for learning purposes. Therefore, the results may not fully represent real-world business behaviour.
Customer segmentation and lapse prediction are based on historical order data. Customer behaviour may change over time, which can affect model performance.
The Premium customer flag was created using the full observation period. Therefore, the retention list should be considered illustrative rather than a completely leakage-free evaluation.
The policy assistant uses TF-IDF retrieval, which depends on keyword matching. If two questions have the same meaning but use very different wording, retrieval quality may decrease.
The project uses the provided offline mock_llm.py file instead of a real production language model.

Next Steps

Replace TF-IDF retrieval with semantic vector embeddings to improve retrieval accuracy.
Improve the lapse prediction model by including more behavioural and time-based features.
Build a dashboard for customer segmentation, retention analysis and support ticket monitoring.
Deploy the ticket triage system and refund agent as real-time services.
Integrate the system with actual customer support platforms and databases.

CONCLUSION
This project successfully developed an end-to-end Customer Intelligence and Support Copilot. The solution combines data cleaning, SQL analysis, customer segmentation, machine learning, support ticket triage, retrieval-augmented policy search and an automated refund agent into a single workflow. The project demonstrates practical applications of data engineering, machine learning and AI-based automation in customer support and business decision making.
 #🛒 INSTAMART CUSTOMER INTELLIGENCE COPILOT

An end-to-end Customer Intelligence and Support Copilot combining data engineering, SQL analytics, machine learning, customer segmentation, support ticket automation, Retrieval-Augmented Generation (RAG), and AI agents.

---

# 📌 PROJECT OVERVIEW

This project is divided into four major parts:

## PART A: DATA FOUNDATION

This part focuses on data cleaning, auditing, and validation of raw customer, product, and order datasets.

**Key Activities:**
- Data auditing and quality checks.
- Customer, product, and order data cleaning.
- Handling missing and invalid values.
- SQLite database creation.
- SQL and Pandas-based data analysis.

## PART B: CUSTOMER SEGMENTATION AND LAPSE PREDICTION

Customer purchasing behaviour is analysed using RFM (Recency, Frequency, Monetary) metrics.

**Key Activities:**
- RFM analysis.
- Customer segmentation using K-Means clustering.
- Customer lapse prediction using Logistic Regression and Random Forest.
- Identification of customers requiring retention campaigns.

## PART C: SUPPORT TICKET TRIAGE WITH GUARDRAILS

This part processes customer support tickets using input guardrails and privacy protection techniques.

**Key Activities:**
- Input validation and guardrails.
- Personally Identifiable Information (PII) redaction.
- Support ticket classification.
- Automated ticket routing.
- Human review for sensitive or invalid cases.

## PART D: POLICY ASSISTANT AND REFUND AGENT

A Retrieval-Augmented Generation (RAG) system is developed to answer policy-related questions using company policy documents.

A ReAct-style refund agent is implemented to automate refund decisions.

**Key Activities:**
- Policy document retrieval.
- RAG-based question answering.
- Refund calculation and decision-making.
- Automated refund processing.
- Human escalation for complex cases.

## PROJECT SUMMARY

Together, these four parts create an end-to-end Customer Intelligence and Support Copilot combining:

- Data Engineering
- SQL Analytics
- Machine Learning
- Customer Segmentation
- AI-powered Support Automation
- Retrieval-Augmented Generation
- AI Agent Workflows

---

# 🛠️ TECHNOLOGIES USED

- Python
- Pandas
- NumPy
- SQLite
- SQL
- Scikit-learn
- K-Means Clustering
- Logistic Regression
- Random Forest
- TF-IDF
- Retrieval-Augmented Generation (RAG)
- AI Agents

---

# 🚀 PROJECT REPRODUCTION

Follow the steps below to reproduce the project results.

## Step 1: Create Virtual Environment

```bash
python -m venv .venv
```

## Step 2: Activate Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Generate Synthetic Data

```bash
python generate_data.py
```

**Expected Output:**

| Dataset | Records |
|:---|---:|
| Customers | 1,200 |
| Products | 40 |
| Orders | 13,084 |
| Tickets | 164 |

## Step 5: Audit Raw Data

```bash
python src/part_a/audit.py
```

## Step 6: Clean Customer Data

```bash
python src/part_a/clean_customers.py
```

## Step 7: Clean Product Data

```bash
python src/part_a/clean_products.py
```

## Step 8: Clean Order Data

```bash
python src/part_a/clean_orders.py
```

## Step 9: Build SQLite Database

```bash
python src/part_a/build_database.py
```

## Step 10: Validate Checkpoints

```bash
python src/part_a/validate.py
```

**Expected Output:**

```text
ALL CHECKPOINTS PASSED
```

## Step 11: Run SQL Analysis

```bash
python src/part_a/run_queries.py
```

## Step 12: Run Customer Segmentation

```bash
python src/part_b/customer_segmentation.py
```

## Step 13: Run Lapse Prediction

```bash
python src/part_b/lapse_prediction.py
```

**Generated Outputs:**

- `outputs/customer_segmentation.csv`
- `outputs/lapse_model.joblib`
- `outputs/retention_list.csv`

## Step 14: Run Support Ticket Triage

```bash
python src/part_c/ticket_triage.py
```

**Generated Outputs:**

- `outputs/triage_results.csv`
- `outputs/triage_budget_demo.csv`

## Step 15: Run Policy Assistant and Refund Agent

```bash
python src/part_d/policy_assistant.py
```

**Generated Outputs:**

- `outputs/refund_ledger.jsonl`
- `outputs/agent_runs.jsonl`

---

# 📊 PART A: DATA FOUNDATION

## Objective

Build a reliable data foundation by auditing, cleaning, validating, and analysing customer, product, and order datasets.

## 1. Customer Data Cleaning

### Key Cleaning Steps

- Standardised city names.
- Consolidated city spellings into six valid cities.
- Normalised gender values.
- Treated invalid ages as missing.
- Imputed missing ages using city-level median values.
- Converted signup dates into datetime format.

### Final Customer Summary

| Gender | Count |
|:---|---:|
| Female | 610 |
| Male | 560 |
| Unknown | 30 |
| **Total** | **1,200** |

All missing ages were successfully imputed.

## 2. Order Data Cleaning

### Key Cleaning Steps

- Removed duplicate records.
- Standardised timestamps.
- Converted order amounts to numeric values.
- Recalculated missing order amounts.
- Corrected invalid delivery times.
- Imputed missing delivery durations for completed orders.

### Final Order Summary

| Metric | Value |
|:---|---:|
| Final Orders | 12,309 |
| Completed Orders | 11,110 |
| Cancelled Orders | 1,199 |
| Missing Order Amounts | 0 |
| Revenue | ₹2,998,668.80 |

## 3. Data Validation

All required project checkpoints were successfully validated.

**Validation Result:**

```text
ALL CHECKPOINTS PASSED
```

## 4. SQL Analysis Highlights

| Query | Result |
|:---|---:|
| Customers spending above ₹8,000 | 30 |
| Products above average price | 11 |
| Customers without completed orders | 25 |
| Customers above average spend | 550 |

### Revenue Summary

| Metric | Value |
|:---|---:|
| Total Revenue | ₹2,998,668.80 |

### Highest Revenue Combination

| City | Category | Revenue |
|:---|:---|---:|
| Bengaluru | Electronics | ₹233,909.45 |

---

# 🤖 PART B: CUSTOMER SEGMENTATION AND LAPSE PREDICTION

## Objective

Understand customer purchasing behaviour and identify customers likely to become inactive.

## 1. RFM Analysis

RFM metrics were calculated using completed orders.

| Metric | Value |
|:---|---:|
| Customers Analysed | 1,175 |
| Median Recency | 19 Days |
| Mean Frequency | 9.46 |
| Mean Monetary Value | ₹2,552.06 |

## 2. Customer Segmentation

K-Means clustering was applied after feature standardisation.

### Customer Segments

1. Premium Customers
2. Frequent Loyal Customers
3. Regular Customers
4. Dormant Customers

### PCA Results

| Component | Explained Variance |
|:---|---:|
| PC1 | 63.4% |
| PC2 | 21.8% |
| **Total** | **85.2%** |

The first two principal components explain 85.2% of the total variance.

## 3. Lapse Prediction

The following machine learning models were evaluated:

- Logistic Regression
- Random Forest

### Final Model

**Selected Model: Logistic Regression**

### Model Performance

| Metric | Logistic Regression |
|:---|---:|
| Precision | 0.655 |
| Recall | 0.809 |
| F1 Score | 0.724 |

### Generated Outputs

| Output File | Description |
|:---|:---|
| `outputs/customer_segmentation.csv` | Customer segment assignments |
| `outputs/lapse_model.joblib` | Trained lapse prediction model |
| `outputs/retention_list.csv` | Customer retention list |

---

# 🎫 PART C: SUPPORT TICKET TRIAGE WITH GUARDRAILS

## Objective

Develop a secure support ticket processing system with safety checks and automated routing.

## 1. Input Guardrails

### Validation Rules

- Skip empty tickets.
- Flag excessively long tickets.
- Protect processing budget.

### Guardrail Results

| Status | Count |
|:---|---:|
| Eligible | 156 |
| Skipped Empty | 4 |
| Flagged Long | 4 |
| **Total** | **164** |

## 2. PII Redaction

The following sensitive information was removed:

- Email Addresses
- Phone Numbers
- Order IDs

### Redaction Results

| Entity | Count |
|:---|---:|
| Emails | 55 |
| Phones | 91 |
| Order IDs | 132 |

No sensitive data remained after validation.

## 3. Ticket Classification

### Classification Categories

- Billing
- Delivery
- Technical
- Fraud

### Prompt Performance

| Approach | Accuracy |
|:---|---:|
| Zero-Shot | 85.7% |
| Few-Shot | 100% |

## 4. Automated Ticket Routing

| Support Team | Routing Conditions |
|:---|:---|
| Security Team | Fraud cases and high-priority tickets |
| Premium Desk | Premium customers and high-priority tickets |
| Support Queue | Standard support tickets |
| Human Review | Empty tickets, long tickets, and invalid model responses |

### Generated Outputs

- `outputs/triage_results.csv`
- `outputs/triage_budget_demo.csv`

---

# 📚 PART D: POLICY ASSISTANT AND REFUND AGENT

## Objective

Develop a Retrieval-Augmented Generation (RAG) assistant and automated refund agent.

## 1. Document Chunking

Policy documents were divided into smaller chunks to support information retrieval.

| Document | Chunks |
|:---|---:|
| refund_policy.txt | 4 |
| delivery_policy.txt | 3 |
| payment_policy.txt | 3 |
| escalation_policy.txt | 3 |
| privacy_policy.txt | 2 |
| **Total** | **15** |

## 2. Retrieval Evaluation

| Metric | Result |
|:---|---:|
| Expected Document Found | 12 / 12 |
| Expected Facts Found | 12 / 12 |
| Unanswerable Questions Handled | 2 / 2 |

The retrieval system successfully retrieved the expected documents and facts during evaluation.

## 3. Refund Agent Tools

The ReAct-style refund agent uses the following tools:

| Tool | Purpose |
|:---|:---|
| `get_order()` | Retrieves order information |
| `search_policy()` | Searches relevant policy documents |
| `calculate_refund()` | Calculates eligible refund amounts |
| `issue_refund()` | Processes refunds |
| `escalate_to_human()` | Escalates cases requiring human evaluation |

## 4. Agent Outcomes

| Scenario | Status |
|:---|:---|
| S1 | REFUND |
| S2 | REFUND |
| S3 | ESCALATE |
| S4 | DENIED |
| S5 | DENIED |
| S6 | NOT_FOUND |
| S7 | FALLBACK_MAX_ITERATIONS |

## 5. Safety Mechanisms

The refund agent includes the following safety mechanisms:

- Maximum Iteration Protection
- Token Limit Protection
- Timeout Protection
- Human Escalation for complex cases

### Generated Outputs

- `outputs/agent_runs.jsonl`
- `outputs/refund_ledger.jsonl`

---

# ⚠️ LIMITATIONS

The project has the following limitations:

1. Uses synthetic data for demonstration purposes.
2. Customer behaviour may change over time.
3. TF-IDF retrieval depends on keyword matching.
4. Uses a mock LLM instead of a production language model.
5. The retention list should be considered illustrative rather than fully leakage-free.

---

# 🔮 NEXT STEPS

The following improvements can enhance the project further:

- Replace TF-IDF retrieval with semantic vector embeddings.
- Enhance lapse prediction using behavioural and temporal features.
- Develop business intelligence dashboards.
- Deploy ticket triage as a real-time service.
- Integrate with production databases and customer support platforms.

---

# 🎯 CONCLUSION

This project successfully developed an end-to-end **Instamart Customer Intelligence and Support Copilot**.

The solution combines:

- Data Engineering
- SQL Analytics
- Machine Learning
- Customer Segmentation
- Support Ticket Automation
- Retrieval-Augmented Generation (RAG)
- AI Agent Workflows

The project demonstrates practical applications of modern data science and AI technologies for improving customer retention, automating customer support operations, and supporting business decision-making.

It showcases how multiple data and AI technologies can work together in a unified system to solve real-world business problems.
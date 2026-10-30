# INSTAMART CUSTOMER INTELLIGENCE AND SUPPORT COPILOT
      
      The project develops an Instamart Customer Intelligence and Support Copilot for a Swiggy Instamart company which delivers instant groceries. It creates an end-to-end internal tool that combines data foundation,machine learning,information retrieval and AI agent workflow. 

# OVERVIEW 
      PART A : DATA FOUNDATION
      This part works on data cleaning and validation on raw data such as customer,product and order.The cleaned data is stored in a SQLite database and analysed using SQL and pandas. 
      
      PART B : CUSTOMER SEGMENTATION AND LAPSE PREDICTION
      The customer behaviour is analysed using RFM(Recency,Frequency,monetary)metrics,Customers are segmented using K-Means Clustering and lapse prediction model is developed to predict the customers.

      Part C : SUPPORT TICKET WITH GUARDRAIL
      This processes customer support tickets by applying input guardrails and privacy protection techniques.Sensitive information is redacted,tickets are classified into categories and they are routed to appropriate support team.

      Part D : POLICY ASSISTANT AND REFUND AGENT
      Finally Retrieval Augmented Generation(RAG)policy is built to answer the policy related questions using company policy documents.A ReAct style refund agent are built to answer policy questions and automate refund decisions.Escalate cases when human evaluation is required.
      
## TECHNOLOGY

Python,Pandas,NumPy,SQLite,SQL,Scikit-learn,K-Means,Logistic Regression,Random Forest, TF-IDF,RAG and AI Agents.

## RESULTS

| Component | Results |
|---|---|
| Data Foundation | 1,200 customers, 40 products, 12,309 cleaned orders |
| Total Revenue | ₹2,998,668.80 |
| Customer Segmentation | 4 segments; PCA explained variance: 85.2% |
| Lapse Prediction | F1-score: 0.724; Recall: 0.809 |
| Ticket Triage | 164 tickets; 100% few-shot accuracy |
| PII Redaction | 55 emails, 91 phone numbers, 132 order IDs |
| RAG Evaluation | 12/12 expected documents and facts retrieved |
| Refund Agent | Refund, denial, escalation, and fallback workflows |

## CONCLUSION

This project successfully developed a Customer Intelligence and Support Copilot by combining data foundation,machine learning and AI support automation.It demonstrates how machine learning and AI agents can help businesses improve customer retention and support operations.

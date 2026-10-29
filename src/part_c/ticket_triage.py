import sys
import os
import re
import time
import random
import json
from sklearn.metrics import accuracy_score

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
sys.path.append(project_root)
from mock_llm import (chat,reset,est_tokens,TransientLLMError)

sys.path.append(project_root)
from mock_llm import (chat,reset,TransientLLMError)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".." )))
import pandas as pd
from mock_llm import est_tokens
#INPUT GUARDRAIL
MAX_INPUT_TOKENS=400
tickets = pd.read_csv("data/raw/tickets.csv",keep_default_na=False)
print("Shape:", tickets.shape)
def get_ticket_status(text):
    if str(text).strip() == "":
    
        return "skipped_empty"
    if est_tokens(text) > MAX_INPUT_TOKENS:
        return "flagged_long"
    return "eligible"
tickets["status"]=tickets["text"].apply(get_ticket_status)
print("\nStatus Counts")
print(tickets["status"].value_counts())
print("\nLong Ticket Token Counts")
long_tickets=tickets[tickets["status"]=="flagged_long"]
for text in long_tickets["text"]:
    print(est_tokens(text))
#CREATE REDACTION FUNCTION
email_count = 0
phone_count = 0
order_count = 0
def redact_text(text):
    global email_count
    global phone_count
    global order_count
    #EMAIL
    text, count = re.subn(r'[\w.+-]+@[\w-]+\.[\w.]+','[EMAIL]',text)
    email_count += count
    #PHONE
    text, count = re.subn(r'\b[6-9]\d{9}\b','[PHONE]',text)
    phone_count += count
    #ORDER ID
    text, count = re.subn(r'ORD-\d{6}','[ORDER_ID]',text)
    order_count += count
    return text    
#APPLY REDACTION
tickets["redacted_text"]=tickets["text"]
eligible_mask=(tickets["status"] == "eligible")
tickets.loc[eligible_mask,"redacted_text"]=tickets.loc[eligible_mask,"text"].apply(redact_text)
#PRINT COUNTS
print("\nREDACTION RESULTS")
print("Emails:", email_count)
print("Phones:", phone_count)
print("Order IDs:", order_count)
print("Total:",email_count +phone_count +order_count)
#NOTHING REMAINS
remaining_email = 0
remaining_phone = 0
remaining_order = 0
for text in tickets["redacted_text"]:
    remaining_email += len(re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+',text))
    remaining_phone += len(re.findall(r'\b[6-9]\d{9}\b',text))
    remaining_order += len(re.findall(r'ORD-\d{6}',text))
print("\nRemaining after redaction")
print("Emails:", remaining_email)
print("Phones:", remaining_phone)
print("Order IDs:", remaining_order)
tickets.to_csv("outputs/redacted_tickets.csv",index=False)
#ZERO SHOT PROMPT
ZERO_SHOT_PROMPT = """
CLASSIFY
Allowed categories:
billing
delivery
technical
fraud
Return JSON only.
Format:
{"category":"...","reason":"..."}"""
#FEW SHOT PROMPT
FEW_SHOT_PROMPT = """
CLASSIFY
Allowed categories:
billing
delivery
technical
fraud
Return JSON only.
Format:
{"category":"...","reason":"..."}
EXAMPLES:
Ticket:
I was charged twice for my order.
Response:
{"category":"billing","reason":"double charge"}
Ticket:
Someone hacked my account and used my wallet balance.
Response:
{"category":"fraud","reason":"account compromise"}"""
print(ZERO_SHOT_PROMPT)
print(FEW_SHOT_PROMPT)
#RESILIENT CALLS
BASE_DELAY=0.05
MAX_RETRIES=3
def call_with_retry(ticket_id, system_prompt, user_text):
    for retry in range(MAX_RETRIES + 1):
        try:
           response=chat([{"role": "system","content": system_prompt},
                {"role": "user","content": user_text}])
           return response
        except TransientLLMError:
            if retry==MAX_RETRIES:
                raise 
            wait=(BASE_DELAY* (2 ** retry)* random.uniform(0.9, 1.15))
            print(f"{ticket_id} retry={retry} "f"wait={wait:.4f}")
            time.sleep(wait)
reset()
#CALL MODEL RETRY FUNCTION
eligible_tickets=tickets[tickets["status"] == "eligible"]
sample_ticket=eligible_tickets.iloc[0]
response=call_with_retry(
    sample_ticket["ticket_id"],
    ZERO_SHOT_PROMPT,
    sample_ticket["redacted_text"])
print(response.choices[0].message.content)
#VALIDATE ANSWER
ALLOWED_CATEGORIES={"billing","delivery","technical","fraud"}
def validate_response(text):
    try:
        data=json.loads(text)
        category=data.get("category")
        if category in ALLOWED_CATEGORIES:
            return ("classified_json",category)
        return ("flagged_invalid_output","")
    except:
        words=set(re.findall(r"[a-z]+",text.lower()))
        matches=(ALLOWED_CATEGORIES &words)
        if len(matches)==1:
           return ("classified_keyword",list(matches)[0])
        return("flagged_invalid_output","")
#PROCESS ELIGIBLE TICKETS
reset()
results=[]
for _, row in tickets.iterrows():
    if row["status"] != "eligible":
       continue
    response=call_with_retry(row["ticket_id"],FEW_SHOT_PROMPT,row["redacted_text"])
    text=(response.choices[0].message.content)
    status,category=(validate_response(text))
    results.append({"ticket_id": row["ticket_id"],
    "customer_id": row["customer_id"],
    "status": status,
    "category": category,
    "true_category": row["true_category"]})
#COUNT STATUSES
results_df=pd.DataFrame(results)
print(results_df["status"].value_counts())
#COMPARE FEW SHOT & ZERO SHOT
#CALCULATE ACCURACY
classified=results_df[results_df["status"]!="flagged_invalid_output"]
accuracy=accuracy_score(classified["true_category"],classified["category"])
print(accuracy)
tokens_used=0
for _, row in tickets.iterrows():
    if row["status"]!="eligible":
        continue
    response=call_with_retry(row["ticket_id"],FEW_SHOT_PROMPT,row["redacted_text"])
    tokens_used+=response.usage.total_tokens
    text=response.choices[0].message.content
    status,category=validate_response(text)
    results.append({
        "ticket_id":row["ticket_id"],
        "customer_id":row["customer_id"],
        "status":status,
        "category":category,
        "true_category":row["true_category"]
    })
results_df=pd.DataFrame(results)
classified=results_df[results_df["status"]!="flagged_invalid_output"]
accuracy=accuracy_score(classified["true_category"],classified["category"])
classified_count=len(classified)
print("Accuracy:", round(accuracy * 100, 2))
print("Total Tokens:", tokens_used)
print("Tokens Per Ticket:",round(tokens_used / classified_count, 2))
#LOAD CUSTOMER SEGMENTS
segments=pd.read_csv("outputs/customer_segments.csv")
segments=segments[["customer_id","segment_name","is_premium"]]
#MERGE RESULTS
results_df=pd.DataFrame(results)
print(results_df.columns.tolist())
results_df=results_df.merge(segments,on="customer_id",how="left")
#ROUTING FUNCTION
def route_ticket(row):
    if row["status"] in ["skipped_empty","flagged_long","flagged_invalid_output","budget_exhausted"]:
        return pd.Series(["NORMAL","human_review"])
    if row["category"]=="fraud":
        return pd.Series(["HIGH","security_team"])
    if row["is_premium"]==True:
        return pd.Series(["HIGH","premium_desk"])
    return pd.Series(["NORMAL","support_queue"])
#APPLY ROUTE
results_df[["priority","route"]]=results_df.apply(route_ticket,axis=1)
#APPLY TOKEN COLUMNS
results_df["tokens_used"]=(round(tokens_used/len(results_df),2))
#OUTPUT
final_df=results_df[["ticket_id","customer_id","status","category","segment_name","priority","route","tokens_used"]]
#PARTC OUTPUT
final_df.to_csv("outputs/triage_results.csv",index=False)
print("triage_results.csv saved")
#BUDGET
budget_demo=final_df.copy()
budget_demo.loc[100:,"status"]="budget_exhausted"
budget_demo.to_csv("outputs/triage_budget_demo.csv",index=False)
print("triage_budget_demo.csv saved")
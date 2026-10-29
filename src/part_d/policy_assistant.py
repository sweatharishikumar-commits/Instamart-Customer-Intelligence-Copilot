import os
import pandas as pd
import sys
import sqlite3
import json
import time
project_root=os.path.abspath(os.path.join(os.path.dirname(__file__),"..",".."))
sys.path.append(project_root)
from datetime import datetime
from mock_llm import chat
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#READ POLICY FILE
POLICY_FOLDER="data/policies"
documents=[]
for file_name in os.listdir(POLICY_FOLDER):
    if file_name.endswith(".txt"):
        path=os.path.join(POLICY_FOLDER,file_name)
        with open(path,"r",encoding="utf-8") as f:
            text=f.read()
        documents.append((file_name,text))
#CHUNK FUNCTION
def chunk_text(text,chunk_size=40,overlap=10):
    words=text.split()
    chunks=[]
    step=(chunk_size-overlap)
    for start in range(0,len(words),step):
        end=start + chunk_size
        chunk_words=words[start:end]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if end>=len(words):
            break
    return chunks
#CHUNK TABLE
chunks=[]
for source, text in documents:
    for chunk in chunk_text(text):
        chunks.append({"source": source,"text": chunk})
#COUNT CHUNKS
chunk_df=pd.DataFrame(chunks)
print(chunk_df.groupby("source").size())
print("Total Chunks:",len(chunk_df))
#TF IDF MODEL
vectorizer=TfidfVectorizer()
tfidf_matrix=vectorizer.fit_transform(
chunk_df["text"])
#CREATE RETRIVAL FUNCTION
def retrieve(query, k=3):
    query_vec=vectorizer.transform([query])
    similarities=cosine_similarity(query_vec,tfidf_matrix)[0]
    chunk_df["score"]=similarities
    top_chunks=(chunk_df.sort_values("score",ascending=False).head(k))
    results=[]
    for _, row in top_chunks.iterrows():
        results.append({"source": row["source"],"score": row["score"],"text": row["text"]})
    return results
#TEST RETRIVAL
results=retrieve("refund policy late delivery")
for r in results:
    print(r["source"],round(r["score"],4))
retrieve("refund policy late delivery")
#RAG AUGMENT & ANSWER
def answer(question):
    retrieved=retrieve(question,k=3)
    context = ""
    for chunk in retrieved:
        context += (f"[{chunk['source']}]\n"f"{chunk['text']}\n\n")
    system_prompt = """
POLICY ASSISTANT
Answer only from the provided context.
If the answer cannot be found,
say:
I could not find that information in the policy documents.
"""
    user_prompt=("CONTEXT:\n"+ context+ "\nQUESTION:\n"+ question)
    response=chat([{"role": "system","content": system_prompt},
        {"role": "user","content": user_prompt}])
    return {"answer":response.choices[0].message.content,
            "sources":[r["source"] for r in retrieved]}
#TEST QUESTIONS
result=answer("What delivery time makes a completed order eligible for a full refund?")
print("\nANSWER")
print(result["answer"])
print("\nSOURCES")
print(result["sources"])
#EVALUATION
eval_df=pd.read_csv("data/raw/policy_eval.csv")
retrieval_hits=0
fact_hits=0
fallback_hits=0
for _, row in eval_df.iterrows():
    result=answer(row["question"])
    sources=result["sources"]
    response_text=result["answer"]
    expected_doc=row["expected_doc"]
    expected_fact=str(row["expected_fact"])
    # Retrieval check
    if (expected_doc!="NONE"and expected_doc in sources):
        retrieval_hits+=1
    # Fact check
    if (expected_doc!="NONE"and expected_fact in response_text):
        fact_hits+=1
    # Fallback check
    if (expected_doc=="NONE"and response_text.startswith("I could not find")):
        fallback_hits+=1
print("\nEvaluation Results")
print("Retrieval Hits:",retrieval_hits)
print("Fact Hits:",fact_hits)
print("Fallback Hits:",fallback_hits)
#DEFINE TOOLS & CREATE TOOL SPECIFICATION
TOOLS_SPEC=[{"name":"get_order","description":"Get order information from database."},
            {"name":"search_policy","description":"Search policy documents."},
            {"name":"calculate_refund","description":"Calculate refund amount."},
            {"name":"issue_refund","description":"Issue refund."},
            {"name":"escalate_to_human","description":"Escalate refund."}]
#TOOL1 get_order
def get_order(order_id):
    conn=sqlite3.connect("data/instamart.db")
    query="""SELECT order_id,status,order_amount,delivery_minutes
    FROM orders
    WHERE order_id=?"""
    row=conn.execute(query,(order_id,)).fetchone()
    conn.close()
    if row is None:
        return{"error":"order not found"}
    return{"order_id":row[0],"status":row[1],"order_amount":float(row[2]),"delivery_minutes":None if row[3] is None
        else int(row[3])}
#TOOL2 SEARCH POLICY
def search_policy(query):
    results=retrieve(query,k=3)
    return{"results": results}
#TOOL3 CALCULATE REFUND
def calculate_refund(order_amount,delivery_minutes):
    if delivery_minutes > 45:
        refund = order_amount
    else:
        refund = 0
    return {"refund_inr":round(refund, 2)}
#TOOL4 ISSUE REFUND
os.makedirs("outputs",exist_ok=True)
def issue_refund(order_id,refund_inr):
    record={"timestamp":datetime.now().isoformat(),
            "tool":"issue_refund",
            "order_id":order_id,
            "refund_inr":refund_inr}
    with open("outputs/refund_ledger.jsonl","a",encoding="utf-8") as f:
        f.write(json.dumps(record)+ "\n")
    return{"refund_inr":refund_inr}
#ESCULATE TO HUMAN
def escalate_to_human(order_id,refund_inr):
    record={"timestamp":datetime.now().isoformat(),
        "tool":"escalate_to_human",
        "order_id":order_id,
        "refund_inr":refund_inr}
    with open("outputs/refund_ledger.jsonl","a",encoding="utf-8") as f:
      f.write(json.dumps(record)+ "\n")
    return{"refund_inr":refund_inr}
#TOOL MAP
TOOL_MAP={"get_order":get_order,
   "search_policy":search_policy,
    "calculate_refund":calculate_refund,
    "issue_refund":issue_refund,
    "escalate_to_human":escalate_to_human}
print(get_order("ORD-999999"))
print(search_policy("refund policy late delivery"))
#RUN AGENT
def run_agent(user_message,
    scenario_id,
    max_iterations=6,
    token_limit=6000,
    time_limit_seconds=10):
    messages=[{"role":"system","content": "AGENT"},
              {"role":"user","content":user_message}]
    steps=[]
    llm_calls=0
    tokens_used=0
    start_time=time.monotonic()
    for _ in range(max_iterations):
        # TIMEOUT CHECK
        elapsed=(time.monotonic()- start_time)
        if elapsed>=time_limit_seconds:
            return {
                "status": "FALLBACK_TIMEOUT",
                "final_answer": "Human handoff due to timeout.",
                "steps": steps,
                "llm_calls": llm_calls,
                "tokens_used": tokens_used}
        response=chat(messages,tools=TOOLS_SPEC)
        llm_calls+=1
        tokens_used+=(response.usage.total_tokens)
        # TOKEN LIMIT CHECK
        if tokens_used>token_limit:
            return {
                "status": "FALLBACK_TOKEN_LIMIT",
                "final_answer": "Human handoff due to token limit.",
                "steps": steps,
                "llm_calls": llm_calls,
                "tokens_used": tokens_used }
        message=(response.choices[0].message)
        # FINAL ANSWER
        if not message.tool_calls:
            final_answer=(message.content)
            status=(final_answer.split(":")[0])
            return {
                "status": status,
                "final_answer": final_answer,
                "steps": steps,
                "llm_calls": llm_calls,
                "tokens_used": tokens_used}
        # EXECUTE TOOL
        tool_call=(message.tool_calls[0])
        tool_name=(tool_call.name)
        arguments=(tool_call.arguments)
        result=TOOL_MAP[tool_name](**arguments)
        steps.append({"tool":tool_name,"arguments":arguments,"observation":result})
        messages.append({"role":"assistant","content":None,
            "tool_calls":[{"id":tool_call.id,"name": tool_name,"arguments": arguments}]})
        messages.append({"role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_name,
            "content": json.dumps(result)})
    # MAX ITERATIONS
    return {
        "status":"FALLBACK_MAX_ITERATIONS",
        "final_answer":"Max iterations reached.",
        "steps":steps,
        "llm_calls":llm_calls,
        "tokens_used":tokens_used}

scenarios=pd.read_csv("data/raw/agent_scenarios.csv")
with open("outputs/agent_runs.jsonl","w",encoding="utf-8")as f:
    for _, row in scenarios.iterrows():
        result=run_agent(row["message"],row["scenario_id"])
        record={"scenario_id": row["scenario_id"],
            "status":result["status"],
            "final_answer":result["final_answer"],
            "llm_calls":result["llm_calls"],
            "tokens_used":result["tokens_used"],
            "steps":result["steps"]}
        f.write(json.dumps(record)+ "\n")

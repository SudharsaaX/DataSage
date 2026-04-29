from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import generate_sql, classify_intent
from app.db import execute_query
from app.safety import is_safe_query

app = FastAPI()


class QueryRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "AI SQL Assistant API is running"}


@app.post("/query")
def run_query(request: QueryRequest):
    user_input = request.question

    # 🧠 Detect intent using LLM
    intent = classify_intent(user_input)

    # 💬 Chat mode
    if intent == "CHAT":
        return {
            "question": user_input,
            "response": "👋 Hi! I can help you query your database.\n\nTry:\n- Show all users\n- Show users in Chennai\n- Show orders above 3000"
        }

    # 🗄️ SQL mode
    sql_query = generate_sql(user_input)

    # 🛡️ Safety check
    if not is_safe_query(sql_query):
        return {
            "error": "Unsafe query detected",
            "generated_sql": sql_query
        }

    # Execute query
    result = execute_query(sql_query)

    return {
        "question": user_input,
        "sql": sql_query,
        "result": result
    }
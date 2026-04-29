import requests
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"


def clean_sql(response: str) -> str:
    response = response.strip()

    # Remove markdown
    response = response.replace("```sql", "").replace("```", "")

    # Extract SELECT query
    match = re.search(r"(SELECT .*?;)", response, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    # fallback
    lower_resp = response.lower()
    if "select" in lower_resp:
        start = lower_resp.find("select")
        return response[start:].strip()

    return response.strip()


def generate_sql(user_input: str) -> str:
    prompt = f"""
You are a strict MySQL query generator.

Database schema:
Table users(id, name, age, city)
Table orders(id, user_id, amount)

Rules:
- ONLY generate a valid SELECT SQL query
- DO NOT explain anything
- DO NOT add extra text
- Use single quotes for strings
- End query with semicolon ;

User Input: {user_input}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return clean_sql(result["response"])


def explain_sql(sql_query: str) -> str:
    prompt = f"""
Explain this SQL query in simple English:

{sql_query}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return result["response"].strip()


def classify_intent(user_input: str) -> str:
    prompt = f"""
Classify the user input into ONE word:

SQL → if it's asking about database query
CHAT → if it's normal conversation

Examples:
"Show all users" → SQL
"List orders above 3000" → SQL
"Hi" → CHAT
"What can you do?" → CHAT

User Input: {user_input}

Answer ONLY one word: SQL or CHAT
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()["response"].strip().upper()

    if "SQL" in result:
        return "SQL"
    return "CHAT"
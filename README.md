# DataSage

DataSage is an AI-powered SQL assistant that lets you interact with a MySQL database using natural language. Instead of writing SQL queries manually, you can simply ask questions in plain English and get results instantly.

---

## Overview

DataSage combines a local large language model with a database backend to translate natural language into SQL queries, execute them safely, and present the results in a clean interface. It also explains the generated SQL so users can understand what is happening behind the scenes.

---

## Features

* Natural language to SQL conversion using a local LLM
* Safe query execution (only SELECT queries allowed)
* SQL query explanation in plain English
* Interactive chat-based interface
* Dynamic sidebar filters for result exploration
* CSV export for filtered data
* Local execution with no external API dependency

---

## Tech Stack

* Python
* FastAPI
* Streamlit
* MySQL
* Ollama (Llama 3.1 model)
* Pandas

---

## Project Structure

```
ai-sql-assistant/
│
├── app/
│   ├── main.py        # FastAPI backend
│   ├── llm.py         # LLM logic (SQL generation + explanation)
│   ├── db.py          # Database connection
│   ├── safety.py      # Query safety checks
│   ├── ui.py          # Streamlit frontend
│
├── .env               # Environment variables (not committed)
├── .env.example       # Example environment config
├── requirements.txt
├── README.md
```

---

## How It Works

1. User enters a question in natural language
2. LLM converts it into a SQL query
3. Safety layer ensures only read-only queries
4. Query is executed on MySQL
5. Results are returned and displayed
6. LLM explains the SQL query

---

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/your-username/datasage.git
cd datasage
```

---

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Setup Environment Variables

Create a `.env` file based on `.env.example`:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=ai_sql_db
```

---

### 5. Run Local LLM (Ollama)

Make sure Ollama is installed and run:

```
ollama run llama3.1:8b
```

---

### 6. Start Backend Server

```
uvicorn app.main:app --reload
```

---

### 7. Start Frontend

```
streamlit run app/ui.py
```

---

## Example Queries

* Show all users
* Show users in Chennai
* Show users older than 25
* Show orders above 3000

---

## Safety

* Only SELECT queries are allowed
* Dangerous operations like DELETE, UPDATE, DROP are blocked
* Fallback queries prevent unintended execution

---

## Screenshots

### Main Interface
![Main UI](outputs/main-interface.png)

### Demo
![Demo](assets/demo.gif)

---

## Future Improvements

* Better intent detection
* Query optimization
* Advanced data visualizations
* Deployment support
* User authentication

---

## Author

Sudharsan S

---

## License

This project is for educational and demonstration purposes.

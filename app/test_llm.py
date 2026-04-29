from llm import generate_sql

query = "Show all users in Chennai"
sql = generate_sql(query)

print(sql)
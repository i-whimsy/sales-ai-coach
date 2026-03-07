import sqlite3

conn = sqlite3.connect('sales_coach.db')
cursor = conn.cursor()

# Check ai_models table
cursor.execute("SELECT id, name, type, category FROM ai_models")
models = cursor.fetchall()
print("Models in database:")
for model in models:
    print(f"  ID: {model[0]}, Name: {model[1]}, Type: {model[2]}, Category: {model[3]}")

conn.close()
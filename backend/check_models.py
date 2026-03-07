import sqlite3

conn = sqlite3.connect('sales_coach.db')
cursor = conn.cursor()

# Check current models
cursor.execute("SELECT id, name, type, category, provider, is_default FROM ai_models")
models = cursor.fetchall()
print('Current models:')
for model in models:
    print(f'  ID: {model[0]}, Name: {model[1]}, Type: {model[2]}, Category: {model[3]}, Provider: {model[4]}, Default: {model[5]}')

# Check categories
cursor.execute("SELECT DISTINCT category FROM ai_models")
categories = cursor.fetchall()
print('\nCurrent categories:')
for cat in categories:
    print(f'  {cat[0]}')

conn.close()
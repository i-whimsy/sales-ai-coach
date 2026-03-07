import sqlite3

conn = sqlite3.connect('sales_coach.db')
cursor = conn.cursor()

# Check task_model_configs table
cursor.execute("SELECT task_name, description, prompt_config FROM task_model_configs")
tasks = cursor.fetchall()
print("Tasks in database:")
for task in tasks:
    print(f"  Name: {task[0]}")
    print(f"  Description: {task[1]}")
    print(f"  Prompt: {task[2]}")
    print()

conn.close()
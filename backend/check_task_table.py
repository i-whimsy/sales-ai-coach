import sqlite3

conn = sqlite3.connect('sales_coach.db')
cursor = conn.cursor()

# 检查task_model_configs表结构
cursor.execute("PRAGMA table_info(task_model_configs)")
columns = cursor.fetchall()
print("Table structure for task_model_configs:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.close()
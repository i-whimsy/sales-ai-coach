import sqlite3

conn = sqlite3.connect('sales_coach.db')
cursor = conn.cursor()

# 检查表结构
cursor.execute("PRAGMA table_info(ai_models)")
columns = cursor.fetchall()
print("Table structure for ai_models:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.close()
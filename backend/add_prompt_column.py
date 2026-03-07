import sqlite3

conn = sqlite3.connect('sales_coach.db')
cursor = conn.cursor()

# 添加prompt_config字段到task_model_configs表
try:
    cursor.execute("ALTER TABLE task_model_configs ADD COLUMN prompt_config TEXT")
    print("Added prompt_config column to task_model_configs table")
except sqlite3.OperationalError as e:
    print(f"Column may already exist: {e}")

# 检查更新后的表结构
cursor.execute("PRAGMA table_info(task_model_configs)")
columns = cursor.fetchall()
print("\nUpdated table structure for task_model_configs:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

conn.commit()
conn.close()

import sys
import requests
from database import SessionLocal
import models

def test_encoding():
    print("=== Encoding Information ===")
    print(f"Python version: {sys.version}")
    print(f"Default encoding: {sys.getdefaultencoding()}")
    print(f"File system encoding: {sys.getfilesystemencoding()}")
    try:
        import locale
        print(f"Locale: {locale.getdefaultlocale()}")
        print(f"Locale encoding: {locale.getlocale()}")
    except:
        pass

    print()

    db = SessionLocal()

    print("=== Tasks from Database ===")
    
    tasks = db.query(models.TaskModelConfig).all()
    
    if tasks:
        for task in tasks:
            print(f"Task ID: {task.id}")
            print(f"  Raw:    '{repr(task.task_name)}'")
            print(f"  Decoded: '{task.task_name}'")
            
            try:
                print(f"  UTF-8:   '{task.task_name.encode('cp936').decode('utf-8')}'")
            except:
                pass
                
            print()
    else:
        print("No tasks found")

    print()
    
    print("=== Calling API ===")
    base_url = "http://localhost:8001/api/v1"

    try:
        print(f"Calling {base_url}/tasks")
        response = requests.get(f"{base_url}/tasks")
        data = response.json()
        
        print(f"API Status: {response.status_code}")
        print(f"API Response:")
        
        for task in data.get("tasks"):
            print(f"  Task: '{task['task_name']}'")
            print(f"    Description: '{task['description']}'")
            
    except Exception as e:
        print(f"Error calling API: {type(e)} - {e}")
        import traceback
        print(traceback.format_exc())

    db.close()

if __name__ == "__main__":
    test_encoding()

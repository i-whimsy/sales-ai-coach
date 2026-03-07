
from main import app
from database import SessionLocal
import models

db = SessionLocal()

print('=== All task configurations in database ===')

tasks = db.query(models.TaskModelConfig).all()

for task in tasks:
    print(f'ID: {task.id}')
    print(f'Task Name: "{task.task_name}"')
    print(f'Description: "{task.description}"')
    print(f'Required Tags: {task.required_tags}')
    print(f'Default Model ID: {task.default_model_id}')
    
    if task.default_model_id:
        model = db.query(models.AIModel).filter(models.AIModel.id == task.default_model_id).first()
        if model:
            print(f'Default Model: "{model.name}"')
    
    print(f'Fallback Model IDs: {task.fallback_model_ids}')
    print()

print('=== All model tags in database ===')

tags = db.query(models.ModelTag).all()

for tag in tags:
    print(f'ID: {tag.id}')
    print(f'Name: "{tag.name}"')
    print(f'Description: "{tag.description}"')
    print(f'Color: {tag.color}')
    print()

db.close()

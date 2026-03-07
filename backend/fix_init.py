import json
# Read the file
with open('init_model_system.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace config: { ... } with config: json.dumps(...)
content = content.replace('"config": {"timeout": 60}', '"config": "{\\"timeout\\": 60}"')
content = content.replace('"config": {}', '"config": "{}"')

# Write back
with open('init_model_system.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed config in init_model_system.py')

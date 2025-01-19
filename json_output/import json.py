import os
import json

data_dir = 'json_output'
file_path = os.path.join(data_dir, 'facilities_data.json')

# Read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

# Explore and print the structure
def explore_json(data, indent=0):
    indent_str = ' ' * indent
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{indent_str}{key}:")
            explore_json(value, indent + 2)
    elif isinstance(data, list):
        print(f"{indent_str}List of {len(data)} items:")
        for item in data:
            explore_json(item, indent + 2)
    else:
        print(f"{indent_str}{data}")

explore_json(data)
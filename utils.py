import json

def get_json(file_path):
    with open(file_path, 'r') as fi:
        return json.load(fi)
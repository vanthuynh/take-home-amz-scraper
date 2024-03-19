# query_reader.py

import json

def read_queries(file_path):
    with open(file_path) as f:
        queries = json.load(f)
    return queries

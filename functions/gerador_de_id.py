from config_db import db

def generate_unique_id(collection):
    current_id = 1
    while db[collection].find_one({"id": current_id}):
        current_id += 1
    return current_id
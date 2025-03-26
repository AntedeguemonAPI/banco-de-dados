from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Carrega as variáveis do .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['meuBanco']
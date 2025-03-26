# app.py
from flask import Flask
from routes.csv_routes import csv_bp
from routes.preprocessamento_routes import preprocessamento_bp
from routes.processo_routes import processamento_bp
from routes.ids_gerais import ids_gerais_bp
from config_db import db
import os

app = Flask(__name__)

# Registrando os blueprints
app.register_blueprint(csv_bp, url_prefix='/csv')
app.register_blueprint(preprocessamento_bp, url_prefix='/preprocessamento')
app.register_blueprint(processamento_bp, url_prefix='/processamento')
app.register_blueprint(ids_gerais_bp, url_prefix='/ids')

try:  
    print("✅ Conexão estabelecida com sucesso!")
    print("📦 Bancos de dados disponíveis:", db)
    
except Exception as e:
    print("⚠️ Falha na conexão com o MongoDB:")
    print(e)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
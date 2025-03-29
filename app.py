from flask import Flask
from flask_restx import Api
from routes.csv_routes import csv_bp
from routes.preprocessamento_routes import preprocessamento_bp
from routes.processo_routes import processamento_bp
from routes.ids_gerais import ids_gerais_bp
from config_db import db
from routes.processo_routes import processamento_ns  # Importe o Namespace do processamento

app = Flask(__name__)

# Inicialize a API Flask-RESTX
api = Api(app, version='1.0', title='API de Gerenciamento do Banco de Dados',
          description='Uma API para gerenciar os endpoints do banco de dados.')

# Registre os blueprints
app.register_blueprint(csv_bp, url_prefix='/csv')
app.register_blueprint(preprocessamento_bp, url_prefix='/preprocessamento')
app.register_blueprint(processamento_bp, url_prefix='/processamento')
app.register_blueprint(ids_gerais_bp, url_prefix='/ids')

# Registre o namespace do processamento para que o Swagger funcione
api.add_namespace(processamento_ns, path='/processamento')

try:
    print("Conexão estabelecida com sucesso!")
    print("Bancos de dados disponíveis:", db)
except Exception as e:
    print("Falha na conexão com o MongoDB:")
    print(e)

if __name__ == "__main__":
    app.run(debug=True, port=5003)

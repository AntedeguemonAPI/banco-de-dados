# app.py
from flask import Flask, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from routes.csv_routes import csv_bp
from routes.preprocessamento_routes import preprocessamento_bp
from routes.processo_routes import processamento_bp
from routes.ids_gerais import ids_gerais_bp
from config_db import db
from routes.processo_routes import processamento_ns
from flask_restx import Api
from flask_cors import CORS 

app = Flask(__name__)


CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3001"}})


# Inicialize a API Flask-RESTX
api = Api(app, version='1.0', title='API de Gerenciamento do Banco de Dados',
          description='Uma API para gerenciar os endpoints do banco de dados.')

# Registre os blueprints
app.register_blueprint(csv_bp, url_prefix='/csv')
app.register_blueprint(preprocessamento_bp, url_prefix='/preprocessamento')
app.register_blueprint(processamento_bp, url_prefix='/processamento')
app.register_blueprint(ids_gerais_bp, url_prefix='/ids')

@app.route('/swagger.yaml')
def serve_swagger():
    return send_from_directory('.', 'swagger.yaml')

SWAGGER_URL = '/api/docs'
API_URL = '/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Processamento e Pré-processamento"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Registre o namespace do processamento para que o Swagger funcione
api.add_namespace(processamento_ns, path='/processamento')

try:
    print("Conexão estabelecida com sucesso!")
    print("Bancos de dados disponíveis:", db)
except Exception as e:
    print("Falha na conexão com o MongoDB:")
    print(e)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5003, debug=True)


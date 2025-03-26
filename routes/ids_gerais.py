from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from routes.csv_routes import create_csv
from routes.preprocessamento_routes import create_preprocessamento
from routes.processo_routes import create_processamento
from config_db import db
from functions.gerador_de_id import generate_unique_id

ids_gerais_bp = Blueprint('ids', __name__)

ids_gerais_collection = db['ids_gerais']
preprocessamento_collection = db['preprocessamento']
processamento_collection = db['processamento']

# Função para criar o ID Geral
def create_id_geral():
    
    id_geral = generate_unique_id('ids_gerais')
    id_preprocessamento = generate_unique_id('preprocessamento')
    id_processamento = generate_unique_id('processamento')

    preprocessamento = {
        "id": id_preprocessamento,
        "id_geral": id_geral,
        "preprocessamento_concluido": 0,
    }

    # Inserir o processamento no banco de dados
    preprocessamento_collection.insert_one(preprocessamento)
    
    processamento = {
        "id": id_processamento,
        "id_geral": id_geral,
        "processamento_concluido": 0,
    }

    # Inserir o processamento no banco de dados
    processamento_collection.insert_one(processamento)

    # Montar o JSON final
    id_geral_json = {
        "id": id_geral,
        "id_preprocessamento": id_preprocessamento,
        "preprocessamento_concluido": 0,
        "id_processamento": id_processamento,
        "processamento_concluido": 0,
    }

    # Salvar o id_geral na coleção
    ids_gerais_collection.insert_one(id_geral_json)

    return jsonify({"message": "ID Geral criado com sucesso", "id_geral": id_geral}), 201

# Função para obter um ID Geral específico
def get_id_geral(id):
    id_geral = ids_gerais_collection.find_one({"id": int(id)})

    if not id_geral:
        return jsonify({"message": "ID Geral não encontrado"}), 404

    # Converter ObjectId para string
    id_geral['_id'] = str(id_geral['_id']) 

    return jsonify(id_geral)

# Função para obter todos os IDs Gerais
def get_all_ids_gerais():
    ids_gerais = list(ids_gerais_collection.find())

    for id_geral in ids_gerais:
        id_geral['_id'] = str(id_geral['_id'])

    return jsonify(ids_gerais)

# Função para atualizar um ID Geral
def update_id_geral(id):
    data = request.json

    # Agora, estamos buscando pelo campo 'id' e não 'id_geral'
    id_geral = ids_gerais_collection.find_one({"id": int(id)})

    if not id_geral:
        return jsonify({"message": "ID Geral não encontrado"}), 404

    # Garantir que o id e _id não sejam alterados
    data['id'] = id_geral['id'] 
    data['_id'] = str(id_geral['_id']) 
    data['id_preprocessamento'] = id_geral['id_preprocessamento']
    data['id_processamento'] = id_geral['id_processamento']

    # Atualizar o documento com os novos dados, exceto id e _id
    updated_data = {
        "id": data['id'],
        "_id": data['_id'],
        "id_preprocessamento": data['id_preprocessamento'],
        "id_processamento": data['id_processamento'],
        "preprocessamento_concluido": data.get('preprocessamento_concluido', id_geral['preprocessamento_concluido']),
        "processamento_concluido": data.get('processamento_concluido', id_geral['processamento_concluido'])
    }

    # Atualiza o documento na coleção ids_gerais_collection
    ids_gerais_collection.replace_one({"_id": int(id)}, updated_data)

    # Retorna o documento atualizado como resposta
    return jsonify(updated_data), 200

# Função para deletar um ID Geral
def delete_id_geral(id):
    id_geral = ids_gerais_collection.find_one({"id": int(id)})

    if not id_geral:
        return jsonify({"message": "ID Geral não encontrado"}), 404

    preprocessamento_collection.delete_one({"id": int(id)})
    processamento_collection.delete_one({"id": int(id)})
    ids_gerais_collection.delete_one({"id": int(id)})
    
    return jsonify({"message": "ID Geral deletado com sucesso"}), 200


# Rotas
@ids_gerais_bp.route('/', methods=['POST'])
def create():
    return create_id_geral()

@ids_gerais_bp.route('/<id>', methods=['GET'])
def read_one(id):
    return get_id_geral(id)

@ids_gerais_bp.route('/', methods=['GET'])
def read_all():
    return get_all_ids_gerais()

@ids_gerais_bp.route('/<id>', methods=['PUT'])
def update(id):
    return update_id_geral(id)

@ids_gerais_bp.route('/<id>', methods=['DELETE'])
def delete(id):
    return delete_id_geral(id)
    
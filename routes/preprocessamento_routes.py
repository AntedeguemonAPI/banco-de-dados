from flask import Blueprint, request, jsonify
from config_db import db
from functions.gerador_de_id import generate_unique_id

preprocessamento_bp = Blueprint('preprocessamento', __name__)
preprocessamento_collection = db['preprocessamento']

ids_gerais_collection = db['ids_gerais']

# Criar um preprocessamento
def create_preprocessamento():
    data = request.json

    unique_id = generate_unique_id('preprocessamento')

    preprocessamento = {
        "id": unique_id,
        **data  # Adiciona todos os dados recebidos no JSON
    }

    # Inserir o preprocessamento no banco de dados
    preprocessamento_collection.insert_one(preprocessamento)

    # Retorna uma resposta JSON corretamente
    return jsonify({"message": "Preprocessamento criado com sucesso", "id": unique_id}), 201



# Ler todos os preprocessamentos
def get_preprocessamentoes():
    preprocessamentos = list(preprocessamento_collection.find())
    
    # Remover o campo _id do resultado
    for preprocessamento in preprocessamentos:
        preprocessamento['_id'] = str(preprocessamento['_id']) 
    
    return jsonify(preprocessamentos)

# Ler um preprocessamento específico
def get_preprocessamento(id):
    # Buscar o preprocessamento por id
    preprocessamento = preprocessamento_collection.find_one({"id": int(id)})

    if not preprocessamento:
        return jsonify({"message": "Preprocessamento não encontrado"}), 404

    preprocessamento['_id'] = str(preprocessamento['_id']) 
    return jsonify(preprocessamento)

# Atualizar um preprocessamento
def update_preprocessamento(id):
    data = request.json

    # Buscar o preprocessamento para verificar se existe
    preprocessamento = preprocessamento_collection.find_one({"id": int(id)})

    if not preprocessamento:
        return jsonify({"message": "Preprocessamento não encontrado"}), 404
    
    data['_id'] = preprocessamento['_id']
    data['id'] = preprocessamento['id'] 
    data['id_geral'] = preprocessamento['id_geral']
    data['preprocessamento_concluido'] = 1

    # Atualizando o preprocessamento na coleção
    preprocessamento_collection.replace_one({"id": int(id)}, data)

    # Atualizando a coleção ids_gerais_collection
    ids_gerais = ids_gerais_collection.find_one({"id_preprocessamento": int(id)})
    
    if ids_gerais:
        # Atualizando o atributo 'preprocessamento_concluido' para 1
        ids_gerais_collection.update_one(
            {"id_preprocessamento": int(id)},
            {"$set": {"preprocessamento_concluido": 1}}
        )

    data['_id'] = str(data['_id'])

    return jsonify(data), 200

# Deletar um preprocessamento
def delete_preprocessamento(id):
    # Buscar o preprocessamento para verificar se existe
    preprocessamento = preprocessamento_collection.find_one({"id": int(id)})

    if not preprocessamento:
        return jsonify({"message": "Preprocessamento não encontrado"}), 404

    preprocessamento_collection.delete_one({"id": int(id)})

    return jsonify({"message": "Preprocessamento deletado com sucesso"}), 200

# Rotas
@preprocessamento_bp.route('/', methods=['POST'])
def create():
    return create_preprocessamento()

@preprocessamento_bp.route('/', methods=['GET'])
def read_all():
    return get_preprocessamentoes()

@preprocessamento_bp.route('/<id>', methods=['GET'])
def read_one(id):
    return get_preprocessamento(id)

@preprocessamento_bp.route('/<id>', methods=['PUT'])
def update(id):
    return update_preprocessamento(id)

@preprocessamento_bp.route('/<id>', methods=['DELETE'])
def delete(id):
    return delete_preprocessamento(id)

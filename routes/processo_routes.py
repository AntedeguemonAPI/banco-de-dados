from flask import Blueprint, request, jsonify
from config_db import db
from functions.gerador_de_id import generate_unique_id

processamento_bp = Blueprint('processamento', __name__)
processamento_collection = db['processamento']

ids_gerais_collection = db['ids_gerais']

# Criar um processamento
def create_processamento():
    data = request.json
    # Gerar um ID único para o novo processamento
    unique_id = generate_unique_id('processamento')

    processamento = {
        "id": unique_id,
        **data  # Adiciona todos os dados recebidos no JSON
    }

    # Inserir o processamento no banco de dados
    processamento_collection.insert_one(processamento)

    # Retorna uma resposta JSON corretamente
    return jsonify({"message": "Processamento criado com sucesso", "id": unique_id}), 201


# Ler todos os processamentos
def get_processamentos():
    processamentos = list(processamento_collection.find())
    
    # Remover o campo _id do resultado
    for processamento in processamentos:
        processamento['_id'] = str(processamento['_id'])  # Convertendo o ObjectId para string
    
    return jsonify(processamentos)

# Ler um processamento específico
def get_processamento(id):
    # Buscar o processamento por id
    processamento = processamento_collection.find_one({"id": int(id)})

    if not processamento:
        return jsonify({"message": "Processamento não encontrado"}), 404

    processamento['_id'] = str(processamento['_id']) 
    return jsonify(processamento)

# Atualizar um processamento
def update_processamento(id):
    data = request.json

    # Buscar o processamento para verificar se existe
    processamento = processamento_collection.find_one({"id": int(id)})

    if not processamento:
        return jsonify({"message": "Processamento não encontrado"}), 404

    data['_id'] = processamento['_id']
    data['id'] = processamento['id'] 
    data['id_geral'] = processamento['id_geral']
    data['processamento_concluido'] = 1

    # Atualizando o processamento na coleção
    processamento_collection.replace_one({"id": int(id)}, data)

    # Atualizando a coleção ids_gerais_collection
    ids_gerais = ids_gerais_collection.find_one({"id_processamento": int(id)})
    
    if ids_gerais:
        # Atualizando o atributo 'processamento_concluido' para 1
        ids_gerais_collection.update_one(
            {"id_processamento": int(id)},
            {"$set": {"processamento_concluido": 1}}
        )
        
    data['_id'] = str(data['_id'])

    return jsonify(data), 200

# Deletar um processamento
def delete_processamento(id):
    # Buscar o processamento para verificar se existe
    processamento = processamento_collection.find_one({"id": int(id)})

    if not processamento:
        return jsonify({"message": "Processamento não encontrado"}), 404

    processamento_collection.delete_one({"id": int(id)})

    return jsonify({"message": "Processamento deletado com sucesso"}), 200

# Rotas
@processamento_bp.route('/', methods=['POST'])
def create():
    return create_processamento()

@processamento_bp.route('/', methods=['GET'])
def read_all():
    return get_processamentos()

@processamento_bp.route('/<id>', methods=['GET'])
def read_one(id):
    return get_processamento(id)

@processamento_bp.route('/<id>', methods=['PUT'])
def update(id):
    return update_processamento(id)

@processamento_bp.route('/<id>', methods=['DELETE'])
def delete(id):
    return delete_processamento(id)

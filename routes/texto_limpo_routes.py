# routes/texto_limpo_routes.py
from flask import Blueprint, request, jsonify
from config_db import db
from functions.gerador_de_id import generate_unique_id

texto_limpo_bp = Blueprint('texto_limpo', __name__)
texto_limpo_collection = db['texto_limpo']

# Criar um texto_limpo
def create_texto_limpo():
    data = request.json

    unique_id = generate_unique_id('texto_limpo')

    texto_limpo = {
        "id": unique_id,
        **data
    }

    texto_limpo_collection.insert_one(texto_limpo)

    return jsonify({"message": "Texto limpo criado com sucesso", "id": unique_id}), 201

# Obter todos os textos limpos
def get_all_texto_limpo():
    textos = list(texto_limpo_collection.find())
    for texto in textos:
        texto['_id'] = str(texto['_id'])
    return jsonify(textos)

# Obter um texto limpo específico
def get_texto_limpo(id):
    texto = texto_limpo_collection.find_one({"id": int(id)})
    if not texto:
        return jsonify({"message": "Texto limpo não encontrado"}), 404
    texto['_id'] = str(texto['_id'])
    return jsonify(texto)

@texto_limpo_bp.route('/id_geral/<id_geral>', methods=['GET'])
def get_by_id_geral(id_geral):
    try:
        id_geral_int = int(id_geral)
    except ValueError:
        return jsonify({"message": "ID_geral deve ser um número inteiro"}), 400

    resultados = list(texto_limpo_collection.find({"ID_geral": id_geral_int}))

    if not resultados:
        return jsonify({"message": "Nenhum texto limpo encontrado com esse ID_geral"}), 404

    for r in resultados:
        r['_id'] = str(r['_id'])

    return jsonify(resultados), 200

# Atualizar um texto limpo
def update_texto_limpo(id):
    data = request.json
    texto = texto_limpo_collection.find_one({"id": int(id)})

    if not texto:
        return jsonify({"message": "Texto limpo não encontrado"}), 404

    data['_id'] = texto['_id']
    data['id'] = texto['id']

    texto_limpo_collection.replace_one({"id": int(id)}, data)

    data['_id'] = str(data['_id'])

    return jsonify(data), 200

# Deletar um texto limpo
def delete_texto_limpo(id):
    texto = texto_limpo_collection.find_one({"id": int(id)})

    if not texto:
        return jsonify({"message": "Texto limpo não encontrado"}), 404

    texto_limpo_collection.delete_one({"id": int(id)})

    return jsonify({"message": "Texto limpo deletado com sucesso"}), 200

@texto_limpo_bp.route('/', methods=['POST'])
def create():
    return create_texto_limpo()

@texto_limpo_bp.route('/', methods=['GET'])
def read_all():
    return get_all_texto_limpo()

@texto_limpo_bp.route('/<id>', methods=['GET'])
def read_one(id):
    return get_texto_limpo(id)

@texto_limpo_bp.route('/<id>', methods=['PUT'])
def update(id):
    return update_texto_limpo(id)

@texto_limpo_bp.route('/<id>', methods=['DELETE'])
def delete(id):
    return delete_texto_limpo(id)


from flask import Blueprint, request, jsonify
from config_db import db
from functions.gerador_de_id import generate_unique_id

sumarizacao_textos_bp = Blueprint('sumarizacao_textos', __name__)
sumarizacao_textos_collection = db['sumarizacao_textos']

# Criar um sumarizacao_texto
def create_sumarizacao_texto():
    data = request.json

    unique_id = generate_unique_id('sumarizacao_textos')

    sumarizacao_texto = {
        "id": unique_id,
        **data
    }

    sumarizacao_textos_collection.insert_one(sumarizacao_texto)

    return jsonify({"message": "Sumarização de texto criada com sucesso", "id": unique_id}), 201

# Obter todos os sumarizacao_textos
def get_all_sumarizacao_textos():
    textos = list(sumarizacao_textos_collection.find())
    for texto in textos:
        texto['_id'] = str(texto['_id'])
    return jsonify(textos)

# Obter uma sumarizacao_texto específico
def get_sumarizacao_texto(id):
    texto = sumarizacao_textos_collection.find_one({"id": int(id)})
    if not texto:
        return jsonify({"message": "Sumarização de texto não encontrada"}), 404
    texto['_id'] = str(texto['_id'])
    return jsonify(texto)

@sumarizacao_textos_bp.route('/id_geral/<id_geral>', methods=['GET'])
def get_by_id_geral(id_geral):
    try:
        id_geral_int = int(id_geral)
    except ValueError:
        return jsonify({"message": "ID_geral deve ser um número inteiro"}), 400

    resultados = list(sumarizacao_textos_collection.find({"ID_geral": id_geral_int}))

    if not resultados:
        return jsonify({"message": "Nenhuma sumarização de texto encontrada com esse ID_geral"}), 404

    for r in resultados:
        r['_id'] = str(r['_id'])

    return jsonify(resultados), 200

# Atualizar uma sumarizacao_texto
def update_sumarizacao_texto(id):
    data = request.json
    texto = sumarizacao_textos_collection.find_one({"id": int(id)})

    if not texto:
        return jsonify({"message": "Sumarização de texto não encontrada"}), 404

    data['_id'] = texto['_id']
    data['id'] = texto['id']

    sumarizacao_textos_collection.replace_one({"id": int(id)}, data)

    data['_id'] = str(data['_id'])

    return jsonify(data), 200

# Deletar uma sumarizacao_texto
def delete_sumarizacao_texto(id):
    texto = sumarizacao_textos_collection.find_one({"id": int(id)})

    if not texto:
        return jsonify({"message": "Sumarização de texto não encontrada"}), 404

    sumarizacao_textos_collection.delete_one({"id": int(id)})

    return jsonify({"message": "Sumarização de texto deletada com sucesso"}), 200

# Rotas
@sumarizacao_textos_bp.route('/', methods=['POST'])
def create():
    return create_sumarizacao_texto()

@sumarizacao_textos_bp.route('/', methods=['GET'])
def read_all():
    return get_all_sumarizacao_textos()

@sumarizacao_textos_bp.route('/<id>', methods=['GET'])
def read_one(id):
    return get_sumarizacao_texto(id)

@sumarizacao_textos_bp.route('/<id>', methods=['PUT'])
def update(id):
    return update_sumarizacao_texto(id)

@sumarizacao_textos_bp.route('/<id>', methods=['DELETE'])
def delete(id):
    return delete_sumarizacao_texto(id)

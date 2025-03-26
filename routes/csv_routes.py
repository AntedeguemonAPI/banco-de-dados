from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from config_db import db
import os
import io
import gridfs
import csv

# Conectando ao GridFS
fs = gridfs.GridFS(db)

csv_bp = Blueprint('csv', __name__)

# Função para gerar IDs únicos numéricos
def generate_unique_id(collection):
    current_id = 1
    while db[collection].find_one({"id": current_id}):
        current_id += 1
    return current_id

# Criar um CSV no GridFS
def create_csv():

    return jsonify({"message": "CSV criado com sucesso"}), 201

# Ler todos os CSVs
def get_csvs():

    return jsonify(), 200

# Ler um CSV específico
def get_csv(id):

    return jsonify(csv), 200

# Atualizar um CSV
def update_csv(id):

    return jsonify({"message": "CSV atualizado com sucesso"}), 200

# Deletar um CSV
def delete_csv(id):

    return jsonify({"message": "CSV deletado com sucesso"}), 200

# Rotas
@csv_bp.route('/', methods=['POST'])
def create():
    return create_csv()

@csv_bp.route('/', methods=['GET'])
def read_all():
    return get_csvs()

@csv_bp.route('/<id>', methods=['GET'])
def read_one(id):
    return get_csv(id)

@csv_bp.route('/<id>', methods=['PUT'])
def update(id):
    return update_csv(id)

@csv_bp.route('/<id>', methods=['DELETE'])
def delete(id):
    return delete_csv(id)

from flask import Blueprint, request, jsonify
from config_db import db
from functions.gerador_de_id import generate_unique_id
from flask_restx import Namespace, Resource, fields

processamento_bp = Blueprint('processamento', __name__)
processamento_collection = db['processamento']

ids_gerais_collection = db['ids_gerais']

# Defina o namespace para processamento no Swagger
processamento_ns = Namespace('processamento', description='Operações relacionadas ao processamento')

# Definir o modelo de dados para a API no Swagger
processamento_model = processamento_ns.model('Processamento', {
    'id': fields.String(readOnly=True, description='ID único do processamento'),
    'id_geral': fields.String(required=True, description='ID geral do processamento'),
    'processamento_concluido': fields.Integer(description='Status do processamento (0 ou 1)'),
    'outros_dados': fields.Raw(description='Outros dados adicionais do processamento')
})

# Criar um processamento
@processamento_ns.route('/<id>')
class Processamento(Resource):
    @processamento_ns.doc('Obter um processamento específico')
    def get(self, id):
        try:
            # Convertendo o 'id' para inteiro (caso seja um número)
            id_int = int(id)
        except ValueError:
            # Caso o 'id' não seja um número válido, retornamos um erro
            return jsonify({"message": "ID inválido. O ID deve ser um número."}), 400

        # Buscar o processamento específico
        processamento = processamento_collection.find_one({"id": id_int})

        if not processamento:
            return jsonify({"message": "Processamento não encontrado"}), 404

        # Convertendo o _id do MongoDB para string para compatibilidade com JSON
        processamento['_id'] = str(processamento['_id'])
        
        if '_id' in processamento:
            del processamento['_id']

        # Mapear os dados manualmente, de acordo com o modelo do Swagger
        response_data = {
            'id': processamento['id'],
            'id_geral': processamento.get('id_geral', None),
            'processamento_concluido': processamento.get('processamento_concluido', None),
            'outros_dados': processamento.get('outros_dados', None)
        }

        # Retornando os dados já no formato desejado
        return jsonify(response_data), 200

# Ler um processamento específico
@processamento_ns.route('/<id>')
class Processamento(Resource):
    @processamento_ns.doc('Obter um processamento específico')
    @processamento_ns.marshal_with(processamento_model)
    def get(self, id):
        try:
            # Convertendo o 'id' para inteiro (caso seja um número)
            id_int = int(id)
        except ValueError:
            # Caso o 'id' não seja um número válido, retornamos um erro
            return jsonify({"message": "ID inválido. O ID deve ser um número."}), 400

        # Buscar o processamento específico
        processamento = processamento_collection.find_one({"id": id_int})

        if not processamento:
            return jsonify({"message": "Processamento não encontrado"}), 404

        # Convertendo o _id do MongoDB para string para compatibilidade com JSON
        processamento['_id'] = str(processamento['_id'])
        
        print(processamento)

        return jsonify(processamento), 200
    
    @processamento_ns.doc('Atualizar um processamento')
    @processamento_ns.expect(processamento_model)
    def put(self, id):
        data = request.json

        # Buscar o processamento para verificar se existe
        processamento = processamento_collection.find_one({"id": int(id)})

        if not processamento:
            return {"message": "Processamento não encontrado"}, 404

        # Mantendo os campos que não mudam
        data['_id'] = processamento['_id']
        data['id'] = processamento['id']
        data['id_geral'] = processamento['id_geral']
        data['processamento_concluido'] = 1  # Atualizando este campo para 1

        # Atualizando o processamento na coleção
        processamento_collection.replace_one({"id": int(id)}, data)

        # Atualizando a coleção ids_gerais_collection
        ids_gerais = ids_gerais_collection.find_one({"id_processamento": int(id)})
        
        if ids_gerais:
            # Atualizando o atributo 'processamento_concluido' para 1 na coleção ids_gerais_collection
            ids_gerais_collection.update_one(
                {"id_processamento": int(id)},
                {"$set": {"processamento_concluido": 1}}
            )
        
        # Convertendo o _id para string para compatibilidade com JSON
        data['_id'] = str(data['_id'])

        return data, 200

@processamento_ns.doc('Deletar um processamento')
def delete(self, id):
    processamento = processamento_collection.find_one({"id": int(id)})

    if not processamento:
        return jsonify({"message": "Processamento não encontrado"}), 404

    processamento_collection.delete_one({"id": int(id)})

    return jsonify({"message": "Processamento deletado com sucesso"}), 200

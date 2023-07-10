from flask import Blueprint, jsonify
from pymongo import MongoClient
from config.config import *

cortes_blueprint = Blueprint('cortes', __name__)

# MongoDB

mongoConnection = f'mongodb+srv://{username}:{password}@cortes.9iadh5h.mongodb.net/'
client = MongoClient(mongoConnection)

db = client['CortesDB']
cortes_collection = db['cortes']

# Routes

@cortes_blueprint.route('/')
def corte_home():
    return 'Página de corte'

@cortes_blueprint.route('/details')
def corte_detalle():
    return 'Detalle de corte'

@cortes_blueprint.route('/data')
def get_data():
    cortes = []

    for document in cortes_collection.find():
        # Convertir el ObjectId a una cadena antes de agregarlo a la lista
        document['_id'] = str(document['_id'])
        cortes.append(document)

    return jsonify(cortes), HTTP_OK, {'Content-Type': 'application/json'}    

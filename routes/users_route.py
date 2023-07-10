from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from config.config import *

users_blueprint = Blueprint('users', __name__)

# MongoDB

mongoConnection = f'mongodb+srv://{username}:{password}@cortes.9iadh5h.mongodb.net/'
client = MongoClient(mongoConnection)

db = client['CortesDB']
users_collection = db['users']

# Routes

## GET Ruta Base
@users_blueprint.route('/')
def corte_home():
    return 'Página de users'

## GET Ruta Details
@users_blueprint.route('/details')
def corte_detalle():
    return 'Detalle de users'

## GET Data
@users_blueprint.route('/data')
def get_users():
    users = []

    for document in users_collection.find():
        # Convertir el ObjectId a una cadena antes de agregarlo a la lista
        document['_id'] = str(document['_id'])
        users.append(document)

    return jsonify(users), HTTP_OK, {'Content-Type': 'application/json'}  

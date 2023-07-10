from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
from pytz import timezone
from config.config import *

cortes_blueprint = Blueprint('cortes', __name__)

# MongoDB

mongoConnection = f'mongodb+srv://{username}:{password}@cortes.9iadh5h.mongodb.net/'
client = MongoClient(mongoConnection)

db = client['CortesDB']
cortes_collection = db['cortes']

# Routes

## GET Ruta Base
@cortes_blueprint.route('/')
def corte_home():
    return 'Página de corte'

## GET Ruta Details
@cortes_blueprint.route('/details')
def corte_detalle():
    return 'Detalle de corte'

## GET Data
@cortes_blueprint.route('/data')
def get_data():
    cortes = []

    for document in cortes_collection.find():
        # Convertir el ObjectId a una cadena antes de agregarlo a la lista
        document['_id'] = str(document['_id'])
        cortes.append(document)

    return jsonify(cortes), HTTP_OK, {'Content-Type': 'application/json'}    

## Get Corte Between RCC
@cortes_blueprint.route('/rcc')
def get_cortes_between_rcc():
    rcc1 = request.args.get('rcc1')
    rcc2 = request.args.get('rcc2')

    cortes = []

    for document in cortes_collection.find({'RCC': {'$gte': rcc1, '$lte': rcc2}}):
        document['_id'] = str(document['_id'])
        cortes.append(document)
    
    if(cortes == []):
        error = 'RCC Mal escrito o no encontrado.'
        return jsonify(error), HTTP_BAD_REQUEST, {'Content-Type': 'application/json'}

    return jsonify(cortes)


## GET Corte By RCC
@cortes_blueprint.route('/rcc/<rcc>')
def get_corte_by_rcc(rcc):
    corte_by_rcc = ''

    for document in cortes_collection.find({'RCC': rcc}):
        document['_id'] = str(document['_id'])
        corte_by_rcc = document
    
    if(corte_by_rcc == ''):
        error = 'RCC Mal escrito o no encontrado.'
        return jsonify(error), HTTP_BAD_REQUEST, {'Content-Type': 'application/json'}

    return jsonify(corte_by_rcc)

## GET Corte Between Dates
@cortes_blueprint.route('/date')
def get_cortes_between_dates():
    date1 = request.args.get('date1')
    date2 = request.args.get('date2')

    cortes = []

    try:
        fecha_inicio = datetime.strptime(date1, '%Y-%m-%d')
        fecha_fin = datetime.strptime(date2, '%Y-%m-%d') + timedelta(days=1)  # Agregar un día para incluir la fecha_fin en la búsqueda

        # Convertir fechas a zona horaria del Pacífico
        pacific_timezone = timezone('America/Los_Angeles')
        fecha_inicio = pacific_timezone.localize(fecha_inicio)
        fecha_fin = pacific_timezone.localize(fecha_fin)

        # Convertir fechas a UTC
        utc_timezone = timezone('UTC')
        fecha_inicio_utc = fecha_inicio.astimezone(utc_timezone)
        fecha_fin_utc = fecha_fin.astimezone(utc_timezone)
    except ValueError:
        error = 'Formato de fecha inválido. Utiliza el formato YYYY-MM-DD'
        return jsonify(error), HTTP_BAD_REQUEST, {'Content-Type': 'application/json'}

    for document in cortes_collection.find({'fechaHora': {'$gte': fecha_inicio_utc, '$lt': fecha_fin_utc}}):
        document['_id'] = str(document['_id'])
        cortes.append(document)

    return jsonify(cortes), HTTP_OK, {'Content-Type': 'application/json'}


## GET Corte By Date
@cortes_blueprint.route('/date/<date>')
def get_cortes_by_date(date):
    cortes = []

    try:
        fecha = datetime.strptime(date, '%Y-%m-%d').date()
        fecha_inicio = datetime.combine(fecha, datetime.min.time())
        fecha_fin = datetime.combine(fecha, datetime.max.time())

    except ValueError:
        error = 'Formato de fecha inválido. Utiliza el formato YYYY-MM-DD'
        return jsonify(error), HTTP_BAD_REQUEST, {'Content-Type': 'application/json'}

    for document in cortes_collection.find({'fechaHora': {'$gte': fecha_inicio, '$lt': fecha_fin}}):
        document['_id'] = str(document['_id'])
        cortes.append(document)

    return jsonify(cortes), HTTP_OK, {'Content-Type': 'application/json'}

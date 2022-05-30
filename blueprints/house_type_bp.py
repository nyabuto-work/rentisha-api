from flask import Blueprint,jsonify,request
from models import House_Type as ht

ht_bp = Blueprint('ht_bp',__name__)

@ht_bp.route('/',methods=['GET'])
def get_all_house_types():
    return ht.get_all_types()

@ht_bp.route('/<int:id>',methods=['GET'])
def get_one_ht(id):
    return ht.get_one_type(id)

@ht_bp.route('/',methods=['POST'])
def add_house_type():
    data = request.get_json()
    house_type_data = ht.House_Type(data.get('name'),data.get('description'),data.get('status'))
    response = ht.create_new(house_type_data)
    return response

@ht_bp.route('/',methods=['PUT'])
def update_house_type():
    if(request.get_json().get('id')):
        data = request.get_json()
        id = data.get('id')
        data.pop('id')
        return ht.update(data,id)
    else:
        return {'message':'Identifier for record to be updated is not provided'}

@ht_bp.route('/',methods=['DELETE'])
def delete():
    id = request.get_json().get('id')
    if(id):
        return ht.delete(id)
    else:
        return {'message':'House Type with Provided ID not found'},404
from flask import jsonify,Blueprint,request
from models import Electricity_Type as et

et_bp = Blueprint('et_bp',__name__)

@et_bp.route('/',methods=['GET'])
def get_all():
    return et.find_all()

@et_bp.route('/<int:id>',methods=['GET'])
def get_one(id):
    return et.find_one_type(id)

@et_bp.route('/',methods=['POST'])
def add_new():
    data = request.get_json()
    et_data = et.Electricity_Type(data.get('name'),data.get('description'),data.get('status'))
    return et.create(et_data) 

@et_bp.route('/',methods=['PUT'])
def update():
    data = request.get_json()
    if(data.get("id")):
        id = data.get("id")
        data.pop("id")
        return et.update(data,id)
    else:
        return {'message':'Error updating data. Identifier not provided'},404

@et_bp.route('/',methods=['DELETE'])
def delete():
    data = request.get_json()
    if(data.get("id")):
        id = data.get("id")
        return et.delete(id)
    else:
        return {'message':'Unable to delete any resource. No identifier provided'}
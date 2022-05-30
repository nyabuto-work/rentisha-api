from models import House as hs
from flask import jsonify,Blueprint,request

hs_bp = Blueprint('hs_bp',__name__)

@hs_bp.route('/',methods=['GET'])
def get_all():
    return hs.find_all()

@hs_bp.route('/<int:id>',methods=['GET'])
def get_on_house(id):
    return hs.find_by_id(id)

@hs_bp.route('/',methods=['POST'])
def add_new():
    data = request.get_json()
    hs_data = hs.House(data.get('house_type_id'),data.get('renter_id'),data.get('latitude'),data.get('longitude'),data.get('car_parking'),data.get('has_watchman'),data.get('has_water'),data.get('electricity_type_id'),data.get('own_compound'),data.get('description'))
    return hs.create_new(hs_data)

@hs_bp.route('/',methods=['PUT'])
def update():
    if(request.get_json().get('id')):
        data = request.get_json()
        id = data.get('id')
        data.pop('id')
        return hs.update(data,id)
    else:
        return {'message':'Payload missing house identifier'},404

@hs_bp.route('/',methods=['DELETE'])
def delete():
    if(request.get_json().get('id')):
        id = request.get_json().get('id')
        return hs.delete(id)
    else:
        return {'message':'Payload missing house identifier'}


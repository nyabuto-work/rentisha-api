from flask import jsonify,Blueprint,request
import models.Renter as rt
from werkzeug.security import generate_password_hash, check_password_hash

renter_bp = Blueprint("renter_bp",__name__)

@renter_bp.route("/",methods=['GET'])
def get_all_renters():
    res = rt.find_all()
    return res


@renter_bp.route("/<int:id>",methods=['GET'])
def get_one_renter(id):
    return rt.find_by_id(id)

@renter_bp.route("/",methods=['POST'])
def add_renter():
    data = request.get_json()
    renter = rt.Renter(data.get('firstname'),data.get('middlename'),data.get('surname'),data.get('email'),data.get('phone'),generate_password_hash(data.get('password')),data.get('status'))
    res = rt.create_new(renter)
    return res


@renter_bp.route("/",methods=['PUT'])
def update_renter():
    data = request.get_json()
    id = data.get("id")
    if(id):
        data.pop("id")
        res = rt.update_db(data,id)
        return res
    else:
        return {'message':'missing identifier in the payload'}

@renter_bp.route("/",methods=['DELETE'])
def delete_renter():
    id = request.get_json().get('id')
    if(id):
        records = rt.delete_by_id(id)
        return records
    else:
        return {'message':'User identifier not provided'},404
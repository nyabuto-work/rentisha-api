from flask import Blueprint,jsonify, request
import models.Tenant as tn
from werkzeug.security import generate_password_hash, check_password_hash

tenant_bp = Blueprint('tenant_bp',__name__)

@tenant_bp.route("/",methods=['GET'])
def list_tenants():
    return tn.find_all()

@tenant_bp.route("/<int:id>",methods=['GET'])
def list_one_tenant(id):
    return tn.find_by_id(id)

@tenant_bp.route("/",methods=['POST'])
def add_tenant():
    data = request.get_json()
    tenant = tn.Tenant(data.get('firstname'),data.get('middlename'),data.get('surname'),data.get('email'),data.get('phone'),generate_password_hash(data.get('password')),data.get('status'))
    res = tn.save_to_db(tenant)
    return res

@tenant_bp.route("/",methods=['PUT'])
def update_tenant():
    data = request.get_json()
    id = data.get("id")
    data.pop("id")
    res = tn.update_db(data,id)
    return res

@tenant_bp.route("/login",methods=['GET','POST'])
def login_user():
    req_data = request.get_json()
    username = req_data.get('username')
    data = tn.find_by_email_phone(username)
    # password = data['data'][0]['password']
    response = jsonify(data['data'])
    return response

@tenant_bp.route("/",methods=['DELETE'])
def delete_tenant():
    id = request.get_json().get("id")
    if id:
        records = tn.delete_from_db(id)
        return records
    else:
        return {'message':'Unable to get patient identifier'},404

from flask import Blueprint,request
from models.Tenant import Tenant as tnt
from models.Renter import Renter as rnt



auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/renter/login",methods=['GET','POST'])
def auth_renter():
    username = request.form.get('username')
    password = request.form.get('password')
# from distutils.debug import DEBUG
from sys import prefix
from flask import jsonify
from ma import ma
from db import db,app

# IMPORT ALL Bluprints
from blueprints.tenant_bp import tenant_bp as tbp
from blueprints.renter_bp import renter_bp as rbp
from blueprints.auth_bp import auth_bp as auth_bp
from blueprints.house_type_bp import  ht_bp
from blueprints.electricity_type_bp import  et_bp 
from blueprints.house_bp import  hs_bp

app.config['PROPAGATE_EXCEPTIONS'] = True
app.register_blueprint(tbp,url_prefix='/api/tenants')
app.register_blueprint(rbp,url_prefix='/api/renters')
app.register_blueprint(auth_bp,url_prefix='/api/auth')
app.register_blueprint(ht_bp,url_prefix='/api/house_types')
app.register_blueprint(et_bp,url_prefix='/api/electricity_types')
app.register_blueprint(hs_bp,url_prefix='/api/houses')

@app.route("/")
def home():
    name = "Rentisha API"
    description = "Rentisha API is the core engine that runs Rentisha App and Admin"
    res={"name":name,"description":description}
    return jsonify(res)

@app.errorhandler(404)
def handle(e):
    # handle all other routes here
    return {'message':'No such resource in rentisha', 'description':str(e)},404


    
if __name__=='__main__':
    db.init_app(app)
    ma.init_app(app)
    host="0.0.0.0"
    port=5001
    debug="ON"
    app.run(host=host,port=port,debug=debug)

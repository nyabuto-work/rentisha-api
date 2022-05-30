from db import db
from typing import List
from flask import jsonify
from sqlalchemy.exc import DatabaseError
from sqlalchemy.sql import func


class Tenant(db.Model):
    __tablename__="tenants"

    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(100),nullable=False,unique=False)
    middlename = db.Column(db.String(100),nullable=True,unique=False)
    surname = db.Column(db.String(100),nullable=False,unique=False)
    email = db.Column(db.String(200),nullable=False,unique=True)
    phone=db.Column(db.Integer,nullable=False,unique=True)
    password = db.Column(db.Text,nullable=False,unique=False)
    status = db.Column(db.Integer,default=1,nullable=False,unique=False)
    date_created = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now(),onupdate=func.now())
    # created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self,firstname,middlename,surname,email,phone,password,status):
        self.firstname=firstname
        self.middlename=middlename
        self.surname=surname
        self.email=email
        self.phone=phone
        self.password=password
        self.status=status

    def __repr__(self) -> str:
        return 'Tenant(firstname=%s,middlename=%s,surname=%s,email=%s,phone=%s,password=%s,status=%s)' % (self.firstname,self.middlename,self.surname,self.email,self.phone,self.password,self.status)

    def json(self):
        return {'firstname':self.firstname,'middlename':self.middlename,'surname':self.surname,'email':self.email,'phone':self.phone,'password':self.password,'status':self.status}

db.create_all()
db.session.commit()

def find_by_email_phone(username):
    try:
        records = Tenant.query.filter((Tenant.phone==username) | (Tenant.email==username))
        res = list(map(lambda x: x.json(), records))
        return {'data':res}
        
    except DatabaseError as err:
        return {'message':str(err)}

def find_by_id(_id):
    records = Tenant.query.filter_by(id=_id)
    result = jsonify(list(map(lambda x: x.json(), records)))
    return result

def find_all():
    data = Tenant.query.all()
    result = jsonify(list(map(lambda x: x.json(), data)))
    return result

def update_db(data,_id):
    try:
        records = db.session.query(Tenant).filter(Tenant.id==_id).update(data)
        message="success"
        db.session.commit()
        return {'code':records}
    except DatabaseError as e:
        message="Error Updating Record"
        description = str(e)
        db.session.rollback()
        return {'code':0,'message':message,'description':description}

def save_to_db(self)->None:
    try:
        num = db.session.add(self)
        db.session.commit()
        return {'code':1}
    except DatabaseError as e:
        return {'code':0,'message':"Error adding new tenant information",'description':str(e)}


def delete_from_db(_id)->None:
    num = Tenant.query.filter_by(id=_id).delete()
    db.session.commit()
    return {'code':num}
   


from flask import jsonify
from sqlalchemy.exc import DatabaseError as err
from db import db
from sqlalchemy.sql import func

class Electricity_Type(db.Model):
    __tablename__='electricity_types'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False,unique=True)
    description = db.Column(db.Text,nullable=True,unique=False)
    status = db.Column(db.Integer,nullable=False,unique=False,default=1)
    date_created = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now(),onupdate=func.now())
    houses = db.relationship('House',backref='electricity_type',lazy=True)

    def __init__(self,name,description,status):
        self.name = name
        self.description = description
        self.status = status

    def __repr__(self) -> str:
        return 'Electricity_Type(name=%s,description=%s,status=%s)'%(self.name,self.description,self.status)

    def json(self):
        return {'name':self.name,'description':self.description,'status':self.status}

db.create_all()
db.session.commit()


def find_all():
    data = db.session.query(Electricity_Type).all()
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def find_one_type(id):
    data = db.session.query(Electricity_Type).filter_by(id=id)
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def create(self)->None:
    try:
        db.session.add(self)
        db.session.commit()
        return {},200

    except err:
        message = 'Error adding new Electricity type'
        description = str(err)
        return {'message':message,'description':description},500

def update(data,id):
    try:
        num = db.session.query(Electricity_Type).filter_by(id=id).update(data)
        if num==0:
            return {'message':'Failed to update system. no such identifier'},404
        else:
            return {'message':'Update successful'},200

    except err:
        message = 'Error updating record'
        description = str(err)
        return {'message':message,'description':description},500

def delete(id):
    try:
        db.session.query(Electricity_Type).filter_by(id=id).delete()
        db.session.commit()
        return {},200

    except err:
        message = 'Error deleting electricity type from system'
        description = str(err)
        return {'message':message,'description':description},500



        
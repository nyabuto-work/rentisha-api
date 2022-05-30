'''
Stores all house types. Single room, double Room, one bedroom, 2 bedroom
'''

from db import db
from flask import jsonify
from sqlalchemy.exc import DatabaseError
from sqlalchemy.sql import func



class House_Type(db.Model):
    __tablename__ = 'house_types'

    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String(100),nullable=False,unique=True)
    description = db.Column(db.Text,nullable=True,unique=False)
    status = db.Column(db.Integer,nullable=False,unique=False,default=1)
    date_created = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now(),onupdate=func.now())
    houses = db.relationship('House',backref='house_type',lazy=True)

    def __init__(self,name,description,status):
        self.name = name
        self.description = description
        self.status = status

    def __repr__(self) -> str:
        return 'House_Type(name=%s,description=%s,status=%s)'%(self.name,self.description,self.status)

    def json(self):
        return {'name':self.name,'description':self.description,'status':self.status}

db.create_all()
db.session.commit()


def get_all_types():
    data = db.session.query(House_Type).all()
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def get_one_type(id):
    data = db.session.query(House_Type).filter_by(id=id)
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def create_new(self)->None:
    try:
        db.session.add(self)
        db.session.commit()
        return {'message':'New house type added successfully'},200

    except DatabaseError as err:
        message = 'Error adding new house type'
        description = str(err)
        return {'message':message,'description':description},500

def update(data,id):
    try:
        num = db.session.query(House_Type).filter_by(id=id).update(data)
        return {'message':'Success'},200

    except DatabaseError as err:
        message = 'Failed to update house type'
        description=str(err)
        return {'message':message,'description':description},500

def delete(id):
    try:
        db.session.query(House_Type).filter_by(id=id).delete()
        db.session.commit()
        return {},200

    except DatabaseError as err:
        message = 'Unable to delete house type'
        description = str(err)
        return {'message':message,'description':description},500


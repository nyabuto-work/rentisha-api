
from db import db
from sqlalchemy.exc import DatabaseError
from flask import jsonify
from sqlalchemy.sql import func


class House(db.Model):
    __tablename__="houses"

    id = db.Column(db.Integer,primary_key=True)
    house_type_id = db.Column(db.Integer,db.ForeignKey('house_types.id'),unique=False,nullable=False)
    renter_id = db.Column(db.Integer,db.ForeignKey('renters.id'),unique=False,nullable=False)
    latitude = db.Column(db.String(100),unique=False,nullable=False)
    longitude = db.Column(db.String(100),unique=False,nullable=False)
    car_parking = db.Column(db.Boolean,unique=False,nullable=True,default=0)
    has_watchman = db.Column(db.Boolean,unique=False,nullable=True,default=0)
    has_water = db.Column(db.Boolean,unique=False,nullable=True,default=0)
    electricity_type_id = db.Column(db.Integer,db.ForeignKey('electricity_types.id'),unique=False,nullable=True,default=0)
    own_compound = db.Column(db.Boolean,unique=False,nullable=True,default=0)
    other_description = db.Column(db.Text,unique=False,nullable=True)
    status = db.Column(db.Integer,nullable=False,unique=False,default=1)
    date_created = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now(),onupdate=func.now())


    def __init__(self,house_type_id,renter_id,latitude,longitude,car_parking,has_watchman,has_water,electricity_type_id,own_compound,other_description):
        self.house_type_id = house_type_id
        self.renter_id = renter_id
        self.latitude = latitude
        self.longitude = longitude
        self.car_parking = car_parking
        self.has_watchman = has_watchman
        self.has_water = has_water
        self.electricity_type_id = electricity_type_id
        self.own_compound = own_compound
        self.other_description = other_description


    def __repr__(self) -> str:
        return 'House(house_type_id=%s,renter_id=%s,latitude=%s,longitude=%s,car_parking=%s)',self.house_type_id,self.renter_id,self.latitude,self.longitude,self.car_parking

    def json(self):
        return {'type_id':self.house_type_id,'renter_id':self.renter_id,'latitude':self.latitude,'longitude':self.longitude}

db.create_all()
db.session.commit()

def find_all():
    data = db.session.query(House).all()
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def find_by_id(id):
    data = db.session.query(House).filter_by(id=id)
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def create_new(self):
    try:
        db.session.add(self)
        db.session.commit()
        return {},200

    except DatabaseError as err:
        message = "Failed to add new record"
        description = str(err)
        return {'message':message,'description':description}

def update(data,id):
    try:
        num = db.session.query(House).filter_by(id=id).update(data)
        return {'num':num,'message':'Records updated successfully'},200
    except DatabaseError as err:
        message = 'Failed to update record'
        description = str(err)
        return {'message':message,'description':description},500


def delete(id):
    try:

        '''Delete record from all other related tables '''



        db.session.query(House).find_by(id=id).delete()
        db.session.commit()
        return {'message':'Record deleted successfully'}

    except DatabaseError as err:
        message ='Failed to delete resource identifier by ',id
        description = str(err)
        return{'message':message,'description':description}
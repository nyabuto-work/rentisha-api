from db import db
from flask import jsonify
from sqlalchemy.sql import func



class Renter(db.Model):
    __tablename__="renters"

    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(100),nullable=False,unique=False)
    middlename = db.Column(db.String(100),nullable=True,unique=False)
    surname = db.Column(db.String(100),nullable=False,unique=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    phone = db.Column(db.String(100),nullable=False,unique=True)
    password=db.Column(db.Text,nullable=False,unique=False)
    status = db.Column(db.Integer,nullable=False,unique=False,default=1)
    date_created = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now(),onupdate=func.now())
    houses = db.relationship('House',backref='house',lazy=True) # uselist=False for one to one mapping


    def __init__(self,firstname,middlename,surname,email,phone,password,status):
        self.firstname = firstname
        self.middlename = middlename
        self.surname = surname
        self.email = email
        self.phone = phone
        self.password = password
        self.status = status


    def __repr__(self) -> str:
        return 'Renter(firstname=%s,middlename=%s,surname=%s,email=%s,phone=%s,password=%s,status=%s)' % (self.firstname,self.middlename,self.surname,self.email,self.phone,self.password,self.status)

    def json(self):
        return {'firstname':self.firstname,'middlename':self.middlename,'surname':self.surname,'email':self.email,'phone':self.phone,'password':self.password,'status':self.status}

    

db.create_all()
db.session.commit()    


def find_all():
    fields = ['firstname','middlename','surname','email','phone','status']
    data = db.session.query(Renter).all()
    res_list = list(map(lambda x:x.json(),data))
    result = jsonify(res_list)
    return result

def find_by_id(id):
    data = db.session.query(Renter).filter_by(id=id)
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def create_new(self):
    try:
        num = db.session.add(self)
        db.session.commit()
        if num>0:
            return {'message':'Record added successfully'},200
        else:
            return {'message':'Unknown error occured'},404
    except Exception as err:
        return {'message':"Error saving you renter details",'description':str(err)},500

def update_db(data,_id):
    try:
        num = Renter.query.filter_by(id=_id).update(data)
        db.session.commit()
        return {'code':1,'message':'Details updated successfully'}
    except Exception as err:
        db.session.rollback()
        return {'code':0,'message':'Failed to update details','description':str(err)}


def delete_by_id(_id):
    num = Renter.query.filter_by(id=_id).delete()
    db.session.commit()
    return {'code':num}

def find_by_email_phone(username):
    data = Renter.query.filter_by((Renter.email==username) | (Renter.phone==username) )
    result = list(map(lambda x:x.json(),data ))
    return result
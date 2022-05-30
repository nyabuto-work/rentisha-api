'''
Shows available houses, and their posting history
start date, status, cost
'''


from flask import jsonify
from sqlalchemy.exc import DatabaseError
from db import db 
from sqlalchemy.sql import func


class Posted_House(db.Model):
    __tablename__='posted_houses'

    id = db.Column(db.Integer,primary_key=True)
    house_id = db.Column(db.Integer,nullable=False,unique=False)
    date_posted = db.Column(db.Date,nullable=False,unique=False)
    status = db.Column(db.Integer,nullable=False,unique=False,default=1)
    date_removed = db.Column(db.Date,nullable=True,unique=False)
    date_created = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now(),onupdate=func.now())


    def __init__(self,house_id,date_posted,status,date_removed):
        self.house_id = house_id
        self.date_posted = date_posted
        self.status = status
        self.date_removed = date_removed

    def __repr__(self) -> str:
        return 'Posted_House(date_posted=%s,status=%s,date_removed=%s)'%(self.date_posted,self.status,self.date_removed)

    def json(self):
        return {'house_id':self.house_id,'date_posted':self.date_posted,'status':self.status,'date_removed':self.date_removed}

db.create_all()
db.session.commit()


def get_posting_history(id):
    data = db.session.query(Posted_House).filter_by(house_id=id).order_by('date_posted')
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def create_posting(self):
    try:
        num = db.session.query(Posted_House).add(self)
        db.session.commit()
        return {'message':'House Posted Successfully'},200

    except DatabaseError as err:
        message='Error posting new House'
        description = str(err)
        return {'message':message,'description':description},500

def get_a_posting(id):
    data = db.session.query(Posted_House).filter_by(id=id)
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def delete_posting(id):
    try:
        num = db.session.query(Posted_House).filter_by(id=id).delete()
        db.session.commit()
        return {'message','Successfully deleted record'},200
    except DatabaseError as err:
        message = "Failed to delete posting"
        description = str(err)

        return {'message':message,'description':description},500

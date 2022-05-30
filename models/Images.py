from tkinter import Image
from db import db
from flask import jsonify
from sqlalchemy.sql import func


class Images(db.Model):
    __tablename__='house_images'
    id = db.Column(db.Integer,primary_key=True)
    house_id = db.Column(db.Integer,db.ForeignKey('houses.id'),unique=False,nullable=False)
    image_url = db.Column(db.String(200),nullable=False,unique=False)
    status = db.Column(db.Integer,nullable=False,unique=False,default=1)
    date_created = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now())
    date_updated = db.Column(db.DateTime(timezone=True),nullable=False,unique=False,server_default=func.now(),onupdate=func.now())

    def __init__(self,house_id,image_url,status):
        self.house_id=house_id
        self.image_url=image_url
        self.status=status

    def __repr__(self) -> str:
        return 'Images(image_url=%s), '% (self.image_url)

    def json(self):
        return {'id':self.id,'house_id':self.house_id,'image_url':self.image_url,'date_created':self.date_created,'date_updated':self.date_updated}

db.create_all()
db.session.commit()

def get_all_by_house(house_id):
    data = db.session.query(Images).filter_by(house_id=house_id)
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result

def get_one_image(id):
    data = db.session.query(Images).filter_by(id=id)
    result = jsonify(list(map(lambda x:x.json(),data)))
    return result


def save_image(self):
    db.session.add(self)
    db.session.commit()

def delete_images_by_house(house_id):
    try:
        num = db.session.query(Images).filter_by(house_id=house_id).delete()
        db.session.commit()
        if num>0:
            return {'message', num+' Images deleted successfully'},200
        else:
            return {'message':'No Image deleted'},404
    except Exception as ex:
        return {'message':'Error occured while deleting the image','description':str(ex)}


def delete_image(id):
    try:
        num = db.session.query(Images).filter_by(id=id).delete()
        db.session.commit()
        if num>0:
            return {'message':'Image deleted successfully'},200
        else:
            return {'message':'No Image was deleted'},404
    except Exception as ex:
        return {'message':'Error deleting image ','description':str(ex)},404



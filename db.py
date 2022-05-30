from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_serialize import FlaskSerialize

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/rentisha'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
fs_mixin = FlaskSerialize(db)

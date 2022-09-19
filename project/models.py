from flask_login import UserMixin
from . import db

class User(UserMixin,db.Model):
    # chaves primárias são exigidas pelo SQLAlchemy
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100))
    password = db.Column(db.String(1000))
    phone = db.Column(db.String(100))
    email = db.Column(db.String(100))
    cpf = db.Column(db.String(100), unique=True)
    group = db.Column(db.String(100))

class Posto(UserMixin,db.Model):
    # chaves primárias são exigidas pelo SQLAlchemy
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100))
    cidade = db.Column(db.String(1000))
    lat = db.Column(db.String(100))
    log = db.Column(db.String(100))
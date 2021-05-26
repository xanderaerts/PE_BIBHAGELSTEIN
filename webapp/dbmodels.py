from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30),unique = True)
    password = db.Column(db.String(150))
    naam = db.Column(db.String(50))
    voornaam = db.Column(db.String(50))
    
class Boeken(db.Model):
    BoekID = db.Column(db.Integer,primary_key = True,autoincrement=True)
    titel = db.Column(db.String(150))
    isbn = db.Column(db.String(30))
    auteur = db.Column(db.String(50))
    afkorting_auteur = db.Column(db.String(5))
    categorie = db.Column(db.String(15))
    nummer_jaartal_volgnummer = db.Column(db.String(15))
    LeenID = db.Column(db.Integer) 

class Leerlingen(db.Model):
    LeerlingID = db.Column(db.Integer,primary_key = True)
    klas = db.Column(db.String(10))
    klas_nr = db.Column(db.String(2))
    naam = db.Column(db.String(100))
    voornaam = db.Column(db.String(100))

class Lenen(db.Model):
    LeenID = db.Column(db.Integer,primary_key = True)
    datum = db.Column(db.DateTime(timezone=True), default = func.now())
    userID = db.Column(db.Integer, db.ForeignKey('users.id')) #checking the user who gave the book to the student 
    LeerlingID = db.Column(db.Integer, db.ForeignKey('leerlingen.LeerlingID'))
    BoekID = db.Column(db.Integer, db.ForeignKey('boeken.BoekID'))
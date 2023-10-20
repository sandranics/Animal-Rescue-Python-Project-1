from . import db
from flask_login import UserMixin #custom class
from sqlalchemy.sql import func
    
class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000)) 
    breed = db.Column(db.String(10000))
    age = db.Column(db.String(10000))
    health_status = db.Column(db.String(10000))
    location = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #func stores the time when an object has been created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #one to many relationship
    image = db.relationship('Image', backref='ad', uselist=False) #one to one relationship

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable= False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id')) #one to one relationship

class User(db.Model, UserMixin): #inheriting from Usermixin
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    ads = db.relationship('Ad') #one to many relationship

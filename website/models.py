from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100))
    points=db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique = True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), unique=True, nullable=False)
    points = db.relationship('Points')
    notes = db.relationship('Note')
    ranks = db.relationship('Rank')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(100))
    date = db.Column(db.String(150))
    user_id = db.Column(db.String, db.ForeignKey('user.first_name'))

class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), db.ForeignKey('user.first_name'))
    rank_points = db.Column(db.Integer)

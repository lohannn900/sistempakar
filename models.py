from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Aturan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kategori = db.Column(db.String(128), nullable=False)
    pelaku = db.Column(db.String(128), nullable=False)
    fakta = db.Column(db.Text, nullable=False)
    sanksi = db.Column(db.Text, nullable=False)
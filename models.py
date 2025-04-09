from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(100), nullable=False)
    userName = db.Column(db.String(20), db.ForeignKey('user.uName') , nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    language = db.Column(db.String(15),nullable=False)
    githubLink = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True)
    uName = db.Column(db.String(150))
    password = db.Column(db.String(150))
    isAdmin = db.Column(db.String(20)) 

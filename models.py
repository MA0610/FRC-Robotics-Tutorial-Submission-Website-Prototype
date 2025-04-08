from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(100), nullable=False)
    userName = db.Column(db.String(20),nullable=False)
    description = db.Column(db.String(10000), nullable=False)
    language = db.Column(db.String(15),nullable=False)
    githubLink = db.Column(db.String(150))



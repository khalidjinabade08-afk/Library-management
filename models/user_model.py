from database.db import db

class user(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(db.String(250), default="admin")
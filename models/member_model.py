from database.db import db
from datetime import datetime


class Member(db.Model):
    __tablename__ = "member"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    phone_no = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

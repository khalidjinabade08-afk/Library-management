from database.db import db
from datetime import date

class book(db.Model):
    __tablename__ = "book"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100))
    category = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    available_quantity = db.Column(db.Integer, default=0)
    publishes_year = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.Date, default=date.today)
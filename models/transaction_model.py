from database.db import db
from datetime import date
from models.book_model import book
from models.member_model import Member

class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, unique=True, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date)
    fine_amount = db.Column(db.Numeric(10,2), default=0.00)
    status = db.Column(db.String(200), default ="issued")
    
    member = db.relationship("Member",backref="transactions")
    book = db.relationship("book",backref="transactions")

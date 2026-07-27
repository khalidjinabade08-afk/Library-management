from database.db import db
from datetime import date


class Membership(db.Model):
    __tablename__ = "membership"

    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    membership_type = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(100), default="active")

    member = db.relationship("Member", backref="memberships")
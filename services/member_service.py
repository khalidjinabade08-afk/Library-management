from models.member_model import Member
from models.membership_model import Membership
from sqlalchemy import select
from database.db import db
from flask import session
from datetime import date, timedelta
from utils.response import error_response, success_response


def create_member(data):
    try:
        existing_member = Member.query.filter_by(
            name=data["name"], phone_no=data["phone_no"]
        ).first()

        if existing_member:
            return error_response("member already exists")

        new_member = Member(
            name=data["name"], phone_no=data["phone_no"], address=data["address"]
        )
        db.session.add(new_member)
        db.session.commit()

        return success_response(
            "member added successflly",
            {
                "id": new_member.id,
                "Name": new_member.name,
                "phone": new_member.phone_no,
                "address": new_member.address,
            },
            200,
        )

    except Exception as e:
        return error_response(str(e))


def add_membership(data):
    try:
        member = Member.query.get(data["member_id"])

        if not member:

            return {"message": "member not found"}

        membership_type = data["membership_type"]
        start_date = date.today()

        if membership_type == "1 week":
            end_date = start_date + timedelta(days=7)
        elif membership_type == "1 month":
            end_date = start_date + timedelta(days=30)
        elif membership_type == "6 month":
            end_date = start_date + timedelta(days=180)
        elif membership_type == "1 year":
            end_date = start_date + timedelta(days=365)
        else:
            return {"message": "invalid membership type"}

        membership = Membership(
            member_id=data["member_id"],
            membership_type=membership_type,
            start_date=start_date,
            end_date=end_date,
        )

        db.session.add(membership)
        db.session.commit()

        return {
            "message": "membership added",
            "member_name": member.name,
            "expiry_date": str(end_date),
        }

    except Exception as e:
        return {"error": str(e)}


def search_membership(page=1, per_page=4, **kwargs):
    try:
        page_obj = Member.query.order_by(Member.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        membership = db.select(Membership)
        if kwargs.get("membership_type"):
            membership = membership.where(
                Membership.membership_type == kwargs["membership_type"]
            )
            result = db.session.execute(membership).scalars().all()

        if not result:
            return error_response("Membership not found")

        output = []
        for member_data in result:
            member = db.session.get(Member, member_data.member_id)
            output.append(
                {
                    "member id": member.id,
                    "member name": member.name,
                    "phone no": member.phone_no,
                    "address": member.address,
                    "membership type": member_data.membership_type,
                    "start date": str(member_data.start_date),
                    "end date": str(member_data.end_date),
                }
            )

            return success_response(
                "membership found",
                {
                    "membership": output,
                    "total no": page_obj.total,
                    "total page": page_obj.pages,
                    "current page": page_obj.page,
                },
            )
    except Exception as e:
        return error_response(str(e))


def get_all_member(page=1, per_page=4):
    try:
        page_obj = Member.query.order_by(Member.id.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        members = []

        for member in page_obj.items:
            latest_membership = (
                Membership.query.filter_by(member_id=member.id)
                .order_by(Membership.end_date.desc())
                .first()
            )
            if latest_membership:
                membership_start_date = str(latest_membership.start_date)
                membership_end_date = str(latest_membership.end_date)
                membership_status = latest_membership.status

            else:
                membership_start_date = None
                membership_end_date = None
                membership_status = None

            members.append(
                {
                    "id": member.id,
                    "name": member.name,
                    "address": member.address,
                    "phone no": member.phone_no,
                    "membership start date": membership_start_date,
                    "membership end date": membership_end_date,
                    "membership status": membership_status,
                }
            )

        return {
            "Members": members,
            "total no": page_obj.total,
            "total page": page_obj.pages,
            "current page": page_obj.page,
        }

    except Exception as e:
        return error_response(str(e))


def search_member(**kwargs):

    member = db.select(Member)

    if kwargs.get("id"):
        member = member.where(Member.id == kwargs["id"])

    if kwargs.get("name"):
        member = member.where(Member.name.like(f"%{kwargs['name']}%"))

    result = db.session.execute(member).scalars().all()

    if not result:
        return error_response("member not found")

    output = []
    for members in result:
        latest_membership = (
            Membership.query.filter_by(member_id=members.id)
            .order_by(Membership.end_date.desc())
            .first()
        )

        if latest_membership:
            data = {
                "membership start date": str(latest_membership.start_date),
                "membership end date": str(latest_membership.end_date),
                "membership status": latest_membership.status,
            }

        else:
            data = None

        output.append(
            {
                "id": members.id,
                "name": members.name,
                "phone": members.phone_no,
                "address": members.address,
                "membership": data,
            }
        )
    return success_response("member found", output)


def update_member(member_id, data):
    try:
        member = db.session.get(Member, member_id)

        if not member:
            return error_response("member not found")

        member.name = data.get("name", member.name)
        member.phone_no = data.get("phone no", member.phone_no)
        member.address = data.get("address", member.address)

        db.session.commit()

        return success_response("member information updated")

    except Exception as e:
        return error_response(str(e))


def delete_member(member_id):
    try:
        member = db.session.get(Member, member_id)

        if not member:
            return error_response("member not found")

        memberships = Membership.query.filter_by(member_id=member.id).all()

        for membership in memberships:
            db.session.delete(membership)
        db.session.flush()

        db.session.delete(member)
        db.session.commit()

        return success_response("deleted succefully", {"deleted member id": member_id})

    except Exception as e:
        return error_response(str(e))

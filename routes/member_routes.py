from flask_restx import Namespace, Resource, fields
from flask import request
from utils.role_requirment import role_required
from services.member_service import (
    create_member,
    get_all_member,
    add_membership,
    search_member,
    search_membership,
    update_member,
    delete_member,
)

member_routes = Namespace("Member API", description="member APIs")

# swagger model
# member swagger model
create_member_model = member_routes.model(
    "Add",
    {
        "name": fields.String(required=True, description="name"),
        "phone_no": fields.String(required=True, descripton="phone_no"),
        "address": fields.String(required=True, description="address"),
    },
)

# membership swagger model
membership_model = member_routes.model(
    "membership",
    {
        "member_id": fields.Integer(required=True, description="member id"),
        "membership_type": fields.String(
            required=True, description="1 week / 1 month / 6 month / 1 year"
        ),
    },
)
# show member
show_all_member = Namespace("members", description="show all members", path="/member")

# update member
update_member_model = member_routes.model(
    "update",
    {
        "name": fields.String(required=False, description="member name"),
        "phone_no": fields.String(required=False, description="phone no"),
        "address": fields.String(required=False, description="address"),
    },
)


# create member
@member_routes.route("/create")
class create(Resource):
    @member_routes.expect(create_member_model)
    # @role_required(["superadmin","admin"])
    def post(self):
        data = request.get_json()
        return create_member(data)


# membership add
@member_routes.route("/membership")
class addmembership(Resource):
    @member_routes.expect(membership_model)
    @role_required(["superadmin", "admin"])
    def post(self):
        data = request.get_json()
        return add_membership(data)


# show all member
@member_routes.route("/show")
class Show(Resource):
    @member_routes.doc(
        params={
            "page": {"description": "Page number", "type": "int", "default": 1},
            "per_page": {
                "description": "members per page",
                "type": "int",
                "default": 4,
            },
        }
    )

    # @role_required(["superadmin","admin"])
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 4, type=int)

        return get_all_member(page, per_page)


# search member
@member_routes.route("/search")
class search(Resource):
    @member_routes.doc(
        params={
            "id": "member id",
            "name": "member name",
            "book": "member book",
        }
    )
    # @role_required(["superadmin","admin"])
    def get(self):
        data = request.args.to_dict()
        return search_member(**data)


# search membership
@member_routes.route("/membership/search")
class SearchMember(Resource):
    @member_routes.doc(
        params={
            "membership_type": "1 week / 1 month / 6 month / 1 year",
            "page": {"description": "page number", "type": "int", "default": 1},
            "per_page": {"description": "page number", "type": "int", "default": 4},
        }
    )
    # @role_required(["superadmin","admin"])
    def get(self):
        membership_type = request.args.get("membership_type")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 4, type=int)
        return search_membership(
            membership_type=membership_type, page=page, per_page=per_page
        )


# delete member
@member_routes.route("/delete/<int:member_id>")
class deleteMember(Resource):
    # @role_required(["superadmin"])
    def delete(self, member_id):
        return delete_member(member_id)


# update member
@member_routes.route("/update/<int:member_id>")
class updateMember(Resource):
    @member_routes.expect(update_member_model)
    # @role_required(["superadmin","admin"])
    def put(self, member_id):
        data = request.get_json()
        return update_member(member_id, data)

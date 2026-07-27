from flask_restx import Namespace, Resource, fields
from flask import request
from utils.role_requirment import role_required
from services.transaction_services import (
    issue_book,
    return_book,
    show_transaction,
    show_fines,
)

transaction_routes = Namespace("Transaction API", description="Transaction APIs")

# swagger model
# issue book
issue_book_model = transaction_routes.model(
    "issue",
    {
        "member_id": fields.Integer(required=True, description="member id"),
        "book_id": fields.Integer(required=True, description="Book id"),
    },
)

# return book
return_book_model = transaction_routes.model(
    "return_book",
    {"transaction_id": fields.Integer(required=True, description="Transaction id")},
)


# issue book
@transaction_routes.route("/issue")
class IssueBook(Resource):
    @transaction_routes.expect(issue_book_model)
    # @role_required(["superadmin", "admin"])
    def post(self):
        data = request.get_json()
        return issue_book(data)


# return book
@transaction_routes.route("/return")
class ReturnBook(Resource):
    @transaction_routes.expect(return_book_model)
    # @role_required(["superadmin", "admin"])
    def post(self):
        data = request.get_json()
        return return_book(data)


# show transaction
@transaction_routes.route("/show")
class ShowTransaction(Resource):
    @transaction_routes.doc(
        params={
            "page": {"description": "page", "type": "int", "default": 1},
            "per_page": {"description": "per page", "type": "int", "default": 4},
        }
    )
    # @role_required(["superadmin", "admin"])
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 4, type=int)

        return show_transaction(page, per_page)


@transaction_routes.route("/fines")
class ShowFines(Resource):

    @transaction_routes.doc(
        params={
            "page": {
                "description": "Page Number",
                "type": "int",
                "default": 1,
            },
            "per_page": {
                "description": "Records Per Page",
                "type": "int",
                "default": 4,
            },
        }
    )
    def get(self):
        page = request.args.get(
            "page",
            1,
            type=int,
        )

        per_page = request.args.get(
            "per_page",
            4,
            type=int,
        )

        return show_fines(
            page=page,
            per_page=per_page,
        )

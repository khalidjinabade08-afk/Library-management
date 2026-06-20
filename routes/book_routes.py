from flask import request
from flask_restx import Namespace, Resource, fields
from utils.role_requirment import role_required
from services.book_service import (
    add_book,
    get_all_book,
    update,
    search_book,
    delete_book,
)

book_routes = Namespace("Book API", description="Book APIs")

# swagger model
# create book
create_book_model = book_routes.model(
    "Add",
    {
        "title": fields.String(required=True, description="Book title"),
        "author": fields.String(required=True, description="author name"),
        "category": fields.String(required=True, description="Book category"),
        "quantity": fields.Integer(required=True, descriptiion="book quantity"),
        "publishes_year": fields.Integer(required=True, description="publishes year"),
        "created_at": fields.Date(required=True, description="Book added"),
    },
)
# update book
update_book = book_routes.model(
    "update",
    {
        "title": fields.String(required=True, description="Book title"),
        "author": fields.String(required=True, description="author name"),
        "category": fields.String(required=True, description="Book category"),
        "quantity": fields.Integer(required=True, descriptiion="book quantity"),
        "publishes_year": fields.Integer(required=True, description="publishes year"),
        "created_at": fields.Date(required=True, description="Book added"),
    },
)


# add book
@book_routes.route("/create")
class create(Resource):
    @book_routes.expect(create_book_model)
    # @role_required(["superadmin", "admin"])
    def post(self):
        data = request.get_json()
        return add_book(data)


# show all book
@book_routes.route("/show")
class BookList(Resource):
    @book_routes.doc(
        params={
            "page": {"description": "page", "type": "int", "default": 1},
            "per_page": {"description": "per page", "type": "int", "default": 4},
        }
    )
    # @role_required(["superadmin", "admin"])
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 4, type=int)

        return get_all_book(page, per_page)


# update books
@book_routes.route("/update/<int:book_id>")
class UpdateBook(Resource):
    @book_routes.expect(update_book)
    # @role_required(["superadmin", "admin"])
    def put(self, book_id):
        data = request.get_json()
        return update(book_id, data)


# search books
@book_routes.route("/search")
class search(Resource):
    @book_routes.doc(
        params={
            "id": "Book id",
            "title": "Book title",
        }
    )
    # @role_required(["superadmin", "admin"])
    def get(self):
        data = request.args.to_dict()
        return search_book(**data)


# delete book
@book_routes.route("/delete/<int:book_id>")
class deleteBook(Resource):
    # @role_required(["superadmin"])
    def delete(self, book_id):
        return delete_book(book_id)

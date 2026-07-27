from models.book_model import book
from models.transaction_model import Transaction
from sqlalchemy import select, func
from database.db import db
from flask import session
from datetime import datetime
from utils.response import success_response, error_response


def add_book(data):
    try:
        initial_quantity = data["quantity"]
        new_book = book(
            title=data["title"],
            author=data["author"],
            category=data["category"],
            quantity=initial_quantity,
            available_quantity=initial_quantity,
            publishes_year=data["publishes_year"],
            created_at=datetime.strptime(data["created_at"], "%Y-%m-%d").date(),
        )
        db.session.add(new_book)
        db.session.commit()
        return success_response("Book added successfully")

    except Exception as e:
        return error_response(str(e))


def get_all_book(page=1, per_page=4):
    try:
        page_obj = book.query.order_by(book.id.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        books = []

        for b in page_obj.items:
            books.append(
                {
                    "id": int(b.id),
                    "title": b.title,
                    "author": b.author,
                    "category": b.category,
                    "quantity": int(b.quantity),
                    "available_quantity": int(b.available_quantity),
                    "publishes_year": (
                        int(b.publishes_year) if b.publishes_year is not None else None
                    ),
                    "created_at": str(b.created_at) if b.created_at else None,
                }
            )

        total_available = book.query.filter(book.available_quantity > 0).count()

        return success_response(
            "Books retrieved successfully",
            {
                "books found": int(len(books)),
                "title": books,
                "total records": int(page_obj.total),
                "available books": int(total_available),
                "current page": int(page_obj.page),
                "total pages": int(page_obj.pages),
                "per page": int(page_obj.per_page),
            }
        )

    except Exception as e:
        return error_response(str(e))


def update(book_id, data):
    try:
        Book = db.session.get(book, book_id)

        if not Book:
            return error_response("Book not find")

        new_quantity = data.get("quantity", Book.quantity)
        if new_quantity != Book.quantity:
            quantity_diffrence = new_quantity - Book.quantity
            Book.available_quantity += quantity_diffrence

        Book.title = data.get("title", Book.title)
        Book.author = data.get("author", Book.author)
        Book.category = data.get("category", Book.category)
        Book.quantity = data.get("quantity", Book.quantity)
        Book.publishes_year = data.get("publishes_year", Book.publishes_year)
        Book.created_at = data.get("created_at", Book.created_at)

        if "created_at" in data:
            Book.created_at = datetime.strptime(data["created_at"], "%Y-%m-%d").date()

        db.session.commit()
        return success_response("Book information updated")

    except Exception as e:
        return error_response(str(e))


def search_book(**kwargs):
    try:
        query = select(book)

        if kwargs.get("id"):
            query = query.where(book.id == kwargs["id"])

        if kwargs.get("title"):
            query = query.where(book.title.ilike(f"%{kwargs['title']}%"))

        result = db.session.execute(query).scalars().all()

        if not result:
            return error_response("Book not found")

        output = []

        for Books in result:
            output.append(
                {
                    "id": Books.id,
                    "title": Books.title,
                    "author": Books.author,
                    "category": Books.category,
                    "quantity": Books.quantity,
                    "Book available quantity": Books.available_quantity,
                    "publishes year": Books.publishes_year,
                    "created at": str(Books.created_at) if Books.created_at else None,
                }
            )

        return success_response("Book found", output)

    except Exception as e:
        return error_response(str(e))


def delete_book(book_id):
    try:
        Book = db.session.get(book, book_id)

        if not Book:
            return error_response("book not found")

        Transaction.query.filter_by(book_id=book_id).delete()
        db.session.delete(Book)
        db.session.commit()

        return success_response("Book deleted successfully")

    except Exception as e:
        return error_response(str(e))


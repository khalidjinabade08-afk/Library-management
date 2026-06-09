from models.book_model import book
from sqlalchemy import select, func
from database.db import db
from flask import session
from datetime import datetime
from utils.response import success_response, error_response


def add_book(data):
    try:
        new_book = book(
            title=data["title"],
            author=data["author"],
            category=data["category"],
            quantity=data["quantity"],
            publishes_year=data["publishes_year"],
            created_at=datetime.strptime(data["created_at"], "%Y-%m-%d").date(),
        )
        db.session.add(new_book)
        db.session.commit()
        return success_response("Book added succefully")

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
                    "id": b.id,
                    "title": b.title,
                    "author": b.author,
                    "category": b.category,
                    "quantity": b.quantity,
                    "available_quantity": b.available_quantity,
                    "publishes_year": b.publishes_year,
                    "created_at": b.created_at.strftime("%y-%m-%d"),
                }
            )

        total_available = (
            db.session.query(func.sum(book.available_quantity)).scalar() or 0
        )

        return success_response(
            {
                "books found": len(books),
                "title": books,
                "total records": page_obj.total,
                "available books": total_available,
                "current page": page_obj.page,
                "total pages": page_obj.pages,
                "per page": page_obj.per_page,
            }
        )

    except Exception as e:
        return error_response(str(e))


def update(book_id, data):
    try:
        Book = db.session.get(book, book_id)

        if not Book:
            return error_response("Book not find")

        Book.title = data.get("title", Book.title)
        Book.author = data.get("author", Book.author)
        Book.category = data.get("category", Book.category)
        Book.quantity = data.get("quantity", Book.quantity)
        Book.publishes_year = data.get("publishes_year", Book.publishes_year)
        Book.created_at = data.get("created_at", Book.created_at)

        db.session.commit()
        return success_response("Book information updated")

    except Exception as e:
        return error_response(str(e))


def search_book(**kwargs):
    try:
        Book = db.select(book)

        if kwargs.get("id"):
            Book = Book.where(book.id == kwargs["id"])

        if kwargs.get("title"):
            Book = Book.where(book.title.ilike(f"%{kwargs['title']}%"))

        result = db.session.execute(Book).scalars().all()

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
                    "created at": Books.created_at.strftime("%Y-%m-%d"),
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
        db.session.delete(Book)
        db.session.commit()

        return success_response("Book deleted successfully")

    except Exception as e:
        return error_response(str(e))

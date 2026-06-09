from models.transaction_model import Transaction
from models.book_model import book
from models.member_model import Member
from sqlalchemy import select
from database.db import db
from flask import session
from datetime import date, timedelta
from utils.response import error_response, success_response


def issue_book(data):
    try:
        member_id = data.get("member_id")
        book_id = data.get("book_id")

        member = db.session.get(Member, member_id)
        if not member:
            return error_response("Member not found")

        target_book = db.session.get(book, book_id)
        if not target_book:
            return error_response("Book not found")

        if target_book.quantity <= 0:
            return error_response("Book is out of stock")

        new_transaction = Transaction(
            member_id=member_id,
            book_id=book_id,
            issue_date=date.today(),
            due_date=date.today() + timedelta(days=30),
            status="issued",
        )

        db.session.add(new_transaction)
        target_book.quantity -= 1
        db.session.commit()
        return success_response(
            "Book issued successfully",
            {
                "transaction id": new_transaction.id,
                "member id": member_id,
                "book id": book_id,
                "issue date": str(new_transaction.issue_date),
                "due date": str(new_transaction.due_date),
                "status": new_transaction.status,
            },
        )
    except Exception as e:
        return error_response(str(e))


def return_book(data):
    try:
        transaction_id = data.get("transaction_id")

        transaction = db.session.get(Transaction, transaction_id)

        if not transaction:
            return error_response("Transaction not found")

        if transaction.status == "returned":
            return error_response("Book already returned")

        Book = db.session.get(book, transaction.book_id)

        if not Book:
            return error_response("Book not found")

        transaction.return_date = date.today()
        transaction.status = "returned"

        fine = 0
        if transaction.return_date > transaction.due_date:
            late_days = (transaction.return_date - transaction.due_date).days

            fine = late_days * 10

        transaction.fine_amount = fine

        Book.quantity += 1
        db.session.commit()

        return success_response(
            "Book returned successfully",
            {
                "transaction id": transaction.id,
                "book id": transaction.book_id,
                "member id": transaction.member_id,
                "return date": str(transaction.return_date),
                "fine amount": float(transaction.fine_amount),
                "status": transaction.status,
            },
        )

    except Exception as e:
        return error_response(str(e))


def show_transaction(page=1, per_page=4):
    try:
        page_obj = Transaction.query.order_by(Transaction.id.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        transactions = []

        for transaction in page_obj.items:
            transactions.append(
                {
                    "id": transaction.id,
                    "member_id": transaction.member_id,
                    "book_id": transaction.book_id,
                    "issue_date": transaction.issue_date.strftime("%Y-%m-%d"),
                    "due_date": transaction.due_date.strftime("%Y-%m-%d"),
                    "return_date": (
                        transaction.return_date.strftime("%Y-%m-%d")
                        if transaction.return_date
                        else None
                    ),
                    "fine_amount": float(transaction.fine_amount or 0.0),
                    "status": transaction.status,
                }
            )

        return success_response(
            "transactions found",
            {
                "transaction": transactions,
                "total_records": page_obj.total,
                "current_page": page_obj.page,
                "total_pages": page_obj.pages,
                "per_page": page_obj.per_page,
            },
        )

    except Exception as e:
        return error_response(str(e))

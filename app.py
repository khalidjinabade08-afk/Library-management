from flask import Flask
from flask_restx import Api
from dotenv import load_dotenv
import os

from config import config
from database.db import db

# Models
from models.user_model import User
from models.member_model import Member
from models.book_model import book
from models.transaction_model import Transaction

# Routes
from routes.user_routes import auth_routes
from routes.member_routes import member_routes
from routes.book_routes import book_routes
from routes.transaction_routes import transaction_routes

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("secret_key")
app.config.from_object(config)

db.init_app(app)

api = Api(
    app,
    title="Library Management System API",
    version="1.0",
    description="Library Management System",
    doc="/swagger"
)

api.add_namespace(auth_routes, path="/auth")
api.add_namespace(member_routes, path="/member")
api.add_namespace(book_routes, path="/book")
api.add_namespace(transaction_routes, path="/transaction")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5501,
        debug=True
    )
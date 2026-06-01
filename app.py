from flask import Flask
from flask_restx import Api
import os 
from dotenv import load_dotenv


from config import config
from database.db import db
from models.user_model import user
from routes.user_routes import auth_routes
from models.member_model import Member
from routes.member_routes import member_routes
from models.book_model import book
from routes.book_routes import book_routes
from models.transaction_model import Transaction
from routes.transaction_routes import transaction_routes

load_dotenv()
app = Flask(__name__)

app.config.from_object(config)
db.init_app(app) 

app.secret_key=os.getenv("secret_key")

#create table
with app.app_context():
    db.create_all()

api = Api(app,title="libraty management API",doc="/swagger") 
api.add_namespace(auth_routes)
api.add_namespace(member_routes)
api.add_namespace(book_routes)
api.add_namespace(transaction_routes)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5501)
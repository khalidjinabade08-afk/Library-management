import os 
from dotenv import load_dotenv

load_dotenv()

class config:
    host = os.getenv("DB_host")
    user = os.getenv("DB_user")
    password = os.getenv("DB_password")
    name = os.getenv("DB_name")
    port = os.getenv("DB_port")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{user}:{password}@{host}:{port}/{name}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

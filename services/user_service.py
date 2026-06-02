from models.user_model import User
from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from utils.response import error_response, success_response

# Register
def register(data):
    try:
        username = data.get("username").lower()
        name = data.get("name")
        password = data.get("password")
        role = data.get("role")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return error_response("Username already exists", 400)
    
        if role not in ["admin","superadmin"]:
            return error_response("invalid role select",400)
    
        new_user = User(
            name=name,
            username=username,
            password=generate_password_hash(password),
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return success_response(
            "User registered successfully",
            {
                "username": new_user.username,
                "role": new_user.role
            },
            201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f"Internal error: {str(e)}", 500)

# Login
def login(data):
    try:
        username = data.get("username").lower()
        password = data.get("password")

        current_user = User.query.filter_by(username=username).first()

        if not current_user:
            return error_response("User not found", 404)
        
        if not check_password_hash(current_user.password, password):
            return error_response("Invalid password", 401)

        session["user_id"] = current_user.id
        session["role"] = current_user.role

        return success_response(
            "Login Successful",
            {
                "id": current_user.id,
                "username": current_user.username,
                "role": current_user.role
            }
        )

    except Exception as e:
        return error_response(str(e), 500)
    
# Change Password
def change(data):
    try:
        username = data.get("username").lower()
        current_user = User.query.filter_by(username=username).first()
        
        if not current_user:
            return error_response("User not found", 404)
        
        if not check_password_hash(current_user.password, data.get("old_password")):
            return error_response("Old password is incorrect", 401)
        
        current_user.password = generate_password_hash(data.get("new_password"))
        db.session.commit()
        return success_response("Password changed successfully")
       
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)
    
# Delete User
def delete(user_id):
    try:
        current_user = db.session.get(User, user_id)

        if not current_user:
            return error_response("User not found", 404)
        
        db.session.delete(current_user)
        db.session.commit()
        return success_response("User deleted successfully")
    
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 500)
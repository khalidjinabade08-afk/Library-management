from models.user_model import user
from database.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from utils.response import error_response, success_response

# register
def register(data):
    try:
        existing_user = user.query.filter_by(username = data["username"]).first()

        if existing_user:
            return error_response("Username already exixsts",400)
    

        role = data.get("role","admin")
        if role not in ["admin","superadmin"]:
            return error_response("invalid role",400)
    
        new_user = user(
                    name = data["name"],
                    username=data["username"],
                    password=generate_password_hash(data["password"]),
                    role=role
                    )

        db.session.add(new_user)
        db.session.commit()

        return success_response(
                                "User registered successflly",
                                {
                                "username":new_user.username,
                                "role": new_user.role
                                },
                                201)

    except Exception as e:
        return error_response(str(e))


# Login
def login(data):
    try:
        username = data.get("username")
        password = data.get("password")

        User = user.query.filter_by(username=username).first()

        if not User:
            return error_response("user not found")
        
        if not check_password_hash(User.password,password):
            return error_response("invalid password")


        session["user_id"]=User.id
        session["role"]=User.role

        return success_response(
            "Login Successful",
            {
            "id": User.id,
            "username":User.username,
            "role": User.role
            })

    except Exception as e:
        return error_response(str(e))
    

# change password
def change(data):
    try:

        User = user.query.filter_by(username=data["username"]).first()
        if not User:
            return error_response("user not found")
        
        if not check_password_hash(User.password, data["old_password"]):
            return error_response("old password is incorrect")
        
        User.password = generate_password_hash(data["new_password"])
        db.session.commit()
        return success_response("password change succesfully")
       
    except Exception as e:
        return error_response(str(e))
    

# delete user
def delete(user_id):
    try:
        User = db.session.get(user,user_id)

        if not User:
            return error_response("user not found")
        
        db.session.delete(User)
        db.session.commit()
        return success_response("user deleted successfully")
    
    except Exception as e:
        return error_response(str(e))
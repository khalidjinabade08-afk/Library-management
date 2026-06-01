from utils.response import error_response
from functools import wraps
from flask import session


def role_required(allowed_roles):
    def decotators(func):
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = session.get("role")
            if not role:
                return error_response("Unauthorized please login",401)
            
            if role not in allowed_roles:
                return error_response("Access denined", 403)
            
            return func(*args, **kwargs)
        
        return wrapper
    
    return decotators
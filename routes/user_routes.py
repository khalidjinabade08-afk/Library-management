from flask_restx import Namespace, Resource, fields
from flask import request
from utils.role_requirment import role_required
from services.user_service import (register, login, change, delete)

auth_routes = Namespace("Admin API", description="Authentication APIs")

#swagger model
register_model = auth_routes.model("Register",{
    "name":fields.String(required=True, description= "name"),
    "username":fields.String(required = True, description = "username"),
    "password":fields.String(required = True, description = "Password"),
    "role":fields.String(required = True, description = "admin/superadmin")
})

login_model = auth_routes.model("Login",{
    "username":fields.String(required = True, description = "Username"),
    "password":fields.String(required = True, description = "Password")
})

password_model = auth_routes.model("change_password",{
    "username":fields.String(required=True, description="username"),
    "old_password":fields.String(required=True, description="old_password"),
    "new_password":fields.String(required=True, description="new_password")
})


#Register
@auth_routes.route("/register")
class Register(Resource):
    @auth_routes.expect(register_model)
    def post(self):
        data=request.get_json()
        return register(data)
    

# login
@auth_routes.route("/login")
class Login(Resource):
    @auth_routes.expect(login_model)
    def post(self):
        data = request.get_json()
        return login(data)
    
# change password
@auth_routes.route("/change_password")
class changePassword(Resource):
    @auth_routes.expect(password_model)
    @role_required(["superadmin","admin"])
    def put(self):
        data = request.get_json()
        return change(data)
    
# delete user
@auth_routes.route("/delete/<int:user_id>")
class deleteUser(Resource):
    @role_required(["superadmin"])
    def delete(self,user_id):
        return delete(user_id)
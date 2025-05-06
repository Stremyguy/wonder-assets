from flask_restful import Resource, abort
from app.services.user_service import get_all_users, get_user_by_id, delete_user, create_user, change_user_roles
from app.resources.parsers.user_parser import user_post_args, user_roles_args


class UserResource(Resource):
    def get(self, user_id: int) -> dict:
        user = get_user_by_id(user_id)
        
        if not user:
            abort(404, message="User not found")
        
        return {"user": user.to_dict()}
    
    def delete(self, user_id: int) -> dict:
        if not delete_user(user_id):
            abort(404, message="User not found")
        
        return {"success": "OK"}

    def put(self, user_id: int) -> dict:
        args = user_roles_args.parse_args()
        role_names = args["role_names"]
        
        user = change_user_roles(user_id, role_names)
        
        if not user:
            abort(404, message="User not found")
        
        return {"success": "OK", "user": user.to_dict()}


class UsersResource(Resource):
    def get(self) -> dict:
        users = get_all_users()
        
        return {"users": [user.to_dict() for user in users]}
    
    def post(self) -> dict:
        args = user_post_args.parse_args()
        
        user = create_user(
            username=args["username"],
            email=args["email"],
            password=args["password"],
            avatar_url=args["avatar_url"],
            bio=args["bio"],
        )
        
        return {"success": "OK", "user": user.to_dict()}

from flask_restful import Resource, abort
from app.services.role_service import get_all_roles, get_role_by_id, delete_role, create_role
from app.resources.parsers.role_parser import role_post_args


class RoleResource(Resource):
    def get(self, role_id: int) -> dict:
        role = get_role_by_id(role_id)
        
        if not role:
            abort(404, message="Role not found")
        
        return {"role": role.to_dict()}
    
    def delete(self, role_id: int) -> dict:
        if not delete_role(role_id):
            abort(404, message="Role not found")
        
        return {"success": "OK"}


class RolesResource(Resource):
    def get(self) -> dict:
        roles = get_all_roles()
        
        return {"roles": [role.to_dict() for role in roles]}
    
    def post(self) -> dict:
        args = role_post_args.parse_args()
        
        role = create_role(
            name=args["name"],
        )
        
        return {"success": "OK", "role": role.to_dict()}

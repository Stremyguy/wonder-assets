from flask_restful import Resource, abort
from app.services.type_service import get_all_types, get_type_by_id, delete_type, create_type
from app.resources.parsers.type_parser import type_post_args


class TypeResource(Resource):
    def get(self, type_id: int) -> dict:
        type = get_type_by_id(type_id)
        
        if not type:
            abort(404, message="Type not found")
        
        return {"type": type.to_dict()}
    
    def delete(self, type_id: int) -> dict:
        if not delete_type(type_id):
            abort(404, message="Type not found")
        
        return {"success": "OK"}


class TypesResource(Resource):
    def get(self) -> dict:
        types = get_all_types()
        
        return {"types": [type.to_dict() for type in types]}
    
    def post(self) -> dict:
        args = type_post_args.parse_args()
        
        type = create_type(
            name=args["name"],
            icon_url=args["icon_url"],
        )
        
        return {"success": "OK", "type": type.to_dict()}

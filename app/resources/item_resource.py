from flask_restful import Resource, abort
from app.services.item_service import get_all_items, get_item_by_id, delete_item, create_item
from app.resources.parsers.item_parser import item_post_args


class ItemResource(Resource):
    def get(self, item_id: int) -> dict:
        item = get_item_by_id(item_id)
        
        if not item:
            abort(404, message="Item not found")
        
        return {"item": item.to_dict()}
    
    def delete(self, item_id: int) -> dict:
        if not delete_item(item_id):
            abort(404, message="Item not found")
        
        return {"success": "OK"}


class ItemsResource(Resource):
    def get(self) -> dict:
        items = get_all_items()
        
        return {"items": [item.to_dict() for item in items]}
    
    def post(self) -> dict:
        args = item_post_args.parse_args()
        
        item = create_item(
            title=args["title"],
            description=args["description"],
            item_url=args["item_url"],
            images=args["images"],
            type_id=args["type_id"],
            category_id=args["category_id"],
            creator_id=args["creator_id"],
            is_private=args["is_private"],
            show_meta=args["show_meta"],
            can_download=args["can_download"],
        )
        
        return {"success": "OK", "item": item.to_dict()}

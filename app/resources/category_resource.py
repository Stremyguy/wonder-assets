from flask import jsonify
from flask_restful import Resource, abort
from app.services.category_service import get_all_categories, get_category_by_id, delete_category, create_category
from app.resources.parsers.category_parser import category_post_args


class CategoryResource(Resource):
    def get(self, category_id: int) -> dict:
        category = get_category_by_id(category_id)
        
        if not category:
            abort(404, message="Category not found")
        
        return {"category": category.to_dict()}
    
    def delete(self, category_id: int) -> dict:
        if not delete_category(category_id):
            abort(404, message="Category not found")
        
        return {"success": "OK"}


class CategoriesResource(Resource):
    def get(self) -> dict:
        categories = get_all_categories()
        
        return {"categories": [category.to_dict() for category in categories]}
    
    def post(self) -> dict:
        args = category_post_args.parse_args()
        
        category = create_category(
            title=args["title"],
            short_description=args["short_description"],
            full_description=args["full_description"],
            creator_id=args["creator_id"],
            role_ids=args["role_ids"],
            is_private=args["is_private"],
            is_testing=args["is_testing"],
        )
        
        return {"success": "OK", "category": category.to_dict()}

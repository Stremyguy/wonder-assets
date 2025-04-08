from flask import jsonify
from flask_restful import Resource, abort
from app.scripts import db_session
from app.models import Categories
from app.resources.parsers.category_parser import category_post_args
from sqlalchemy.orm import Session


def get_category_or_404(category_id: int, session: Session) -> Categories:
    category = session.query(Categories).get(category_id)
    
    if not category:
        abort(404, message=f"Category {category_id} not found")
    
    return category


class CategoryResource(Resource):
    def get(self, category_id: int) -> dict:
        session = db_session.create_session()
        category = get_category_or_404(category_id, session)
        
        return jsonify({"category": category.to_dict()})
    
    def delete(self, category_id: int) -> dict:
        session = db_session.create_session()
        category = get_category_or_404(category_id, session)
        
        session.delete(category)
        session.commit()
        
        return jsonify({"success": "OK"})


class CategoriesResource(Resource):
    def get(self) -> dict:
        session = db_session.create_session()
        categories = session.query(Categories).all()
        
        return jsonify({"categories": [category.to_dict() for category in categories]})
    
    def post(self) -> dict:
        args = category_post_args.parse_args()
        session = db_session.create_session()
        
        category = Categories(
            title=args["title"],
            description=args["description"],
            is_testing=args["is_testing"],
        )
        
        session.add(category)
        session.commit()
        
        return jsonify({"success": "OK"})

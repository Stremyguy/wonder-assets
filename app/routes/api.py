from flask_restful import Api
from app.resources.category_resource import CategoryResource, CategoriesResource


def register_api_routes(app: None) -> None:
    api = Api(app)
    api.add_resource(CategoriesResource, "/api/categories")
    api.add_resource(CategoryResource, "/api/categories/<int:category_id>")

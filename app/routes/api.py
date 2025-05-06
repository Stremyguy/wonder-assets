from flask_restful import Api
from app.resources.user_resource import UserResource, UsersResource
from app.resources.role_resource import RoleResource, RolesResource
from app.resources.category_resource import CategoryResource, CategoriesResource
from app.resources.type_resource import TypeResource, TypesResource
from app.resources.item_resource import ItemResource, ItemsResource


def register_api_routes(app: None) -> None:
    api = Api(app)

    # Users API
    api.add_resource(UsersResource, "/api/users")
    api.add_resource(UserResource, "/api/users/<int:user_id>")

    # Roles API
    api.add_resource(RolesResource, "/api/roles")
    api.add_resource(RoleResource, "/api/roles/<int:role_id>")

    # Categories API
    api.add_resource(CategoriesResource, "/api/categories")
    api.add_resource(CategoryResource, "/api/categories/<int:category_id>")

    # Types API
    api.add_resource(TypesResource, "/api/types")
    api.add_resource(TypeResource, "/api/types/<int:type_id>")

    # Items API
    api.add_resource(ItemsResource, "/api/items")
    api.add_resource(ItemResource, "/api/items/<int:item_id>")


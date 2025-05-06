from app.scripts import db_session
from app.models import Category, Role
from app.permissions import has_permission
from sqlalchemy.orm import joinedload


def get_all_categories() -> list[Category]:
    session = db_session.create_session()
    return session.query(Category).options(
        joinedload(Category.creator),
        joinedload(Category.visible_to_roles)
    ).all()


def get_category_by_id(category_id: int) -> Category | None:
    session = db_session.create_session()
    return session.query(Category).options(
        joinedload(Category.creator),
        joinedload(Category.visible_to_roles)
    ).filter(Category.id == category_id).first()


def delete_category(category_id: int) -> bool:
    session = db_session.create_session()
    category = session.query(Category).get(category_id)

    if category:
        session.delete(category)
        session.commit()
        return True
    return False


def create_category(title: str, 
                    short_description: str,
                    full_description: str,
                    creator_id: int,
                    role_ids: list[int],
                    is_private: bool, 
                    is_testing: bool) -> Category | None:
    session = db_session.create_session()
    category = Category(
        title=title,
        short_description=short_description,
        full_description=full_description,
        creator_id=creator_id,
        is_private=is_private,
        is_testing=is_testing
    )
    
    roles = session.query(Role).filter(Role.id.in_(role_ids)).all()
    category.visible_to_roles = roles
    
    session.add(category)
    session.commit()
    
    return category


def edit_category(category_id: int, 
                  title: str, 
                  short_description: str,
                  full_description: str, 
                  role_ids: list[int],
                  is_private: bool, 
                  is_testing: bool) -> Category | None:
    session = db_session.create_session()
    category = session.get(Category, category_id)
    
    if not category:
        return None
    
    category.title = title
    category.short_description = short_description
    category.full_description = full_description
    category.is_private = is_private
    category.is_testing = is_testing
    
    roles = session.query(Role).filter(Role.id.in_(role_ids)).all()
    category.visible_to_roles = roles
    
    session.commit()
    
    return category


def filter_visible_categories(categories: list[Category], user) -> list[Category]:
    if user.is_authenticated:
        user_role_ids = {role.id for role in user.roles}
        can_view_private = has_permission(user, "view_private_category")
    else:
        user_role_ids = {1}
        can_view_private = False
    
    visible = []
    for category in categories:
        if category.is_private:
            if (
                user.is_authenticated and
                (category.creator_id == user.id or can_view_private)
            ):
                visible.append(category)
        else:
            if (
                (user.is_authenticated and category.creator_id == user.id)
                or can_view_private
                or any(role.id in user_role_ids for role in category.visible_to_roles)
            ):
                visible.append(category)
    
    return visible

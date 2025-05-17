import os
from app.scripts import db_session
from app.models import Item, User
from app.permissions import has_permission
from app.utils import get_file_size
from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from flask import current_app


def get_all_items() -> list[Item]:
    session = db_session.create_session()
    return session.query(Item).options(
        joinedload(Item.creator),
        joinedload(Item.category),
        joinedload(Item.type)
    ).all()


def get_items_by_category_id(category_id: int, 
                             search_query: str = None,
                             sort_by: str = None) -> list[Item]:
    session = db_session.create_session()
    query = session.query(Item).options(
        joinedload(Item.creator),
        joinedload(Item.type)
    ).filter(Item.category_id == category_id)

    if search_query:
        query = query.filter(or_(
            Item.title.ilike(f"%{search_query}%"),
            Item.description.ilike(f"%{search_query}%")
        ))
    
    if sort_by:
        if sort_by == "title_asc":
            query = query.order_by(Item.title.asc())
        elif sort_by == "title_desc":
            query = query.order_by(Item.title.desc())
        elif sort_by == "date_asc":
            query = query.order_by(Item.created_date.asc())
        else:
            query = query.order_by(Item.created_date.desc())

    return query.all()


def get_items_by_creator_id(creator_id: int) -> list[Item]:
    session = db_session.create_session()
    return session.query(Item).options(
        joinedload(Item.creator),
        joinedload(Item.category),
        joinedload(Item.type)
    ).filter(Item.creator_id == creator_id).all()


def get_item_by_id(item_id: int) -> Item | None:
    session = db_session.create_session()
    return session.query(Item).options(
        joinedload(Item.creator),
        joinedload(Item.category),
        joinedload(Item.type)
    ).filter(Item.id == item_id).first()


def delete_item(item_id: int) -> bool:
    session = db_session.create_session()
    item = session.query(Item).options(
        joinedload(Item.creator),
        joinedload(Item.category),
        joinedload(Item.type)
    ).get(item_id)

    if item:
        if item.item_url:
            try:
                file_path = os.path.join(current_app.config["ITEMS_FOLDER"], item.item_url)
                
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as exc:
                current_app.logger.error(f"Failed to delete item file {item.item_url}")
        
        session.delete(item)
        session.commit()
        return True
    return False


def create_item(title: str, 
               description: str,
               item_url: str,
               type_id: int,
               category_id: int,
               creator_id: int,
               is_private: bool,
               show_meta: bool,
               can_download: bool,
               ) -> Item | None:
    session = db_session.create_session()
    
    try:
        file_size = 0
        if item_url:
            file_path = os.path.join(current_app.config["ITEMS_FOLDER"], item_url)
            file_size = get_file_size(file_path)
        
        item = Item(
            title=title,
            description=description,
            item_url=item_url,
            file_size_bytes=file_size,
            type_id=type_id,
            category_id=category_id,
            creator_id=creator_id,
            show_meta=show_meta,
            is_private=is_private,
            can_download=can_download,
        )
        
        session.add(item)
        session.commit()
        
        return item
    except Exception as exc:
        session.rollback()
        current_app.logger.error(f"Database error creating item: {str(exc)}")
        return None


def edit_item(item_id: int, 
             title: str,
             description: str,
             item_url: str,
             type_id: int,
             category_id: int,
             creator_id: int,
             show_meta: bool,
             is_private: bool,
             can_download: bool,
             new_file=None) -> Item | None:
    session = db_session.create_session()
    try:
        item = session.get(Item, item_id)
        
        if not item:
            return None
        
        file_size = item.file_size_bytes
        if item_url and item_url != item.item_url:
            file_path = os.path.join(current_app.config["ITEMS_FOLDER"], item_url)
            file_size = get_file_size(file_path)
        
        item.title = title
        item.description = description
        item.item_url = item_url
        item.file_size_bytes = file_size
        item.type_id = type_id
        item.category_id = category_id
        item.creator_id = creator_id
        item.show_meta = show_meta
        item.is_private = is_private
        item.can_download = can_download

        session.commit()
        return item
        
    except Exception as exc:
        session.rollback()
        current_app.logger.error(f"Database error editing item: {str(exc)}")
        return None


def favorite_item_actions(user_id: int, item_id: int) -> dict:
    session = db_session.create_session()
    try:
        user = session.query(User).options(joinedload(User.favorite_items)).get(user_id)
        item = session.query(Item).get(item_id)
        
        if not user or not item:
            return None
        
        is_favorited = any(fav_item.id == item_id for fav_item in user.favorite_items)
        
        if is_favorited:
            user.favorite_items.remove(item)
            action = "removed"
        else:
            user.favorite_items.append(item)
            action = "added"
        
        session.commit()
        return {
            "status": "success",
            "action": action,
            "item_id": item_id,
            "is_favorited": not is_favorited
        }
    except Exception as e:
        session.rollback()
        current_app.logger.error(f"Error in favorite_item_actions: {str(e)}")
        return None
    finally:
        session.close()


def filter_visible_items(items: list[Item], user) -> list[Item]:
    if user.is_authenticated:
        can_view_private = has_permission(user, "view_private_item")
    else:
        can_view_private = False
    
    visible = []
    for item in items:
        if item.is_private:
            if (
                user.is_authenticated and
                (item.creator_id == user.id or can_view_private)
            ):
                visible.append(item)
        else:
            visible.append(item)

    return visible

import os
from app.scripts import db_session
from app.models import Item, ItemImage
from app.permissions import has_permission
from sqlalchemy.orm import joinedload
from flask import current_app


def get_all_items() -> list[Item]:
    session = db_session.create_session()
    return session.query(Item).options(
        joinedload(Item.creator),
        joinedload(Item.images),
        joinedload(Item.type)
    ).all()


def get_items_by_category_id(category_id: int) -> list[Item]:
    session = db_session.create_session()
    return session.query(Item).options(
        joinedload(Item.creator),
        joinedload(Item.images),
        joinedload(Item.type)
    ).filter(Item.category_id == category_id).all()


def get_item_by_id(item_id: int) -> Item | None:
    session = db_session.create_session()
    return session.query(Item).options(
        joinedload(Item.creator),
        joinedload(Item.images),
        joinedload(Item.type)
    ).filter(Item.id == item_id).first()


def delete_item(item_id: int) -> bool:
    session = db_session.create_session()
    item = session.query(Item).options(
        joinedload(Item.creator),
        joinedload(Item.images),
        joinedload(Item.type)
    ).get(item_id)

    if item:
        for image in item.images:
            try:
                image_path = os.path.join(current_app.config["IMAGES_FOLDER"], image.image_url)
                
                if os.path.exists(image_path):
                    if image.image_url != "item_logo_default.png":
                        os.remove(image_path)
            except Exception as exc:
                current_app.logger.error(f"Failed to delete image {image.image_url}")
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
               images: list[str] = None,
               ) -> Item | None:
    session = db_session.create_session()
    
    try:
        item = Item(
            title=title,
            description=description,
            item_url=item_url,
            type_id=type_id,
            category_id=category_id,
            creator_id=creator_id,
            show_meta=show_meta,
            is_private=is_private,
            can_download=can_download
        )
        
        image_objects = []
        if images:
            for i, img_url in enumerate(images):
                image_objects.append(ItemImage(
                    image_url=img_url,
                    display_order=i
                ))
        else:
            image_objects.append(ItemImage(
                image_url="item_logo_default.png",
                display_order=0
            ))
        
        item.images = image_objects
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
             images: list,
             type_id: int,
             category_id: int,
             creator_id: int,
             show_meta: bool,
             is_private: bool,
             can_download: bool) -> Item | None:
    session = db_session.create_session()
    try:
        item = session.get(Item, item_id)
        
        if not item:
            return None
        
        item.title = title
        item.description = description
        item.item_url = item_url
        item.type_id = type_id
        item.category_id = category_id
        item.creator_id = creator_id
        item.show_meta = show_meta
        item.is_private = is_private
        item.can_download = can_download

        existing_images = {img.image_url for img in item.images}
        new_images = set(images)
        
        to_delete = existing_images - new_images
        for img in item.images[:]:
            if img.image_url in to_delete:
                try:
                    if img.image_url != "item_logo_default.png":
                        image_path = os.path.join(current_app.config["IMAGES_FOLDER"], img.image_url)
                        if os.path.exists(image_path):
                            os.remove(image_path)
                except Exception as exc:
                    current_app.logger.error(f"Failed to delete image {img.image_url}: {str(exc)}")
                session.delete(img)
        
        to_add = new_images - existing_images
        for i, img_url in enumerate(images):
            if img_url in to_add:
                item.images.append(ItemImage(
                    image_url=img_url,
                    display_order=i
                ))
        
        session.commit()
        return item
        
    except Exception as exc:
        session.rollback()
        current_app.logger.error(f"Database error editing item: {str(exc)}")
        return None


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

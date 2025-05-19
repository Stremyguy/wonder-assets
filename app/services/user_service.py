import os
import uuid
from app.scripts import db_session
from app.models import User, Role
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from flask import current_app
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.utils import secure_filename
from PIL import Image
from typing import Optional, List


def get_all_users() -> list[User]:
    session = db_session.create_session()
    
    return session.query(User).options(joinedload(User.roles)).all()


def get_user_by_id(user_id: int) -> Optional[User]:
    session = db_session.create_session()

    return session.query(User).options(joinedload(User.roles)).get(user_id)


def delete_user(user_id: int) -> bool:
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if not user:
        return False
    
    session.delete(user)
    session.commit()
    
    return True


def create_user(username: str, 
                email: str, 
                password: str, 
                avatar_url: Optional[str] = None,
                bio: Optional[str] = None) -> Optional[User]:
    session = db_session.create_session()
    
    if avatar_url is None:
        avatar_url = f"images/profile_pics/default.png"
        
    user = User(
        username=username,
        email=email,
        avatar_url=avatar_url,
        bio=bio,
    )

    user.set_password(password)
        
    default_role = session.query(Role).filter(Role.name == "user").first()
    if default_role:
        user.roles.append(default_role)
        
    session.add(user)
    session.commit()
            
    return user


def edit_user(user_id: int, 
              username: Optional[str] = None, 
              email: Optional[str] = None, 
              password: Optional[str] = None, 
              avatar_url: Optional[str] = None,
              bio: Optional[str] = None) -> User | None:
    session = db_session.create_session()
    
    user = session.get(User, user_id)
        
    if not user:
        return None
        
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if password is not None:
        user.set_password(password)
    if avatar_url is not None:
        user.avatar_url = avatar_url
    if bio is not None:
        user.bio = bio
    
    session.commit()    
    return user


def change_user_roles(user_id: int, role_ids: List[str]) -> Optional[User]:
    session = db_session.create_session()
    
    user = session.get(User, user_id)
    
    if not user:
        return None
        
    user.roles.clear()
        
    for role_id in role_ids:
        role = session.get(Role, role_id)
        if role:
            user.roles.append(role)
        
    session.commit()
    session.refresh(user)
    user = session.query(User).options(joinedload(User.roles)).get(user.id)
        
    return user


def check_if_user_exists(email: Optional[str] = None, 
                         username: Optional[str] = None) -> bool:
    if not email and not username:
        return False
    
    session = db_session.create_session()
    
    user = session.query(User).filter(
        or_(
            User.email == email,
            User.username == username
            )
        ).first()
    
    return user


def save_avatar_file(file: FileStorage, user_id: int) -> str | None:
    if not file:
        return None
    
    allowed_extensions = {"png", "jpg", "jpeg", "gif"}
    filename = secure_filename(file.filename)
    
    if "." not in filename or filename.rsplit(".", 1)[1].lower() not in allowed_extensions:
        return None
    
    ext = filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
    save_path = os.path.join(current_app.config["PROFILE_PICS_FOLDER"], unique_filename)
    
    try:
        img = Image.open(file.stream)
        img.thumbnail((500, 500))
        img.save(save_path)
        
        return f"images/profile_pics/{unique_filename}"    
    except Exception as e:
        current_app.logger.error(f"Error processing profile picture: {e}")
        return None


def update_user_avatar(file: FileStorage, user_id: int) -> Optional[User]:
    user = get_user_by_id(user_id)
        
    if not user:
        return None

    if user.avatar_url and user.avatar_url != "images/profile_pics/default.png":
        delete_avatar_file(user_id)
        
    new_avatar_url = save_avatar_file(file, user_id)
        
    if not new_avatar_url:
        return None
        
    user.avatar_url = new_avatar_url
        
    return user


def delete_avatar_file(user_id: int) -> None:
    user = get_user_by_id(user_id)
    
    if not user.avatar_url:
        return
    
    try:
        avatar_path = os.path.join(
            current_app.config["PROFILE_PICS_FOLDER"],
            user.avatar_url.split("/")[-1]
        )
        
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
    except Exception as e:
        current_app.logger.error(f"Error deleting avatar: {e}")

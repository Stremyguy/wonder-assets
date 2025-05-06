from app.scripts import db_session
from app.models import User, Role
from sqlalchemy import or_
from sqlalchemy.orm import joinedload


def get_all_users() -> list[User]:
    session = db_session.create_session()
    return session.query(User).options(joinedload(User.roles)).all()


def get_user_by_id(user_id: int) -> User | None:
    session = db_session.create_session()
    return session.query(User).options(joinedload(User.roles)).get(user_id)


def delete_user(user_id: int) -> bool:
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if user:
        session.delete(user)
        session.commit()
        return True
    return False


def create_user(username: str, 
                email: str, 
                password: str, 
                avatar_url: str = None,
                bio: str = None) -> User | None:
    session = db_session.create_session()

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
              username: str, 
              email: str, 
              password: str, 
              avatar_url: str = None,
              bio: str = None) -> User | None:
    session = db_session.create_session()
    user = session.get(User, user_id)
    
    if not user:
        return None
    
    user.username = username
    user.email = email
    user.set_password(password)
    user.avatar_url = avatar_url
    user.bio = bio

    session.commit()
    
    return user


def change_user_roles(user_id: int, role_names: list[str]) -> User | None:
    session = db_session.create_session()
    user = session.get(User, user_id)
    
    if not user:
        return None
    
    user.roles.clear()
    
    for role_name in role_names:
        role = session.query(Role).filter_by(name=role_name).first()
        if role:
            user.roles.append(role)
    
    session.commit()
    session.refresh(user)
    user = session.query(User).options(joinedload(User.roles)).get(user.id)
    
    return user


def check_if_user_exists(email: str = None, username: str = None) -> bool:
    session = db_session.create_session()
    
    if not email and not username:
        return False
    
    user = session.query(User).filter(
        or_(
            User.email == email,
            User.username == username
            )
        ).first()
    
    return user

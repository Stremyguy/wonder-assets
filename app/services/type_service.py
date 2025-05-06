from app.scripts import db_session
from app.models import Type


def get_all_types() -> list[Type]:
    session = db_session.create_session()
    return session.query(Type).all()


def get_type_by_id(type_id: int) -> Type | None:
    session = db_session.create_session()
    return session.query(Type).get(type_id)


def delete_type(type_id: int) -> bool:
    session = db_session.create_session()
    type = session.query(Type).get(type_id)
    
    if type:
        session.delete(type)
        session.commit()
        return True
    return False


def create_type(name: str, icon_url: str) -> Type:
    session = db_session.create_session()
    type = Type(
        name=name,
        icon_url=icon_url
    )
    
    session.add(type)
    session.commit()
    
    return type


def edit_type(type_id: int, name: str, icon_url: str) -> Type:
    session = db_session.create_session()
    type = session.query(Type).get(type_id)
    
    if not type:
        return None
    
    type.name = name
    type.icon_url = icon_url

    session.commit()
    
    return type

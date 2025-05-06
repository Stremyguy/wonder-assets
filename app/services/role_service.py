from app.scripts import db_session
from app.models import Role


def get_all_roles() -> list[Role]:
    session = db_session.create_session()
    return session.query(Role).all()


def get_role_by_id(role_id: int) -> Role | None:
    session = db_session.create_session()
    return session.query(Role).get(role_id)


def delete_role(role_id: int) -> bool:
    session = db_session.create_session()
    role = session.query(Role).get(role_id)

    if role:
        session.delete(role)
        session.commit()
        return True
    return False


def create_role(name: str) -> Role:
    session = db_session.create_session()
    role = Role(
        name=name,
    )
    
    session.add(role)
    session.commit()
    
    return role


def edit_role(role_id: int, name: str) -> Role:
    session = db_session.create_session()
    role = session.query(Role).get(role_id)
    
    if not role:
        return None
    
    role.name = name
    
    session.commit()
    
    return role

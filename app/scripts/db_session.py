import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import os

SqlAlchemyBase = orm.declarative_base()

__factory = None
__engine = None


def global_init() -> None:
    global __factory, __engine
    
    if __factory:
        return
    
    conn_str = os.getenv("DATABASE_URL")

    if not conn_str:
        raise ValueError("DATABASE_URL is not set in .env")

    print(f"[INFO] Connecting to DB at {conn_str}")
    __engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=__engine)
    
    from app import models
    SqlAlchemyBase.metadata.create_all(__engine)
    

def create_session() -> Session:
    global __factory
    
    return __factory()


def create_engine() -> Session:
    global __engine
    
    return __engine()

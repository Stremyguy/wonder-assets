import sqlalchemy
from app.scripts.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


# user, creator, moderator, admin
class Role(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "roles"
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

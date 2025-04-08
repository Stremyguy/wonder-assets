import datetime
import sqlalchemy
from sqlalchemy import orm
from app.scripts.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Categories(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "categories"
    
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    is_testing = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    # creator_id = sqlalchemy.Column(sqlalchemy.Integer, 
    #                                sqlalchemy.ForeignKey("users.id"))
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    
    # creator = orm.relationship("User", back_populates="categories", 
    #                            foreign_keys=[creator_id])

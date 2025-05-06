import datetime
import sqlalchemy
from sqlalchemy import orm
from app.scripts.db_session import SqlAlchemyBase
from app.models.category_roles import category_to_roles
from sqlalchemy_serializer import SerializerMixin


class Category(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "categories"
    
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    short_description = sqlalchemy.Column(sqlalchemy.String, default="", nullable=True)
    full_description = sqlalchemy.Column(sqlalchemy.String, default="", nullable=True)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    is_testing = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                   sqlalchemy.ForeignKey("users.id"),
                                   default=1)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    
    creator = orm.relationship("User", back_populates="categories", 
                               foreign_keys=[creator_id])
    items = orm.relationship("Item", back_populates="category")
    
    visible_to_roles = orm.relationship(
        "Role",
        secondary=category_to_roles,
        backref="categories_visible"
    )
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "short_description": self.short_description,
            "full_description": self.full_description,
            "is_private": self.is_private,
            "is_testing": self.is_testing,
            "created_date": self.created_date
        }

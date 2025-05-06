import datetime
import sqlalchemy
from sqlalchemy import orm
from app.scripts.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Item(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "items"
    
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    item_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("types.id"),
                                nullable=False)
    category_id = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("categories.id"))
    creator_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"),
                                   default=1)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False, nullable=False)
    show_meta = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    can_download = sqlalchemy.Column(sqlalchemy.Boolean, default=True, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    
    type = orm.relationship("Type", back_populates="items",
                            foreign_keys=[type_id])
    category = orm.relationship("Category", back_populates="items",
                                foreign_keys=[category_id])
    creator = orm.relationship("User", back_populates="items", 
                               foreign_keys=[creator_id])
    images = orm.relationship("ItemImage",
                              back_populates="item",
                              order_by="ItemImage.display_order",
                              cascade="all, delete-orphan")
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type_id": self.type_id,
            "is_private": self.is_private,
            "can_download": self.can_download,
            "category_id": self.category_id,
            "creator_id": self.creator_id,
            "images": [img.image_url for img in self.images],
            "main_image": self.images[0].image_url if self.images else None
        }

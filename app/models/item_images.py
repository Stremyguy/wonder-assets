import datetime
import sqlalchemy
from sqlalchemy import orm
from app.scripts.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class ItemImage(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "item_images"
    
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("items.id"), nullable=False)
    image_url = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    display_order = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    
    item = orm.relationship("Item", back_populates="images")

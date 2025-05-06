import sqlalchemy
from sqlalchemy import orm
from app.scripts.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Type(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "types"
    
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    icon_url = sqlalchemy.Column(sqlalchemy.String, 
                                 default="images/icons/icon_3d_object.png",
                                 nullable=False)

    items = orm.relationship("Item", back_populates="type")
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "icon_url": self.icon_url,
        }

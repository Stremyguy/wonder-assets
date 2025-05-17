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
    file_size_bytes = sqlalchemy.Column(sqlalchemy.BigInteger, default=0)
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
            "file_size": self.get_human_readable_size()
        }

    def get_human_readable_size(self) -> str:
        """Convert file size in bytes to human-readable format"""
        size = self.file_size_bytes
        
        if not size:
            return "0 KB"
        
        for unit in ["bytes", "KB", "MB", "GB", "TB"]:
            if size < 1024.0:
                if unit == "bytes":
                    return f"{int(size)} {unit}"
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"

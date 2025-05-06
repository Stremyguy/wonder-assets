import datetime
import sqlalchemy
from sqlalchemy import orm
from app.scripts.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"
    
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    password_hash = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    avatar_url = sqlalchemy.Column(sqlalchemy.String, default="profile_pics/default.png")
    bio = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    updated_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    categories = orm.relationship("Category", back_populates="creator")
    items = orm.relationship("Item", back_populates="creator")

    roles = orm.relationship(
        "Role",
        secondary="user_roles",
        backref="users"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> check_password_hash:
        return check_password_hash(self.password_hash, password)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password_hash,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "roles": [role.name for role in self.roles]            
        }
    
    def __repr__(self) -> str:
        return f"<User> {self.id} {self.username}"

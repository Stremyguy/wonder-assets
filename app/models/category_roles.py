import sqlalchemy
from app.scripts.db_session import SqlAlchemyBase

category_to_roles = sqlalchemy.Table(
    "category_roles",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("category_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("categories.id")),
    sqlalchemy.Column("role_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("roles.id")),
)
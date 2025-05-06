import sqlalchemy
from app.scripts.db_session import SqlAlchemyBase

user_to_roles = sqlalchemy.Table(
    "user_roles",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("user_id", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("role_id", sqlalchemy.Integer,
                      sqlalchemy.ForeignKey("roles.id"))
)
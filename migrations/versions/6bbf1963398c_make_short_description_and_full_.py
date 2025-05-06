"""Make short_description and full_description V2

Revision ID: 6bbf1963398c
Revises: a60c73470759
Create Date: 2025-04-27 14:55:27.639306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6bbf1963398c'
down_revision: Union[str, None] = 'a60c73470759'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("categories", sa.Column("short_description", sa.String(), nullable=True))
    op.add_column("categories", sa.Column("full_description", sa.String(), nullable=True))
    
    op.execute("UPDATE categories SET short_description = description")
    op.execute("UPDATE categories SET full_description = description")
    
    op.drop_column('categories', 'description')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("categories", sa.Column("description", sa.String(), nullable=True))
    op.execute("UPDATE categories SET description = COALESCE(full_description, short_description, '')")
    
    op.drop_column("categories", "full_description")
    op.drop_column("categories", "short_description")

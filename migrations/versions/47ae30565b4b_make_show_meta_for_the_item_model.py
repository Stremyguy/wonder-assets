"""Make show_meta for the Item model

Revision ID: 47ae30565b4b
Revises: 6bbf1963398c
Create Date: 2025-04-28 15:30:11.962204

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47ae30565b4b'
down_revision: Union[str, None] = '6bbf1963398c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("items", sa.Column("show_meta", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("items", "show_meta")

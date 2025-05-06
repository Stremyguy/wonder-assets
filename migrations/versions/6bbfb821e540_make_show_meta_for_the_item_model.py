"""Make show_meta for the Item model

Revision ID: 6bbfb821e540
Revises: 47ae30565b4b
Create Date: 2025-04-28 15:33:08.189633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '6bbfb821e540'
down_revision: Union[str, None] = '47ae30565b4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "items", 
        sa.Column(
            "show_meta", 
            postgresql.BOOLEAN(), 
            nullable=False,
            server_default=sa.text("true")))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("items", "show_meta")

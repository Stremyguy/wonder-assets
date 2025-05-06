"""Fixed show_meta for the Item model

Revision ID: 8ce24ce8f1cd
Revises: 6bbfb821e540
Create Date: 2025-04-28 16:17:45.520366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '8ce24ce8f1cd'
down_revision: Union[str, None] = '6bbfb821e540'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("items", "show_meta")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "items", 
        sa.Column(
            "show_meta", 
            postgresql.BOOLEAN(), 
            nullable=False,
            server_default=sa.text("true")))

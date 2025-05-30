"""Make item_url nullable

Revision ID: 9b39928720a4
Revises: e2e837dd6bf1
Create Date: 2025-04-27 11:27:14.187024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b39928720a4'
down_revision: Union[str, None] = 'e2e837dd6bf1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("items", "item_url", nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("items", "item_url", nullable=False)

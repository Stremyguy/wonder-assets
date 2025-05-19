"""remove_icon_url_column

Revision ID: 098de1bb055b
Revises: 644b2091da2d
Create Date: 2025-05-19 19:59:39.849122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '098de1bb055b'
down_revision: Union[str, None] = '644b2091da2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("types", "icon_url")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("types", sa.Column("icon_url", sa.String()))

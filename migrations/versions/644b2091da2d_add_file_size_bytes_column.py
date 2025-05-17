"""add_file_size_bytes_column

Revision ID: 644b2091da2d
Revises: fbb2fec70feb
Create Date: 2025-05-16 10:34:21.588229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '644b2091da2d'
down_revision: Union[str, None] = 'fbb2fec70feb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("items", sa.Column("file_size_bytes", sa.BigInteger(), server_default="0", nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("items", "file_size_bytes")

"""Make short and full descriptions for categories

Revision ID: d888bd9696c4
Revises: 9b39928720a4
Create Date: 2025-04-27 14:50:55.186357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd888bd9696c4'
down_revision: Union[str, None] = '9b39928720a4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

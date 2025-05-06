"""Make short_description and full_description nullable

Revision ID: a60c73470759
Revises: d888bd9696c4
Create Date: 2025-04-27 14:53:04.274275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a60c73470759'
down_revision: Union[str, None] = 'd888bd9696c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

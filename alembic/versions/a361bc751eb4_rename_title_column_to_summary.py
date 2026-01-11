"""rename title column to summary

Revision ID: a361bc751eb4
Revises: 666300ce4deb
Create Date: 2026-01-06 20:05:26.816601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a361bc751eb4'
down_revision: Union[str, Sequence[str], None] = '666300ce4deb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('events', 'title', new_column_name='summary')

def downgrade() -> None:
    op.alter_column('events', 'summary', new_column_name='title')

"""merge user table heads

Revision ID: 67ccbf125a88
Revises: 567028042881, recreate_users_with_column_order
Create Date: 2025-05-16 00:40:11.526748
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "67ccbf125a88"
down_revision: Union[str, None] = ("567028042881", "recreate_users_with_column_order")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Ensure users.id sequence is correctly set after merge."""
    op.execute(
        "SELECT setval(pg_get_serial_sequence('users', 'id'), (SELECT MAX(id) FROM users))"
    )


def downgrade() -> None:
    """No-op downgrade for merge."""
    pass

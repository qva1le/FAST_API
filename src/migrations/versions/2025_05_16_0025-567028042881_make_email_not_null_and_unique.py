"""make email not null and unique

Revision ID: 567028042881
Revises: 99445279a701
Create Date: 2025-05-16 00:25:15.614181

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "567028042881"
down_revision: Union[str, None] = "99445279a701"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column("users", "email", nullable=False)
    op.create_unique_constraint("uq_users_email", "users", ["email"])

def downgrade():
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.alter_column("users", "email", nullable=True)

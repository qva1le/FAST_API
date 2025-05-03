"""initional migration

Revision ID: 5af485031b87
Revises: 
Create Date: 2025-05-03 02:56:36.998106

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5af485031b87'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table('hotels',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('locaton', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )



def downgrade() -> None:
    op.drop_table('hotels')


from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "99445279a701"
down_revision: Union[str, None] = "f6d5fadc6446"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Добавляем колонку email как nullable
    op.add_column("users", sa.Column("email", sa.String(length=200), nullable=True))

    # 2. (заполни email для существующих строк вручную или в скрипте вручную после этой миграции)

    # 3. Сделай колонку NOT NULL и уникальной (в следующей миграции или вручную, после заполнения)
    # Пример отложенного изменения:
    # op.alter_column("users", "email", nullable=False)
    # op.create_unique_constraint("uq_users_email", "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "email")

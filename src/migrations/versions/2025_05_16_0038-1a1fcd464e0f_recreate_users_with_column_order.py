from alembic import op
import sqlalchemy as sa


# Уникальные идентификаторы ревизии
revision = 'recreate_users_with_column_order'
down_revision = '99445279a701'  # укажи здесь предыдущий revision ID
branch_labels = None
depends_on = None


def upgrade():
    # 1. Переименовываем текущую таблицу
    op.rename_table('users', 'users_old')

    # 2. Создаем новую таблицу с правильным порядком колонок
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=200), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=200), nullable=False),
    )

    # 3. Копируем данные
    op.execute(
        """
        INSERT INTO users (id, email, hashed_password)
        SELECT id, email, hashed_password FROM users_old
        """
    )

    # 4. Удаляем старую таблицу
    op.drop_table('users_old')


def downgrade():
    # На случай отката можно восстановить старую таблицу (опционально)
    op.rename_table('users', 'users_new')

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('hashed_password', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=200), nullable=False),
    )

    op.execute(
        """
        INSERT INTO users (id, hashed_password, email)
        SELECT id, hashed_password, email FROM users_new
        """
    )

    op.drop_table('users_new')

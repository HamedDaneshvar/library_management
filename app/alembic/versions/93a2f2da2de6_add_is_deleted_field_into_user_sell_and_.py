"""add is_deleted field into user, sell and payment model

Revision ID: 93a2f2da2de6
Revises: db305813212d
Create Date: 2024-07-23 06:09:07.813088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93a2f2da2de6'
down_revision = 'db305813212d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('payments', sa.Column('is_deleted',
                  sa.Boolean(), nullable=False,
                  server_default=sa.sql.expression.false()))
    op.add_column('sells', sa.Column('is_deleted',
                  sa.Boolean(), nullable=False,
                  server_default=sa.sql.expression.false()))
    op.add_column('user', sa.Column('is_deleted',
                  sa.Boolean(), nullable=False,
                  server_default=sa.sql.expression.false()))

    op.execute("UPDATE payments SET is_deleted = false WHERE is_deleted IS NULL")
    op.execute("UPDATE sells SET is_deleted = false WHERE is_deleted IS NULL")
    op.execute('UPDATE "user" SET is_deleted = false WHERE is_deleted IS NULL')


def downgrade() -> None:
    op.drop_column('user', 'is_deleted')
    op.drop_column('sells', 'is_deleted')
    op.drop_column('payments', 'is_deleted')

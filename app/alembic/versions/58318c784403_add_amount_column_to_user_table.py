"""Add amount column to user table

Revision ID: 58318c784403
Revises: a0d2c8235c3b
Create Date: 2024-07-21 13:03:18.487657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58318c784403'
down_revision = 'a0d2c8235c3b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('user', sa.Column('amount', sa.Float(), nullable=False, server_default="0.0"))
    op.execute('UPDATE "user" SET amount = 0.0')


def downgrade() -> None:
    op.drop_column('user', 'amount')

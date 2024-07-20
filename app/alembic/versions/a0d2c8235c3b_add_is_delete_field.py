"""add is_delete field

Revision ID: a0d2c8235c3b
Revises: cd8053a755d7
Create Date: 2024-07-21 03:02:17.113130

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a0d2c8235c3b'
down_revision = 'cd8053a755d7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('books', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    op.add_column('categories', sa.Column('is_deleted', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))

    op.execute("UPDATE books SET is_deleted = false WHERE is_deleted IS NULL")
    op.execute("UPDATE categories SET is_deleted = false WHERE is_deleted IS NULL")


def downgrade() -> None:
    op.drop_column('categories', 'is_deleted')
    op.drop_column('books', 'is_deleted')

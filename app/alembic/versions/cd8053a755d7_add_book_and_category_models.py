"""Add Book and Category models

Revision ID: cd8053a755d7
Revises: 6b05f5028e16
Create Date: 2024-07-20 20:26:38.373784

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd8053a755d7'
down_revision = '6b05f5028e16'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('borrow_limit', sa.Integer(), nullable=False),
        sa.Column('borrow_price_per_day', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('borrow_qty', sa.Integer(), nullable=False),
        sa.Column('sell_qty', sa.Integer(), nullable=False),
        sa.Column('sell_price', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('books')
    op.drop_table('categories')

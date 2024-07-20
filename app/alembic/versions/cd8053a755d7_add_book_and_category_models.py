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
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('borrow_limit', sa.Integer(), nullable=False),
        sa.Column('borrow_price_per_day', sa.Integer(), nullable=False),
        sa.Column('created', sa.DateTime(timezone=True), nullable=True),
        sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'books',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('borrow_qty', sa.Integer(), nullable=False),
        sa.Column('sell_qty', sa.Integer(), nullable=False),
        sa.Column('sell_price', sa.Integer(), nullable=False),
        sa.Column('created', sa.DateTime(timezone=True), nullable=True),
        sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_books_id'), 'books', ['id'], unique=False)
    op.create_index(op.f('ix_books_title'), 'books', ['title'], unique=False)
    op.create_index(op.f('ix_books_category_id'), 'books', ['category_id'], unique=False)
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)
    op.create_index(op.f('ix_categories_title'), 'categories', ['title'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_books_category_id'), table_name='books')
    op.drop_index(op.f('ix_books_title'), table_name='books')
    op.drop_index(op.f('ix_books_id'), table_name='books')
    op.drop_index(op.f('ix_categories_title'), table_name='categories')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')

    op.drop_table('categories')
    op.drop_table('books')

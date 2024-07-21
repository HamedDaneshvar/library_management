"""add payment model and modify sell model

Revision ID: 8d10bf741dcf
Revises: bcfc16b16fcf
Create Date: 2024-07-21 20:03:29.122092

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8d10bf741dcf'
down_revision = 'bcfc16b16fcf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('model_type', sa.String(length=255), nullable=False),
        sa.Column('model_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.Column('created', sa.DateTime(timezone=True), nullable=True),
        sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payments_id'), 'payments', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_payments_id'), table_name='payments')
    op.drop_table('payments')

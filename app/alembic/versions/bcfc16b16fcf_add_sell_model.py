"""add sell model

Revision ID: bcfc16b16fcf
Revises: 58318c784403
Create Date: 2024-07-21 19:01:37.390065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bcfc16b16fcf'
down_revision = '58318c784403'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'sells',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('book_id', sa.Integer(), nullable=False),
        sa.Column('superuser_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['book_id'], ['books.id'], ),
        sa.ForeignKeyConstraint(['superuser_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sells_id'), 'sells', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_sells_id'), table_name='sells')
    op.drop_table('sells')

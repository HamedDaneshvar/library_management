"""Change sell_price and borrow_price_per_day to Float

Revision ID: 3539a16412a9
Revises: 5a7bcce9d6f2
Create Date: 2024-07-22 18:36:45.599388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3539a16412a9'
down_revision = '5a7bcce9d6f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('books', 'sell_price',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)
    op.alter_column('categories', 'borrow_price_per_day',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)


def downgrade() -> None:
    op.alter_column('categories', 'borrow_price_per_day',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('books', 'sell_price',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)

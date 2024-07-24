"""change price field into Decimal

Revision ID: da8b3f1fa00f
Revises: 93a2f2da2de6
Create Date: 2024-07-24 05:31:49.348519

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'da8b3f1fa00f'
down_revision = '93a2f2da2de6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        'books', 'sell_price',
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False
    )
    op.alter_column('borrows', 'borrow_price',
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        existing_nullable=True
    )
    op.alter_column('borrows', 'borrow_penalty_price',
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        existing_nullable=True
    )
    op.alter_column('borrows', 'total_price',
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        existing_nullable=True
    )
    op.alter_column('categories', 'borrow_price_per_day',
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False
    )
    op.alter_column('payments', 'price',
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False
    )
    op.alter_column('sells', 'price',
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False
    )
    op.alter_column('user', 'amount',
        existing_type=sa.Float(),
        type_=sa.Numeric(10, 2),
        existing_nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        'books', 'sell_price',
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        existing_nullable=False
    )
    op.alter_column('borrows', 'borrow_price',
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        existing_nullable=True
    )
    op.alter_column('borrows', 'borrow_penalty_price',
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        existing_nullable=True
    )
    op.alter_column('borrows', 'total_price',
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        existing_nullable=True
    )
    op.alter_column('categories', 'borrow_price_per_day',
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        existing_nullable=False
    )
    op.alter_column('payments', 'price',
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        existing_nullable=False
    )
    op.alter_column('sells', 'price',
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        existing_nullable=False
    )
    op.alter_column('user', 'amount',
        existing_type=sa.Numeric(10, 2),
        type_=sa.Float(),
        existing_nullable=False
    )

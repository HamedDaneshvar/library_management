"""Add Borrow, BorrowActivityLog, UserPenalty models

Revision ID: db305813212d
Revises: 3539a16412a9
Create Date: 2024-07-23 00:27:24.811941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db305813212d'
down_revision = '3539a16412a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'borrows',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('book_id', sa.Integer,
                  sa.ForeignKey('books.id', ondelete="CASCADE")),
        sa.Column('superuser_id',
                  sa.Integer,
                  sa.ForeignKey('user.id', ondelete="SET NULL"),
                  nullable=True),
        sa.Column('user_id', sa.Integer,
                  sa.ForeignKey('user.id', ondelete="CASCADE")),
        sa.Column('start_date', sa.DateTime, nullable=True),
        sa.Column('max_delivery_date', sa.DateTime, nullable=True),
        sa.Column('delivery_date', sa.DateTime, nullable=True),
        sa.Column('borrow_price', sa.Float, nullable=True),
        sa.Column('borrow_penalty_price', sa.Float, nullable=True),
        sa.Column('total_price', sa.Float, nullable=True),
        sa.Column('is_deleted', sa.Boolean, default=False),
        sa.Column('created', sa.DateTime(timezone=True), nullable=True),
        sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        'borrow_activity_log',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('borrow_id', sa.Integer, sa.ForeignKey('borrows.id',
                                                         ondelete="CASCADE")),
        sa.Column('status_id', sa.Integer, sa.ForeignKey('status.id',
                                                         ondelete="CASCADE")),
        sa.Column('is_deleted', sa.Boolean, default=False),
        sa.Column('created', sa.DateTime(timezone=True), nullable=True),
        sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        'user_penalty',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id',
                                                       ondelete="CASCADE")),
        sa.Column('borrow_id', sa.Integer, sa.ForeignKey('borrows.id',
                                                         ondelete="CASCADE")),
        sa.Column('borrow_penalty_day', sa.Integer),
        sa.Column('is_deleted', sa.Boolean, default=False),
    )


def downgrade() -> None:
    op.drop_table('user_penalty')
    op.drop_table('borrow_activity_log')
    op.drop_table('borrows')

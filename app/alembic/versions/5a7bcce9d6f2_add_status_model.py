"""add status model

Revision ID: 5a7bcce9d6f2
Revises: 8d10bf741dcf
Create Date: 2024-07-22 12:56:58.507220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a7bcce9d6f2'
down_revision = '8d10bf741dcf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'status',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False, default=False),
        sa.Column('created', sa.DateTime(timezone=True), nullable=True),
        sa.Column('modified', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_status_id'), 'status', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_status_id'), table_name='status')
    op.drop_table('status')

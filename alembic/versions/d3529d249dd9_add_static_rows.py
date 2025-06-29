"""add static rows

Revision ID: d3529d249dd9
Revises: e74fd422945b
Create Date: 2025-06-10 16:42:46.565826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3529d249dd9'
down_revision: Union[str, None] = 'e74fd422945b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('CONSTRUCTION_STATIC_ROWS',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('resource', sa.String(length=10), nullable=True),
    sa.Column('flow_type', sa.String(length=50), nullable=True),
    sa.Column('fiscal_year', sa.String(length=10), nullable=True),
    sa.Column('flow_source', sa.String(length=50), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('CONSTRUCTION_STATIC_ROWS')
    # ### end Alembic commands ###

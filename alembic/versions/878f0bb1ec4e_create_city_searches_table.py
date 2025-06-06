"""create city_searches table

Revision ID: 878f0bb1ec4e
Revises: 
Create Date: 2025-05-27 09:28:56.374489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '878f0bb1ec4e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('city_searches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city_name', sa.String(), nullable=True),
    sa.Column('searched_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_city_searches_city_name'), 'city_searches', ['city_name'], unique=False)
    op.create_index(op.f('ix_city_searches_id'), 'city_searches', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_city_searches_id'), table_name='city_searches')
    op.drop_index(op.f('ix_city_searches_city_name'), table_name='city_searches')
    op.drop_table('city_searches')
    # ### end Alembic commands ###

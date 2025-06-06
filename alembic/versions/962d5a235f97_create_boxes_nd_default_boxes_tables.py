"""Create Boxes ND Default_boxes tables 

Revision ID: 962d5a235f97
Revises: 03d6afa7b830
Create Date: 2025-05-21 17:17:05.865653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '962d5a235f97'
down_revision: Union[str, None] = '03d6afa7b830'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('default_boxes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('box_type', sa.String(), nullable=False),
    sa.Column('suitable_for_class', sa.Integer(), nullable=False),
    sa.Column('discount', sa.Float(), server_default='0', nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('boxes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('box_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['box_id'], ['default_boxes.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('boxes')
    op.drop_table('default_boxes')
    # ### end Alembic commands ###

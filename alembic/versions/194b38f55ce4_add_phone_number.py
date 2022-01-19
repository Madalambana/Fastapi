"""add phone number

Revision ID: 194b38f55ce4
Revises: 0655b3b5e81e
Create Date: 2022-01-19 00:56:13.434211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '194b38f55ce4'
down_revision = '0655b3b5e81e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###

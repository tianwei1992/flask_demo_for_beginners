"""add language to posts

Revision ID: 4849759fd2c8
Revises: fab5eddd5ee9
Create Date: 2019-08-22 19:29:14.078154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4849759fd2c8'
down_revision = 'fab5eddd5ee9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'language')
    # ### end Alembic commands ###

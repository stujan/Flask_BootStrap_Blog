"""empty message

Revision ID: 37024ccece37
Revises: c0addd040ef9
Create Date: 2017-03-22 13:12:34.914090

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37024ccece37'
down_revision = 'c0addd040ef9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('imgurl', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admin', 'imgurl')
    # ### end Alembic commands ###

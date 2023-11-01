"""add yt and demo link

Revision ID: d092840a5c3c
Revises: 
Create Date: 2022-08-04 16:45:32.113073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd092840a5c3c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('youtube_link', sa.String(length=255), nullable=True))
    op.add_column('project', sa.Column('demo_link', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'demo_link')
    op.drop_column('project', 'youtube_link')
    # ### end Alembic commands ###

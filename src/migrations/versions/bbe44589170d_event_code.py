"""Event code

Revision ID: bbe44589170d
Revises: 2349aea3331d
Create Date: 2022-08-27 10:39:15.709933

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbe44589170d'
down_revision = '2349aea3331d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('Code', sa.String(length=10), nullable=True, comment='Codigo Evento'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'Code')
    # ### end Alembic commands ###
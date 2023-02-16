"""ClientEmail

Revision ID: 75d09cc52842
Revises: bbe44589170d
Create Date: 2022-08-30 14:42:35.827117

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '75d09cc52842'
down_revision = 'bbe44589170d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('ClientEmail', mysql.LONGTEXT(), nullable=True, comment='Email del cliente '))
    op.add_column('notessends', sa.Column('ClientEmail', mysql.LONGTEXT(), nullable=True, comment='Email del cliente '))
    op.add_column('payrollsends', sa.Column('ClientEmail', mysql.LONGTEXT(), nullable=True, comment='Email del cliente '))
    op.add_column('sendsinvoices', sa.Column('ClientEmail', mysql.LONGTEXT(), nullable=True, comment='Email del cliente '))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sendsinvoices', 'ClientEmail')
    op.drop_column('payrollsends', 'ClientEmail')
    op.drop_column('notessends', 'ClientEmail')
    op.drop_column('events', 'ClientEmail')
    # ### end Alembic commands ###

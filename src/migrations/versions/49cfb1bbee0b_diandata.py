"""diandata

Revision ID: 49cfb1bbee0b
Revises: f3c923842d14
Create Date: 2022-04-25 15:41:24.671597

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '49cfb1bbee0b'
down_revision = 'f3c923842d14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('diandata',
    sa.Column('Id', sa.Integer(), nullable=False),
    sa.Column('CreateDate', sa.DateTime(), nullable=True, comment='Fecha de creación'),
    sa.Column('UpdateDate', sa.DateTime(), nullable=True, comment='Fecha de Modificación'),
    sa.Column('IssuerNit', sa.String(length=20), nullable=False, comment='Nit de la empresa o emisor '),
    sa.Column('DianSoftwareId', sa.String(length=100), nullable=False, comment='id del software de la Dian '),
    sa.Column('Prefix', sa.String(length=5), nullable=False, comment='Prefijo'),
    sa.Column('DianPin', sa.String(length=5), nullable=False, comment='id del software de la Dian '),
    sa.Column('DianTestSetId', sa.String(length=100), nullable=True, comment='set de prueba'),
    sa.Column('DocType', sa.String(length=5), nullable=False, comment='Tipo de Doc AD=Contenedor FV=factura NC=Nota Cr ND=Nota DB DS=Documento Soporte NOM=Nomina NOMA=Nomina Ajuste '),
    sa.PrimaryKeyConstraint('Id')
    )
    op.create_index('ix_iddian', 'diandata', ['IssuerNit', 'DocType', 'Prefix', 'DianSoftwareId'], unique=False)
    op.drop_column('applications', 'UpdateBy')
    op.drop_column('applications', 'CreateBy')
    op.drop_column('applications', 'IsDeleted')
    op.drop_column('certs', 'UpdateBy')
    op.drop_column('certs', 'CreateBy')
    op.drop_column('certs', 'IsDeleted')
    op.drop_column('cities', 'UpdateBy')
    op.drop_column('cities', 'CreateBy')
    op.drop_column('cities', 'IsDeleted')
    op.drop_column('consecutiveinvoices', 'UpdateBy')
    op.drop_column('consecutiveinvoices', 'CreateBy')
    op.drop_column('consecutiveinvoices', 'IsDeleted')
    op.drop_column('consecutivenotes', 'UpdateBy')
    op.drop_column('consecutivenotes', 'CreateBy')
    op.drop_column('consecutivenotes', 'IsDeleted')
    op.drop_column('consecutivepayroll', 'UpdateBy')
    op.drop_column('consecutivepayroll', 'CreateBy')
    op.drop_column('consecutivepayroll', 'IsDeleted')
    op.drop_column('departments', 'UpdateBy')
    op.drop_column('departments', 'CreateBy')
    op.drop_column('departments', 'IsDeleted')
    op.drop_column('invoices', 'UpdateBy')
    op.drop_column('invoices', 'IsDeleted')
    op.drop_column('invoices', 'CreateBy')
    op.drop_column('notes', 'UpdateBy')
    op.drop_column('notes', 'IsDeleted')
    op.drop_column('notes', 'CreateBy')
    op.drop_column('notessends', 'UpdateBy')
    op.drop_column('notessends', 'CreateBy')
    op.drop_column('notessends', 'IsDeleted')
    op.drop_column('payrollsends', 'UpdateBy')
    op.drop_column('payrollsends', 'CreateBy')
    op.drop_column('payrollsends', 'IsDeleted')
    op.drop_column('sendsinvoices', 'UpdateBy')
    op.drop_column('sendsinvoices', 'CreateBy')
    op.drop_column('sendsinvoices', 'IsDeleted')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sendsinvoices', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('sendsinvoices', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('sendsinvoices', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('payrollsends', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('payrollsends', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('payrollsends', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('notessends', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('notessends', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('notessends', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('notes', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('notes', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('notes', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('invoices', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('invoices', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('invoices', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('departments', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('departments', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('departments', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('consecutivepayroll', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('consecutivepayroll', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('consecutivepayroll', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('consecutivenotes', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('consecutivenotes', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('consecutivenotes', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('consecutiveinvoices', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('consecutiveinvoices', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('consecutiveinvoices', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('cities', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('cities', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('cities', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('certs', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('certs', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('certs', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('applications', sa.Column('IsDeleted', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('applications', sa.Column('CreateBy', mysql.VARCHAR(length=50), nullable=True))
    op.add_column('applications', sa.Column('UpdateBy', mysql.VARCHAR(length=50), nullable=True))
    op.drop_index('ix_iddian', table_name='diandata')
    op.drop_table('diandata')
    # ### end Alembic commands ###
